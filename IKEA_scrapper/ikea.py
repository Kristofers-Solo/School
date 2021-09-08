from bs4 import BeautifulSoup
import requests
import time

prices = []
names = []

HEADERS = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Vivaldi/4.1.2369.21'}


class IKEA:
	def __init__(self, url, pages):
		self.url = url
		self.pages = pages

	def get_data(self):
		position = self.url.find('page=') + 5
		for i in range(1, self.pages + 1):
			time.sleep(2)
			url = self.url[:position] + str(i) + self.url[position + 1:]

			page = requests.get(url, headers=HEADERS)
			soup = BeautifulSoup(page.content, 'html.parser')

			# getting product name
			for el in soup.find_all(class_='display-7 mr-2'):
				cropped_name = el.get_text().strip()
				names.append(cropped_name)

			# getting product price
			for el in soup.find_all(class_='display-6'):
				cropped_price = el.get_text().strip()
				prices.append(cropped_price[:cropped_price.find("€") + 1])

		combined_list = [i + " - " + j for i, j in zip(names, prices)]
		output = "\n".join(str(elem) for elem in combined_list)

		return output


curtains = IKEA('https://www.ikea.lv/lv/products/virtuve/aizkari-un-zaluzijas/aizkari?&&page=1&order=PRICEASC', 3)
chairs = IKEA('https://www.ikea.lv/lv/products/ikea-uznemumiem/birojam/atputas-kresli?&&page=1&order=PRICEASC', 5)