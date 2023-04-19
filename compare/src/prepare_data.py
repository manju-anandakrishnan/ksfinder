import os
from pathlib import Path
from util.constants import ComparativeAssessmentConstants as ca_constants
from util.constants import ClfConstants as clf_constants
from util.constants import GlobalConstants as g_constants
from util.constants import KSFinderConstants as ksf_constants
from ordered_set import OrderedSet
import random
random.seed(10)

ROOT_DIR_RELATIVE_PATH = '../../'
LINKPHINDER_PREDICTIONS = os.path.join(ROOT_DIR_RELATIVE_PATH,ca_constants.DATA_DIR,ca_constants.LINKPHINDER_PREDICTIONS)
LINKPHINDER_RAW_DATA = os.path.join(ROOT_DIR_RELATIVE_PATH,ca_constants.DATA_DIR,ca_constants.LINKPHINDER_RAW_DATA)

PREDKINKG_PREDICTIONS = os.path.join(ROOT_DIR_RELATIVE_PATH,ca_constants.DATA_DIR,ca_constants.PREDKINKG_PREDICTIONS)
KSFINDER_POS_DATA = os.path.join(ROOT_DIR_RELATIVE_PATH,clf_constants.DATA_DIR,g_constants.CSV_POS_DATA)
KSFINDER_NEG_DATA = os.path.join(ROOT_DIR_RELATIVE_PATH,clf_constants.DATA_DIR,g_constants.CSV_NEG_DATA)
KSFINDER_PROTEINS = os.path.join(ROOT_DIR_RELATIVE_PATH,ksf_constants.DATA_DIR,ksf_constants.TXT_KG_PROTEINS)
KSFINDER_POS_TRAIN = os.path.join(ROOT_DIR_RELATIVE_PATH,clf_constants.DATA_DIR,g_constants.CSV_POS_TRAIN)
KSFINDER_NEG_TRAIN = os.path.join(ROOT_DIR_RELATIVE_PATH,clf_constants.DATA_DIR,g_constants.CSV_NEG_TRAIN)

ASSESS5_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,g_constants.ASSESS5_DATA_PATH)
ASSESS6_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,g_constants.ASSESS6_DATA_PATH)
ASSESS7_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,g_constants.ASSESS7_DATA_PATH)
ASSESS8_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,g_constants.ASSESS8_DATA_PATH)
ASSESS1_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,g_constants.ASSESS1_DATA_PATH)

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
                if prediction_probs.get(k_s,0) < score:
                    prediction_probs[k_s] = score
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