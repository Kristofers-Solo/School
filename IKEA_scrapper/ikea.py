from bs4 import BeautifulSoup
import requests
import time

prices = []
names = []

HEADERS = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Vivaldi/4.1.2369.21'}


class IKEA:
	def __init__(self, url):
		self.url = 'https://www.ikea.lv/en/products/' + url + '?&&page=1&order=PRICEASC'

	def _get_paige_amount(self):
		page_amount = 1
		url = self.url
		page = requests.get(url, headers=HEADERS)
		soup = BeautifulSoup(page.content, 'html.parser')

		# getting page amount
		for el in soup.find_all(class_='page-link'):
			cropped_name = el.get_text().strip()
			if cropped_name.isnumeric():
				cropped_name = int(cropped_name)
				if cropped_name > page_amount:
					page_amount = cropped_name

		return page_amount

	def get_data(self):
		position = self.url.find('page=') + 5
		for i in range(1, self._get_paige_amount() + 1):
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


arm_chairs = IKEA('ikea-for-business/office/armchairs')
bathroom_furniture = IKEA('bathroom/vanity-units/bathroom-furniture')
bathroom_lighting = IKEA('bathroom/bathroom-lighting/bathroom-lighting')
bed_frames = IKEA('bedroom/beds-and-sofa-beds/bed-frames')
bookcases = IKEA('living-room/bookcases/bookcases')
boxes_and_baskets = IKEA('bedroom/sorting-solutions/boxes-and-baskets')
candles = IKEA('kitchen/kitchen-decoration/candles')
ceiling_lamps_and_spotlights = IKEA('decoration/lighting/ceiling-lamps-and-spotlights')
chairs_and_benches = IKEA('dining-room/dining-seating/chairs-and-benches')
chest_of_drawers = IKEA('bedroom/chest-of-drawers-other-furniture/chest-of-drawers')
children_storage_furniture = IKEA('children-s-room/children-3-7/children-s-storage-furniture')
curtains = IKEA('kitchen/curtains-blinds-and-fabrics/curtains')
day_beds = IKEA('bedroom/beds-and-sofa-beds/day-beds')
dining_tables = IKEA('dining-room/dining-tables/dining-tables')
dinnerware_and_serving = IKEA('kitchen/cookware-and-dinnerware/dinnerware-and-serving')
glasses = IKEA('kitchen/cookware-and-dinnerware/glasses')
home_desks = IKEA('home-office/desks/home-desks')
interior_organisers = IKEA('home-office/wardrobes/interior-organisers')
kitchen_interior_organisers = IKEA('kitchen/kitchen-interior-organisers/kitchen-interior-organisers')
light_bulbs = IKEA('bedroom/bedroom-lighting/light-bulbs')
mattresses = IKEA('bedroom/mattresses/mattresses')


def main():
	print(mattresses.get_data())


if __name__ == '__main__':
	main()