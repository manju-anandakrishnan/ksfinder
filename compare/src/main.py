from assess import Assessment
from util.constants import GlobalConstants as g_constants
from prepare_data import LinkPhinderData, PredKinKGData
from clf.src.assess import Assessment as clf_assessment

def process():

    linkphinder = LinkPhinderData()
    predkinkg = PredKinKGData()
    
    # print('Loading linkphinder data---',flush=True)
    # linkphinder.load_data()

    # print('Assessment 5---',flush=True)
    # assessment5 = clf_assessment(g_constants.ASSESS5_DATA_PATH)
    # assessment5.run()

    # print('Loading PredKinKG data---',flush=True)
    # predkinkg.load_data()

    # print('Assessment 6---',flush=True)
    # assessment6 = clf_assessment(g_constants.ASSESS6_DATA_PATH)
    # assessment6.run()
    
    print('--Loading LinkPhinder prediction data---',flush=True)
    linkphinder.load_predictions()

    print('Assessment 7---',flush=True)
    assessment7 = Assessment(g_constants.ASSESS7_DATA_PATH)
    assessment7.run()

    print('Loading predkinkg prediction data---',flush=True)
    predkinkg.load_predictions()

    print('Assessment 8---',flush=True)
    assessment8 = Assessment(g_constants.ASSESS8_DATA_PATH)
    assessment8.run()

process()