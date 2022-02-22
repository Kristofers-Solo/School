# Author - Kristiāns Francis Cagulis
# Date - 21.02.2022.
# Title - Patstāvīgais darbs - pandas

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import sys
from os import mkdir, listdir
from pathlib import Path
from random import randint
from fpdf import FPDF
from statistics import mode, mean
from PIL import Image
from io import BytesIO
from ss_scraper import SS

output_path = "output/graphs"
all_df = []

QUADRATURE = "Kvadratūra"
FLOOR = "Stāvs"
PRICE = "Cena"
SERIES = "Sērija"
ROOM_AMOUNT = "Istabu skaits"
PUB_DATE = "Izvietošanas datums"

COLUMNS = [PRICE, FLOOR, ROOM_AMOUNT, SERIES, QUADRATURE, PUB_DATE]

series_photos = {
    "103.": "https://i.ss.com/gallery/5/902/225301/45060087.th2.jpg",
    "104.": "https://i.ss.com/gallery/5/888/221910/44381841.th2.jpg",
    "119.": "https://i.ss.com/gallery/5/902/225443/45088567.th2.jpg",
    "467.": "https://i.ss.com/gallery/5/892/222881/44576186.th2.jpg",
    "602.": "https://i.ss.com/gallery/5/896/223820/44763891.th2.jpg",
    "Čehu pr.": "https://i.ss.com/gallery/5/902/225358/45071499.th2.jpg",
    "Hrušč.": "https://i.ss.com/gallery/5/896/223961/44792152.th2.jpg",
    "LT proj.": "https://i.ss.com/gallery/5/873/218203/43640498.th2.jpg",
    "M. ģim.": "https://i.ss.com/gallery/5/871/217506/43501012.th2.jpg",
    "P. kara": "https://i.ss.com/gallery/5/902/225490/45097851.th2.jpg",
    "Priv. m.": "https://i.ss.com/gallery/5/895/223697/44739240.th2.jpg",
    "Renov.": "https://i.ss.com/gallery/5/902/225442/45088303.th2.jpg",
    "Specpr.": "https://i.ss.com/gallery/5/902/225492/45098378.th2.jpg",
    "Staļina": "https://i.ss.com/gallery/5/902/225440/45087952.th2.jpg",
    "Jaun.": "https://i.ss.com/gallery/5/902/225456/45091154.th2.jpg"
}


class priceGraph:

	def __init__(self, data, pos, title, x_value, xlabel, xticks=None, y_value=PRICE, ylabel="Price"):
		self.pos = pos
		self.x_value = data[x_value]
		self.y_value = data[y_value]
		self.title = title
		self.xlabel = xlabel
		self.ylabel = ylabel
		self.xticks = xticks

	def _graph_price(self):
		plot = plt.subplot2grid((3, 2), self.pos)
		plot.scatter(self.x_value, self.y_value)
		plot.set_title(self.title)
		plot.set_xlabel(self.xlabel)
		plot.set_ylabel(self.ylabel)
		if self.xticks != None:
			plot.set_xticks(self.xticks)


def read():
	files = list(Path(Path(__file__).parent.absolute()).glob("**/*.xlsx"))

	for file_path in files:
		all_df.append(pd.read_excel(file_path))
	df_combined = pd.concat(all_df).reset_index(drop=True)  # combine DataFrames
	df_combined.sort_values(by=[PRICE, PUB_DATE], inplace=True)  # sort DataFrame
	df_combined.drop_duplicates(keep="first", inplace=True)  # drop duplicates
	# replaces floor value to intiger
	for value in df_combined[FLOOR]:
		df_combined = df_combined.replace(value, int(float(value[:value.find("/")])))

	# replaces price value to intiger
	for value in df_combined[PRICE]:
		df_combined = df_combined.replace(value, replace_value(value, " ", ",", ""))

	# replaces "Citi" to 7
	for _ in df_combined[ROOM_AMOUNT]:
		df_combined = df_combined.replace(["citi", "Citi"], "7")

	# converts room amount to intiger
	for value in df_combined[ROOM_AMOUNT]:
		df_combined = df_combined.replace(value, int(value))

	# converts to datetime
	df_combined[PUB_DATE] = pd.to_datetime(df_combined[PUB_DATE], format="%d.%m.%Y").dt.date

	df_combined.to_excel("output/excel/combined.xlsx", index=False)
	return df_combined.sort_values(by=PUB_DATE)


# replace value
replace_value = lambda value, find, replace, replace_to: int(value[:value.find(find)].replace(replace, replace_to))


def graph_corr(data):
	data_corr = data.copy()
	plt.rc("font", size=8)
	# gets all series
	series = []
	for i in data_corr[SERIES]:
		if i not in series:
			series.append(i)
	# change series names to numbers
	data_corr[SERIES] = data_corr[SERIES].replace(series, range(len(series)))

	sns.heatmap(data_corr.corr())
	plt.savefig(f"{output_path}/korelacija.png")


