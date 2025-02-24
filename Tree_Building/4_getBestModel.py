import os
import subprocess

input_folder = "/Users/victor_torres/Documents/MR_Bayes/mafft_nex"
output_folder = "/Users/victor_torres/Documents/MR_Bayes/bestmodel_results"

os.makedirs(output_folder, exist_ok=True)

iq_tree = "/Users/victor_torres/Downloads/iqtree-2.0.7-MacOSX/bin/iqtree2"

for filename in os.listdir(input_folder):
    if filename.endswith(".nex"):
        file_path = os.path.join(input_folder, filename)

        base_name = os.path.splitext(filename)[0]
        output_prefix = os.path.join(output_folder, base_name)

        iqtree_command = [
            iq_tree,
            "-s", file_path,
            "-m", "MFP",
            "-pre", output_prefix
        ]

        print(f"Running IQ-TREE for: {filename}")

        try:
            subprocess.run(iqtree_command, check=True)
            print(f"Completed: {filename}, results in {output_folder}")
        except subprocess.CalledProcessError as e:
            print(f"Error running IQ-TREE for {filename}: {e}")

print("All IQ-TREE analyses are completed.")
