#!/bin/bash

# This initialization script downloads the data and models for KSFinder
# Setting the PYTHONPATH and home directory of KSFinder
KSFINDER_HOME_DIR=$(pwd)

# Download the raw KG data
cd $KSFINDER_HOME_DIR/preprocess/data
wget https://zenodo.org/record/7856947/files/KSFinder_KG_data.zip
unzip KSFinder_KG_data.zip
rm KSFinder_KG_data.zip

# Download the trained KGE models
cd $KSFINDER_HOME_DIR/kge/output
wget https://zenodo.org/record/7856947/files/KGE_models.zip
unzip KGE_models.zip
rm KGE_models.zip

# Download the KSFinder model
cd $KSFINDER_HOME_DIR/clf/output
wget https://zenodo.org/record/7856947/files/KSFinder.zip
unzip KSFinder.zip
rm KSFinder.zip

# Download LinkPhinder predictions
cd $KSFINDER_HOME_DIR/compare/data
wget https://doi.org/10.1371/journal.pcbi.1007578.s008
bunzip2 journal.pcbi.1007578.s008
mv journal.pcbi.1007578.s008.out linkphinder_predictions.csv

wget https://doi.org/10.1371/journal.pcbi.1007578.s009
tar -xf journal.pcbi.1007578.s009
rm journal.pcbi.1007578.s009

# Download PredKinKG predictions
wget https://github.com/udel-cbcb/ikg_v2_public/releases/download/1.0.0/supplementary_file_3.csv
mv supplementary_file_3.csv predkinkg_predictions.csv

wget https://figshare.com/ndownloader/files/22378023
unzip 22378023
rm 22378023
mv linkphinder_data_splits linkphinder_raw_data
cd linkphinder_raw_data
rm -rf !(benchmark9010)
