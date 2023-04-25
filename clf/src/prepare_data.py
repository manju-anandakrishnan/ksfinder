import os
import random
import pandas as pd
from ampligraph.utils import restore_model
from util.constants import GlobalConstants as g_constants
from util.constants import KGEConstants as kge_constants

ROOT_DIR_RELATIVE_PATH = ''

CLF_DATA_PATH = g_constants.DATA_PATH
KG_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,kge_constants.DATA_PATH)
KGE_MODEL_DIR = os.path.join(ROOT_DIR_RELATIVE_PATH,kge_constants.MODEL_PATH)
NEGATOME_PATH = os.path.join(CLF_DATA_PATH,g_constants.CSV_NEGATOME)
NEGATIVES_PREDKINKG_CC_PATH = os.path.join(CLF_DATA_PATH,g_constants.CSV_NEGATIVES_PREDKINKG_CC)

POS_DATA = os.path.join(CLF_DATA_PATH,g_constants.CSV_POS_DATA)
NEG_DATA = os.path.join(CLF_DATA_PATH,g_constants.CSV_NEG_DATA)
PREDKINKG_UNBIASED_NEGATIVES = os.path.join(ROOT_DIR_RELATIVE_PATH,g_constants.ASSESS2_DATA_PATH,g_constants.CSV_NEG_TEST)
KG_POS_TEST = os.path.join(KG_DATA_PATH,g_constants.CSV_POS_TEST)
POS_TRAIN = os.path.join(CLF_DATA_PATH,g_constants.CSV_POS_TRAIN)
NEG_TRAIN = os.path.join(CLF_DATA_PATH,g_constants.CSV_NEG_TRAIN)

ASSESS2_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,g_constants.ASSESS2_DATA_PATH)
ASSESS3_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,g_constants.ASSESS3_DATA_PATH)
ASSESS4_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,g_constants.ASSESS4_DATA_PATH)

random.seed(10)