def graph_price(data):
	plt.figure(figsize=(50, 30))
	plt.rc("font", size=15)

	plot1 = priceGraph(data, (0, 0), "Price to floor", FLOOR, "Floor", range(1, max(data[FLOOR]) + 1))
	plot2 = priceGraph(data, (0, 1), "Price to room amount", ROOM_AMOUNT, "Room amount")
	plot3 = priceGraph(data, (1, 0), "Price to quadrature", QUADRATURE, "Quadrature")
	plot4 = priceGraph(data, (1, 1), "Price to series", SERIES, "Series")
	plot5 = priceGraph(data, (2, 0), "Price to date", PUB_DATE, "Date")

	plot1._graph_price()
	plot2._graph_price()
	plot3._graph_price()
	plot4._graph_price()
	plot5._graph_price()

	plt.savefig(f"{output_path}/cenu_grafiki.png")


def create_pdf(data):
	pdf = FPDF("P", "mm", "A4")
	pdf.add_page()
	pdf.add_font("Roboto", fname="fonts/Roboto-Regular.ttf", uni=True)
	pdf.set_font("Roboto", size=12)

	usable_w = pdf.w - 2 * pdf.l_margin
	width = usable_w / 7
	height = pdf.font_size * 2
	LINE_HEIGHT = 5

	# table head
	for column in COLUMNS:
		if column == PUB_DATE:
			col_width = width * 2
		else:
			col_width = width
		pdf.cell(col_width, height, column, border=1)

	pdf.ln(height)
	# table contents
	for _ in range(5):
		rand_num = randint(2, len(data))
		for column in COLUMNS:
			if column == PUB_DATE:
				col_width = width * 2
			else:
				col_width = width
			pdf.cell(col_width, height, str(data[column].iloc[rand_num]), border=1)
		pdf.ln(height)

	pdf.ln(height)
	pdf.image(f"{output_path}/korelacija.png", w=usable_w)  # corr graph
	pdf.write(LINE_HEIGHT, "Starp istabu skaitu un cenu, kvadratūru un cenu ir liela korelācija.")
	pdf.ln(height)
	pdf.image(f"{output_path}/cenu_grafiki.png", w=usable_w)  # price graph

	# price graph conclusions
	text = """
	"Price to floor" grafiks - lielākā daļa pārdodamo dzīvokļu ir līdz 6. stāvam.
	"Price to room amount" grafiks - veido normālo sadalījumu (Gausa sadalījumu).
	"Price to quadrature" grafiks - jo lielāka dzīvokļa platība, jo dārgāks dzīvoklis.
	"Price to series" grafiks - jaunie, renovētie un pēc kara dzīvokļi ir dārgāki.
	"Price to date" grafiks - nav nekādas sakarības.
	"""
	for txt in text.split("\n"):
		pdf.write(LINE_HEIGHT, txt.strip())
		pdf.ln(LINE_HEIGHT)

	# mean/mode values
	text = [
	    "Vidējā cena: ", "Vidējā cena attiecībā pret kvadratūru: ", "Sērijas moda: ", "Vidējā cena attiecībā pret istabu skaitu: ",
	    "Vidējā cena attiecībā pret stāvu: "
	]
	values = [
	    round(mean(data[PRICE]), 2),
	    round(mean(data[PRICE]) / mean(data[QUADRATURE])),
	    mode(data[SERIES]),
	    round(mean(data[PRICE]) / mean(data[ROOM_AMOUNT])),
	    round(mean(data[PRICE]) / mean(data[FLOOR]))
	]
	for txt, value in zip(text, values):
		pdf.write(LINE_HEIGHT, f"{txt}{value}")
		pdf.ln(LINE_HEIGHT)

	# adds photo of most frequent series
	response = requests.get(series_photos[mode(data[SERIES])])
	img = Image.open(BytesIO(response.content))
	pdf.image(img)

	pdf.output("output/pdf/secinajumi.pdf")


def make_dir():
	if "output" not in listdir():
		mkdir("output")
	if "excel" not in listdir("output"):
		mkdir("output/excel")
	if "graphs" not in listdir("output"):
		mkdir("output/graphs")
	if "pdf" not in listdir("output"):
		mkdir("output/pdf")


def graph_plot():
	data = read()
	graph_corr(data)
	graph_price(data)
	create_pdf(data)


flats_riga = SS("https://www.ss.com/lv/real-estate/flats/riga/all/sell/", "riga")
flats_rigareg = SS("https://www.ss.com/lv/real-estate/flats/riga-region/all/sell/", "rigareg")
flats_aizkraukle = SS("https://www.ss.com/lv/real-estate/flats/aizkraukle-and-reg/sell/", "aizkraukle")
flats_tukums = SS("https://www.ss.com/lv/real-estate/flats/tukums-and-reg/sell/", "tukums")
flats_ogre = SS("https://www.ss.com/lv/real-estate/flats/ogre-and-reg/sell/", "ogre")

OPERATIONS = """
python pd_pandas_k_f_cagulis.py
python pd_pandas_k_f_cagulis.py  <operations>

Operations:
    -h --help
    -n --new        Scrape new file
"""


def main(argv):
	for arg in argv:
		if arg in ["-h", "--help"]:
			print(OPERATIONS)
			exit()
		elif arg in ["-n", "--new"]:
			flats_riga.get_data()
	make_dir()
	graph_plot()


if __name__ == "__main__":
	main(sys.argv[1:])