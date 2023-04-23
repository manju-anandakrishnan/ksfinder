from util.constants import GlobalConstants as g_constants
from util.constants import PreprocessConstants as pp_constants
from util.constants import KGEConstants as kge_constants
import pandas as pd
import os

ROOT_DIR_RELATIVE_PATH = '../../'
DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,pp_constants.DATA_DIR)
KGE_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,kge_constants.DATA_DIR)

class PrepareKGData:

    def __init__(self):
        pass

    def run(self):
        biokg = pd.read_csv(os.path.join(DATA_PATH,pp_constants.CSV_BIOKG))
        go = pd.read_csv(os.path.join(DATA_PATH,pp_constants.CSV_GO))
        pro = pd.read_csv(os.path.join(DATA_PATH,pp_constants.CSV_PRO))
        kg2 = pd.concat([biokg,go,pro],axis=0)
        kg2.drop_duplicates(inplace=True)
        kg2.to_csv(os.path.join(KGE_DATA_PATH,kge_constants.KG_OTHER_REL),index=False)

        iPTMnet =pd.read_csv(os.path.join(DATA_PATH,pp_constants.CSV_iPTMNET))
        iPTMnet.drop(columns=['source'],inplace=True)
        iPTMnet.to_csv(os.path.join(KGE_DATA_PATH,kge_constants.KG_PHOSPHORYLATION),index=False)

        iPTMnet_test = pd.read_csv(os.path.join(DATA_PATH,pp_constants.CSV_iPTMNET_TEST))
        iPTMnet_test.drop(columns=['source'],inplace=True)
        iPTMnet_test.to_csv(os.path.join(KGE_DATA_PATH,g_constants.CSV_POS_TEST),index=False)