class NegativeGenerator:

    def __init__(self):
        self.kge_model =  restore_model(model_name_path=os.path.join(KGE_MODEL_DIR,kge_constants.COMPLEX+'.pkl'))
        pos_triples = pd.read_csv(os.path.join(KG_DATA_PATH,kge_constants.KG_PHOSPHORYLATION), sep=',')
        self._load_pos_entities(pos_triples)
        self.ent_emb_vector = {}
        for entity in self.p_entities:
            self._load_emb_vector(entity)
        self._load_pos_ks(pos_triples)
        self.p_substrate_cnt = {}
        self._load_substrate_count()
        self.p_k_substrates = {}
        self._load_kinase_substrates(pos_triples)
        self.ks_distance = {}
    
    def _load_pos_entities(self,pos_triples):        
        p_entities = list(pd.unique(pd.Series(pos_triples['head'].to_list())))
        p_entities.extend(pd.unique(pd.Series(pos_triples['tail'].to_list())))
        self.p_entities = p_entities


    def _load_pos_ks(self,pos_triples):
        p_kinases = pos_triples['head'].to_list()
        p_substrates = pos_triples['tail'].to_list()
        self.pos_ks = list()
        for i in range(0,len(p_kinases)):
            self.pos_ks.append(p_kinases[i]+','+p_substrates[i])
        self.p_substrates = p_substrates
        self.p_kinases = p_kinases
        self.p_unique_substrates = pd.unique(pd.Series(pos_triples['tail'].to_list()))
        self.p_unique_kinases = pd.unique(pd.Series(pos_triples['head'].to_list()))

    def _load_emb_vector(self,entity):
        self.ent_emb_vector[entity] = self.kge_model.get_embeddings(entity)

    def _load_substrate_count(self):
        for p_substrate in self.p_unique_substrates:
            self.p_substrate_cnt[p_substrate] = self.p_substrates.count(p_substrate)
    
    def _load_kinase_substrates(self,pos_triples):
        for p_kinase in self.p_unique_kinases:
            self.p_k_substrates[p_kinase] = pos_triples[pos_triples['head']==p_kinase]['tail'].to_list()

    def _load_negatome_data(self):
        self.negatome_kinase_cnt = {}
        with open(NEGATOME_PATH,'r') as ip_f:
            ip_f.readline()
            for record in ip_f:
                record = record.strip()
                negatome_k = record.split(',')[0]
                negatome_s = record.split(',')[2]
                self.n_substrates.append(negatome_s)
                self.neg_ks.append(negatome_k+','+negatome_s)
                self.negatome_kinase_cnt[negatome_k] = self.negatome_kinase_cnt.get(negatome_k,0)+1
    
    def _init_predkinkg_cc(self):
        predkinkg_cc = pd.read_csv(NEGATIVES_PREDKINKG_CC_PATH,sep=',')
        n_unique_kinases_cc = pd.unique(pd.Series(predkinkg_cc['head'].to_list()))
        self.n_kinase_substrates_cc = {}
        for k in n_unique_kinases_cc:
            self.n_kinase_substrates_cc[k] = list(pd.unique(pd.Series(predkinkg_cc[predkinkg_cc['head'] == k]['tail'].to_list())))
    
    def _kinase_calculate_distance(self,ent_kinase,coverage_cnt):
        if self.ks_distance.get(ent_kinase) is None:
            ks_kge_score = self._compute_kge_scores(ent_kinase)
            self.ks_distance[ent_kinase] = ks_kge_score
        ks_by_distance = self.ks_distance.get(ent_kinase)
        selected_substrates = ks_by_distance['substrate'].to_list()[:coverage_cnt]
        return selected_substrates

    def _compute_kge_scores(self,ent_kinase):
        triples = list()
        substrates = list()
        for ent_substrate in self.p_unique_substrates:
            triple = [ent_kinase,'p',ent_substrate]
            triples.append(triple)
            substrates.append(ent_substrate)
        scores = self.kge_model.predict(triples)
        substrates_scores = pd.DataFrame({'substrate':substrates,'scores':scores})
        substrates_scores.sort_values(by=['scores'],inplace=True)
        return substrates_scores

    def _write_data(self):
        with open(POS_DATA,'w') as op_f:
            op_f.write(g_constants.HEAD_TAIL+'\n')
            for pd in self.pos_ks: op_f.write(pd+'\n')
            
        with open(NEG_DATA,'w') as op_f:
            op_f.write(g_constants.HEAD_TAIL+'\n')
            for nd in self.neg_ks: op_f.write(nd+'\n')

    def run(self):
        op_file=open('log.txt','w')
        self.neg_ks = list()
        self.n_substrates = list()
        self._load_negatome_data()
        self._init_predkinkg_cc()
        self.p_kinases.reverse()
        neg_triple = None
        for idx,p_kinase in enumerate(self.p_kinases):
            self.negatome_kinase_cnt[p_kinase] = self.negatome_kinase_cnt.get(p_kinase,0)-1
            if self.negatome_kinase_cnt.get(p_kinase) < 0:
                k_substrates = self.n_kinase_substrates_cc.get(p_kinase)
                selected_s = None
                neg_kcd_cnt = 1000
                while (selected_s == None) or (self.n_substrates.count(selected_s) > self.p_substrate_cnt.get(selected_s,1)) or (selected_s in self.p_k_substrates.get(p_kinase)) or (neg_triple in self.neg_ks):
                    if len(k_substrates) == 0:
                        k_substrates = self._kinase_calculate_distance(p_kinase,neg_kcd_cnt)
                        neg_kcd_cnt += 100
                    rand_pos = random.randint(0,len(k_substrates)-1)
                    selected_s = k_substrates[rand_pos]
                    neg_triple = p_kinase+','+selected_s
                    k_substrates.remove(selected_s)
                else:
                    self.n_substrates.append(selected_s)            
                    self.neg_ks.append(p_kinase+','+selected_s)
            print(idx,sep='|',file=op_file,flush=True)
        self._write_data()
        

