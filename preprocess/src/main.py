'''
This is the main module for preprocessing the downloaded data from Zenodo to KG model build ready data.
'''

from preprocess.src.prepare_data import PrepareKGData

def process():

    prepare_kg_data = PrepareKGData()
    prepare_kg_data.run()

process()