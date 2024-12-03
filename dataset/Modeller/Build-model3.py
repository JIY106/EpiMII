from modeller import *
from modeller.automodel import *
import os
import time

import shutil

start_time = time.time()

# Create a Modeller environment
env = Environ()

#log_filename = 'modeling.log'


# Specify the path to the "target" folder
target_folder = 'ali1' 

combined_output_file = 'combined_output1.txt'

new_folder = 'tmp'

output_folder = 'output_pdb'

os.makedirs(new_folder, exist_ok = True)
os.makedirs(output_folder, exist_ok = True)

# Loop through target sequences
for filename in os.listdir(target_folder):
    if filename.endswith('.ali'):
        align_code = os.path.splitext(filename)[0]  # Remove the .ali extension

        # Create a new Modeller environment and alignment object for each target sequence
        #env = Environ()
        #aln = Alignment(env)

        # Add the template structures to the alignment
        with open(combined_output_file, 'r') as combined_output:
            for line in combined_output:
                parts = line.strip().split(',')
                if parts[0] == align_code:
                    template_pdb_code = parts[1]
                    sequence = parts[2]
                    # Do something with the template PDB code and sequence
                    print(f"Align Code: {align_code}, Template PDB Code: {template_pdb_code}, Sequence: {sequence}")

                    # Now you can use the template PDB code to construct the path to the corresponding PDB file
                    atom_files = f"{template_pdb_code}.pdb"

                    # Create a new Modeller environment and alignment object for each target sequence
                    env = Environ()
                    aln = Alignment(env)

                    # Add the template structures to the alignment
                    mdl = Model(env, file=atom_files)
                    aln.append_model(mdl, align_codes=template_pdb_code)
        
        # Add the current target sequence
        aln.append(file=os.path.join(target_folder, filename), align_codes=align_code)

       # Perform a multiple sequence alignment
        aln.malign()

        # Write the resulting alignment to a file
        alignment_file = f'{align_code}.ali'
        aln.write(file=alignment_file, alignment_format='PIR')

        # Now, build the comparative model in the output folder
        a = AutoModel(env, alnfile=alignment_file, knowns=f"{template_pdb_code}", sequence=align_code, assess_methods=assess.GA341) #, 
        a.very_fast()
        a.starting_model = 1
        a.ending_model = 1
        a.final_malign3d = True

        # Specify the output file for the model
        output_model_file = f'{align_code}.pdb'

        # Build the model
        a.make()

        # Rename the model file to the desired output path
        os.rename(f'{align_code}.B99990001.pdb', output_model_file)

       # Move the alignment file to the new folder
        shutil.move(f'{align_code}.B99990001_fit.pdb', os.path.join(new_folder, f'{align_code}.B99990001_fit.pdb'))
       # Move the alignment file to the new folder
        shutil.move(f'{align_code}.D00000001', os.path.join(new_folder, f'{align_code}.D00000001'))
       # Move the alignment file to the new folder
        shutil.move(f'{align_code}.rsr', os.path.join(new_folder, f'{align_code}.rsr'))
       # Move the alignment file to the new folder
        shutil.move(f'{align_code}.ini', os.path.join(new_folder, f'{align_code}.ini'))
       # Move the alignment file to the new folder
        shutil.move(f'{align_code}.sch', os.path.join(new_folder, f'{align_code}.sch'))
       # Move the alignment file to the new folder
        shutil.move(f'{align_code}.V99990001', os.path.join(new_folder, f'{align_code}.V99990001'))
       # Move the alignment file to the new folder
        shutil.move(alignment_file, os.path.join(new_folder, alignment_file))
       # Move the alignment file to the new folder
        shutil.move( f"{template_pdb_code}_fit.pdb", os.path.join(new_folder, f"{template_pdb_code}_fit.pdb"))
 
	# Move the renamed .pdb file to the new folder
        shutil.move(output_model_file, os.path.join(output_folder, output_model_file))

end_time = time.time()
elapsed_time = end_time - start_time
# Print the elapsed time
print(f"Elapsed time: {elapsed_time} seconds")

