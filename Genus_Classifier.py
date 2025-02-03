import os
import pandas as pd
import regex as re

MasterSequence = pd.read_csv("/Users/victor_torres/Downloads/ModifiedCodesMasterSequence.csv", )

MasterSequence['Gene'] = MasterSequence['Gene'].str.strip()

main_folder = "Gene_n_Genus_Classification"
os.makedirs(main_folder, exist_ok=True)

for gene in MasterSequence["Gene"].dropna().unique():
    gene_folder = os.path.join(main_folder, gene)
    os.makedirs(gene_folder, exist_ok=True)

    genera = MasterSequence[MasterSequence["Gene"] == gene]["Genus"].dropna().unique()
    for genus in genera:
        genus_folder = os.path.join(gene_folder, genus)
        os.makedirs(genus_folder, exist_ok=True)

        file_path = os.path.join(genus_folder, f"{genus}.txt")
        with open(file_path, "w") as new_fasta_file:
            for _, row in MasterSequence[(MasterSequence["Genus"] == genus) & (MasterSequence['Gene'] == gene)].iterrows():
                header = f">{row['Genus']}_{row['Species']}_{row['Gene']}_{row['Location']}_{row['Code5']}\n"
                sequence = f"{row['Sequence']}\n"
                new_fasta_file.write(header + sequence)

print(f"Folders were created in {main_folder}")