from ampligraph.utils import restore_model
from clf.src.build_model import NNClassifier
from util.constants import GlobalConstants as g_constants
from util.constants import KGEConstants as kge_constants
from util.constants import ClfConstants as clf_constants
from util.constants import KSFinderConstants as ksf_constants
from sklearn.preprocessing import StandardScaler
import pickle
import numpy as np
import os

ROOT_DIR_RELATIVE_PATH = '../../'
KGE_MODEL_DIR = os.path.join(ROOT_DIR_RELATIVE_PATH,kge_constants.MODEL_PATH)
CLF_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,clf_constants.MODEL_PATH)
KSFINDER_PATH = os.path.join(CLF_DATA_PATH,g_constants.KSFINDER+'.sav')
KSFINDER_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,ksf_constants.DATA_DIR)
KSFINDER_RESULT_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,ksf_constants.RESULTS_DIR)
KG_PROTEINS = os.path.join(KSFINDER_DATA_PATH,ksf_constants.TXT_KG_PROTEINS)

class KSFinder:

    def __init__(self):
        self.ks_finder = pickle.load(open(KSFINDER_PATH, 'rb'))
        self.scaler = StandardScaler()
        self.nn_classifier = NNClassifier()
    
    def _load_emb_vectors(self):
        self.entity_emb_vector = {}
        entities = set()
        for ent_kinase, ent_substrate in self.ks_records:
                entities.add(ent_kinase)
                entities.add(ent_substrate)
        for entity in entities:
            self.entity_emb_vector[entity] = self.nn_classifier.get_emb_vector(entity)

    def _load_substrates(self):
        self.substrates = list()
        with open(KG_PROTEINS) as ip_f:
            ip_f.readline()
            for record in ip_f:
                record = record.strip()
                self.substrates.append(record)

    def get_predictions_ks(self,ent_kinase,ent_substrate):
        k_emb_vector = self.entity_emb_vector.get(ent_kinase)
        s_emb_vector = self.entity_emb_vector.get(ent_substrate)
        ks_emb_vector = np.concatenate((k_emb_vector,s_emb_vector))
        scaled_ks_vector = self.nn_classifier.transform([ks_emb_vector])
        prob = self.ks_finder.predict_proba(scaled_ks_vector)
        prob = str(round(prob[0][1],5))
        return prob                                       

    def _write_predictions(self,output_file):
        with open(os.path.join(KSFINDER_RESULT_PATH,output_file),'w') as op_f:
            op_f.write(g_constants.KINASE_SUBSTRATE_PROB+'\n')
            for k,s,prob in self.predictions:
                op_f.write(k+','+s+','+prob+'\n')

    def get_predictions(self,kinases,output_file):
        self._load_substrates()
        self.predictions=list()
        self.ks_records = list()
        for kinase in kinases:
            for substrate in self.substrates:
                self.ks_records.append((kinase,substrate))
        self._load_emb_vectors()
        for ent_kinase,ent_substrate in self.ks_records:
            prob = self.get_predictions_ks(ent_kinase,ent_substrate)
            self.predictions.append((ent_kinase,ent_substrate,prob))
        self._write_predictions(output_file)
        

        



    

        