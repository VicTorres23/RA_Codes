import regex as re
import pandas as pd

fasta_COI = open("C:/Users/vemma/Documents/Master in Bioinformatics/Spring_2025_Semester/RA/EchiCS manuscript/Epi_COI_united.fasta", "r")
fasta_ITS = open("C:/Users/vemma/Documents/Master in Bioinformatics/Spring_2025_Semester/RA/EchiCS manuscript/Epiph_ITS_united.fasta", "r")
MasterSequence = pd.read_excel("C:/Users/vemma/Documents/Master in Bioinformatics/Spring_2025_Semester/RA/MasterSequence_Database (06.15.24) (3).xlsx", sheet_name="To be added")

str_fasta_COI = str(fasta_COI.read())
str_fasta_ITS = str(fasta_ITS.read())
titles_COI = re.findall(r"\>([A-Z0-9\_a-z]+)\s", str_fasta_COI)
titles_ITS = re.findall(r"\>([A-Z0-9\_a-z]+)\s", str_fasta_ITS)
str_fasta_COI = re.sub(r"\>[A-Z0-9\_a-z]+\s", " ", str_fasta_COI)
str_fasta_ITS = re.sub(r"\>[A-Z0-9\_a-z]+\s", " ", str_fasta_ITS)
sequences_COI = str_fasta_COI.split(" ")
sequences_ITS = str_fasta_ITS.split(" ")
sequences_COI.remove(sequences_COI[0])
sequences_ITS.remove(sequences_ITS[0])

print(len(titles_ITS))
print(len(sequences_ITS))

Abbreviations = {"HT_": "Hueco Tanks", "HTNT":"Hueco Tanks North Temp", "RBC1": "Rio Bosque Channel 1", "RBC2": "Rio Bosque Channel 2", "STR": "STR(Ask)", "IMRS": "Indio Mountain Research Station", "BRH": "Behind Ranch House", "HLit": "Lake Littra(Ask)", "AmDam": "American Dam", "DQ":"DQ(Ask)", "JF": "JF(Ask)", "Rat": "Ratlesnake Tank", "FL": "FL(Ask)", "LW6": "LW(Ask)", "LW19": "LW(Ask)"}

locations_COI = []
for i in range(len(titles_COI)):
    for keys in Abbreviations.keys():
        if keys in titles_COI[i]:
            locations_COI.append(Abbreviations[keys])

locations_ITS = []
for i in range(len(titles_ITS)):
    for keys in Abbreviations.keys():
        if keys in titles_ITS[i]:
            locations_ITS.append(Abbreviations[keys])

print(len(locations_ITS))

for i in range(len(titles_COI)):
    MasterSequence.loc[len(MasterSequence)] = {"Genus": "Epiphanis", "Species": "Chihuahuensis", "Lab": "Walsh",
                                               "Gene": "COI", "Sequence": sequences_COI[i], "Location": locations_COI[i], "Seq Len": len(sequences_COI[i]), "Sequence": sequences_COI[i], "Code5": titles_COI[i]}

for i in range(len(titles_ITS)):
    MasterSequence.loc[len(MasterSequence)] = {"Genus": "Epiphanis", "Species": "Chihuahuensis", "Lab": "Walsh",
                                               "Gene": "ITS", "Sequence": sequences_ITS[i], "Location": locations_ITS[i], "Seq Len": len(sequences_ITS[i]), "Sequence": sequences_ITS[i], "Code5": titles_ITS[i]}
MasterSequence.to_csv("MasterSequenceWithAaronsSequences.csv", index=False)