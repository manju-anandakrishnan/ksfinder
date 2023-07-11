import os
from pathlib import Path
from util.constants import ComparativeAssessmentConstants as ca_constants
from util.constants import ClfConstants as clf_constants
from util.constants import GlobalConstants as g_constants
from util.constants import KSFinderConstants as ksf_constants
from ordered_set import OrderedSet
import random
import numpy as np
import pandas as pd
random.seed(10)

ROOT_DIR_RELATIVE_PATH = ''
LINKPHINDER_PREDICTIONS = os.path.join(ROOT_DIR_RELATIVE_PATH,ca_constants.DATA_DIR,ca_constants.LINKPHINDER_PREDICTIONS)
LINKPHINDER_RAW_DATA = os.path.join(ROOT_DIR_RELATIVE_PATH,ca_constants.DATA_DIR,ca_constants.LINKPHINDER_RAW_DATA)

PREDKINKG_PREDICTIONS = os.path.join(ROOT_DIR_RELATIVE_PATH,ca_constants.DATA_DIR,ca_constants.PREDKINKG_PREDICTIONS)
KSFINDER_POS_DATA = os.path.join(ROOT_DIR_RELATIVE_PATH,clf_constants.DATA_DIR,g_constants.CSV_POS_DATA)
KSFINDER_NEG_DATA = os.path.join(ROOT_DIR_RELATIVE_PATH,clf_constants.DATA_DIR,g_constants.CSV_NEG_DATA)
KSFINDER_PROTEINS = os.path.join(ROOT_DIR_RELATIVE_PATH,ksf_constants.DATA_DIR,ksf_constants.TXT_KG_PROTEINS)
KSFINDER_POS_TRAIN = os.path.join(ROOT_DIR_RELATIVE_PATH,clf_constants.DATA_DIR,g_constants.CSV_POS_TRAIN)
KSFINDER_NEG_TRAIN = os.path.join(ROOT_DIR_RELATIVE_PATH,clf_constants.DATA_DIR,g_constants.CSV_NEG_TRAIN)

UNIPROT_MAPPING = os.path.join(ROOT_DIR_RELATIVE_PATH,ca_constants.DATA_DIR,ca_constants.UNIPROT_GENE_CSV)
SER_THR_KS_ATLAS = os.path.join(ROOT_DIR_RELATIVE_PATH,ca_constants.DATA_DIR,ca_constants.SER_THR_KS_ATLAS)

ASSESS5_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,g_constants.ASSESS5_DATA_PATH)
ASSESS6_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,g_constants.ASSESS6_DATA_PATH)
ASSESS7_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,g_constants.ASSESS7_DATA_PATH)
ASSESS8_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,g_constants.ASSESS8_DATA_PATH)
ASSESS1_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,g_constants.ASSESS1_DATA_PATH)
ASSESS9_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,g_constants.ASSESS9_DATA_PATH)

