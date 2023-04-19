from ampligraph.latent_features import TransE
from ampligraph.latent_features import DistMult
from ampligraph.latent_features import HolE
from ampligraph.latent_features import ComplEx
from ampligraph.evaluation import select_best_model_ranking
from ampligraph.utils import save_model
from ampligraph.datasets import load_from_csv
import os
import pandas as pd
import numpy as np
from util.constants import GlobalConstants as g_constants
from util.constants import KGEConstants as kge_constants

KGE_OUTPUT_PATH = g_constants.OUTPUT_PATH
OUTPUT_FILE = kge_constants.TXT_BEST_PARAMS_OUTPUT
KG_DATA_PATH = g_constants.DATA_PATH

class KGE:

    algorithms = {kge_constants.COMPLEX: ComplEx, 
                  kge_constants.TRANSE: TransE, 
                  kge_constants.DISTMULT: DistMult, 
                  kge_constants.HOLE: HolE} 
    
    param_grid = {
        "batches_count": [8,12,16],
        "epochs": [10000],
        "k": [90, 120, 150],
        "eta": [10, 15, 20],
        "embedding_model_params": {
            'negative_corruption_entities': 'batch', 
            'corrupt_sides': 's+o'
        },
        "loss": ["pairwise", "multiclass_nll"],
        "regularizer": ["LP"],
        "regularizer_params": {
            "p": [1, 2, 3],
            "lambda": [1e-5]
        },
        "optimizer": ["adam"],
        "optimizer_params": {
            "lr": [0.001,0.0001]
        },
        "verbose": True        
    }

    def __init__(self,algorithm_nm):
        self.algorithm_nm = algorithm_nm
        self.algorithm = KGE.algorithms[algorithm_nm]

    def _load_data(self):
        self.training = load_from_csv('.', os.path.join(KG_DATA_PATH,g_constants.CSV_KG_TRAIN), sep=',', header=0)
        self.validation = load_from_csv('.', os.path.join(KG_DATA_PATH,g_constants.CSV_POS_VALID), sep=',', header=0)
        self.test = load_from_csv('.', os.path.join(KG_DATA_PATH,g_constants.CSV_POS_TEST), sep=',', header=0)

    def _load_corruption_entities(self):
        kg = pd.DataFrame(self.training,columns=['head','rel','tail'])
        self.corruptions = list(kg[kg['rel']=='p']['tail'].unique())
        self.corruptions.extend(list(kg[kg['rel']=='p']['head'].unique()))
        self.corruptions = list(set(self.corruptions))

    def _load_filter_triples(self):
        self.filter_triples = np.concatenate((self.training,self.validation,self.test))

    def _store_model(self):        
        output_file = self.algorithm_nm+'_params.txt'
        output_model = self.algorithm_nm+'.pkl'
        op_file = open(os.path.join(KGE_OUTPUT_PATH,output_file),'w')
        op_file.write('Recording best hyperparameters for model::'+self.algorithm_nm+'\n')
        op_file.write('Best parameters::'+str(self.best_params)+'\n')
        op_file.write('Best MRR valid::'+str(self.best_mrr_valid)+'\n')
        op_file.write('Test Evaluation::'+str(self.test_evaluation)+'\n')
        op_file.close()
        save_model(self.best_model, model_name_path=os.path.join(KGE_OUTPUT_PATH,output_model))

    def _find_best_hyperparameters(self):
        best_model, best_params, best_mrr_train, _, test_evaluation, experimental_history = select_best_model_ranking (
                self.algorithm, self.training, self.validation, self.test,
                self.param_grid,
                entities_subset = self.corruptions,
                corrupt_side = 'o',
                early_stopping=True, 
                early_stopping_params={'x_valid': self.validation, 
                                    'criteria':'mrr',
                                    'corruption_entities': self.corruptions,
                                    'x_filter': self.filter_triples,
                                    'burn_in': 300,
                                    'check_interval': 100,
                                    'corrupt_side':'o'})
        self.best_model=best_model
        self.best_params=best_params
        self.best_mrr_valid=best_mrr_train
        self.test_evaluation=test_evaluation
        self._store_model()

    def run(self):
        self._load_data()
        self._load_corruption_entities()
        self._load_filter_triples()
        self._find_best_hyperparameters()
