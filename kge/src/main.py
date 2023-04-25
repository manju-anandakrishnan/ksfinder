'''

'''
import argparse
from prepare_data import KGEDataLoader
from prepare_data import EvaluationData
from build_model import KGE
from assess import Assessment
from util.constants import KGEConstants as kge_constants
from util.constants import GlobalConstants as g_constants

class KGEProcessor:

    def train_kge():   
        kge_transE = KGE(kge_constants.TRANSE)
        kge_transE.run()
        kge_distmult = KGE(kge_constants.DISTMULT)
        kge_distmult.run()
        kge_complex = KGE(kge_constants.COMPLEX)
        kge_complex.run()
        kge_hole = KGE(kge_constants.HOLE)
        kge_hole.run()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--t_kge',default=False)
    args = parser.parse_args()

    if args.t_kge:
        print('Beginning the training of the knowledge graph embedding models. This may take weeks depending on the GPU capability. Optionally use may use the trained embedding models.')
        is_train = input("Are you sure you want to train the models from scratch? Hit 'Y' to continue, else press any other key")
        if is_train == 'Y':
            data_loader = KGEDataLoader()
            data_loader.run()
            KGEProcessor.train_kge()    
            evaluation_data = EvaluationData()
            evaluation_data.run()
        
    assessment1 = Assessment(g_constants.ASSESS1_DATA_PATH)
    assessment1.run(kge_constants.TRANSE)
    assessment1.run(kge_constants.DISTMULT)
    assessment1.run(kge_constants.COMPLEX)
    assessment1.run(kge_constants.HOLE)
        
    assessment2 = Assessment(g_constants.ASSESS2_DATA_PATH)
    assessment2.run(kge_constants.TRANSE)
    assessment2.run(kge_constants.DISTMULT)
    assessment2.run(kge_constants.COMPLEX)
    assessment2.run(kge_constants.HOLE)