class ClassifierData:

    def __init__(self):
        self._load_raw_data()

    def _load_raw_data(self):
        if (os.path.exists(POS_DATA)) & (os.path.exists(NEG_DATA)):
            pass
        else:
            negative_generator = NegativeGenerator()
            negative_generator.run()
        self.pos_train = list()
        self.neg_triples = list()
        with open(POS_DATA) as ip_f:
            ip_f.readline()
            for record in ip_f:
                self.pos_train.append(record.strip())
        with open(NEG_DATA,'r') as ip_f:
            ip_f.readline()
            for record in ip_f:
                self.neg_triples.append(record.strip())

    def _prepare_pos(self):
        self.pos_test = list()
        with open(KG_POS_TEST,'r') as ip_f:
            ip_f.readline()
            for record in ip_f:
                record = record.strip()
                record_vals = record.split(',')
                self.pos_test.append(record_vals[0]+','+record_vals[2])
        for triple in self.pos_train[:]:
            if triple in self.pos_test:
                self.pos_train.remove(triple)
        self.p_substrate_cnt = {}
        for triple in self.pos_train:
            substrate = triple.split(',')[1]
            self.p_substrate_cnt[substrate] = self.p_substrate_cnt.get(substrate,0)+1

    def _prepare_neg(self):
        self.neg_train = list()
        self.neg_test = list()
        self.n_substrate_cnt = {}
        for triple in self.neg_triples:
            substrate = triple.split(',')[1]
            if self.n_substrate_cnt.get(substrate,0) <= self.p_substrate_cnt.get(substrate,0)+5:
                self.neg_train.append(triple) 
                self.n_substrate_cnt[substrate]=self.n_substrate_cnt.get(substrate,0)+1
        with open(PREDKINKG_UNBIASED_NEGATIVES,'r') as ip_f:
            ip_f.readline()
            for record in ip_f:
                record_vals = record.strip().split(',')
                triple = record_vals[0]+','+record_vals[2]
                self.neg_test.append(triple)
                if triple in self.neg_train: self.neg_train.remove(triple)

        while len(self.neg_test) < len(self.pos_test):
            rand_index = random.randint(0,len(self.neg_train)-1)
            triple = self.neg_train[rand_index]
            self.neg_test.append(triple)
            self.neg_train.remove(triple)

    def _write_data(self):
        with open(POS_TRAIN,'w') as op_f:
            op_f.write(g_constants.HEAD_TAIL+'\n')
            for pd in self.pos_train: op_f.write(pd+'\n')
            
        with open(NEG_TRAIN,'w') as op_f:
            op_f.write(g_constants.HEAD_TAIL+'\n')
            for nd in self.neg_train: op_f.write(nd+'\n')

    def _load_assess3_data(self):
        with open(os.path.join(ASSESS3_DATA_PATH,g_constants.CSV_POS_TEST),'w') as op_f:
            op_f.write(g_constants.HEAD_TAIL+'\n')
            for pd in self.pos_test: op_f.write(pd+'\n')

        with open(os.path.join(ASSESS3_DATA_PATH,g_constants.CSV_NEG_TEST),'w') as op_f:
            op_f.write(g_constants.HEAD_TAIL+'\n')
            for pd in self.neg_test: op_f.write(pd+'\n')

    def _load_assess4_data(self):
        with open(os.path.join(ASSESS2_DATA_PATH,g_constants.CSV_POS_TEST)) as ip_f, open(os.path.join(ASSESS4_DATA_PATH,g_constants.CSV_POS_TEST),'w') as op_f:
            ip_f.readline()
            op_f.write(g_constants.HEAD_TAIL+'\n')
            for record in ip_f:
                record = record.strip()
                record_vals = record.split(',')
                op_f.write(record_vals[0]+','+record_vals[2]+'\n')
        with open(os.path.join(ASSESS2_DATA_PATH,g_constants.CSV_NEG_TEST)) as ip_f, open(os.path.join(ASSESS4_DATA_PATH,g_constants.CSV_NEG_TEST),'w') as op_f:
            ip_f.readline()
            op_f.write(g_constants.HEAD_TAIL+'\n')
            for record in ip_f:
                record = record.strip()
                record_vals = record.split(',')
                op_f.write(record_vals[0]+','+record_vals[2]+'\n')

    def run(self):
        self._prepare_pos()
        self._prepare_neg()  
        self._write_data()  
        self._load_assess3_data()
        self._load_assess4_data()

        



        

