from textmine.src.literature_search import Predictions
from textmine.src.literature_search import TextMine

def process():
    #predictions = Predictions(l_prob=0.7)
    #predictions.search_literature()
    predictions = Predictions(h_prob=0.3,l_prob=0.2)
    predictions.search_literature()

process()