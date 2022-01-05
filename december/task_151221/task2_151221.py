# Date - 15.12.2021
# Author - Kristiāns Francis Cagulis
# Title - Pandas demo 2

from textwrap import indent
from numpy import arctan
import pandas as pd

file = pd.ExcelFile("dati_masiviem.xlsx")

data = []

for sheet_name in file.sheet_names:
	data.append(file.parse(sheet_name))

# print(data[0]["Nosaukums"])
data[0]["Cena"] = round((data[0]["Pašizmaksa"] + .4) * 1.21, 2)
# print(data[0]["Cena"])

data[0]["Kopā"] = round(data[0]["Cena"] * data[0]["Skaits"], 2)

# print(data[0]["Kopā"])

data[0]["Peļņa"] = round(data[0]["Skaits"] * .4 / 1.21, 2)
# print(data[0])

insertable_line = data[0][["Skaits", "Cena"]].sum()
changed_line = pd.DataFrame(data=insertable_line).T
changed_line = changed_line.reindex(columns=data[0].columns)
data.append(data[0])
data[1] = data[1].append(changed_line)
# print(data[1])
# print(data[1]["Skaits"])

# dates
grouped_data = data[0][["Datums", "Skaits"]].groupby("Datums").sum()
grouped_data.insert(0, "Datums2", grouped_data.index)
# print(grouped_data)

data.append(grouped_data)

found = data[2]["Datums2"] == "2020-09-09"
# print(data[2][found])

page_num = 1
with pd.ExcelWriter("new_file2.xlsx") as file:
	for page in data:
		page.to_excel(file, sheet_name=str(page_num), index=False)
		page_num += 1