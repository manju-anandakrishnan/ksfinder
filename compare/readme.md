download linkphinder predictions from here - 
wget https://doi.org/10.1371/journal.pcbi.1007578.s008
bunzip2 journal.pcbi.1007578.s008
mv journal.pcbi.1007578.s008.out linkphinder_predictions.csv

wget https://doi.org/10.1371/journal.pcbi.1007578.s009
tar -xf journal.pcbi.1007578.s009
rm journal.pcbi.1007578.s009

https://github.com/udel-cbcb/ikg_v2_public/releases/download/1.0.0/supplementary_file_3.csv
mv supplementary_file_3.csv predkinkg_predictions.csv

wget https://figshare.com/ndownloader/files/22378023
unzip 22378023
rm 22378023
mv linkphinder_data_splits linkphinder_raw_data
cd linkphinder_raw_data
rm -rf !(benchmark9010)