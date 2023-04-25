from enrich_analysis.src.prepare_data import DarkKinase
from enrich_analysis.src.perform_enrichment import DAVIDEnrichment

def process():
    david_enrichment = DAVIDEnrichment()
    run_enrich = input('Are you sure you want to re-run DAVID enrichment analysis for HIPK3 and CAMKK1? Hit "Y" to continue else press another key')
    if run_enrich == 'Y':
        understudied_kinase = 'Q9H422' #HIPK3
        dark_kinase = DarkKinase(understudied_kinase)
        substrates = dark_kinase.get_substrates(0.9)
        david_enrichment.perform_analysis(understudied_kinase,substrates)

        understudied_kinase = 'Q8N5S9' #CAMKK1
        dark_kinase = DarkKinase(understudied_kinase)
        substrates = dark_kinase.get_substrates(0.9)
        david_enrichment.perform_analysis(understudied_kinase,substrates)
    
    # Add understudied kinases as required to perform the enrichment analysis. You may also update the threshold for probability values.


process()