from modeller import *
from modeller.automodel import *
import os
import time
import shutil

# Define function to classify amino acids into specific categories
def classify_amino_acids_detailed(sequence):
    neutral_nonpolar = "AGFPILVM"
    negative_charge_acidic_polar = "DE"
    positive_charge_basic_polar = "HKR"
    neutral_polar = "CQNSTYW"

    categories = {
        'neutral_nonpolar': neutral_nonpolar,
        'negative_charge_acidic_polar': negative_charge_acidic_polar,
        'positive_charge_basic_polar': positive_charge_basic_polar,
        'neutral_polar': neutral_polar
    }

    classified_sequence = []

    for residue in sequence:
        # Classify the residue into one of the categories
        classified = None
        if residue == '-':
            classified = 'gap'
        else:
            for category, amino_acids in categories.items():
                if residue in amino_acids:
                    classified = category
                    break
        classified_sequence.append((residue, classified))

    return classified_sequence

# Define function to calculate sequence identity
def sequence_identity(seq1, seq2):
    # Check that the sequences are of the same length
    if len(seq1) != len(seq2):
        raise ValueError("Sequences must be of the same length for identity comparison")

    identical_count = 0

    # Iterate through the sequences and count identical residues
    for (residue1, category1), (residue2, category2) in zip(classify_amino_acids_detailed(seq1), classify_amino_acids_detailed(seq2)):
        if residue1 == residue2 and (residue1 !='-' and residue2 !='-') and category1 == category2:
            identical_count += 1
        elif residue1 != residue2 and (residue1 !='-' and residue2 !='-') and category1 == category2:
            identical_count += 0.5
        elif residue1 == '-' and residue2 == '-':
            identical_count += 0
        elif residue1 == '-' or residue2 == '-':
            identical_count -= 0

    # Calculate and return the sequence identity as a percentage
    return (identical_count / len(seq1)) * 100

start_time = time.time()

# Create a Modeller environment
env = Environ()

log_filename = 'modeling.log'

new_folder = 'combined_output1'

# Read the template structures into the alignment
templates = [
    ('1aqd', '1aqd.pdb'),
    ('1bx2', '1bx2.pdb'),
    ('1fv1', '1fv1.pdb'),
    ('1h15', '1h15.pdb'),
    ('1hxy', '1hxy.pdb'),
    ('1jk8', '1jk8.pdb'),
    ('1klg', '1klg.pdb'),
    ('1s9v', '1s9v.pdb'),
    ('1sje', '1sje.pdb'),
    ('1t5w', '1t5w.pdb'),
    ('1uvq', '1uvq.pdb'),
    ('2nna', '2nna.pdb'),
    ('2q6w', '2q6w.pdb'),
    ('2seb', '2seb.pdb'),
    ('3c5j', '3c5j.pdb'),
    ('3wex', '3wex.pdb'),
    ('4fqx', '4fqx.pdb'),
    ('4h1l', '4h1l.pdb'),
    ('4h25', '4h25.pdb'),
    ('4i5b', '4i5b.pdb'),
    ('4is6', '4is6.pdb'),
    ('4may', '4may.pdb'),
    ('4mdj', '4mdj.pdb'),
    ('4ov5', '4ov5.pdb'),
    ('4ozh', '4ozh.pdb'),
    ('4ozi', '4ozi.pdb'),
    ('4p5k', '4p5k.pdb'),
    ('4p5m', '4p5m.pdb'),
    ('4p57', '4p57.pdb'),
    ('4y1a', '4y1a.pdb'),
    ('4z7u', '4z7u.pdb'),
    ('5lax', '5lax.pdb'),
    ('5ni9', '5ni9.pdb'),
    ('5v4m', '5v4m.pdb'),
    ('5v4n', '5v4n.pdb'),
    ('6atf', '6atf.pdb'),
    ('6biy', '6biy.pdb'),
    ('6cpl', '6cpl.pdb'),
    ('6dfx', '6dfx.pdb'),
    ('6dig', '6dig.pdb'),
    ('6hby', '6hby.pdb'),
    ('6mff', '6mff.pdb'),
    ('6nix', '6nix.pdb'),
    ('6py2', '6py2.pdb'),
    ('6u3m', '6u3m.pdb'),
    ('6u3o', '6u3o.pdb'),
    ('6xcp', '6xcp.pdb'),
    ('6xp6', '6xp6.pdb'),
    ('7kei', '7kei.pdb'),
    ('7n19', '7n19.pdb')
]

