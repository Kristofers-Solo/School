# Author - Kristiāns Francis Cagulis
# Date - 01.12.2021
# Title - Patstāvīgais darbs

from bs4 import BeautifulSoup
import requests
import pandas as pd
import openpyxl

HEADERS = {
    "User-Agent":
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Vivaldi/4.1.2369.21'
}


class SS:
	def __init__(self, url):
		self.url = url

	def _get_page_amount(self):
		current_page = None
		page_amount = 1
		url = self.url
		while current_page != page_amount:
			current_page = page_amount
			page = requests.get(url, headers=HEADERS)
			soup = BeautifulSoup(page.content, 'html.parser')

			# getting max page amount
			for el in soup.find_all(class_='navi'):
				cropped_number = el.get_text().strip()
				if cropped_number.isnumeric():
					cropped_number = int(cropped_number)
					if cropped_number > page_amount:
						page_amount = cropped_number
			url = self.url + f"/page{page_amount}.html"

		return page_amount

	def get_data(self):
		items = []
		combined_list = []
		# combined_list.clear()
		for page_number in range(1, self._get_page_amount() + 1):
			url = self.url + f"/page{page_number}.html"

			page = requests.get(url, headers=HEADERS)
			soup = BeautifulSoup(page.content, 'html.parser')
			ids = [tag['id'] for tag in soup.select('tr[id]')]  # creates list with ids
			ids = [x for x in ids if "tr_bnr" not in x]  # removes "tr_bnr" from list
			ids.remove("head_line")  # removes first "head_line" id

			# TODO
			# Atrašānās vieta
			# stāvs
			# istabu skaits
			# kvadratūra
			# cena
			# sērija
			# Pilns sludinājuma teksts
			# Sludinājuma ievietošanas datums

			# getting product name
			for el in soup.find_all(id=ids):
				for elem in el.find_all(class_='msga2-o pp6'):
					items.append(elem.get_text())

		chunk_size = 6
		chunked_items_list = [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]
		# print(chunked_items_list)
		columns = [
		    "Atrašanās vieta",
		    "Istabu skaits",
		    "Kvadratūra",
		    "Stāvs",
		    "Sērija",
		    "Cena",
		    #"Pilns sludinājuma teksts",
		    #"Izvietošanas datums"
		]

		df = pd.DataFrame(chunked_items_list, columns=columns)
		df.to_excel(excel_writer='test.xlsx', index=False)
		print(df)


flats = SS("https://www.ss.com/lv/real-estate/flats/riga-region/all/sell")


def main():
	flats.get_data()


if __name__ == '__main__':
	main()