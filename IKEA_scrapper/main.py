from bs4 import BeautifulSoup
import requests

prices = []
names = []

HEADERS = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 OPR/77.0.4054.275'}


class IKEA:
	def __init__(self, url, price, name):
		self.url = url
		self.price = price
		self.name = name

	def function(self):
		prices.clear()
		url = self.url
		page = requests.get(url, headers=HEADERS)
		soup = BeautifulSoup(page.content, 'html.parser')

		for el in soup.find_all(class_=self.price):
			cropped_price = el.get_text().strip()  # strip necessary info
			prices.append(cropped_price)

		for el in soup.find_all(class_=self.name):
			cropped_name = el.get_text().strip()
			names.append(cropped_name)
		# converted_price = list(map(convertor, prices))  # converts . to ,
		# adds € at the end of each element
		# new_prices = map((lambda x: x + "€"), converted_price)

		# converts list to string
		# output = f"{self.name}\n" + "\n".join(str(elem) for elem in new_prices)
		output = names
		return output


aizskari = IKEA('https://www.ikea.lv/lv/products/virtuve/aizkari-un-zaluzijas/aizkari', 'itemBTI display-6', 'display-7 mr-2')


def main():
	print(aizskari.function())


if __name__ == '__main__':
	main()