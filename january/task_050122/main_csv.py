# Author - Kristiāns Francis Cagulis
# Date - 05.01.2022
# Title - csv

import pandas as pd


def main():
    data = pd.read_csv("auto_imports_mainits.csv")
    blank = data.isnull().any().sum()
    print(f"There are empty spaces in {blank} columns")

    print(data.isnull().sum())
    print(data.columns[data.isnull().any()])


if __name__ == '__main__':
    main()
