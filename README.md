# EpiMII: An Advanced GNN Model for Re/Co-designing MHC-II Epitopes and Neoantigens 
## Overview:

## Quick guide
## Training Data Preparation:
1. Collect epitope sequences and save them as multiple FASTA files. One epitope sequence is in one FASTA, like './dataset/Modeller/fasta/86269.fasta'.
2. Modeling 3D structures of epitope sequences using MODELLER:
   1) Download MODELLER from https://salilab.org/modeller/download_installation.html and register for a license.
      Open cmd or MODELLER.exe.
      cd './dataset/Modeller'
      Unzip templates that will be used in MODELLER.
      tar zxf ./templates.tar.gz .
   3) Two approaches to modeling epitopes' 3D structures:
      1> Run Fast2Pir.sh to generate .ali files for all FASTA files. The output .ali files will be stored in the .ali folder.
      ./FAST2Pir.sh
          Run Buildmodel2.py to start modeling. Then, you will obtain the Modelled .pdb files in the current folder with temporary files.
      python Buildmodel2.py
      2> 
