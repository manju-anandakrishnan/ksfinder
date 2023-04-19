import requests
import json
import time
import os
import pandas as pd
from util.constants import KSFinderConstants as ksf_constants
from util.constants import TextMineConstants as tm_constants
from util.constants import KGEConstants as kge_constants

ROOT_DIR_RELATIVE_PATH = '../../'
KSFINDER_RESULT_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,ksf_constants.RESULTS_DIR)
DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,tm_constants.DATA_DIR)
UNIPROT_GENE_NAME_FILE = os.path.join(DATA_PATH,tm_constants.UNIPROT_GENE_FILE)
EVIDENCE_FILE = os.path.join(ROOT_DIR_RELATIVE_PATH,tm_constants.RESULTS_DIR, tm_constants.EVIDENCE_FILE)
ERR_FILE = os.path.join(ROOT_DIR_RELATIVE_PATH,tm_constants.RESULTS_DIR, tm_constants.ERR_FILE)
KG_PHOSPHORYLATION = os.path.join(ROOT_DIR_RELATIVE_PATH,kge_constants.DATA_PATH,kge_constants.KG_PHOSPHORYLATION)

class APIResponseError(Exception):

    def __init__(self,response_code,source,query):
        self.message = 'Error::Response Code:'+str(response_code)+' Source:'+source+' Query:'+query

    def get_message(self):
        return self.message

class TextMine:

    PMC_URL = tm_constants.ITEXTMINE_API_URL+tm_constants.RLIMS+tm_constants.PMC
    MEDLINE_URL = tm_constants.ITEXTMINE_API_URL+tm_constants.RLIMS+tm_constants.MEDLINE

    def __init__(self):
        pass

    def _parse_response(self,response,kinase_names,substrate_names):
        #if response.status_code != 200: return None
        result = json.loads(response.text)  
        for res in result:
            kinase_found = False
            res_kinase = res['KINASE']
            k_text = ''
            if len(res_kinase) > 0:
                k_text = res_kinase[0].get('text')
            res_substrate = res['SUBSTRATE']
            s_text = ''
            if len(res_substrate) > 0:
                s_text = res_substrate[0].get('text')
            for kinase in kinase_names:
                if kinase in k_text:
                    kinase_found = True
                    break
            if kinase_found:
                for substrate in substrate_names:
                    if substrate in s_text:
                        return (kinase,substrate)

    def perform_search(self,query, kinase_nm, substrate_nm):
        kinase_names = kinase_nm.split(' ')
        substrate_names = substrate_nm.split(' ')
        response = requests.get(TextMine.PMC_URL+query)
        if (response.status_code == 200) & (response == '[]'): return None
        try:
            result =  self._parse_response(response,kinase_names,substrate_names)
        except:
            raise APIResponseError(response.status_code,'PMC',query)
        if result is None: 
            response = requests.get(TextMine.MEDLINE_URL+query)
            if (response.status_code == 200) & (response == '[]'): return None
            try:
                result = self._parse_response(response,kinase_names,substrate_names)
            except:
                raise APIResponseError(response.status_code,'MEDLINE',query)
        return result
        
class Predictions:

    PREDICTION_FILE_PATH = os.path.join(KSFINDER_RESULT_PATH,ksf_constants.TXT_IDG_K_PREDICTIONS)

    def __init__(self,l_prob=0,h_prob=1):
        pred_data = pd.read_csv(Predictions.PREDICTION_FILE_PATH,sep=',')
        self.l_prob = l_prob
        self.h_prob = h_prob
        self.pred_data = pred_data[(pred_data['prob'] > l_prob) & (pred_data['prob'] <= h_prob)].copy()
        self.uniprot_gene = {}
        with open(UNIPROT_GENE_NAME_FILE) as ip_f:
            ip_f.readline()
            for record in ip_f:
                record_vals = record.strip().split(':')
                self.uniprot_gene[record_vals[0]] = record_vals[1]
        kg_df = pd.read_csv(KG_PHOSPHORYLATION,sep=',')
        kg_df['ht'] = kg_df['head']+kg_df['tail']
        self.kg_ks = kg_df['ht'].to_list()

    def _build_query(self, kinase_nm, substrate_nm):
        kinase_nm = kinase_nm.replace(' ',' OR ')
        substrate_nm = substrate_nm.replace(' ', ' OR ')
        query = '('+kinase_nm+') AND ('+substrate_nm+')'
        return query

    def search_literature(self):
        #op_f_err = open(ERR_FILE+'_'+str(self.l_prob)+'_'+str(self.h_prob),'w')
        op_f_success = open(EVIDENCE_FILE+'_'+str(self.l_prob)+'_'+str(self.h_prob),'w')
        text_mine = TextMine()
        record_cnt = self.pred_data.shape[0]
        print(record_cnt)
        for i in range(record_cnt):
            time.sleep(0.5)
            if i%100 == 0: print(i,flush=True)
            kinase = self.pred_data.iloc[i]['kinase']
            substrate = self.pred_data.iloc[i]['substrate']
            ks = kinase+substrate
            if ks in self.kg_ks: continue
            prob = self.pred_data.iloc[i]['prob']
            kinase_nm = self.uniprot_gene[kinase]
            substrate_nm = self.uniprot_gene[substrate]
            query = self._build_query(kinase_nm,substrate_nm)
            try:
                result = text_mine.perform_search(query, kinase_nm, substrate_nm) 
                if result:
                    print(prob,kinase,substrate,query,'::::',result,file=op_f_success,flush=True)   
            except APIResponseError as api_e:
                time.sleep(1)