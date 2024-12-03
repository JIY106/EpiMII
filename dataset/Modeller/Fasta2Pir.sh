#!/bin/bash

# Create the "ali" folder if it doesn't exist
mkdir -p ali

# Loop through all .fasta files in the "fasta" folder
for fasta_file in fasta/*.fasta; do
    name=$(basename "$fasta_file" .fasta)
    cp "$fasta_file" "${name}.sequence" # Copy your fasta to a new file
    sed -i '1d' "${name}.sequence" # Remove the top line and rewrite
    grep pattern "${name}.sequence" | tr '\n' ' ' # Consolidate multiple lines into one
    touch temp_pir.ali # Make a temp file
    cat << EOF >> temp_pir.ali # This copies the following to tempfile
>P1;$name
sequence:$name:::::::0.00: 0.00
EOF
    cat "${name}.sequence" >> temp_pir.ali # Append the protein sequence to this file
    mv temp_pir.ali "ali/${name}.ali" # Save the .ali file in the "fasta" folder

    # Add an asterisk to the end of the last line in the .ali file
    sed -i '${s/$/*/}' "ali/${name}.ali"

    rm "${name}.sequence" # Delete the temp file containing the seq
done

