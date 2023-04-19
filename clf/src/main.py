from prepare_data import ClassifierData
from build_model import NNClassifier
from assess import Assessment
from util.constants import GlobalConstants as g_constants

def process():
    # classifer_data = ClassifierData()
    # classifer_data.run()

    nn_classifier = NNClassifier()
    nn_classifier.run()

    assessment3 = Assessment(g_constants.ASSESS3_DATA_PATH)
    assessment3.run()
    
    assessment4 = Assessment(g_constants.ASSESS4_DATA_PATH)
    assessment4.run()    

process()
