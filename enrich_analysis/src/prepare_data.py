import os
import pandas as pd
from util.constants import KSFinderConstants as ksf_constants

ROOT_DIR_RELATIVE_PATH = '../../'
KSFINDER_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,ksf_constants.RESULTS_DIR)
PREDICTION_DATA = os.path.join(KSFINDER_DATA_PATH,ksf_constants.TXT_IDG_K_PREDICTIONS)

class DarkKinase:

    def __init__(self,kinase):
        self.dk = kinase
        self._read_predictions()

    def _read_predictions(self):
        pred_df = pd.read_csv(PREDICTION_DATA,sep=',')
        self.predictions = pred_df[pred_df['kinase']==self.dk].copy()        

    def get_substrates(self,prob):
        substrates = self.predictions[self.predictions['prob'] >= prob]['substrate'].to_list()
        return substrates

