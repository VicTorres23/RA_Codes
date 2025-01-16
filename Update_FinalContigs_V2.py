import requests
from bs4 import BeautifulSoup
import regex as re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

MasterSequence = pd.read_excel("C:/Users/vemma/Documents/Master in Bioinformatics/Spring_2025_Semester/MasterSequence_Database for Gnesiophylogeny 01.07.25.xlsx")
rows = []
for i in range(len(MasterSequence["Lab"])):
    if MasterSequence["Lab"][i] == "Genbank":
        rows.append(MasterSequence.iloc[i])
genbank_sequences = pd.DataFrame(rows)

url = "https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=Tree&id=1709199&lvl=3&lin=f&keep=1&srchmode=1&unlock"

response = requests.get(url)

if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    links = re.findall(r"href\=\"(wwwtax\.cgi\?mode\=Tree\&amp\;id\=\d+\&amp\;lvl\=3\&amp\;lin\=f\&amp\;keep\=1\&amp\;srchmode\=1\&amp\;unlock)\"\stitle\=\"genus\"\>\<strong\>\w+\<", str(soup))
    links = ["https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/" + re.sub(r"amp\;", "", link) for link in links]

    for link in links:
        response1 = requests.get(link)
        if response1.status_code == 200:
            html_content1 = response1.text
            soup1 = BeautifulSoup(html_content1, 'html.parser')

            species = re.findall(r"href\=\"wwwtax\.cgi\?mode\=Info\&amp\;id\=\d+\&amp\;lvl\=3\&amp\;lin\=f\&amp\;keep\=1\&amp\;srchmode\=1\&amp\;unlock\" title\=\"species\"\>\<strong\>([\w\s]+)\<", str(soup1))
            subspecies = re.findall(r"href\=\"wwwtax\.cgi\?mode\=Info\&amp\;id\=\d+\&amp\;lvl\=3\&amp\;lin\=f\&amp\;keep\=1\&amp\;srchmode\=1\&amp\;unlock\" title\=\"subspecies\"\>\<strong\>([\w\s]+)\<", str(soup1))
            species_n_subspecies = species + subspecies
            species_links1 = re.findall(r"href\=\"(wwwtax\.cgi\?mode\=Info\&amp\;id\=\d+\&amp\;lvl\=3\&amp\;lin\=f\&amp\;keep\=1\&amp\;srchmode\=1\&amp\;unlock)\" title\=\"species\"\>\<strong\>[\w\s]+\<", str(soup1))
            subspecies_links1 = re.findall(r"href\=\"(wwwtax\.cgi\?mode\=Info\&amp\;id\=\d+\&amp\;lvl\=3\&amp\;lin\=f\&amp\;keep\=1\&amp\;srchmode\=1\&amp\;unlock)\" title\=\"subspecies\"\>\<strong\>[\w\s]+\<", str(soup1))
            species_links1 = ["https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/" + re.sub(r"amp\;", "", link) for link in species_links1]
            subspecies_links1 = ["https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/" + re.sub(r"amp\;", "", link) for link in subspecies_links1]
            species_n_subspecies_links = species_links1 + subspecies_links1

            for website in species_n_subspecies_links:
                response2 = requests.get(website)
                if response2.status_code == 200:
                    html_content2 = response2.text
                    soup2 = BeautifulSoup(html_content2, 'html.parser')
                    Info_link = re.findall(r"href\=\"(\/nuccore\/\?term\=txid\d+\[Organism\:noexp\])\"\>", str(soup2))
                    Info_link = ["https://www.ncbi.nlm.nih.gov" + link for link in Info_link]

                    for Info_website in Info_link:
                        response3 = requests.get(Info_website)
                        if response3.status_code == 200:
                            html_content3 = response3.text
                            soup3 = BeautifulSoup(html_content3, 'html.parser')
                            genes = ["18S", "oxidase subuni", "ITS"]
                            titles = re.findall("\;ordinalpos\=\d\"\>([\w\s\d\(\)\_\n\;\-]+)\,", str(soup3))
                            GenBank_ID_multiple = re.findall("href\=\"\/nuccore\/([A-Z][A-Z]\d+\.\d)", str(soup3))
                            GenBank_ID_multiple = list(dict.fromkeys(GenBank_ID_multiple))
                            '''
                            Fasta_links = re.findall(r"\<a\sclass\=\"dblinks\"\shref\=\"(\/nuccore\/[A-Z][A-Z]\d+\.\d\?report\=fasta)\"\sid\=", str(soup3))
                            Fasta_links = ["https://www.ncbi.nlm.nih.gov" + link for link in Fasta_links]
                            #print(Fasta_links)
                            for hyperlink in Fasta_links:
                                response4 = requests.get(hyperlink)
                                if response4.status_code == 200:
                                    html_content4 = response4.text
                                    soup4 = BeautifulSoup(html_content4, 'html.parser')
                                    #print(html_content4)'''

                            approved_titles = []
                            approved_titles_ID = []

                            for i in range(len(titles)):
                                if any(gene in titles[i] for gene in genes):
                                    approved_titles.append(titles[i])
                                    approved_titles_ID.append(GenBank_ID_multiple[i])
                            for element, current_id in zip(approved_titles, approved_titles_ID):
                                genus_species_GenBankID = False  # Assume not found initially
                                for i in range(len(genbank_sequences["Genus"])):
                                    if (genbank_sequences["Genus"].iloc[i] in element and
                                        genbank_sequences["Species"].iloc[i] in element and
                                        current_id in genbank_sequences["SeqName"].iloc[i]):
                                        genus_species_GenBankID = True
                                        break
                                if genus_species_GenBankID:
                                    print(f"Already in Excel: {current_id}")
                                    pass
                                else:
                                    print(f"Adding sequence to Excel: {current_id}")
                                    keywords = element.split(" ")
                                    url_fasta = "https://www.ncbi.nlm.nih.gov/nuccore/" + current_id + "?report=fasta"
                                    print(url_fasta)
                                    driver = webdriver.Chrome()
                                    driver.get(url_fasta)
                                    try:
                                        fasta_content = WebDriverWait(driver, 10).until(
                                            EC.presence_of_element_located((By.TAG_NAME, "pre"))
                                        ).text
                                        #print(fasta_content)
                                        #print(type(fasta_content))
                                        fasta_content = re.sub(r"(\>.+\n)", "", fasta_content)
                                        fasta_content = re.sub(r"\n", "", fasta_content)
                                        print(fasta_content)
                                    except Exception as e:
                                        print(f"Error: {e}")
                                    finally:
                                        driver.quit()
                                    if "18S" in element:
                                        MasterSequence.loc[len(MasterSequence)] = {"Genus": keywords[0], "Species": keywords[1], "Lab": "Genbank", "Gene": "18S", "SeqName": "| gb |" + current_id + " | " + element, "Coordinates A": "GB", "Coordinates B": "GB", "Sequence": fasta_content, "Seq Len": len(fasta_content)}
                                    elif "cytochrome" in element:
                                        MasterSequence.loc[len(MasterSequence)] = {"Genus": keywords[0],
                                                                                   "Species": keywords[1],
                                                                                   "Lab": "Genbank", "Gene": "COI",
                                                                                   "SeqName": "| gb |" + current_id + " | " + element,
                                                                                   "Coordinates A": "GB",
                                                                                   "Coordinates B": "GB", "Sequence": fasta_content, "Seq Len": len(fasta_content)}
                                    elif "ITS" in element:
                                        MasterSequence.loc[len(MasterSequence)] = {"Genus": keywords[0],
                                                                                   "Species": keywords[1],
                                                                                   "Lab": "Genbank", "Gene": "ITS",
                                                                                   "SeqName": "| gb |" + current_id + " | " + element,
                                                                                   "Coordinates A": "GB",
                                                                                   "Coordinates B": "GB", "Sequence": fasta_content, "Seq Len": len(fasta_content)}

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    pass

MasterSequence.to_csv("NewFinalContigs.csv", index=False)
print(MasterSequence["Genus"])