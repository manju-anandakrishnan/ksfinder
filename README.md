git clone https://github.com/manju-anandakrishnan/ksfinder.git
cd ksfinder

# Create environment and load libraries
conda create --name <env name> python=3.7
conda activate <env name>
conda install --file requirements.txt
pip install ampligraph
pip install ordered_set

# Download the data
cd preprocess/data
wget https://zenodo.org/record/7806916/files/KSFinder_KG_data.zip?download=1
unzip KSFinder_KG_data

# Load KG data & assess the model
python kge/src/main.py

# To train knowledge graph embedding models from scratch, pass the argument --t_kge=True to the above script (KGE embedding from scratch may take weeks to complete depending on the GPU capability. Optionally use the trained KGE models)

# The results of evaluation and test data will be loaded in the appropriate assessment folders.

# Train the MLP classifier and assess KSFinder
python clf/src/main.py

# Comparative assessments (Assessment 5, 6, 7, 8)
python compare/src/main.py

# Predict using KSFinder
python ksfinder/src/main.py

# Literature mining using iTextMine API
python textmine/src/main.py

# Enrichment Analysis using the predicted substrates
python enrich_analysis/src/main.py




