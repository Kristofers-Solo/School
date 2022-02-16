# Author - Kristiāns Francis Cagulis
# Date - 16.02.2022.
# Title - Patstāvīgais darbs - pandas

from pathlib import Path as p
from ss_scraper import SS

# flats_few = SS("https://www.ss.com/lv/real-estate/flats/riga-region/all/sell/")
# flats_few.get_data()


def read():
	pass


def address():
	pass


print(list(p(p(__file__).parent.absolute()).glob("*/*.xlsx")))