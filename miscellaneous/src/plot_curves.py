from clf.src.assess import Assessment
from compare.src.assess import Assessment as compare_assess
from util.constants import GlobalConstants as g_constants
import matplotlib.pyplot as plt
from util.metrics import Curve, Score

'''
This class has methods to create the roc and pr curves by different datasets.
It assess multiple test and plots the curves in one figure.
'''
class PerformanceDataSets:

    def plot_roc_curve():
        plt.close('all')
        fig, ax = plt.subplots(figsize=(9, 9))
        assess3 = Assessment(g_constants.ASSESS3_DATA_PATH)
        assess3.run()
        y_labels, y_probs = assess3.y_labels, assess3.y_probs
        roc_score3, fpr3, tpr3, _ = Score.get_roc_scores(y_labels, y_probs)
    
        assess4 = Assessment(g_constants.ASSESS4_DATA_PATH)
        assess4.run()
        y_labels, y_probs = assess4.y_labels, assess4.y_probs
        roc_score4, fpr4, tpr4, _ = Score.get_roc_scores(y_labels, y_probs)

        assess5 = Assessment(g_constants.ASSESS5_DATA_PATH)
        assess5.run()
        y_labels, y_probs = assess5.y_labels, assess5.y_probs
        roc_score5, fpr5, tpr5, _ = Score.get_roc_scores(y_labels, y_probs)

        assess6 = Assessment(g_constants.ASSESS6_DATA_PATH)
        assess6.run()
        y_labels, y_probs = assess6.y_labels, assess6.y_probs
        roc_score6, fpr6, tpr6, _ = Score.get_roc_scores(y_labels, y_probs)

        plt.plot(fpr3, tpr3, color='red', label='Assessment 3 - KSFinder dataset (AUC = %0.3f)' % roc_score3)
        plt.plot(fpr4, tpr4, label='Assessment 4 - PredKinKG-B dataset (AUC = %0.3f)' % roc_score4)
        plt.plot(fpr5, tpr5, color='green', label='Assessment 5 - LinkPhinder dataset (AUC = %0.3f)' % roc_score5)
        plt.plot(fpr6, tpr6, color='orange', label='Assessment 6 - PredKinKG dataset (AUC = %0.3f)' % roc_score6)

        #plt.plot([0, 1], [0, 1], linestyle='--', color='blue', label='Random classifier')  
        plt.plot([0, 0, 1], [0, 1, 1], linestyle=':', color='green', label='Perfect classifier')
        plt.xlabel('False positive rate')
        plt.ylabel('True positive rate')
        plt.legend(loc=(0.25,0.1))

        plt.savefig(g_constants.MISC_OUTPUT+'comparative_dataset_roc.png',dpi=400)

    def plot_pr_curve():
        plt.close('all')
        fig, ax = plt.subplots(figsize=(9, 9))
        assess3 = Assessment(g_constants.ASSESS3_DATA_PATH)
        assess3.run()
        y_labels, y_probs = assess3.y_labels, assess3.y_probs
        pr_score3, precision3, recall3, _ = Score.get_pr_scores(y_labels, y_probs)
    
        assess4 = Assessment(g_constants.ASSESS4_DATA_PATH)
        assess4.run()
        y_labels, y_probs = assess4.y_labels, assess4.y_probs
        pr_score4, precision4, recall4, _ = Score.get_pr_scores(y_labels, y_probs)

        assess5 = Assessment(g_constants.ASSESS5_DATA_PATH)
        assess5.run()
        y_labels, y_probs = assess5.y_labels, assess5.y_probs
        pr_score5, precision5, recall5, _ = Score.get_pr_scores(y_labels, y_probs)

        assess6 = Assessment(g_constants.ASSESS6_DATA_PATH)
        assess6.run()
        y_labels, y_probs = assess6.y_labels, assess6.y_probs
        pr_score6, precision6, recall6, _ = Score.get_pr_scores(y_labels, y_probs)

        plt.plot(recall3, precision3, color='red', label='Assessment 3 - KSFinder dataset (Avg PR = %0.3f)' % pr_score3)
        plt.plot(recall4, precision4, label='Assessment 4 - PredKinKG-B dataset (Avg PR = %0.3f)' % pr_score4)
        plt.plot(recall5, precision5, color='green', label='Assessment 5 -LinkPhinder dataset (Avg PR = %0.3f)' % pr_score5)
        plt.plot(recall6, precision6, color='orange', label='Assessment 6 - PredKinKG dataset (Avg PR = %0.3f)' % pr_score6)

        #plt.plot([0, 0, 1], [0, 0, 0], linestyle='--', color='blue', label='Random classifier')  
        plt.plot([0, 1, 1], [1, 1, 0], linestyle=':', color='green', label='Perfect classifier')
        plt.xlabel('recall')
        plt.ylabel('precision')
        plt.legend(loc=(0.2,0.1))

        plt.savefig(g_constants.MISC_OUTPUT+'comparative_dataset_pr.png',dpi=400)


