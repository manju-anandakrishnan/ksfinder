'''
This is the main module for preparing the data, building and assessing the classifier model.
'''
import argparse
from prepare_data import ClassifierData
from build_model import NNClassifier
from assess import Assessment
from util.constants import GlobalConstants as g_constants

def process():
    parser = argparse.ArgumentParser()
    parser.add_argument('--t_clf',default=False)
    args = parser.parse_args()

    if args.t_clf:
        print('Beginning the training of the classifier model, this may regenerate the negative data. Optionally use may use the trained model and the generated negatives.')
        is_train = input("Are you sure you want to continue? Hit 'Y' to continue, else press any other key")
        if is_train == 'Y':
            classifer_data = ClassifierData()
            classifer_data.run()

            nn_classifier = NNClassifier()
            nn_classifier.run()    

    assessment3 = Assessment(g_constants.ASSESS3_DATA_PATH)
    assessment3.run()
    
    assessment4 = Assessment(g_constants.ASSESS4_DATA_PATH)
    assessment4.run()    

process()
