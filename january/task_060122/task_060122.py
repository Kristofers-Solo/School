# Author - Kristiāns Francis Cagulis
# Date - 05.01.2022
# Title - csv homework

import pandas as pd


def main():
	data = pd.read_csv("auto_imports_mainits.csv")
	for column in data.columns:
		if data[column].isnull().sum() > 0:
			print(f"{column} {str(data[column].isnull().sum())}")


if __name__ == '__main__':
	main()