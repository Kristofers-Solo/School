from bs4 import BeautifulSoup
import requests

prices = []
names = []

HEADERS = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Vivaldi/4.1.2369.21'}


class IKEA:
	def __init__(self, url, name, price):
		self.url = url
		self.name = name
		self.price = price

	def get_data(self):
		prices.clear()
		url = self.url
		page = requests.get(url, headers=HEADERS)
		soup = BeautifulSoup(page.content, 'html.parser')

		for el in soup.find_all(class_=self.name):
			cropped_name = el.get_text().strip()
			names.append(cropped_name)

		for el in soup.find_all(class_=self.price):
			cropped_price = el.get_text().strip()
			prices.append(cropped_price[:cropped_price.find("€") + 1])

		combined_list = [i + " - " + j for i, j in zip(names, prices)]
		output = "\n".join(str(elem) for elem in combined_list)

		return output


curtains = IKEA('https://www.ikea.lv/lv/products/virtuve/aizkari-un-zaluzijas/aizkari', 'display-7 mr-2', 'display-6')


def main():
	print(curtains.get_data())


if __name__ == '__main__':
	main()