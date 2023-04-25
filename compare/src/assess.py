import os
from util.constants import GlobalConstants as g_constants
from util.constants import ClfConstants as clf_constants
from util.metrics import Curve, Score

ROOT_DIR_RELATIVE_PATH = ''
CLF_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,clf_constants.MODEL_PATH)
KSFINDER_PATH = os.path.join(CLF_DATA_PATH,g_constants.KSFINDER+'.sav')

class Assessment:

    def __init__(self,data_path):
        self.ASSESS_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,data_path)
        self.ASSESS_RESULT_PATH = os.path.join(self.ASSESS_DATA_PATH,g_constants.RESULTS_PATH)
        for r_file in os.listdir(self.ASSESS_RESULT_PATH):
            os.remove(os.path.join(self.ASSESS_RESULT_PATH,r_file))
        self._load_test_data()   

    def _load_test_data(self):
        self.y_probs = list()
        self.y_labels = list()
        with open(os.path.join(self.ASSESS_DATA_PATH,g_constants.CSV_POS_TEST)) as ip_f:
            ip_f.readline()
            for record in ip_f:
                prob = record.strip().split(',')[2]
                self.y_probs.append(float(prob))
                self.y_labels.append(1)
        with open(os.path.join(self.ASSESS_DATA_PATH,g_constants.CSV_NEG_TEST)) as ip_f:
            ip_f.readline()
            for record in ip_f:
                prob = record.strip().split(',')[2]
                self.y_probs.append(float(prob))
                self.y_labels.append(0)

    def run(self):
        y_labels, y_probs = self.y_labels, self.y_probs
        score_roc, _, _, _ = Score.get_roc_scores(y_labels,y_probs)
        score_pr, _, _, _ = Score.get_pr_scores(y_labels,y_probs)
        roc_curve = Curve.get_roc_curve(y_labels,y_probs)
        pr_curve = Curve.get_pr_curve(y_labels, y_probs)
        roc_curve.savefig(os.path.join(self.ASSESS_DATA_PATH,g_constants.RESULTS_PATH,g_constants.ROC_CURVE))
        pr_curve.savefig(os.path.join(self.ASSESS_DATA_PATH,g_constants.RESULTS_PATH,g_constants.PR_CURVE))
        self.scores_file = open(os.path.join(self.ASSESS_DATA_PATH,g_constants.RESULTS_PATH,g_constants.SCORES),'w')
        print('ROC-AUC',score_roc,'PR-AUC',score_pr,file=self.scores_file,sep='\t')
        self.scores_file.close()
        Curve.reset_plt()