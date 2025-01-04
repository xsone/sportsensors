# Functie om specifieke data uit een tekstbestand te halen
import json
import re
import matplotlib.pyplot as plt
import datetime

#Geen speciale leestekens zoals: ;: etc. opnemen in text_fragmenten
#text_fragment = "onLocationChanged"
text_fragment = "saveMultipleSportsData"
#start_text = "LogSports"
input_file = r"D:\Sportdata\GloryFit\20230917.txt"
output_file = r"D:\Sportdata\GloryFit\20230917_filtered.txt"

json_data = []
datum_data = []
hartslag_data = []

def filter_data(input_file, output_file, text_fragement):
    with open(input_file, 'r', encoding='utf-8') as file:
         for line in file:
              #print(line)
              if text_fragment in line:
                 #print(line)
                 patroon = r"\{(.*?)\}"
                 json_match = re.search(patroon, line)
                 if json_match:
                     json_string = json_match.group(0)
                     data = json.loads(json_string)
                     json_data.append(data)
                     datum = data["calendar"]
                     hartslag = data["heart"]
                     stappen = data["step"]
                     print(f"Datum: {datum}, Hartslag: {hartslag}, Stappen: {stappen}")
                     datum_data.append(datum)
                     hartslag_data.append(hartslag)
                 else:
                     print("Geen JSON data gevonden in de string.")

    with open(output_file, 'w') as file:
       json.dump(json_data, file, indent=4)

# Filter de data
filter_data(input_file, output_file, text_fragment)

#Plot data
plt.scatter(datum_data, hartslag_data, marker='o', linestyle='-')
plt.grid(True)
plt.show()
