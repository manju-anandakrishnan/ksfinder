'''
This is the main module for running the textmining component. 
The probability thresholds for filtering the predictions and mining the literature should be passed when initializing the Prediction class
'''

from textmine.src.literature_search import Predictions
from textmine.src.literature_search import TextMine

def process():
    predictions = Predictions(l_prob=0.7)
    predictions.search_literature()

    # Uncomment as required for mining evidence at different prediction probabilities
    # predictions = Predictions(h_prob=0.3,l_prob=0.0)
    # predictions.search_literature()

process()