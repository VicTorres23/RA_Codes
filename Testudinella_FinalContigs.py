import regex as re
import pandas as pd

MasterSequence = pd.read_excel("C:/Users/vemma/Documents/Master in Bioinformatics/Spring_2025_Semester/MasterSequence_Database for Gnesiophylogeny 01.07.25.xlsx")
genbank_sequences = MasterSequence[MasterSequence["Lab"] == "Genbank"].reset_index(drop=True)

with open("C:/Users/vemma/Documents/Master in Bioinformatics/Spring_2025_Semester/Testudinella_Clypeata.txt", "r") as file:
    file_content = file.read()

accessionIDs = re.findall(r"Accession\:\n\s+([A-Z][A-Z]\d+\.\d)", file_content)

GenesOfInterest = {"18S": "18S", "ITS": "ITS", "cytochrome": "COI"}

for accession_id in accessionIDs:
    if any(accession_id in seq for seq in genbank_sequences["SeqName"]):
        print(f"Already in Excel: {accession_id}")
    else:
        print(f"Adding to Excel: {accession_id}")

        FASTA_URL = f"https://www.ncbi.nlm.nih.gov/nuccore/{accession_id}?report=fasta"

        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        driver = webdriver.Chrome()
        driver.get(FASTA_URL)
        try:
            fasta_content = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "pre"))
            ).text
            fasta_header = re.search(r"^>(.+)", fasta_content, re.MULTILINE).group(1)  # Extract FASTA title
            fasta_sequence = re.sub(r"(\>.+\n)", "", fasta_content).replace("\n", "")
            print(f"Retrieved sequence: {fasta_sequence}")

            gene_type = None
            for keyword, gene_name in GenesOfInterest.items():
                if keyword.lower() in fasta_header.lower():
                    gene_type = gene_name
                    break

            if not gene_type:
                print(f"Warning: No matching gene type found for {accession_id}. Defaulting to 'Unknown'.")
                gene_type = "Unknown"

            MasterSequence = MasterSequence.append({
                "Genus": "Testudinella",
                "Species": "clypeata",
                "Lab": "Genbank",
                "Gene": gene_type,
                "SeqName": f"| gb | {accession_id} | Testudinella clypeata",
                "Coordinates A": "GB",
                "Coordinates B": "GB",
                "Sequence": fasta_sequence,
                "Seq Len": len(fasta_sequence)
            }, ignore_index=True)

        except Exception as e:
            print(f"Error retrieving FASTA for {accession_id}: {e}")
        finally:
            driver.quit()

MasterSequence.to_csv("Updated_MasterSequence.csv", index=False)