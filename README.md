git clone https://github.com/manju-anandakrishnan/ksfinder.git <br>
cd ksfinder <br>

# Create environment and load libraries
conda create --name ksf_env python=3.7 <br>
conda activate ksf_env <br>
conda install --file requirements.txt <br>
pip install ampligraph <br>
pip install ordered_set <br>
pip install suds <br>
conda install openpyxl

Hardware Requirements -  Nvidia GPU with at least 16 GB memory and support for CUDA 10.0 or higher.

# Initialize & download the data from Zenodo
bash init.sh <br>
export PYTHONPATH=$(pwd)

# Load KG data & assess the model (Assessment 1 & 2)
python preprocess/src/main.py <br>
python kge/src/main.py <br>

To train knowledge graph embedding models from scratch, pass the argument --t_kge=True to the above script (KGE embedding from scratch may take weeks to complete depending on the GPU capability. Optionally use the trained KGE models)

The results of evaluation and test data will be loaded in the assessment folders 1 & 2.

# Train the MLP classifier and assess KSFinder (Assessment 3 & 4)
python clf/src/main.py <br>

To train the classifier model with the embedded vectors, pass the argument --t_clf=True to the above script.
The results of evaluation and test data will be loaded in the assessment folders 3 & 4.

# Comparative assessments (Assessment 5, 6, 7, 8, 9)
python compare/src/main.py <br>
The results of evaluation and test data will be loaded in the appropriate assessment folders.

# Predict using KSFinder
python ksfinder/src/main.py <br>
The prediction results will be loaded in the folder, ksfinder/results

# Literature mining using iTextMine API
python textmine/src/main.py <br>

# Enrichment Analysis using the predicted substrates
python enrich_analysis/src/main.py <br>

By using the data or code in this repository, you accept the terms and conditions governed by the license.

# Cite this work as,
Anandakrishnan M, Ross KE, Chen C, Shanker V, Cowart J, Wu CH. 2023. KSFinder—a knowledge graph model for link prediction of novel phosphorylated substrates of kinases. PeerJ 11:e16164 https://doi.org/10.7717/peerj.16164
