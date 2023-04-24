'''
This is an utility module maintaining classes for plotting curves and computing performance metrics
'''

from sklearn.metrics import average_precision_score,roc_auc_score, roc_curve, precision_recall_curve
import matplotlib.pyplot as plt

class Curve:

    def get_roc_curve(y_labels,y_probs):
        roc_score, fpr, tpr, thresholds = Score.get_roc_scores(y_labels, y_probs)
        fig, ax = plt.subplots(figsize=(7.5, 7.5))
        plt.plot(fpr, tpr, label='ROC Curve (AUC = %0.3f)' % roc_score)
        plt.plot([0, 1], [0, 1], linestyle='--', color='orange', label='Random classifier')  
        plt.plot([0, 0, 1], [0, 1, 1], linestyle=':', color='green', label='Perfect classifier')
        plt.xlabel('False positive rate')
        plt.ylabel('True positive rate')
        plt.legend(loc="lower right")
        return fig

    def get_pr_curve(y_labels,y_probs):
        pr_score, precision, recall, thresholds = Score.get_pr_scores(y_labels, y_probs)
        fig, ax = plt.subplots(figsize=(7.5, 7.5))
        plt.plot(recall, precision, label='PR Curve (Avg precision = %0.3f)' % pr_score)
        plt.plot([0, 0, 1], [0, 0, 0], linestyle='--', color='orange', label='Random classifier')  
        plt.plot([0, 1, 1], [1, 1, 0], linestyle=':', color='green', label='Perfect classifier')
        plt.xlabel('recall')
        plt.ylabel('precision')
        plt.legend(loc="center left")
        return fig
    
    def reset_plt():
        plt.clf()
    
class Score:

    def get_roc_scores(y_labels,y_probs):
        roc_score = roc_auc_score(y_labels, y_probs)
        roc_score = round(roc_score,3)
        fpr, tpr, thresholds = roc_curve(y_labels, y_probs)
        return roc_score, fpr, tpr, thresholds

    def get_pr_scores(y_labels,y_probs):
        pr_score = average_precision_score(y_labels, y_probs)
        pr_score = round(pr_score,3)
        precision, recall, thresholds = precision_recall_curve(y_labels, y_probs)
        return pr_score, precision, recall, thresholds


