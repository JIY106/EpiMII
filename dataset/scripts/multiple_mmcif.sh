#!/bin/bash

input_folder="../Modeller/output_pdb"
output_folder="../mmcif"
log_file="../mmcif/logfile.log"

mkdir -p "$output_folder"

for input_file in "$input_folder"/*.pdb; do
    base_name=$(basename "$input_file")
    output_file="$output_folder/${base_name%.pdb}.cif"
    
    maxit -input "$input_file" -output "$output_file" -o 1 -log "$log_file"
    echo Finish "$output_folder/${base_name%.pdb}.cif"
done