# Specify the path to the "target" folder
target_folder = 'ali'

# Open a file to save the output
output_file_path = 'output1.txt'
# Loop through target sequences and calculate similarity

# Loop through target sequences
for filename in os.listdir(target_folder):
    if filename.endswith('.ali'):
        align_code = os.path.splitext(filename)[0]  # Remove the .ali extension

        # Create a new Modeller environment and alignment object for each target sequence
        env = Environ()
        aln = Alignment(env)

        # Add the template structures to the alignment
        for code, atom_files in templates:
            mdl = Model(env, file=atom_files)
            aln.append_model(mdl, align_codes=code)

        # Add the current target sequence
        aln.append(file=os.path.join(target_folder, filename), align_codes=align_code)

        # Perform a multiple sequence alignment
        aln.malign()

        # Write the resulting alignment to a file
        alignment_file = f'{align_code}.ali'
        aln.write(file=alignment_file, alignment_format='PIR')

        # Initialize variables to store alignment data
        alignment_data = []

        # Initialize the target sequence
        target_sequence = ""

        # Read the alignment file
        alignment_file = f'{align_code}.ali'

        # Initialize flags to control data extraction
        current_code = None
        current_sequence = ""
        extract_target_sequence = False  # Flag to determine if the current line contains the target sequence

        # Read the alignment file line by line
        with open(alignment_file, 'r') as file:
            lines = file.readlines()

        # Loop through the lines and extract relevant information
        index = 0  # Initialize the index
        while index < len(lines):
            line = lines[index].strip()

            if line.startswith('>P1;'):
                if current_code is not None:
                    alignment_data.append((current_code, current_sequence))
                current_code = line.split(';')[1]
                current_sequence = ""
            elif line.startswith('structureX:') and "-1.00:-1.00" in line:
                # Check if this is the line containing the target sequence
                # Find the line with the sequence
                index += 1  # Move to the next line
                sequence_line = lines[index].strip('*')
                current_sequence = sequence_line

            # Check if this line contains the target sequence
            elif line.startswith('sequence:') and "0.00: 0.00" in line:
                if "0.00: 0.00" in line:
                    extract_target_sequence = True
                else:
                    extract_target_sequence = False
                # Extract the target sequence
                index += 1  # Move to the next line
                target_sequence_line = lines[index].strip('*')
                target_sequence = target_sequence_line.rstrip('*')

            index += 1  # Move to the next line

        # Save the extracted data to a file
        output_filename = f'{align_code}_extracted_data.txt'
        with open(output_filename, 'w') as output_file:
            for code, sequence in alignment_data:
                output_file.write(f'{code}\n{sequence}\n')

        # Initialize variables to store the extracted data
        alignment_data = []
        current_code = None
        current_sequence = ""

        # Read the extracted data from the file
        with open(output_filename, 'r') as file:
            lines = file.readlines()

        # Loop through the lines and extract relevant information
        for line in lines:
            line = line.strip()
            if line:  # Check if the line is not empty
                if current_code is None:
                    current_code = line
                else:
                    current_sequence = line.rstrip('*')
                    alignment_data.append((current_code, current_sequence))
                    current_code = None

        # Assuming alignment_data contains the extracted sequences and TvLDH.ali contains the target sequence
        # Example comparison with the first sequence in alignment_data
        target_seq = target_sequence.rstrip('* \n')  # Replace with the actual target sequence

        # Initialize best_similarity to a lower value than 0
        best_similarity = -100.0

        # Initialize best_template to None
        best_template = None

        for code, sequence in alignment_data:
            identity = sequence_identity(target_seq, sequence)

            # Check if the current template has a higher similarity
            if identity >= best_similarity:
                best_similarity = identity
                best_template = code

            # Prepare output text
        output_text = f'{align_code}\n'
        output_text += f'Best Template: {best_template}\nBest Similarity: {best_similarity:.2f}%\n'

        #output_file_path = f'{align_code}_output.txt'
        with open(output_file_path, 'a') as output_file:
            # Write the output text to the file
            output_file.write(output_text)

        # Print the output to the console
        #print(output_text)

       # Move the alignment file to the new folder
        shutil.move(alignment_file, os.path.join(new_folder, alignment_file))

        # Move the extracted data file to the new folder
        shutil.move(output_filename, os.path.join(new_folder, output_filename))

# Print elapsed time
print(f"Elapsed time: {time.time() - start_time} seconds")
