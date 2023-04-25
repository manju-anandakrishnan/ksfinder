import os
from util.constants import GlobalConstants as g_constants
from util.constants import KGEConstants as kge_constants
from ampligraph.datasets import load_from_csv
from ampligraph.utils import restore_model
from sklearn.metrics import average_precision_score,roc_auc_score, roc_curve, precision_recall_curve
import numpy as np
import matplotlib.pyplot as plt

ROOT_DIR_RELATIVE_PATH = ''

KGE_MODEL_DIR = os.path.join(ROOT_DIR_RELATIVE_PATH,kge_constants.MODEL_PATH)
ASSESS1_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,g_constants.ASSESS1_DATA_PATH)
ASSESS2_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,g_constants.ASSESS2_DATA_PATH)

class Evaluation:

    def __init__(self,model,pos_valid,neg_valid,pos_test,neg_test):
        self.pos_valid = pos_valid
        self.neg_valid = neg_valid
        self.pos_test = pos_test
        self.neg_test = neg_test
        self.kge_model = model
    
    def _evaluate(self):
        self.kge_model.calibrate(np.array(self.pos_valid), np.array(self.neg_valid))
        pos_labels = np.full((len(self.pos_test),1),1)
        neg_labels = np.full((len(self.neg_test),1),0)
        pos_probas = self.kge_model.predict_proba(np.array(self.pos_test))
        neg_probas = self.kge_model.predict_proba(np.array(self.neg_test))
        self.y_labels = np.concatenate((np.array(pos_labels),np.array(neg_labels)))
        self.y_probs = np.concatenate((pos_probas,neg_probas))
        
    def _plot_roc_curve(self):
        roc_score = roc_auc_score(self.y_labels, self.y_probs)
        self.roc_score = round(roc_score,3)
        fpr, tpr, thresholds = roc_curve(self.y_labels, self.y_probs)
        fig, ax = plt.subplots(figsize=(7.5, 7.5))
        plt.plot(fpr, tpr, label='ROC Curve (AUC = %0.3f)' % self.roc_score)
        plt.plot([0, 1], [0, 1], linestyle='--', color='orange', label='Random classifier')  
        plt.plot([0, 0, 1], [0, 1, 1], linestyle=':', color='green', label='Perfect classifier')
        plt.xlabel('False positive rate')
        plt.ylabel('True positive rate')
        plt.legend(loc="lower right")
        self.roc_curve=fig

    def _plot_pr_curve(self):
        pr_score = average_precision_score(self.y_labels, self.y_probs)
        self.pr_score = round(pr_score,3)
        precision, recall, thresholds = precision_recall_curve(self.y_labels, self.y_probs)
        fig, ax = plt.subplots(figsize=(7.5, 7.5))
        plt.plot(recall, precision, label='PR Curve (Avg precision = %0.3f)' % self.pr_score)
        plt.plot([0, 0, 1], [0, 0, 0], linestyle='--', color='orange', label='Random classifier')  
        plt.plot([0, 1, 1], [1, 1, 0], linestyle=':', color='green', label='Perfect classifier')
        plt.xlabel('recall')
        plt.ylabel('precision')
        plt.legend(loc="center left")
        self.pr_curve=fig

    def run(self):
        self._evaluate()
        self._plot_pr_curve()
        self._plot_roc_curve()
        return self.roc_curve, self.pr_curve, self.roc_score, self.pr_score


class Assessment:

    def __init__(self,data_path):
        self.ASSESS_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,data_path)
        self.ASSESS_RESULT_PATH = os.path.join(self.ASSESS_DATA_PATH,g_constants.RESULTS_PATH)
        for r_file in os.listdir(self.ASSESS_RESULT_PATH):
            os.remove(os.path.join(self.ASSESS_RESULT_PATH,r_file))
        self.pos_valid = load_from_csv('.', os.path.join(self.ASSESS_DATA_PATH,g_constants.CSV_POS_VALID), sep=',',header=0)
        self.neg_valid = load_from_csv('.', os.path.join(self.ASSESS_DATA_PATH,g_constants.CSV_NEG_VALID), sep=',',header=0)
        self.pos_test = load_from_csv('.', os.path.join(self.ASSESS_DATA_PATH,g_constants.CSV_POS_TEST), sep=',',header=0)
        self.neg_test = load_from_csv('.', os.path.join(self.ASSESS_DATA_PATH,g_constants.CSV_NEG_TEST), sep=',',header=0)
        
    def run(self,kge_model):
        model = restore_model(model_name_path=os.path.join(KGE_MODEL_DIR,kge_model+'.pkl'))
        evaluation = Evaluation(model,self.pos_valid,self.neg_valid,self.pos_test,self.neg_test)
        plot_roc, plot_pr, score_roc, score_pr = evaluation.run()
        plot_roc.savefig(os.path.join(self.ASSESS_DATA_PATH,g_constants.RESULTS_PATH,kge_model+'_'+g_constants.ROC_CURVE))
        plot_pr.savefig(os.path.join(self.ASSESS_DATA_PATH,g_constants.RESULTS_PATH,kge_model+'_'+g_constants.PR_CURVE))
        self.scores_file = open(os.path.join(self.ASSESS_DATA_PATH,g_constants.RESULTS_PATH,g_constants.SCORES),'a')
        print(kge_model,'ROC-AUC',score_roc,'PR-AUC',score_pr,file=self.scores_file,sep='\t')
        self.scores_file.close()
