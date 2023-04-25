import pandas as pd
import os
from suds.client import Client
from util.constants import EnrichmentAnalysisConstants as ea_constants
from util.constants import KSFinderConstants as ksf_constants

ROOT_DIR_RELATIVE_PATH = ''
KSFINDER_DATA_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,ksf_constants.DATA_DIR)
KG_PROTEINS = os.path.join(KSFINDER_DATA_PATH,ksf_constants.TXT_KG_PROTEINS)
ENRICH_RESULTS_PATH = os.path.join(ROOT_DIR_RELATIVE_PATH,ea_constants.RESULTS_DIR)

class DAVIDEnrichment:

    URL = ea_constants.DAVID_WSDL
    LOCATION = ea_constants.DAVID_ENDPOINT
    ID_TYPE = ea_constants.PROTEIN_ID_TYPE

    def __init__(self):
        self.client = Client(DAVIDEnrichment.URL)
        self.client.wsdl.services[0].setlocation(DAVIDEnrichment.LOCATION)
        self.client.service.authenticate(ea_constants.AUTH_EMAIL)
        self.bg_proteins = '' 
        self._load_bg_proteins()

    def _load_bg_proteins(self):               
        with open(KG_PROTEINS) as subs_f:
            subs_f.readline()
            for line in subs_f: self.bg_proteins+=line.rstrip('\n')+','
    
    def _prepare_request(self,substrates):
        query_proteins = ''
        for protein in substrates: 
            query_proteins+=protein+','
        self.client.service.addList(query_proteins, DAVIDEnrichment.ID_TYPE, ea_constants.QUERY_SET_NAME, ea_constants.QUERY_SET_LABEL)
        self.client.service.addList(self.bg_proteins, DAVIDEnrichment.ID_TYPE, ea_constants.BG_SET_NAME, ea_constants.BG_SET_LABEL)

    def _call_client(self):
        threshold_ease = 0.1
        pr_count = 2
        results = self.client.service.getChartReport(threshold_ease,pr_count)
        return results

    def _parse_response(self,results):
        category_results = {}
        for result in results:
            categoryName = result.categoryName
            if categoryName in ea_constants.CATEGORIES:
                category_results.setdefault(categoryName,list())
                if round(result.benjamini,5) <= 0.1:
                    record = [round(result.foldEnrichment,3),result.benjamini,result.ease,result.termName]
                    category_results.get(categoryName).append(record)                    
        category_results = self._sort(category_results)
        return category_results

    def _sort(self,category_results):
        for category in category_results.keys():
            records = category_results.get(category)
            sorted_benjamini_p_value = sorted(records,key=lambda x:(x[1]))
            sorted_fold = sorted(sorted_benjamini_p_value,key=lambda x:(x[0]),reverse=True)
            category_results[category] = sorted_fold
        return category_results
    
    def _write(self,kinase,category_results):
        op_f = open(ENRICH_RESULTS_PATH+kinase+'.txt','w')
        op_f.write(ea_constants.RESULT_HEADER)
        for category in ea_constants.CATEGORIES:
            records = category_results.get(category)
            for record in records:
                print(category,file=op_f,end='\t')
                for value in record:
                    print(value,file=op_f,end='\t')
                print(file=op_f)
        op_f.close()

    def perform_analysis(self,kinase,substrates):        
        self._prepare_request(substrates)
        results = self._call_client()
        category_results = self._parse_response(results)
        self._write(kinase,category_results)



        

        




    