'''

'''

from prepare_data import KGEDataLoader
from prepare_data import EvaluationData
from build_model import KGE
from assess import Assessment
from util.constants import KGEConstants as kge_constants
from util.constants import GlobalConstants as g_constants

def process():
    # data_loader = KGEDataLoader()
    # data_loader.run()
    
    # kge_transE = KGE(kge_constants.TRANSE)
    # kge_transE.run()
    # kge_distmult = KGE(kge_constants.DISTMULT)
    # kge_distmult.run()
    # kge_complex = KGE(kge_constants.COMPLEX)
    # kge_complex.run()
    # kge_hole = KGE(kge_constants.HOLE)
    # kge_hole.run()

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

process()