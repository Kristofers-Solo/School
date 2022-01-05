# Date - 15.12.2021
# Author - Kristiāns Francis Cagulis
# Title - Pandas demo

import pandas as pd

file = pd.ExcelFile("dzivnieki.xls")

data = []

for sheet_name in file.sheet_names:
	data.append(file.parse(sheet_name))

# print(data)
# print(data[0])
# print(data[0].head(2))
# print(data[0].tail(2))
# print(data[0].shape)  # outputs size in tuple
# print(data[0].shape[0])
# print(data[0].shape[1])

new_data = pd.concat([data[0], data[1]])  # concatenates data
# print(new_data)

print(new_data.sort_values("Vecums", ascending=False))  # sorts table by age, inverted

new_data.to_excel("new_file.xls", index=False)