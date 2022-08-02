import pandas

dati = pandas.read_csv('auto_imports_mainits.csv')

for index, element in enumerate(dati.isnull().sum()):
    if element != 0:
        print(f"|  {dati.columns[index]}" + " " * (25 -
              len(str(dati.columns[index]))) + f"{element}")
