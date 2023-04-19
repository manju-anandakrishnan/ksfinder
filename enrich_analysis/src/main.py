from enrich_analysis.src.prepare_data import DarkKinase
from enrich_analysis.src.perform_enrichment import DAVIDEnrichment

def process():

    david_enrichment = DAVIDEnrichment()

    # understudied_kinase = 'Q9H422' #HIPK3
    # dark_kinase = DarkKinase(understudied_kinase)
    # substrates = dark_kinase.get_substrates(0.9)
    # print(len(substrates))
    # david_enrichment.perform_analysis(understudied_kinase,substrates)

    understudied_kinase = 'Q8N5S9' #CAMKK1
    dark_kinase = DarkKinase(understudied_kinase)
    substrates = dark_kinase.get_substrates(0.9)
    print(len(substrates))
    david_enrichment.perform_analysis(understudied_kinase,substrates)

    # understudied_kinase = 'Q9H093' #NUAK2
    # dark_kinase = DarkKinase(understudied_kinase)
    # substrates = dark_kinase.get_substrates(0.93)
    # print(len(substrates))
    # #david_enrichment.perform_analysis(understudied_kinase,substrates)

    # understudied_kinase = 'P22612' #PRKACG
    # dark_kinase = DarkKinase(understudied_kinase)
    # substrates = dark_kinase.get_substrates(0.88)
    # print(len(substrates))
    # david_enrichment.perform_analysis(understudied_kinase,substrates)

    # understudied_kinase = 'Q6P5Z2' # PKN3
    # dark_kinase = DarkKinase(understudied_kinase)
    # substrates = dark_kinase.get_substrates(0.97)
    # print(len(substrates))
    # david_enrichment.perform_analysis(understudied_kinase,substrates)
    
    # understudied_kinase = 'Q8IV63' #
    # dark_kinase = DarkKinase(understudied_kinase)
    # substrates = dark_kinase.get_substrates(0.87)
    # print(len(substrates))
    # #david_enrichment.perform_analysis(understudied_kinase,substrates)
    
    # understudied_kinase = 'Q9Y3S1' #
    # dark_kinase = DarkKinase(understudied_kinase)
    # substrates = dark_kinase.get_substrates(0.83)
    # print(len(substrates))
    # david_enrichment.perform_analysis(understudied_kinase,substrates)

process()