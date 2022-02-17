# Author - Kristiāns Francis Cagulis
# Date - 17.02.2022.
# Title - Patstāvīgais darbs - pandas

from pathlib import Path
import matplotlib
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


def address():
	pass


def get_data():
	files = list(Path(Path(__file__).parent.absolute()).glob("**/*.xlsx"))

	for file in files:
		read(file)
	df_out = pd.concat(all_df).reset_index(drop=True)
	df_out.to_excel("output/excel/combined.xlsx", index=False)
	return df_out


def graph_plot():
	data = get_data()
	# graph_corr(data)
	graph_price(data)


def graph_corr(data):
	data_corr = data.copy()
	sns.set_style("whitegrid")
	# plt.figure(figsize=(15, 10))
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

	# price to floor
	plot1.scatter(data["Cena"], data["Stāvs"])
	plot1.set_title("Price to floor")

	# price to room amount
	plot2.scatter(data["Cena"], data["Istabu skaits"])
	plot2.set_title("Price to room amount")

	# price to quadrature
	plot3.scatter(data["Cena"], data["Kvadratūra"])
	plot3.set_title("Price to quadrature")

	# price to series
	plot4.scatter(data["Cena"], data["Sērija"])
	plot4.set_title("Price to series")

	# price to date
	plot5.scatter(data["Cena"], data["Izvietošanas datums"])
	plot5.set_title("Price to floor")

	plt.savefig(f"{output_path}/cenu_grafiki.png")


def main():
	graph_plot()


if __name__ == "__main__":
	main()