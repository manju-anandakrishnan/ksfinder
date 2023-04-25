'''
This is the main module for running the textmining component. 
The probability thresholds for filtering the predictions and mining the literature should be passed when initializing the Prediction class
'''

from textmine.src.literature_search import Predictions

def process():
    print('Warning: This action will hit iTextMine API for all the predictions over 0.7. It may take hours to complete. Alternatively, you can update the probability threshold values in the main.py file and run the module.')
    run_textmine = input('Do you want to continue with the default threshold of 0.7? Hit "Y" to proceed else press another key.')
    if run_textmine == 'Y':
        predictions = Predictions(l_prob=0.7)
        predictions.search_literature()

    # Uncomment as required for mining evidence at different prediction probabilities
    # predictions = Predictions(h_prob=0.3,l_prob=0.0)
    # predictions.search_literature()

process()