class BaseData:
    def __init__(self):
        self._load_ksfinder_data()

    def _load_ksfinder_data(self):
        self.ksfinder_pos = list()
        self.ksfinder_neg = list()
        self.ksfinder_proteins = list()
        self.ksfinder_train = list()
        with open(KSFINDER_POS_DATA) as ip_f:
            ip_f.readline()
            for line in ip_f:
                line_vals = line.strip().split(',')
                k_s = (line_vals[0],line_vals[1])
                self.ksfinder_pos.append(k_s)
        with open(KSFINDER_NEG_DATA) as ip_f:
            ip_f.readline()
            for line in ip_f:
                line_vals = line.strip().split(',')
                k_s = (line_vals[0],line_vals[1])
                self.ksfinder_neg.append(k_s)
        with open(KSFINDER_PROTEINS) as ip_f:
            ip_f.readline()
            for line in ip_f:
                self.ksfinder_proteins.append(line.strip())
        with open(KSFINDER_POS_TRAIN) as ip_f:
            ip_f.readline()
            for line in ip_f:
                line_vals = line.strip().split(',')
                k_s = (line_vals[0],line_vals[1])
                self.ksfinder_train.append(k_s)        
        with open(KSFINDER_NEG_TRAIN) as ip_f:
            ip_f.readline()
            for line in ip_f:
                line_vals = line.strip().split(',')
                k_s = (line_vals[0],line_vals[1])
                self.ksfinder_train.append(k_s)

    def _write_data(self,assess_data_path,prediction_probs=None, pos_data=None, neg_data = None):
        if prediction_probs:
            with open(os.path.join(assess_data_path,g_constants.CSV_POS_TEST),'w') as op_f_pos, open(os.path.join(assess_data_path,g_constants.CSV_NEG_TEST),'w') as op_f_neg:
                op_f_pos.write(g_constants.KINASE_SUBSTRATE_PROB+'\n')
                op_f_neg.write(g_constants.KINASE_SUBSTRATE_PROB+'\n')
                for k_s in prediction_probs.keys():
                    if k_s in self.ksfinder_pos:
                        print(k_s[0],k_s[1],prediction_probs.get(k_s),sep=',',file=op_f_pos)
                    if k_s in self.ksfinder_neg:
                        print(k_s[0],k_s[1],prediction_probs.get(k_s),sep=',',file=op_f_neg)
            with open(os.path.join(assess_data_path,'prediction_data'),'w') as pr_opf:
                pr_opf.write(g_constants.KINASE_SUBSTRATE_PROB+'\n')
                for k_s in prediction_probs.keys():
                    print(k_s[0],k_s[1],prediction_probs.get(k_s),sep=',',file=pr_opf)
        else:
            with open(os.path.join(assess_data_path,g_constants.CSV_POS_TEST),'w') as op_f_pos, open(os.path.join(assess_data_path,g_constants.CSV_NEG_TEST),'w') as op_f_neg:
                op_f_pos.write(g_constants.HEAD_TAIL+'\n')
                op_f_neg.write(g_constants.HEAD_TAIL+'\n')
                for k_s in pos_data:
                    print(k_s[0],k_s[1],sep=',',file=op_f_pos)
                for k_s in neg_data:
                    print(k_s[0],k_s[1],sep=',',file=op_f_neg)

class LinkPhinderData(BaseData):

    def load_predictions(self):
        prediction_probs = {}
        with open(LINKPHINDER_PREDICTIONS) as ip_f:
            ip_f.readline()
            for line in ip_f:
                line_vals = line.strip().split('\t')
                k_s = (line_vals[3],line_vals[1])
                score = round(float(line_vals[6]),3)
                prediction_probs.setdefault(k_s,list())
                prediction_probs.get(k_s).append(score)
                # if prediction_probs.get(k_s,0) < score:
                #     prediction_probs[k_s] = score
        for ks_pair in prediction_probs.keys():
            scores = np.array(prediction_probs.get(ks_pair),dtype='float32')
            prediction_probs[ks_pair] = 1-np.prod(1-scores)

        self._write_data(ASSESS7_DATA_PATH,prediction_probs=prediction_probs)
    
    def load_data(self):
        linkphinder_pos_data = OrderedSet()
        linkphinder_neg_data = OrderedSet()
        s1_dir_path = os.path.join(LINKPHINDER_RAW_DATA,ca_constants.LINKPHINDER_BENCHMARK_9010)
        for s2_dir in os.listdir(s1_dir_path):
            s2_dir_path = os.path.join(s1_dir_path,s2_dir)
            for s12_file in os.listdir(s2_dir_path):
                file_path = os.path.join(s2_dir_path,s12_file)
                file_name = Path(file_path).name
                if (file_name == ca_constants.LINKPHINDER_TRAIN_FILE) or (file_name == ca_constants.LINKPHINDER_TEST_FILE):
                    with open(file_path) as ip_f:
                        ip_f.readline()
                        for record in ip_f:
                            record_vals = record.strip().split('\t')
                            kinase = record_vals[0]
                            substrate = record_vals[2]
                            label = record_vals[3]
                            if (kinase,substrate) in self.ksfinder_train: continue
                            if (kinase in self.ksfinder_proteins) & (substrate in self.ksfinder_proteins):
                                if label == '1': linkphinder_pos_data.add((kinase,substrate))                    
                                elif label == '-1': linkphinder_neg_data.add((kinase,substrate))
            break

        common_ks_data = linkphinder_pos_data.intersection(linkphinder_neg_data)
        for data in common_ks_data: linkphinder_neg_data.remove(data)
        test_size = len(linkphinder_pos_data)
        linkphinder_neg_data = list(linkphinder_neg_data)
        linkphinder_neg_data = random.sample(linkphinder_neg_data,test_size)
        self._write_data(ASSESS5_DATA_PATH,pos_data=linkphinder_pos_data, neg_data=linkphinder_neg_data)


