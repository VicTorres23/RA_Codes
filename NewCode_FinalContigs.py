import regex as re
import pandas as pd

MasterSequence = pd.read_excel("C:/Users/vemma/Documents/Master in Bioinformatics/Spring_2025_Semester/RA/MasterSequence_Database (06.15.24) (2).xlsx")
counter = 0
for i in range(len(MasterSequence["#"])):
    MasterSequence["#"][i] = counter
    MasterSequence["Num"][i] = "A" + str(counter)
    counter = counter + 1
    if str(MasterSequence["Lab"][i]) == "Walsh":
        MasterSequence["Code5"][i] = str(MasterSequence["Num"][i]) + str(MasterSequence["Genus"][i][0]) + str(MasterSequence["Species"][i][0]) + "_" + str(MasterSequence["Location"][i][0:3]) + "_" + "W"
        #print(MasterSequence["Code5"][i])
    elif str(MasterSequence["Lab"][i]) == "Genbank":
        MasterSequence["Code5"][i] = str(MasterSequence["Num"][i]) + str(MasterSequence["Genus"][i][0]) + str(MasterSequence["Species"][i][0]) + "_" + str(MasterSequence["Location"][i][0:3]) + "_" + "G"
        #print(MasterSequence["Code5"][i])
#print(MasterSequence["#"])
#print(MasterSequence["Num"])
print(MasterSequence["Code5"][0:10])
#print(MasterSequence["Num"])

MasterSequence.to_csv("ModifiedCodesMasterSequence.csv", index=False)