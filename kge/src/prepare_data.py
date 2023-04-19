import os
import numpy as np
import pandas as pd
from ampligraph.datasets import load_from_csv
from ampligraph.evaluation import train_test_split_no_unseen
from ordered_set import OrderedSet
from util.constants import GlobalConstants as g_constants
from util.constants import KGEConstants as kge_constants
import random

'''


'''

np.random.seed(0)
ROOT_DIR_RELATIVE_PATH = '../../'
KG_DATA_PATH = g_constants.DATA_PATH

ASSESS1_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,g_constants.ASSESS1_DATA_PATH)
ASSESS2_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,g_constants.ASSESS2_DATA_PATH)

class KGEDataLoader:

    test_size = valid_size = 1400

    def __init__(self):
        self.test_size = KGEDataLoader.test_size
        self.val_size = KGEDataLoader.valid_size

    def _load_data(self):
        self.kg = load_from_csv('.', os.path.join(KG_DATA_PATH,kge_constants.KG_OTHER_REL), sep=',',header=0)
        self.pos_triples = load_from_csv('.', os.path.join(KG_DATA_PATH,kge_constants.KG_PHOSPHORYLATION), sep=',',header=0)
        self.neg_triples = load_from_csv('.', os.path.join(KG_DATA_PATH,kge_constants.PREDKINKG_NEGATIVES), sep=',',header=0)

    def _split_data(self,triples):
        np.random.shuffle(triples)
        X_train_valid, X_test = train_test_split_no_unseen(triples, test_size=self.test_size, seed=0)
        X_train, X_valid = train_test_split_no_unseen(X_train_valid, test_size=self.val_size, seed=0)
        return X_train,X_valid,X_test
    
    def _write_split(self):   
        (pd.DataFrame(self.kg_train)).to_csv(os.path.join(KG_DATA_PATH,g_constants.CSV_KG_TRAIN),sep=',',index=False,header=['head','rel','tail'])
        (pd.DataFrame(self.pos_valid)).to_csv(os.path.join(KG_DATA_PATH,g_constants.CSV_POS_VALID),sep=',',index=False,header=['head','rel','tail'])
        (pd.DataFrame(self.pos_test)).to_csv(os.path.join(KG_DATA_PATH,g_constants.CSV_POS_TEST),sep=',',index=False,header=['head','rel','tail'])
    
    def _load_assess1_data(self):       
        (pd.DataFrame(self.pos_valid)).to_csv(os.path.join(ASSESS1_DATA_PATH,g_constants.CSV_POS_VALID),sep=',',index=False,header=['head','rel','tail'])
        (pd.DataFrame(self.pos_test)).to_csv(os.path.join(ASSESS1_DATA_PATH,g_constants.CSV_POS_TEST),sep=',',index=False,header=['head','rel','tail'])
        neg_valid = pd.DataFrame(self.neg_valid,columns=['head','rel','tail'])
        neg_test = pd.DataFrame(self.neg_test,columns=['head','rel','tail'])
        neg_valid['rel']='p'
        neg_test['rel']='p'
        (pd.DataFrame(neg_valid)).to_csv(os.path.join(ASSESS1_DATA_PATH,g_constants.CSV_NEG_VALID),sep=',',index=False)
        (pd.DataFrame(neg_test)).to_csv(os.path.join(ASSESS1_DATA_PATH,g_constants.CSV_NEG_TEST),sep=',',index=False)

    def run(self):
        if (os.path.exists(os.path.join(KG_DATA_PATH,g_constants.CSV_KG_TRAIN))) & (os.path.exists(os.path.join(KG_DATA_PATH,g_constants.CSV_POS_VALID))) & (os.path.exists(os.path.join(KG_DATA_PATH,g_constants.CSV_POS_TEST))):
            self.pos_valid = load_from_csv('.', os.path.join(KG_DATA_PATH,g_constants.CSV_POS_VALID), sep=',',header=0)
            self.pos_test = load_from_csv('.', os.path.join(KG_DATA_PATH,g_constants.CSV_POS_TEST), sep=',',header=0)      
            self.neg_triples = load_from_csv('.', os.path.join(KG_DATA_PATH,kge_constants.PREDKINKG_NEGATIVES), sep=',',header=0)
        else:
            self._load_data()
            self.pos_train, self.pos_valid, self.pos_test = self._split_data(self.pos_triples)
            self.kg_train = np.vstack((self.kg,self.pos_train))
            self._write_split()
        self.neg_train, self.neg_valid, self.neg_test = self._split_data(self.neg_triples)
        self._load_assess1_data()
    
