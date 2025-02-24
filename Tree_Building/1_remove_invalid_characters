import os
import re

input_folder = "/Users/victor_torres/Documents/Master_in_Bioinformatics/Spring_2025/RA_Tasks/18S/For_Removing_Spaces_And_Numbers"
output_folder = "/Users/victor_torres/Documents/MR_Bayes/ready"

os.makedirs(output_folder, exist_ok=True)

def clean_fasta_headers(input_path, output_path):
    with open(input_path, "r") as infile, open(output_path, "w") as outfile:
        for line in infile:
            if line.startswith(">"):
                new_header = re.sub(r"^>\d+", ">", line)
                new_header = re.sub(r" ", "_", new_header)
                new_header = re.sub(r"\,", "", new_header)
                new_header = re.sub(r"\;", "", new_header)
                new_header = re.sub(r"'", "", new_header)
                new_header = re.sub(r"[\(\)]", "", new_header)
                new_header = re.sub(r"[^\x00-\x7F]+", "", new_header)
                outfile.write(new_header)
            else:
                line = re.sub(r"[Nn]", "?", line)
                new_header = re.sub(r"[^\x00-\x7F]+", "", line)
                outfile.write(line)

for filename in os.listdir(input_folder):
    if filename.endswith(".fasta") or filename.endswith(".fa") or filename.endswith(".txt"):
        input_file = os.path.join(input_folder, filename)
        output_file = os.path.join(output_folder, filename)

        clean_fasta_headers(input_file, output_file)
        print(f"Processed: {filename}: Saved to {output_folder}")

print("FASTA headers cleaned and saved successfully.")
