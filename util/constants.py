'''
The classes in this file maintains all the constants
'''

'''
This class maintains the generic constants used across the project
'''
class GlobalConstants:
    DATA_PATH = '../data/'
    OUTPUT_PATH = '../output/'
    RESULT_PATH = '../results/'
    RESULTS_PATH = 'results/'
    CSV_KG_TRAIN = 'kg_train.csv'
    CSV_POS_VALID = 'pos_valid.csv'
    CSV_NEG_VALID = 'neg_valid.csv'
    CSV_POS_TEST = 'pos_test.csv'
    CSV_NEG_TEST = 'neg_test.csv'
    CSV_POS_TRAIN = 'pos_train.csv'
    CSV_NEG_TRAIN = 'neg_train.csv'
    DIR_ASSESSMENT = 'assessment/'
    ASSESS1_DATA_PATH = DIR_ASSESSMENT+'assess1/'
    ASSESS2_DATA_PATH = DIR_ASSESSMENT+'assess2/'
    ASSESS3_DATA_PATH = DIR_ASSESSMENT+'assess3/'
    ASSESS4_DATA_PATH = DIR_ASSESSMENT+'assess4/'
    ASSESS5_DATA_PATH = DIR_ASSESSMENT+'assess5/'
    ASSESS6_DATA_PATH = DIR_ASSESSMENT+'assess6/'
    ASSESS7_DATA_PATH = DIR_ASSESSMENT+'assess7/'
    ASSESS8_DATA_PATH = DIR_ASSESSMENT+'assess8/'
    SCORES = 'scores.txt'
    PR_CURVE = 'pr_auc.png'
    ROC_CURVE = 'roc_auc.png'
    CSV_NEGATOME = 'negatome.csv'
    CSV_NEGATIVES_PREDKINKG_CC = 'predkinkg_negatives_cc.csv'
    CSV_POS_DATA = 'pos_data.csv'
    CSV_NEG_DATA = 'neg_data.csv'
    HEAD_TAIL = 'head,tail'
    KINASE_SUBSTRATE_PROB = 'kinase,substrate,prob'
    KINASE = 'kinase'
    KSFINDER = 'KSFinder'
    DIR_MISCELLANEOUS = 'miscellaneous/'
    MISC_OUTPUT = DIR_MISCELLANEOUS+'output/'
    
'''
This class maintains the constants used by knowledge graph embedding module
'''
class KGEConstants:
    KG_PHOSPHORYLATION = 'kg1.csv'
    KG_OTHER_REL = 'kg2.csv'
    PREDKINKG_NEGATIVES = 'predkinkg_negatives.csv'
    TXT_BEST_PARAMS_OUTPUT = 'best_params_output.txt'
    TRANSE = 'TransE'
    DISTMULT = 'DistMult'
    HOLE = 'HolE'
    COMPLEX = 'ComplEx'
    MODEL_PATH = 'kge/output/'
    DATA_PATH = 'kge/data/'

'''
This class maintains the constants used by the classifier module
'''
class ClfConstants:
    DATA_DIR = 'clf/data/'
    MODEL_PATH = 'clf/output/'

'''
This class maintains the constants used by KSFinder, includes predictions
'''
class KSFinderConstants:
    DATA_DIR = 'ksfinder/data/'
    RESULTS_DIR = 'ksfinder/results/'
    TXT_IDG_KINASES = 'idg_kinases.txt'
    TXT_KG_IDG_KINASES = 'kg_idg_kinases.txt'
    TXT_IDG_K_PREDICTIONS = 'idg_kinase_predictions.csv'
    TXT_KG_PROTEINS = 'kg_proteins.txt'

'''
This class maintains the constants used by the EnrichmentAnalysis module
'''
class EnrichmentAnalysisConstants:
    RESULTS_DIR = 'enrich_analysis/results/'
    PROTEIN_ID_TYPE = 'UNIPROT_ACCESSION'
    DAVID_WSDL = 'https://david.ncifcrf.gov/webservice/services/DAVIDWebService?wsdl'
    DAVID_ENDPOINT = 'https://david.ncifcrf.gov/webservice/services/DAVIDWebService.DAVIDWebServiceHttpSoap11Endpoint/'
    AUTH_EMAIL = 'manjua@udel.edu'
    BG_SET_LABEL = 1
    BG_SET_NAME = 'bg_proteins'
    QUERY_SET_LABEL = 0
    QUERY_SET_NAME = 'query_proteins'
    RESULT_HEADER = 'Category\tFoldEnrichment \t Corrected p-value (Benjamini) \t Raw p-value \t Term\n'
    CATEGORIES = ('GOTERM_BP_DIRECT','GOTERM_CC_DIRECT','GOTERM_MF_DIRECT')

'''
This class maintains the constants used by the TextMine component
'''
class TextMineConstants:
    DATA_DIR = 'textmine/data/'
    UNIPROT_GENE_FILE = 'uniprot_gene_name.txt'
    RESULTS_DIR = 'textmine/results/'
    EVIDENCE_FILE = 'raw_evidence.txt'
    ERR_FILE = 'err.txt'
    ITEXTMINE_API_URL = 'https://research.bioinformatics.udel.edu/itextmine/api/search/query/'
    RLIMS = 'rlims/'
    PMC = 'pmc/'
    MEDLINE = 'medline/'

'''
This class maintains the constants used for comparative assessments
'''
class ComparativeAssessmentConstants:
    DATA_DIR = 'compare/data/'
    LINKPHINDER_PREDICTIONS = 'linkphinder_predictions.csv'
    PREDKINKG_PREDICTIONS = 'predkinkg_predictions.csv'
    LINKPHINDER_RAW_DATA = 'linkphinder_raw_data'
    LINKPHINDER_BENCHMARK_9010 = 'benchmark9010'
    LINKPHINDER_TRAIN_FILE = 'train.tsv'
    LINKPHINDER_TEST_FILE = 'test.tsv'

class PreprocessConstants:
    DATA_DIR = 'preprocess/data/'
    CSV_BIOKG = 'BioKG.csv'
    CSV_GO = 'Gene_Ontology.csv'
    CSV_PRO = 'Protein_Ontology.csv'
    CSV_iPTMNET = 'iPTMnet.csv'
    CSV_iPTMNET_TEST = 'iPTMnet_test.csv'