# Author - Kristiāns Francis Cagulis
# Date - 19.01.2022
# Title - Classwork

import pandas as pd
from word2number import w2n


def main():
    data = pd.read_csv("auto_imports_mainits.csv")

    # summary = data["normalized-losses"].notnull()  # returns boolean
    # print(data[summary], "\n") # "normalized-losses" is not empty
    # print(data[~summary])  # inverts all the bits
    # print(len(data[~summary]))

    data_copy = data.copy()

    # Delete rows with empty spots
    # print(f"Before erasing: {data_copy.shape}")
    # print(f"After erasing: {data_copy.dropna().shape}")

    # Delete column
    # print(f"Before erasing: {data_copy.shape}")
    del data_copy["normalized-losses"]
    # print(f"After erasing: {data_copy.shape}")
    # print(f"Blank spots: {data_copy.isnull().any().sum()}")

    # data_copy2 = data_copy.copy()
    # print(data_copy2.head())
    # data_copy2.drop(data_copy2.columns[[0, 1]], axis=1, inplace=True)
    # print(data_copy2.head())

    dislike = ["N/A", "NA", "--"]
    data_copy3 = pd.read_csv("auto_imports_mainits.csv", na_values=dislike)

    # Mean
    # print(data_copy3.iloc[52], "\n")
    # mean = data_copy3["bore"].mean()
    # data_copy3["bore"].fillna(mean, inplace=True)
    # print(data_copy3.iloc[52])

    # Median
    # print(data_copy3.iloc[53], "\n")
    # median = data_copy3["bore"].median()
    # data_copy3["bore"].fillna(median, inplace=True)
    # print(data_copy3.iloc[53])

    # Mode
    # print(data_copy3.iloc[60], "\n")
    # mode = data_copy3["bore"].mode()
    # data_copy3["bore"].fillna(mode, inplace=True)
    # print(data_copy3.iloc[60])

    # print(data_copy3.dtypes)

    # data_copy3["curb-weight"] = pd.to_numeric(data_copy3["curb-weight"], errors='coerce')
    # data_copy3["curb-weight"] = data_copy3["curb-weight"].astype("float64")
    # print(data_copy3.dtypes)

    # Replaces word written numbers to intigers
    columns = ["num-of-doors", "num-of-cylinders"]
    for column in columns:
        for value in data_copy3[column]:
            try:
                data_copy3 = data_copy3.replace(
                    to_replace=value, value=w2n.word_to_num(value))
                print(type(w2n.word_to_num(value)))
            except:
                pass
    print(data_copy3[["num-of-doors", "num-of-cylinders"]])

    # Leaves only columns that contain numbers
    data_copy4 = data_copy3.copy()
    for column in data_copy4:
        if isinstance(data_copy4[column][0], str):
            del data_copy4[column]
    print(data_copy4)


if __name__ == '__main__':
    main()
