# Author - Kristiāns Francis Cagulis
# Date - 17.02.2022.
# Title - Patstāvīgais darbs - pandas

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests
from pathlib import Path
from random import randint
from fpdf import FPDF
from statistics import mode
from PIL import Image
from io import BytesIO
from ss_scraper import SS

# flats_few = SS("https://www.ss.com/lv/real-estate/flats/riga-region/all/sell/")
# flats_few.get_data()
output_path = "output/graphs"
all_df = []

QUADRATURE = "Kvadratūra"
FLOOR = "Stāvs"
PRICE = "Cena"
SERIES = "Sērija"
ROOM_AMOUNT = "Istabu skaits"
PUB_DATE = "Izvietošanas datums"

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


class priceGraphs:

	def __init__(self, data, pos, x_value, title, xlabel, y_value=PRICE, ylabel="Price"):
		self.pos = pos
		self.x_value = data[x_value]
		self.y_value = data[y_value]
		self.title = title
		self.xlabel = xlabel
		self.ylabel = ylabel

	def _graph_price(self):
		plot = plt.subplot2grid((3, 2), self.pos)
		plot.scatter(self.x_value, self.y_value)
		plot.set_title(self.title)
		plot.set_xlabel(self.xlabel)
		plot.set_ylabel(self.ylabel)


def read():
	files = list(Path(Path(__file__).parent.absolute()).glob("**/*.xlsx"))

	for file_path in files:
		all_df.append(pd.read_excel(file_path))
	df_combined = pd.concat(all_df).reset_index(drop=True)
	df_combined.sort_values(by=[PRICE, PUB_DATE], inplace=True)
	df_combined.drop_duplicates(subset="Pilns sludinājuma teksts", keep=False, inplace=True)

	# replaces floor value to intiger
	for value in df_combined[FLOOR]:
		df_combined = df_combined.replace(value, int(float(value[:value.find("/")])))

	# replaces price value to intiger
	for value in df_combined[PRICE]:
		df_combined = df_combined.replace(value, replace_value(value, " ", ",", ""))

	for _ in df_combined[ROOM_AMOUNT]:
		df_combined = df_combined.replace(["citi", "Citi"], "2")
	try:
		for value in df_combined[ROOM_AMOUNT]:
			df_combined = df_combined.replace(value, int(value))
	except:
		pass
	# converts to datetime
	df_combined[PUB_DATE] = pd.to_datetime(df_combined[PUB_DATE], format="%d.%m.%Y")

	# df_combined.to_excel("output/excel/combined.xlsx", index=False)
	return df_combined.sort_values(by=[PRICE, PUB_DATE])


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
	calc_average(data_corr)


def graph_price(data):
	plt.figure(figsize=(50, 30))
	plt.rc("font", size=15)

	plot1 = priceGraphs(data, (0, 0), FLOOR, "Price to floor", "Floor")
	plot2 = priceGraphs(data, (0, 1), ROOM_AMOUNT, "Price to room amount", "Room amount")
	plot3 = priceGraphs(data, (1, 0), QUADRATURE, "Price to quadrature", "Quadrature")
	plot4 = priceGraphs(data, (1, 1), SERIES, "Price to series", "Series")
	plot5 = priceGraphs(data, (2, 0), PUB_DATE, "Price to date", "Date")

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
	hight = pdf.font_size * 2
	LINE_HIGHT = 5

	columns = [PRICE, FLOOR, ROOM_AMOUNT, SERIES, QUADRATURE, PUB_DATE]

	for column in columns:
		if column == PUB_DATE:
			col_width = width * 2
		else:
			col_width = width
		pdf.cell(col_width, hight, column, border=1)

	pdf.ln(hight)
	pdf.set_font()
	for _ in range(5):
		rand_num = randint(2, len(data) - 10)
		for column in columns:
			if column == PUB_DATE:
				col_width = width * 2
			else:
				col_width = width
			pdf.cell(col_width, hight, str(data[column][rand_num]), border=1)
		pdf.ln(hight)

	text = """
	"Price to floor" grafiks - lielākā daļa pārdodamo dzīvokļu ir līdz 5. stāvam.
	"Price to room amount" grafiks - jo mazāk istabu, jo lētāks dzīvoklis.
	"Price to quadrature" grafiks - jo lielāka dzīvokļa platība, jo dārgāks dzīvoklis.
	"Price to series" grafiks - dārgākie dzīvokļi ir jaunie.
	"Price to date" grafiks - nesen pārdošanā ielikto dzīvokļu ir vairāk.
	"""
	pdf.ln(hight)
	pdf.image(f"{output_path}/korelacija.png", w=usable_w)
	# pdf.write(LINE_HIGHT, "Starp istabu skaitu un cenu, kvadratūru un cenu ir liela korelācija.")
	pdf.image(f"{output_path}/cenu_grafiki.png", w=usable_w)

	for txt in text.split("\n"):
		pdf.write(LINE_HIGHT, txt.strip())
		pdf.ln(LINE_HIGHT)

	average = calc_average(data)
	for key, value in average.items():
		if not isinstance(value, str):
			value = str(round(value))
		pdf.write(LINE_HIGHT, f"{key} - {value}")
		pdf.ln(LINE_HIGHT)

	response = requests.get(series_photos[average[SERIES]])
	img = Image.open(BytesIO(response.content))
	pdf.image(img)
	pdf.output("output/pdf.pdf")


def calc_average(data):
	columns = [FLOOR, ROOM_AMOUNT, SERIES, QUADRATURE]
	mean_price_columns = {FLOOR: None, ROOM_AMOUNT: None, SERIES: None, QUADRATURE: None}
	for column in columns:
		if column == SERIES:
			# print(data[column])
			# print(f"{column} = {mode(data[column])}")
			mean_price_columns[column] = (mode(data[SERIES]))
		else:
			# print(f"{column} = {mode(data[column])}")
			mean_price_columns[column] = mode(data[PRICE]) / mode(data[column])
	return mean_price_columns


def graph_plot():
	data = read()
	graph_corr(data)
	graph_price(data)
	create_pdf(data)


def main():
	graph_plot()


if __name__ == "__main__":
	main()