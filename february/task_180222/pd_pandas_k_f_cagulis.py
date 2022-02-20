# Author - Kristiāns Francis Cagulis
# Date - 17.02.2022.
# Title - Patstāvīgais darbs - pandas

from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from ss_scraper import SS

# flats_few = SS("https://www.ss.com/lv/real-estate/flats/riga-region/all/sell/")
# flats_few.get_data()
output_path = "output/graphs"
all_df = []


def read(path):
	df = pd.read_excel(path)
	all_df.append(df)


def get_data():
	files = list(Path(Path(__file__).parent.absolute()).glob("**/*.xlsx"))

	for file in files:
		read(file)
	df_out = pd.concat(all_df).reset_index(drop=True)
	# df_out.to_excel("output/excel/combined.xlsx", index=False)

	# replaces floor value to intiger
	for value in df_out["Stāvs"]:
		df_out = df_out.replace(value, int(value[:value.find("/")]))

	# replaces price value to intiger
	for value in df_out["Cena"]:
		df_out = df_out.replace(value, replace_value(value))
	return df_out.sort_values(by="Cena")


def replace_value(value):
	new_value = value[:value.find(" ")]
	new_value = new_value.replace(",", "")
	return int(new_value)


def graph_plot():
	data = get_data()
	graph_corr(data)
	graph_price(data)


def graph_corr(data):
	data_corr = data.copy()

	series = []
	for i in data_corr["Sērija"]:
		if i not in series:
			series.append(i)
	j = 0
	for s in series:
		data_corr = list(map(lambda x: x.replace(s, j), data_corr))
		j += 1

	print(data_corr["Sērija"])
	sns.heatmap(data_corr.corr())
	plt.savefig(f"{output_path}/korelacija.png")


def graph_price(data):
	# plot settings
	plt.figure(figsize=(50, 30))
	plt.rc("font", size=15)
	# plt.rc("font", titlesize=24)

	# placing the plots in the plane
	plot1 = plt.subplot2grid((3, 2), (0, 0))
	plot2 = plt.subplot2grid((3, 2), (0, 1))
	plot3 = plt.subplot2grid((3, 2), (1, 0))
	plot4 = plt.subplot2grid((3, 2), (1, 1))
	plot5 = plt.subplot2grid((3, 2), (2, 0))

	# floor to price
	plot1.scatter(data["Cena"], data["Stāvs"])
	plot1.set_title("Floor to price")
	plot1.set_xlabel("Price")
	plot1.set_ylabel("Floor")

	# room amount to price
	plot2.scatter(data["Cena"], data["Istabu skaits"])
	plot2.set_title("Room amount to price")
	plot2.set_xlabel("Price")
	plot2.set_ylabel("Room amount")

	# quadrature to price
	plot3.scatter(data["Cena"], data["Kvadratūra"])
	plot3.set_title("Quadrature to price")
	plot3.set_xlabel("Price")
	plot3.set_ylabel("Quadrature")

	# series to price
	plot4.scatter(data["Cena"], data["Sērija"])
	plot4.set_title("Series to price")
	plot4.set_xlabel("Price")
	plot4.set_ylabel("Series")

	# date to price
	plot5.scatter(data["Cena"], data["Izvietošanas datums"])
	plot5.set_title("Date to price")
	plot5.set_xlabel("Price")
	plot5.set_ylabel("Date")

	plt.savefig(f"{output_path}/cenu_grafiki.png")


def main():
	graph_plot()


if __name__ == "__main__":
	main()