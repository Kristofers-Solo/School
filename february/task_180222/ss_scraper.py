# Author - Kristiāns Francis Cagulis
# Date - 21.02.2022
# Title - Patstāvīgais darbs "SS.com scraping"

from bs4 import BeautifulSoup
import requests
import pandas as pd
from loadbar import LoadBar
from os import mkdir, listdir
from datetime import datetime

HEADERS = {
    "User-Agent":
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.97 Safari/537.36 Vivaldi/4.1.2369.21'
}


class SS:

	def __init__(self, url, name):
		self.url = url
		self.name = name

	def _get_page_amount(self):
		page = requests.get(self.url, headers=HEADERS)
		soup = BeautifulSoup(page.content, 'html.parser')

		try:
			last_url = soup.find(class_='td2').findChild('a')['href']
			page_amount = last_url[last_url.find("page") + 4:last_url.find(".html")]
		except:
			page_amount = 1
		# print(f"Page amount = {page_amount}")

		return int(page_amount)

	def get_data(self):
		items = []
		item_no = 1
		page_amount = self._get_page_amount()
		# widgets = ["Getting data...", pbar.Bar("*")]
		# bar = pbar.ProgressBar(max_value=page_amount, widgets=widgets).start()
		bar = LoadBar(max=page_amount * 30, head="#", body="#")
		bar.start()

		for page_number in range(1, page_amount + 1):

			url = self.url + f"/page{page_number}.html"
			page = requests.get(url, headers=HEADERS)
			soup = BeautifulSoup(page.content, 'html.parser')

			# item ids
			ids = [tag['id'] for tag in soup.select('tr[id]')]  # creates list with ids
			ids = [x for x in ids if "tr_bnr" not in x]  # removes "tr_bnr" elements from list
			ids.remove("head_line")  # removes first "head_line" id
			# print(f"Page {page_number}")

			# getting item data
			for id in soup.find_all(id=ids):
				# print(f"Item {item_no}")
				bar.update(step=item_no)

				item_no += 1

				for elem in id.find_all(class_='msga2-o pp6'):
					items.append(elem.get_text())

				if len(id.find_all(class_='msga2-o pp6')) == 7:
					del items[-2]

				# adverts url
				item_url = id.findChild(class_='msg2').findChild('div').findChild('a')['href']  # gets url
				item_url = "https://www.ss.com" + item_url
				item_page = requests.get(item_url, headers=HEADERS)
				item_soup = BeautifulSoup(item_page.content, 'html.parser')

				# adverts full text
				item_text = item_soup.find(id='msg_div_msg').get_text()  # gets full text
				item_text = item_text[:item_text.find("Pilsēta:")]  # removes text last part (table)
				items.append(item_text)

				# adverts publication date
				item_date = item_soup.find_all('td', class_='msg_footer')  # gets all 'msg_footer' class'
				item_date = item_date[2].get_text()  # extracts 3rd element
				items.append(item_date[8:18])  # crops date
		bar.end()
		chunk_size = 8
		chunked_items_list = [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]  # combines each 'chunk_size' elements into array
		columns = ["Atrašanās vieta", "Istabu skaits", "Kvadratūra", "Stāvs", "Sērija", "Cena", "Pilns sludinājuma teksts", "Izvietošanas datums"]
		df = pd.DataFrame(chunked_items_list, columns=columns)
		time = datetime.now().strftime("%d%m%y%H%M%S")  # current time
		if "excel" not in listdir("output"):
			mkdir("output/excel")
		df.to_excel(excel_writer=f"output/excel/ss_{self.name}_{time}.xlsx", index=False)


flats_riga = SS("https://www.ss.com/lv/real-estate/flats/riga/all/sell/", "riga")
flats_rigareg = SS("https://www.ss.com/lv/real-estate/flats/riga-region/all/sell/", "rigareg")
flats_aizkraukle = SS("https://www.ss.com/lv/real-estate/flats/aizkraukle-and-reg/sell/", "aizkraukle")
flats_tukums = SS("https://www.ss.com/lv/real-estate/flats/tukums-and-reg/sell/", "tukums")
flats_ogre = SS("https://www.ss.com/lv/real-estate/flats/ogre-and-reg/sell/", "ogre")


def main():
	flats_riga.get_data()
	# flats_rigareg.get_data()


if __name__ == '__main__':
	main()