class PredKinKGData(BaseData):

    def load_predictions(self):
        prediction_probs = {}
        with open(PREDKINKG_PREDICTIONS) as ip_f:
            ip_f.readline()
            for line in ip_f:
                line_vals = line.strip().split(',')
                k_s = (line_vals[0],line_vals[1])
                score = round(float(line_vals[2]),3)
                prediction_probs[k_s] = score
        self._write_data(ASSESS8_DATA_PATH,prediction_probs=prediction_probs)

    def load_data(self):
        predkinkg_pos_data = list()
        predkinkg_neg_data = list()
        with open(os.path.join(ASSESS1_DATA_PATH,g_constants.CSV_POS_TEST)) as ip_f:
            ip_f.readline()
            for record in ip_f:
                record = record.strip().split(',')
                predkinkg_pos_data.append((record[0],record[2]))
        with open(os.path.join(ASSESS1_DATA_PATH,g_constants.CSV_NEG_TEST)) as ip_f:
            ip_f.readline()
            for record in ip_f:
                record = record.strip().split(',')
                predkinkg_neg_data.append((record[0],record[2]))
        self._write_data(ASSESS6_DATA_PATH,pos_data=predkinkg_pos_data,neg_data=predkinkg_neg_data)

class KSAtlas:

    def load_predictions():    
        op_f_pos = open(os.path.join(ASSESS9_DATA_PATH,g_constants.CSV_POS_TEST),'w')
        op_f_pos.write(g_constants.HEAD_TAIL+'\n')
        op_f_neg = open(os.path.join(ASSESS9_DATA_PATH,g_constants.CSV_NEG_TEST),'w')
        op_f_neg.write(g_constants.HEAD_TAIL+'\n')

        uniprot_id_map = pd.read_csv(UNIPROT_MAPPING,sep='|')
        gene_names = uniprot_id_map['From'].to_list()
        uniprot_id = uniprot_id_map['Entry'].to_list()
        uniprot_id_map = dict(zip(gene_names,uniprot_id))

        entities = list()
        with open(KSFINDER_PROTEINS) as ip_f:
            ip_f.readline()
            for line in ip_f:
                entities.append(line.strip())
        # kg1 = pd.read_csv('/home/manjua/github_manjua/ksfinder/kge/data/kg1.csv',sep=',')
        # entities = kg1['head'].to_list()
        # entities.extend(kg1['tail'].to_list())
        # entities = set(entities)

        pos_data = pd.read_csv(KSFINDER_POS_DATA,sep=',')
        pos_data['ht']=pos_data['head']+pos_data['tail']
        pos_data_ht = pos_data['ht'].to_list()

        neg_data = pd.read_csv(KSFINDER_NEG_DATA,sep=',')
        neg_data['ht']=neg_data['head']+neg_data['tail']
        neg_data_ht = neg_data['ht'].to_list()

        ks_atlas = pd.read_excel(SER_THR_KS_ATLAS)
        for col_name in ks_atlas.columns:
            if 'rank' in col_name:
                kinase_nm = col_name.split('_')[0]
                ks_atlas[col_name] = ks_atlas[col_name].astype('int')
                pos_records = ks_atlas[ks_atlas[col_name] <= 15]['Uniprot Primary Accession'].unique()
                kinase_id = uniprot_id_map.get(kinase_nm)
                if kinase_id is None: continue
                if kinase_id in entities:
                    neg_records = set(ks_atlas[ks_atlas[col_name] > 150]['Uniprot Primary Accession'].unique())
                    for record in pos_records:
                        if record in neg_records: neg_records.discard(record)
                        if record in entities:
                            ks = kinase_id+record
                            if ks in pos_data_ht:
                                print(kinase_id,record,1,file=op_f_pos,sep=',')
                            elif ks in neg_data_ht:
                                print(kinase_id,record,1,file=op_f_neg,sep=',')
                    for record in neg_records:
                        if record in entities:
                            ks = kinase_id+record
                            if ks in neg_data_ht:
                                print(kinase_id,record,0,file=op_f_neg,sep=',')
                            elif ks in pos_data_ht:
                                print(kinase_id,record,0,file=op_f_pos,sep=',')
        