# Author - Kristiāns Francis Cagulis
# Date - 05.01.2022
# Title - csv homework

import pandas as pd


def main():
	data = pd.read_csv("auto_imports_mainits.csv")
	# 1st method
	for column in data.columns:
		if data[column].isnull().sum() > 0:
			print(f"{column} {data[column].isnull().sum()}")

	print("-" * 22)

	# 2nd method
	print(pd.DataFrame(data.isnull().sum(), data.columns[data.isnull().any()]).to_string(header=None))


if __name__ == '__main__':
	main()