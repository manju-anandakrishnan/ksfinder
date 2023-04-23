from prepare_data import IDGDataLoader, KGKinasesDataLoader
from ksfinder.src.predict_links import KSFinder
import os
from util.constants import GlobalConstants as g_constants
from util.constants import KSFinderConstants as ksf_constants

KSFINDER_DATA_PATH = g_constants.DATA_PATH
TXT_IDG_K_PREDICTIONS = ksf_constants.TXT_IDG_K_PREDICTIONS
TXT_KS_PREDICTIONS = ksf_constants.TXT_KS_PREDICTIONS

def process():
    # data_loader = IDGDataLoader()
    # idg_kg_kinases = data_loader.get_idg_kg_kinases()

    ksfinder = KSFinder()
    # ksfinder.get_predictions(idg_kg_kinases,TXT_IDG_K_PREDICTIONS)

    data_loader = KGKinasesDataLoader()
    kg_kinases = data_loader.get_kg_kinases()

    ksfinder.get_predictions(kg_kinases,TXT_KS_PREDICTIONS)


process()