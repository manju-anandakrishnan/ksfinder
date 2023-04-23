# Setting the PYTHONPATH and home directory of KSFinder
KSFINDER_HOME_DIR=$(pwd)
PYTHONPATH=$KSFINDER_HOME_DIR

# Download the raw KG data
cd $KSFINDER_HOME_DIR/preprocess/data
wget https://zenodo.org/record/7856947/files/KSFinder_KG_data.zip
unzip KSFinder_KG_data.zip

# Download the trained KGE models
cd $KSFINDER_HOME_DIR/kge/output
wget https://zenodo.org/record/7856947/files/KGE_models.zip
unzip KGE_models.zip

# Download the KSFinder model
cd $KSFINDER_HOME_DIR/clf/output
wget https://zenodo.org/record/7856947/files/KSFinder.zip
unzip KSFinder.zip
