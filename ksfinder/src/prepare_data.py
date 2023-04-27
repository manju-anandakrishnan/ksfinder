import os
from util.constants import GlobalConstants as g_constants
from util.constants import KGEConstants as kge_constants
from util.constants import KSFinderConstants as ksf_constants


ROOT_DIR_RELATIVE_PATH = ''
KG_PHOSPHORYLATION_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,kge_constants.DATA_PATH,kge_constants.KG_PHOSPHORYLATION)
KSFINDER_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,ksf_constants.DATA_DIR)
KG_PROTEINS = os.path.join(KSFINDER_DATA_PATH,ksf_constants.TXT_KG_PROTEINS)
IDG_KINASES = os.path.join(KSFINDER_DATA_PATH,ksf_constants.TXT_IDG_KINASES)
KG_KINASES = os.path.join(KSFINDER_DATA_PATH,ksf_constants.TXT_KG_KINASES)
KG_IDG_KINASES = os.path.join(KSFINDER_DATA_PATH,ksf_constants.TXT_KG_IDG_KINASES)
IDG_K_S = os.path.join(KSFINDER_DATA_PATH,ksf_constants.TXT_IDG_K_PREDICTIONS)

'''
This class compares the dark kinases reported by IDG with the proteins in our KG and creates an ouput with the overlapping 68 IDGs
'''
class IDGDataLoader:

    def __init__(self):
        self.idg_kinases = list()
        with open(IDG_KINASES) as ip_f:
            for line in ip_f:
                self.idg_kinases.append(line.strip())

    def get_idg_kg_kinases(self):
        self.idg_kg_kinases = set()
        with open(KG_PHOSPHORYLATION_PATH) as ip_f:
            ip_f.readline()
            for line in ip_f:
                line_vals = line.strip().split(',')
                kinase = line_vals[0]
                if kinase in self.idg_kinases:
                    self.idg_kg_kinases.add(kinase)
                    
        with open(KG_IDG_KINASES,'w') as op_f:
            op_f.write(g_constants.KINASE+'\n')
            for kinase in self.idg_kg_kinases:
                op_f.write(kinase+'\n')
        return self.idg_kg_kinases


'''
This class loads all the kinases in the knowledge graph
'''
class KGKinasesDataLoader:

    def __init__(self):
        self.kg_kinases = list()
    
    def get_kg_kinases(self):
        with open(KG_KINASES) as ip_f:
            ip_f.readline()
            for line in ip_f:
               self.kg_kinases.append(line.strip())
        return self.kg_kinases
    