PerformanceDataSets.plot_roc_curve()
PerformanceDataSets.plot_pr_curve()


'''
This class has methods to create the roc and pr curves by different models.
It assess multiple models on KSFinder test data and plots the curves in one figure.
'''
class CompareModels:

    def plot_roc_curve():
        plt.close('all')
        fig, ax = plt.subplots(figsize=(9, 9))
        assess3 = Assessment(g_constants.ASSESS3_DATA_PATH)
        assess3.run()
        y_labels, y_probs = assess3.y_labels, assess3.y_probs
        roc_score3, fpr3, tpr3, _ = Score.get_roc_scores(y_labels, y_probs)
    
        assess7 = compare_assess(g_constants.ASSESS7_DATA_PATH)
        assess7.run()
        y_labels, y_probs = assess7.y_labels, assess7.y_probs
        roc_score7, fpr7, tpr7, _ = Score.get_roc_scores(y_labels, y_probs)

        assess8 = compare_assess(g_constants.ASSESS8_DATA_PATH)
        assess8.run()
        y_labels, y_probs = assess8.y_labels, assess8.y_probs
        roc_score8, fpr8, tpr8, _ = Score.get_roc_scores(y_labels, y_probs)

        assess9 = compare_assess(g_constants.ASSESS9_DATA_PATH)
        assess9.run()
        y_labels, y_probs = assess9.y_labels, assess9.y_probs
        roc_score9, fpr9, tpr9, _ = Score.get_roc_scores(y_labels, y_probs)

        plt.plot(fpr3, tpr3, color='red', label='Assessment 3 - KSFinder (AUC = %0.3f)' % roc_score3)
        plt.plot(fpr7, tpr7, color='orange', label='Assessment 7 - LinkPhinder (AUC = %0.3f)' % roc_score7)
        plt.plot(fpr8, tpr8, label='Assessment 8 - PredKinKG (AUC = %0.3f)' % roc_score8)
        plt.plot(fpr9, tpr9, color='green', label='Assessment 9 - Ser-Thr-KS atlas (AUC = %0.3f)' % roc_score9)
        
        # plt.plot([0, 1], [0, 1], linestyle='--', color='blue', label='Random classifier')  
        plt.plot([0, 0, 1], [0, 1, 1], linestyle=':', color='green', label='Perfect classifier')
        plt.xlabel('False positive rate')
        plt.ylabel('True positive rate')
        plt.legend(loc=(0.25,0.1))

        plt.savefig(g_constants.MISC_OUTPUT+'comparative_models_roc.png',dpi=400)

    def plot_pr_curve():
        plt.close('all')
        fig, ax = plt.subplots(figsize=(9, 9))
        assess3 = Assessment(g_constants.ASSESS3_DATA_PATH)
        assess3.run()
        y_labels, y_probs = assess3.y_labels, assess3.y_probs
        pr_score3, precision3, recall3, _ = Score.get_pr_scores(y_labels, y_probs)
    
        assess7 = compare_assess(g_constants.ASSESS7_DATA_PATH)
        assess7.run()
        y_labels, y_probs = assess7.y_labels, assess7.y_probs
        pr_score7, precision7, recall7, _ = Score.get_pr_scores(y_labels, y_probs)

        assess8 = compare_assess(g_constants.ASSESS8_DATA_PATH)
        assess8.run()
        y_labels, y_probs = assess8.y_labels, assess8.y_probs
        pr_score8, precision8, recall8, _ = Score.get_pr_scores(y_labels, y_probs)

        assess9 = compare_assess(g_constants.ASSESS9_DATA_PATH)
        assess9.run()
        y_labels, y_probs = assess9.y_labels, assess9.y_probs
        pr_score9, precision9, recall9, _ = Score.get_pr_scores(y_labels, y_probs)

        plt.plot(recall3, precision3, color='red', label='Assessment 3 - KSFinder (Avg PR = %0.3f)' % pr_score3)
        plt.plot(recall7, precision7, color='orange', label='Assessment 7 - LinkPhinder (Avg PR = %0.3f)' % pr_score7)
        plt.plot(recall8, precision8, label='Assessment 8 - PredKinKG (Avg PR = %0.3f)' % pr_score8)
        plt.plot(recall9, precision9, color='green', label='Assessment 9 - Ser-Thr-KS atlas (AUC = %0.3f)'  % pr_score9)

        # plt.plot([0, 0, 1], [0, 0, 0], linestyle='--', color='blue', label='Random classifier')  
        plt.plot([0, 1, 1], [1, 1, 0], linestyle=':', color='green', label='Perfect classifier')
        plt.xlabel('recall')
        plt.ylabel('precision')
        plt.legend(loc=(0.25,0.1))

        plt.savefig(g_constants.MISC_OUTPUT+'comparative_models_pr.png',dpi=400)

CompareModels.plot_roc_curve()
CompareModels.plot_pr_curve()