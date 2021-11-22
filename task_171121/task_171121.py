# Author - Kristiāns Francis Cagulis
# Date - 22.11.2021

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('company_sales_data.csv')


x = range(len(df["month_number"]))
plt.plot(x, df["total_profit"])
plt.xticks(x, df["month_number"])
plt.xlabel("Month number")
plt.ylabel("Total profit")

plt.show()