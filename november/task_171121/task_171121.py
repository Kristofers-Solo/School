# Author - Kristiāns Francis Cagulis
# Date - 22.11.2021

import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("company_sales_data.csv")


def task_1():
    plt.figure(figsize=(10, 6))  # (x, y)
    x = range(len(data["month_number"]))  # gets range of months
    plt.plot(x, data["total_profit"])  # sets up the plot
    plt.xticks(x, data["month_number"], fontsize=15)  # sets x value step
    plt.yticks(fontsize=15)
    plt.ylim(ymin=100000)  # sets minimal y value

    set_labels("Company profit per month", "Month number", "Total profit")

    plt.show()


def task_2():
    plt.figure(figsize=(10, 6))  # (x, y)

    x = range(len(data["month_number"]))  # gets range of months

    data_list = list(data.columns)[1:-2]  # gets and trims column names

    for column in data_list:
        plt.plot(x, data[column], lw=4, marker='o', ms=10)  # ms = marker size

    plt.xticks(x, data["month_number"], fontsize=15)  # sets x value step
    plt.yticks(fontsize=15)

    set_labels("Sales data", "Month number", "Sales units in number")

    # capitalizes each word in list
    new_data_list = list(
        map(lambda x: x.capitalize() + " Sales Data", data_list))
    plt.legend(new_data_list, loc='upper left', fontsize=15)
    plt.show()


def task_3():
    plt.figure(figsize=(10, 6))  # (x, y)
    x = range(len(data["month_number"]))  # gets range of months

    plt.scatter(x, data["toothpaste"], s=75)  # sets up the plot
    plt.grid(ls='dashed', lw=1.5)  # sets grid line type and width
    plt.xticks(x, data["month_number"], fontsize=15)  # sets x value step
    plt.yticks(fontsize=15)

    set_labels("Toothpaste Sales data", "Month number", "Number of units Sold")
    plt.legend(["Toothpaste Sales data"], loc='upper left', fontsize=15)
    plt.show()


def task_4():
    items = ["facecream", "facewash"]

    data.plot(x="month_number", y=[
              "facecream", "facewash"], kind='bar', figsize=(10, 6), fontsize=15)

    plt.xticks(rotation=0)  # rotates x lables to 0
    plt.grid(ls='dashed', lw=1.5)  # sets grid line type and width

    set_labels("Facewash and Facecream Sales data",
               "Month number", "Sales units in number")
    new_items_list = list(map(lambda x: x.capitalize() + " Sales Data", items))
    plt.legend(new_items_list, loc='upper left', fontsize=15)
    plt.show()


def set_labels(title: str, xlabel: str, ylabel: str):
    plt.title(title, fontsize=15)
    plt.xlabel(xlabel, fontsize=15)
    plt.ylabel(ylabel, fontsize=15)


def main():
    task = input("""Ivēlieties uzdevumu:
1 - pirmais uzdevums
2 - otrais uzdevums
3 - trešais uzdevums
4 - ceturtais uzdevums
""")

    if task == "1":
        task_1()
    elif task == "2":
        task_2()
    elif task == "3":
        task_3()
    elif task == "4":
        task_4()
    else:
        print("Tika ievadīts nepareiz cipars")


if __name__ == '__main__':
    main()
