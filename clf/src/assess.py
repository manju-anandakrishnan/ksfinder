import os
import pandas as pd
import numpy as np
from util.constants import GlobalConstants as g_constants
from util.constants import KGEConstants as kge_constants
from util.constants import ClfConstants as clf_constants
from clf.src.build_model import NNClassifier
import pickle
from util.metrics import Curve, Score

ROOT_DIR_RELATIVE_PATH = ''
CLF_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,clf_constants.MODEL_PATH)
KSFINDER_PATH = os.path.join(CLF_DATA_PATH,g_constants.KSFINDER+'.sav')

'''
This class loads the KSFinder model and evaluates the probabilities of the kinase-susbtrate pair
'''
class Evaluation:

    def __init__(self,test_features,test_target):
        self.features = test_features
        self.y_labels = test_target
        self.model = pickle.load(open(KSFINDER_PATH, 'rb'))

    def _evaluate(self):
        y_probs = self.model.predict_proba(self.features)
        self.y_probs = np.array(((pd.DataFrame(y_probs)).round(3))[1].to_list())

    def run(self):
        self._evaluate()
        return self.y_labels, self.y_probs

'''
This class loads the raw test data, constructs the features by retrieving the entities vectors from the KGE model. It invokes the evaluation class, plots and writes the results.
'''
class Assessment:

    def __init__(self,data_path):
        self.ASSESS_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,data_path)
        self.ASSESS_RESULT_PATH = os.path.join(self.ASSESS_DATA_PATH,g_constants.RESULTS_PATH)
        for r_file in os.listdir(self.ASSESS_RESULT_PATH):
            os.remove(os.path.join(self.ASSESS_RESULT_PATH,r_file))
        self.nn_classifier = NNClassifier()
        self._load_test_data()        
        
    def _load_test_data(self):
        self.ksfinder_test = list()
        with open(os.path.join(self.ASSESS_DATA_PATH,g_constants.CSV_POS_TEST)) as ip_f:
            ip_f.readline()
            for record in ip_f:
                self.ksfinder_test.append(self.nn_classifier.get_ht_vector(record.strip(),1))
        with open(os.path.join(self.ASSESS_DATA_PATH,g_constants.CSV_NEG_TEST)) as ip_f:
            ip_f.readline()
            for record in ip_f:
                self.ksfinder_test.append(self.nn_classifier.get_ht_vector(record.strip(),0))
        ksfinder_test = pd.DataFrame(self.ksfinder_test)
        shape = ksfinder_test.shape
        label_index = shape[1]-1
        self.test_features = np.array(ksfinder_test.iloc[:,:label_index])
        self.test_target = ksfinder_test.iloc[:,label_index].astype('int').values
        self.test_features = self.nn_classifier.transform(self.test_features)
  
    def run(self):
        y_labels, y_probs = Evaluation(self.test_features,self.test_target).run()
        self.y_labels = y_labels
        self.y_probs = y_probs
        score_roc, _, _, _ = Score.get_roc_scores(y_labels,y_probs)
        score_pr, _, _, _ = Score.get_pr_scores(y_labels,y_probs)
        roc_curve = Curve.get_roc_curve(y_labels,y_probs)
        pr_curve = Curve.get_pr_curve(y_labels, y_probs)
        roc_curve.savefig(os.path.join(self.ASSESS_DATA_PATH,g_constants.RESULTS_PATH,g_constants.ROC_CURVE))
        pr_curve.savefig(os.path.join(self.ASSESS_DATA_PATH,g_constants.RESULTS_PATH,g_constants.PR_CURVE))
        self.scores_file = open(os.path.join(self.ASSESS_DATA_PATH,g_constants.RESULTS_PATH,g_constants.SCORES),'a')
        print('ROC-AUC',score_roc,'PR-AUC',score_pr,file=self.scores_file,sep='\t')
        self.scores_file.close()
        Curve.reset_plt()

        


