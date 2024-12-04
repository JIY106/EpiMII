# EpiMII: An Advanced GNN Model for Re/Co-designing MHC-II Epitopes and Neoantigens 
## Overview:

<p align="center">
<img width="100" src="https://github.com/JIY106/EpiMII/blob/main/figures/Figure%204.png">
</p>


## Quick guide
1. Set up conda environment:
   ```
   conda env create -f epim2.yml
   conda activate epim2
   ```
2. Open 'Run_JY_try_epitope.ipynb' in _testing_ folder in <ins>Jupyterlab </ins> or <ins>Jupyter notebook </ins>.
3. 
## Training Data Preparation:
1. Collect epitope sequences and save them as multiple FASTA files. One epitope sequence is in one FASTA, like './dataset/Modeller/fasta/86269.fasta'.
2. Modeling 3D structures of epitope sequences using MODELLER:
   1) Download MODELLER from [https://salilab.org/modeller/download_installation.html] and register for a license. (MODELLER is available free of charge to academic non-profit institutions)

      Open cmd or MODELLER.exe and go to the _Modeller_ folder.
      ```
      cd ./dataset/Modeller
      ```
      Unzip templates that will be used in MODELLER.
      ```
      tar zxf ./templates.tar.gz .
      ```
   2) Two approaches to modeling epitopes' 3D structures:
      * **Approach one:** Structure modeling only without calculating sequence similarity.
        
      Run Fast2Pir.sh to generate .ali files for all FASTA files. The output .ali files will be stored in the _ali_ folder.
      ```
      ./FAST2Pir.sh
      ```
      Run Buildmodel2.py to start modeling. Then, you will get the Modelled .pdb files in the current folder with temporary files.
      ```
      python Buildmodel2.py
      ```
      * **Approach two:** Calculating sequence similarity and structure modeling.
     
      Run CalculateSimilarityAndSave.py and get output1.txt that contains the epitiopes' name, best template and the sequence similarity. The best template here means the template has the highest sequence similarity with the epitoipe sequence.
      ```
      python CalculateSimilarityAndSave.py
      ```
      Run Data-clean.ipynb in <ins>Jupyterlab </ins> or <ins>Jupyter notebook </ins> to get haha.txt. The final output will be .ali files in _ali1_ folder and combined_output1.txt which contains epitopes' name, epitopes' sequence, best template, and sequence similarity.
      
      Run Build-model3.py to construct the 3D structures of epitopes using their best template. The output pdb files will be stored in _output_pdb_ folder. All temporpary files will be automatically deleted as shown in the script.
3. Convert pdb files to mmcif files.
   1) Download MAXIT Suite from [https://sw-tools.rcsb.org/apps/MAXIT/index.html] to your Linux/Unix environment or WSL. Then, follow the README file inside maxit folder to install MAXIT.
   2) Go to _script_ folder and run multiple_mmcif.sh to convert multiple pdb files to mmcif files. The output cif files will be stored in _../mmcif_ folder.
      ```
      cd ..
      cd scripts
      ./multiple_mmcif.sh
      ```
4. Convert mmcif files to pt files. The output pt files will be stored in _../pt_ folder.
   ```
   ./multiple_convert_cif_to_pt.sh
   ```
## Available sources:
* The dataset (pt files) used in EpiMII paper can be downloaded from []. If you would like to retrain the model, please put all pt files in this directory _./training/training_data/pdb/pt_.
* The MODELLER-modeled 3D structures of 142934 MHC-II epitopes (pdb files) used in EpiMII paper can be downloaded from [].
* All model weights can be downloaded from []. In the EpiMII paper, 'epoch50_step47050.pt' are used as the final model weight '128_earlystop.pt'.
* 133 3D structures obtained by X-ray crystalography of MHC-II epitopes collected from PDB can be found in the directory _./dataset/3D_crystalized_all.tar.gz_.
* Original csv file that contains around 480,000 MHC-II epitopes' sequences collected from IEDB can be found in the directory _./dataset/list_no_cluster.zip_.
   
