# EpiMII: An Advanced GNN Model for Re/Co-designing MHC-II Epitopes and Neoantigens 

<p align="center">
<img width="1000" src="https://github.com/JIY106/EpiMII/blob/main/figures/Figure%204.png">
</p>
This is a repo of EpiMII. Please read EpiMII [paper](url).

## Quick guide
1. Set up conda environment:
   ```
   conda env create -f epim2.yml
   conda activate epim2
   ```
2. Download [MODELLER](https://salilab.org/modeller/download_installation.html) and register for a license. (MODELLER is available free of charge to academic non-profit institutions.)\
   Open cmd or MODELLER.exe and go to the _Modeller_ folder.
   ```
   cd ./dataset/Modeller
   ```
   Unzip templates that will be used in MODELLER.
   ```
   tar zxf ./templates.tar.gz .
3. Open 'Run_JY_try_epitope.ipynb' in _testing_ folder in <ins>JupyterLab </ins> or <ins>Jupyter notebook </ins>.
4. Please check the model_name is '128_earlystop'.
5. To test the code, use pdb files in _sample_data_ folder. Make sure to open the pdb files and check the Chain ID. Run all lines in this .ipynb file, then redesigned epitope sequences with their sequence recoveries will be output.
   ```
   'designed_chain = "B"      #change B with the correct Chain ID.
   ```
6. Example of redesigning epitope or neoantigen: (here, use a neoantigen as an example.) \
   Input: MODELLER-modeled 3D structure of the neoantigen (.pdb file). 
   * Prepare the FASTA file of the neoantigen. Run Fast2Pir.sh to generate a .ali file for the FASTA file. The output .ali file will be stored in the _ali_ folder.
   ```
   ./FAST2Pir.sh
   ```
   * Run Buildmodel2.py to start modeling. Then, you will get the modeled .pdb files in the current folder with temporary files.
   ```
   python Buildmodel2.py
   ```
   * Run Run_JY_try_epitope.ipynb in <ins>JupyterLab </ins> or <ins>Jupyter notebook </ins>.
   ```
   pdb = 'xxxx'      #make sure to change this to your modeled neoantigen name
   pdb_path = 'your_pdb_path/xxxx.pdb'      #make sure to change this to your modeled neoantigen name
   designed_chain = 'A'      #the chain ID for all MODELLER-modeled epitopes is A.
   ```
7. Mask strategy:
   * Open 1bx2_mhcii.pdb in [Pymol](https://www.pymol.org/) and open the 3D structure of the modeled neoantigen (input pdb file).\
     Copy chain C of 1bx2_mhcii as a new object (1bx2 epitope). Show sticks and hide cartoons of both 1bx2 epitope and modeled neoantigen.
      > Because MODELLER uses 3D templates to model neoantigens, the modeled neoantigens have already aligned with templates.
   * Find the correct position using [1bx2-mhcii complex](https://www.rcsb.org/structure/1bx2) as reference (use 83269.pdb as an example).
   
   ![image](https://github.com/user-attachments/assets/e9964828-e7ee-4914-9059-0bb1bf882423)
   <p align="center">
   <img width="500" src="https://github.com/JIY106/EpiMII/blob/main/figures/Position_example.png">
   </p>
   
   * In Run_JY_try_epitope.ipynb, input the masked residues. The first residue index in the pdb file is 1. The output sequence recovery is calculated on the sequence without the masked residues.
   ```
   fixed_positions_dict ={'83269':{'A': [3,4,9,10,11]}}      #Here mask positions are: 2,3,8,9,10, but input the corresponding residue indexes in pdb file.
   ```

## Example output:
```
>83269, score=0.5653, global_score=0.5653, fixed_chains=[], designed_chains=['A'], model_name=128_earlystop, seed=37
HVFEENLIGLIGRGG
> T=0.1, sample=1, score=0.3561, global_score=0.3561, seq_recovery=0.9333
HVFEENLIGLIGFGG
>T=0.1, sample=2, score=0.3412, global_score=0.3412, seq_recovery=0.8667
YVFEENLIGLIGFGG
>T=0.1, sample=3, score=0.3966, global_score=0.3966, seq_recovery=0.8667
HVFEEELIGLIGFGG
>T=0.1, sample=4, score=0.3463, global_score=0.3463, seq_recovery=0.8667
YVFEENLIGLIGFGG
>T=0.1, sample=5, score=0.3783, global_score=0.3783, seq_recovery=0.8000
YVFVENLIGLIGFGG
>T=0.1, sample=6, score=0.3573, global_score=0.3573, seq_recovery=0.8667
HVFWENLIGLIGFGG
>T=0.1, sample=7, score=0.3822, global_score=0.3822, seq_recovery=0.8667
HVFEEELIGLIGFGG
>T=0.1, sample=8, score=0.3223, global_score=0.3223, seq_recovery=0.9333
HVFEENLIGLIGFGG
 ```
* T: Sample temperature. Here, we use 0.1 as the default.
* score: Average of the negative log probabilities of all designed residues.
* global_score: Average of the negative log probabilities of both masked and designed residues.
* designed_chains: Chain ID of the input pdb file.
   > Because epitope or neoantigen have only one chain, which is the designed chain, the 'fixed_chains' is empty.
* seq_recovery: Sequence recovery measures the percentage of amino acids in the designed sequence that match the amino acids in the native sequence for a given protein backbone structure.
   > It measures how well the designed sequence matches the input sequence for a given protein structure.
* seed: random seed.
   > Different random seeds will cause 0.01-0.02 variation in the output score and global_score for the same output sequence but will not impact the seq_recovery.

## Training Data Preparation:
1. Collect epitope sequences and save them as multiple FASTA files. One epitope sequence is in one FASTA, like './dataset/Modeller/fasta/86269.fasta'.
2. Modeling 3D structures of epitope sequences using MODELLER:
   + Download [MODELLER](https://salilab.org/modeller/download_installation.html) and register for a license.(MODELLER is available free of charge to academic non-profit institutions) \
     Open cmd or MODELLER.exe and go to the _Modeller_ folder.
     ```
     cd ./dataset/Modeller
     ```
     Unzip templates that will be used in MODELLER.
     ```
     tar zxf ./templates.tar.gz .
     ```
   + Two approaches to modeling epitopes' 3D structures: 
     
   **Approach one:** Structure modeling only without calculating sequence similarity.
      - Run Fast2Pir.sh to generate .ali files for all FASTA files. The output .ali files will be stored in the _ali_ folder.
      ```
      ./FAST2Pir.sh
      ```

      - Run Buildmodel2.py to start modeling. Then, you will get the Modeled .pdb files in the current folder with temporary files.
      ```
      python Buildmodel2.py
      ```
   **Approach two:** Calculating sequence similarity and structure modeling.
      - Run CalculateSimilarityAndSave.py and get output1.txt that contains the epitopes name, best template, and the sequence similarity. The best template here means the template has the highest sequence similarity with the epitope sequence.
        ```
        python CalculateSimilarityAndSave.py
        ```
      - Run Data-clean.ipynb in <ins>Jupyterlab </ins> or <ins>Jupyter notebook </ins> to get haha.txt. The final output will be .ali files in _ali1_ folder and combined_output1.txt which contains epitopes' name, epitopes' sequence, best template, and sequence similarity.
      - Run Build-model3.py to construct the 3D structures of epitopes using their best template. The output pdb files will be stored in _output_pdb_ folder. All temporary files will be automatically deleted, as shown in the script.
3. Convert pdb files to mmcif files.
   + Download [MAXIT Suite](https://sw-tools.rcsb.org/apps/MAXIT/index.html) to your Linux/Unix environment or WSL. Then, follow the README file inside maxit folder to install MAXIT.
   + Go to _script_ folder and run multiple_mmcif.sh to convert multiple pdb files to mmcif files. The output cif files will be stored in _../mmcif_ folder.
      ```
      cd ..
      cd scripts
      ./multiple_mmcif.sh
      ```
4. Convert mmcif files to pt files. The output pt files will be stored in _../pt_ folder.
   ```
   ./multiple_convert_cif_to_pt.sh
   ```
5. Generate the _training_data_ folder
   * Run _./dataset/scripts/Generate_list_csv.ipynb_ to create csv file using combined_output.txt and epitope list exported from [IEDB](https://www.iedb.org/).
   * Run _./dataset/scripts/Split.ipynb_ to create cluster.txt and split the dataset. Here, one cluster contains one epitope.
   ```
   > training data
      > list_142934.csv
      > test.txt
      > validation.txt
      > pdb
         > pt
            > xxx.pt
            > xxx_A.pt
            ...
   ```
## Model evaluation:
1. Run Test_multiple_pdbs_seq_rec.ipynb in _testing_ folder and use the pdb folder _sample_data_ to test model performance. (You can change it to your own test set.)
2. Each epitope will generate four redesigned epitope sequences and four sequence recoveries.
3. Average sequence recovery will be calculated and plotted, as shown in _example_output_ folder.
## Available sources:
* The dataset (pt files) used in EpiMII paper can be downloaded from []. If you want to retrain the model, please put all pt files in this directory _./training/training_data/pdb/pt_.
* The MODELLER-modeled 3D structures of 142934 MHC-II epitopes (pdb files) used in EpiMII paper can be downloaded from [].
* All model weights can be downloaded from []. In the EpiMII paper, 'epoch50_step47050.pt' is used as the final model weight '128_earlystop.pt'.
* 133 3D structures obtained by X-ray crystallography of MHC-II epitopes collected from PDB can be found in the directory _./dataset/3D_crystalized_all.tar.gz_.
* Original csv file that contains around 480,000 MHC-II epitopes' sequences collected from IEDB can be found in the directory _./dataset/list_no_cluster.zip_.
   
