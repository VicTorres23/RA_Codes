import os
import subprocess
import shlex

input_folder = "/Users/victor_torres/Documents/MR_Bayes/ready"
output_folder = "/Users/victor_torres/Documents/MR_Bayes/ready_mafft"

os.makedirs(output_folder, exist_ok=True)

mafft_path = "/opt/homebrew/bin/mafft"

for filename in os.listdir(input_folder):
    if filename.endswith(".fasta") or filename.endswith(".fa") or filename.endswith(".txt"):
        input_file = os.path.join(input_folder, filename)
        output_file = os.path.join(output_folder, filename.replace(".fasta", "_aligned.fasta").replace(".fa", "_aligned.fa"))

        safe_input = shlex.quote(input_file)
        safe_output = shlex.quote(output_file)

        mafft_command = f"{mafft_path} --auto {safe_input} > {safe_output}"
        subprocess.run(mafft_command, shell=True, check=True)

        print(f"Aligned: {filename}: Saved to {output_folder}")

print("All FASTA files have been aligned and saved successfully.")
