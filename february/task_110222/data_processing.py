# Author - Kristiāns Francis Cagulis
# Date - 04.02.2022
# Title - Classwork

import matplotlib.pyplot as plt
import pandas as pd
from word2number import w2n
import seaborn as sns
import matplotlib

matplotlib.use('Qt5Agg')

# mathplotlib ir bibliotēka statisku, animētu un interaktīvu vizualizāciju izveidei
# seaborn padara matplotlib sarežģītākos momentus par vienkāršākiem


def get_data():
    data = pd.read_csv("auto_imports_mainits.csv")

    data_copy = data.copy()

    del data_copy["normalized-losses"]

    dislike = ["N/A", "NA", "--"]
    data_copy3 = pd.read_csv("auto_imports_mainits.csv", na_values=dislike)

    # Replaces word written numbers to intigers
    columns = ["num-of-doors", "num-of-cylinders"]
    for column in columns:
        for value in data_copy3[column]:
            try:
                data_copy3 = data_copy3.replace(
                    to_replace=value, value=w2n.word_to_num(value))
            except:
                pass
    print(data_copy3[["num-of-doors", "num-of-cylinders"]])

    # Leaves only columns that contain numbers
    data_copy4 = data_copy3.copy()
    for column in data_copy4:
        if isinstance(data_copy4[column][0], str):
            del data_copy4[column]
    print(data_copy4)
    return data_copy4


def graph_plot():
    data = get_data()

    sns.set_style("whitegrid")
    plt.figure(figsize=(15, 10))
    sns.heatmap(data.corr())
    plt.savefig("plot1.png")
    plt.show()

    # korealācija novērojama starp kolonnām [length,width,wheel-base] un [engine-size,price,horsepower]
    # noderīga ir otrā korelācija, jo tā atklāj to savstarpējo ietekmi

    # matplotlib heatmap veido korealāciju starp datiem savstarpēji salīdzinot to vērtības un norādot iegūtos koeficientus
    # seaborn heatmap veido korealāciju starp datu vērtībām pēc pašnoteiktas korealācijas skalas

    sns.displot(data["price"])
    plt.savefig("plot2.png")
    plt.show()

    plt.scatter(data["price"], data["engine-size"])
    plt.savefig("plot3.png")
    plt.show()

    sns.scatterplot(data["price"], data["engine-size"])
    plt.savefig("plot4.png")
    plt.show()


if __name__ == '__main__':
    # get_data()
    graph_plot()
