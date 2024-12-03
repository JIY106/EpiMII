#!/bin/bash

# Input and output folder paths
input_folder="../mmcif"
output_folder="../pt"

# Make sure output folder exists, if not, create it
mkdir -p "$output_folder"

# Path to the parse_cif_noX.py script
parse_script_path="parse_cif_noX_change_cifinput.py"

# Iterate through .cif.gz files in the input folder
for filepath in "$input_folder"/*.cif; do
    filename=$(basename "$filepath")
    output_filename="${filename%.cif}"
    output_filepath="$output_folder/$output_filename"
    
    # Run the script
    python "$parse_script_path" "$filepath" "$output_filepath"
    
    if [ $? -eq 0 ]; then
        echo "Processed $filename successfully."
    else
        echo "Error processing $filename."
    fi
done

echo "All files processed."
