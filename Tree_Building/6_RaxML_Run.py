import os
import re
import subprocess

input_folder = "/Users/victor_torres/Documents/MR_Bayes/ready_mafft"
output_folder = "/Users/victor_torres/Documents/MR_Bayes/rax-ml_results"
iqtree_results_folder = "/Users/victor_torres/Documents/MR_Bayes/bestmodel_results"

os.makedirs(output_folder, exist_ok=True)

model_mapping = {
    # JC models
    "JC": "GTR",
    "JC+I": "GTR+I",
    "JC+G": "GTR+G",
    "JC+I+G": "GTR+I+G",
    "JC+F": "GTR",
    "JC+I+F": "GTR+I",
    "JC+G+F": "GTR+G",
    "JC+I+G+F": "GTR+I+G",

    "K80": "HKY",
    "K80+I": "HKY+I",
    "K80+G": "HKY+G",
    "K80+I+G": "HKY+I+G",
    "K80+F": "HKY",
    "K80+I+F": "HKY+I",
    "K80+G+F": "HKY+G",
    "K80+I+G+F": "HKY+I+G",

    "HKY": "HKY",
    "HKY+I": "HKY+I",
    "HKY+G": "HKY+G",
    "HKY+I+G": "HKY+I+G",
    "HKY+F": "HKY",
    "HKY+I+F": "HKY+I",
    "HKY+G+F": "HKY+G",
    "HKY+I+G+F": "HKY+I+G",

    "TN93": "TN93",
    "TNe": "TN93",
    "TN93+I": "TN93+I",
    "TNe+I": "TN93+I",
    "TN93+G": "TN93+G",
    "TNe+G": "TN93+G",
    "TN93+I+G": "TN93+I+G",
    "TNe+I+G": "TN93+I+G",
    "TN93+F": "TN93",
    "TNe+F": "TN93",
    "TN93+I+F": "TN93+I",
    "TNe+I+F": "TN93+I",
    "TN93+G+F": "TN93+G",
    "TNe+G+F": "TN93+G",
    "TN93+I+G+F": "TN93+I+G",
    "TNe+I+G+F": "TN93+I+G",

    "GTR": "GTR",
    "GTR+I": "GTR+I",
    "GTR+G": "GTR+G",
    "GTR+I+G": "GTR+I+G",
    "GTR+F": "GTR",
    "GTR+I+F": "GTR+I",
    "GTR+G+F": "GTR+G",
    "GTR+I+G+F": "GTR+I+G",

    "TIM": "GTR",
    "TIM+I": "GTR+I",
    "TIM+G": "GTR+G",
    "TIM+I+G": "GTR+I+G",
    "TIM+F": "GTR",
    "TIM+I+F": "GTR+I",
    "TIM+G+F": "GTR+G",
    "TIM+I+G+F": "GTR+I+G",

    "TVM": "GTR",
    "TVM+I": "GTR+I",
    "TVM+G": "GTR+G",
    "TVM+I+G": "GTR+I+G",
    "TVM+F": "GTR",
    "TVM+I+F": "GTR+I",
    "TVM+G+F": "GTR+G",
    "TVM+I+G+F": "GTR+I+G",

    "SYM": "GTR",
    "SYM+I": "GTR+I",
    "SYM+G": "GTR+G",
    "SYM+I+G": "GTR+I+G",
    "SYM+F": "GTR",
    "SYM+I+F": "GTR+I",
    "SYM+G+F": "GTR+G",
    "SYM+I+G+F": "GTR+I+G",

    "F81": "GTR",
    "F81+I": "GTR+I",
    "F81+G": "GTR+G",
    "F81+I+G": "GTR+I+G",
    "F81+F": "GTR",
    "F81+I+F": "GTR+I",
    "F81+G+F": "GTR+G",
    "F81+I+G+F": "GTR+I+G"
}

invalid_chars = r"[ ;:,()']"

for filename in os.listdir(input_folder):
    if filename.endswith(".fasta"):
        fasta_path = os.path.join(input_folder, filename)
        temp_path = fasta_path + "_temp"

        base_name = os.path.splitext(filename)[0]
        result_dir = os.path.join(output_folder, base_name)
        os.makedirs(result_dir, exist_ok=True)

        print(f"Cleaning FASTA headers: {filename}")

        with open(fasta_path, "r") as infile, open(temp_path, "w") as outfile:
            for line in infile:
                if line.startswith(">"):
                    cleaned_header = re.sub(invalid_chars, "", line.strip())
                    cleaned_header = cleaned_header.replace(" ", "_")
                    outfile.write(cleaned_header + "\n")
                else:
                    outfile.write(line)

        os.replace(temp_path, fasta_path)

        print(f"Cleaned and overwritten: {fasta_path}")

        iqtree_file = os.path.join(iqtree_results_folder, f"{base_name}.iqtree")
        model = "GTR+G"

        if os.path.exists(iqtree_file):
            with open(iqtree_file, "r") as iqtree:
                for line in iqtree:
                    if "Best-fit model according to BIC" in line:
                        model = line.split(":")[1].strip()
                        raxml_model = model_mapping.get(model, "GTR+I")
                        print(f"Model found for {filename}: {raxml_model}")
                        break
        else:
            print(f"No model found for {filename}. Using default ({raxml_model}).")

        raxml_command = [
            "/opt/homebrew/bin/raxml-ng",
            "--all",
            "--msa", fasta_path,
            "--model", raxml_model,
            "--tree", "pars{10},rand{10}",
            "--bs-trees", "100",
            "--prefix", os.path.join(result_dir, base_name)
        ]

        print(f"Running RAxML-NG for: {filename}")
        subprocess.run(raxml_command)

        print(f"Completed: {filename}. Results stored in {result_dir}.")

print("All RAxML-NG analyses are finished.")
