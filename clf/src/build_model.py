from util.constants import GlobalConstants as g_constants
from util.constants import KGEConstants as kge_constants
from util.constants import ClfConstants as clf_constants
from ampligraph.utils import restore_model
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import average_precision_score,roc_auc_score,roc_curve,precision_recall_curve
import pickle
import numpy as np
import pandas as pd
import os

ROOT_DIR_RELATIVE_PATH = ''
KGE_MODEL_DIR = os.path.join(ROOT_DIR_RELATIVE_PATH,kge_constants.MODEL_PATH)

CLF_DATA_DIR = os.path.join(ROOT_DIR_RELATIVE_PATH,clf_constants.DATA_DIR)
POS_TRAIN = os.path.join(CLF_DATA_DIR,g_constants.CSV_POS_TRAIN)
NEG_TRAIN = os.path.join(CLF_DATA_DIR,g_constants.CSV_NEG_TRAIN)

CLF_OUTPUT_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,clf_constants.MODEL_PATH)
KSFINDER_PATH = os.path.join(CLF_OUTPUT_PATH,g_constants.KSFINDER+'.sav')

'''
This class scales the input data, performs cross validation, builds a neural network classifier and stores the trained model.
'''
class NNClassifier:

    mlpc_params = {
              "alpha": [0.0001],
              "hidden_layer_sizes": [(40,)],
              "solver" : ["adam"],
              "learning_rate_init":[0.0001],
              "activation": ["relu"],
              "max_iter":[500]}
    
    mlpc = MLPClassifier(random_state=10, 
                         validation_fraction=0.1, 
                         early_stopping=True,
                         shuffle=True,
                         verbose=False)

    def __init__(self):
        self.kge_model =  restore_model(model_name_path=os.path.join(KGE_MODEL_DIR,kge_constants.COMPLEX+'.pkl'))
        self.scaler = StandardScaler()
        self.scaler_fitted = False

    def get_emb_vector(self,entity):
        return self.kge_model.get_embeddings(entity)

    def get_ht_vector(self,data,label):
        data = data.split(',')
        h_vector = self.kge_model.get_embeddings(data[0])
        t_vector = self.kge_model.get_embeddings(data[1])
        ht_vector = np.concatenate((h_vector,t_vector,np.array([label])))
        return ht_vector

    def _load_train_data(self):
        clf_train = list()
        with open(POS_TRAIN) as ip_f:
            ip_f.readline()
            for record in ip_f:
                clf_train.append(self.get_ht_vector(record.strip(),1))
        with open(NEG_TRAIN) as ip_f:
            ip_f.readline()
            for record in ip_f:
                clf_train.append(self.get_ht_vector(record.strip(),0))
        clf_train = pd.DataFrame(clf_train)
        shape = clf_train.shape
        label_index = shape[1]-1
        self.train_features = np.array(clf_train.iloc[:,:label_index])
        self.train_target = clf_train.iloc[:,label_index].astype('int').values       
    
    def _store_model(self):
        output_model = KSFINDER_PATH
        pickle.dump(self.ksfinder,open(output_model,'wb'))

    def _fit_scaler(self):
        self.scaler.fit(self.train_features)
        self.scaler_fitted=True

    def _train_model(self):   
        self._fit_scaler()    
        scaled_train = self.scaler.transform(self.train_features)
        mlpc_cv_model = GridSearchCV(NNClassifier.mlpc, NNClassifier.mlpc_params, 
                         cv = 10, 
                         n_jobs = -1, 
                         )
        mlpc_cv_model.fit(scaled_train, self.train_target)
        print("The best parameters: " + str(mlpc_cv_model.best_params_))
        print(mlpc_cv_model.best_estimator_)
        print(mlpc_cv_model.best_score_)
        self.ksfinder = mlpc_cv_model.best_estimator_
        self.ksfinder.fit(scaled_train, self.train_target)
        self._store_model()

    def transform(self,features):
        if not self.scaler_fitted:
            self._load_train_data()
            self._fit_scaler()
        return self.scaler.transform(features)

    def run(self):
        self._load_train_data()
        self._train_model()




