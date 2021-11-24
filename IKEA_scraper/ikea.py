from bs4 import BeautifulSoup
import requests

HEADERS = {
    "User-Agent":
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Vivaldi/4.1.2369.21'
}


class IKEA:
	def __init__(self, url):
		self.url = 'https://www.ikea.lv/en/products/' + url + '?&&page=1&order=PRICEASC'

	def _get_paige_amount(self):
		page_amount = 1
		page = requests.get(self.url, headers=HEADERS)
		soup = BeautifulSoup(page.content, 'html.parser')

		# getting max page amount
		for el in soup.find_all(class_='page-link'):
			cropped_name = el.get_text().strip()
			if cropped_name.isnumeric():
				cropped_name = int(cropped_name)
				if cropped_name > page_amount:
					page_amount = cropped_name

		return page_amount

	def get_data(self):
		prices = []
		names = []
		prices.clear()
		names.clear()
		# combined_list.clear()
		position = self.url.find('page=') + 5
		for i in range(1, self._get_paige_amount() + 1):
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
		if __name__ == '__main__':
			SEPARATOR = "\n"
		else:
			SEPARATOR = "<br>"

		output = SEPARATOR.join(str(elem) for elem in combined_list)
		print(len(names))
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
mirrors = IKEA('kitchen/kitchen-decoration/mirrors')
office_chairs = IKEA('home-office/work-seating-range/office-chairs')
office_desks_and_tables = IKEA('home-office/desks/office-desks-and-tables')
open_shelving_units = IKEA('living-room/shelving-units-systems/open-shelving-units')
pax_wardrobes = IKEA('ikea-for-business/retail/system-wardrobes')
pendant_lamps = IKEA('ikea-for-business/retail/pendant-lamps')
pillows = IKEA('bedroom/bedding/pillows')
pots = IKEA('kitchen/cookware-and-dinnerware/pots')
quilt_covers_and_pillow_cases = IKEA('bedroom/bedding/quilt-covers-and-pillow-cases')
quilts = IKEA('bedroom/bedding/quilts')
rugs = IKEA('living-room/home-furnishing-rugs/rugs')
sheets_and_pillow_cases = IKEA('bedroom/bedding/sheets-and-pillow-cases')
sofa_beds_and_chair_beds = IKEA('living-room/sofa-armchairs/sofas')
sofa_tables = IKEA('living-room/coffee-side-tables/sofa-tables')
solitaire_cabinets = IKEA('living-room/solitaire-cabinets/solitaire-cabinets')
solitaire_wardrobes = IKEA('bedroom/wardrobes/solitaire-wardrobes')
system_cabinets = IKEA('living-room/solitaire-cabinets/system-cabinets')
table_lamps = IKEA('bedroom/bedroom-lighting/table-lamps')
towels = IKEA('bathroom/towels/towels')
toys_for_small_children = IKEA('children-s-room/children-3-7/toys-for-small-children')
tv_benches = IKEA('living-room/tv-stands-media-units/tv-benches')


def main():
	# import cProfile
	# import pstats
	# with cProfile.Profile() as pr:
	# 	tv_benches.get_data()

	# stats = pstats.Stats(pr)
	# stats.sort_stats(pstats.SortKey.TIME)
	# # stats.print_stats()
	# stats.dump_stats(filename='stats.prof')
	print(tv_benches.get_data())


if __name__ == '__main__':
	main()