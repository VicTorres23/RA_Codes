import os
import subprocess

seqmagick_path = "/Users/victor_torres/seqmagick_env/bin/seqmagick"
input_folder = "/Users/victor_torres/Documents/MR_Bayes/ready_mafft"
output_folder = "/Users/victor_torres/Documents/MR_Bayes/mafft_nex"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        old_path = os.path.join(input_folder, filename)
        new_path = os.path.join(input_folder, filename.replace(".txt", ".fasta"))
        os.rename(old_path, new_path)
        print(f"Renamed: {filename}: {new_path}")

for filename in os.listdir(input_folder):
    if filename.endswith(".fasta") or filename.endswith(".fa"):
        input_file = os.path.join(input_folder, filename)
        output_file = os.path.join(output_folder, filename.replace(".fasta", ".nex").replace(".fa", ".nex"))

        seqmagick_command = f"{seqmagick_path} convert --alphabet dna {input_file} {output_file}"
        subprocess.run(seqmagick_command, shell=True, check=True)

        print(f"Converted: {filename}: {output_file}")

print("All FASTA files have been converted to PHYLIP successfully.")