class EvaluationData:

    def __init__(self):
        pass

    def _select_unbiased_negatives(self):
        p_kinase_cnt = {}
        p_substrate_cnt = {}
        with open(os.path.join(KG_DATA_PATH,g_constants.CSV_POS_TEST),'r') as pos_test:
            pos_test.readline()
            for data in pos_test:
                data = data.strip()
                kinase = data.split(',')[0]
                substrate = data.split(',')[2]
                p_substrate_cnt[substrate] = p_substrate_cnt.get(substrate,0)+1
                p_kinase_cnt[kinase] = p_kinase_cnt.get(kinase,0)+1

        kg = pd.read_csv(os.path.join(KG_DATA_PATH,g_constants.CSV_KG_TRAIN),sep=',')
        kg_entities = kg['head'].tolist()
        kg_entities.extend(kg['tail'].tolist())
        n_substrates = list()
        n_kinases = list()
        sel_negatives = OrderedSet()
        with open(os.path.join(KG_DATA_PATH,kge_constants.PREDKINKG_NEGATIVES)) as neg_triples:
            for data in neg_triples:
                data = data.strip()
                kinase = data.split(',')[0]
                substrate = data.split(',')[2]
                if (kinase in kg_entities) & (substrate in kg_entities):
                    positive_cnt = p_substrate_cnt.get(substrate,1)
                    negative_cnt = n_substrates.count(substrate)
                    if negative_cnt < positive_cnt:
                        n_substrates.append(substrate)
                        n_kinases.append(kinase)
                        sel_negatives.add(data)

        with open(os.path.join(KG_DATA_PATH,kge_constants.PREDKINKG_NEGATIVES)) as neg_triples:
            for data in neg_triples:
                data = data.strip()
                kinase = data.split(',')[0]
                substrate = data.split(',')[2]
                if (kinase in kg_entities) & (substrate in kg_entities):
                    positive_cnt = p_kinase_cnt.get(kinase,1)
                    negative_cnt = n_kinases.count(kinase)
                    if (negative_cnt < positive_cnt) & (n_substrates.count(substrate) < p_substrate_cnt.get(substrate,1)):
                        n_substrates.append(substrate)
                        n_kinases.append(kinase)
                        sel_negatives.add(data)
        return list(sel_negatives)

    def _get_data(self,path):
        records = list()
        with open(path,'r') as ip_f:
            ip_f.readline()
            for record in ip_f:
                records.append(record.strip())
        return records

    def _random_sample(self,records,size):
        random.seed(10)
        subset = list()
        while len(subset) < size:
            rand_index = random.randint(0,len(records)-1)
            triple = records[rand_index]
            subset.append([triple.split(',')[0],'p',triple.split(',')[2]])
            records.remove(triple)
        return subset

    def _load_assess2_data(self):
        unbiased_negatives = self._select_unbiased_negatives()
        valid_size = test_size = int(len(unbiased_negatives)/2)
        pos_valid = self._random_sample(self._get_data(os.path.join(KG_DATA_PATH,g_constants.CSV_POS_VALID)),valid_size)
        pos_test = self._random_sample(self._get_data(os.path.join(KG_DATA_PATH,g_constants.CSV_POS_TEST)),test_size)
        neg_valid = self._random_sample(unbiased_negatives,valid_size)
        neg_test = self._random_sample(unbiased_negatives,test_size)
        (pd.DataFrame(pos_valid)).to_csv(os.path.join(ASSESS2_DATA_PATH,g_constants.CSV_POS_VALID),sep=',',index=False,header=['head','rel','tail'])
        (pd.DataFrame(pos_test)).to_csv(os.path.join(ASSESS2_DATA_PATH,g_constants.CSV_POS_TEST),sep=',',index=False,header=['head','rel','tail'])
        (pd.DataFrame(neg_valid)).to_csv(os.path.join(ASSESS2_DATA_PATH,g_constants.CSV_NEG_VALID),sep=',',index=False,header=['head','rel','tail'])
        (pd.DataFrame(neg_test)).to_csv(os.path.join(ASSESS2_DATA_PATH,g_constants.CSV_NEG_TEST),sep=',',index=False,header=['head','rel','tail'])

    def run(self):
        self._load_assess2_data()





