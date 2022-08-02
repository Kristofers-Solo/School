# Author - Kristiāns Francis Cagulis
# Date - 01.12.2021
# Title - Stundas kopdarbs
from bs4 import BeautifulSoup
import requests

url = "https://www.ikea.lv/"
all_page = requests.get(url)

if all_page.status_code == 200:
    page = BeautifulSoup(all_page.content, 'html.parser')
    found = page.find_all(class_="itemBlock")

    info = []
    item_array = []
    for item in found:
        item = item.findChild("div").findChild(class_="card-body")

        item_name = item.findChild(class_="itemName")
        item_name = item_name.findChild("div").findChild("h6")

        item_array.append(item_name.string)

        price = item.findChild(class_="itemPrice-wrapper")
        price = price.findChild("p").findChild("span")

        try:
            item_array.append(price.attrs["data-price"])
        except:
            item_array.append(price.attrs["data-pricefamily"])

        all_facts = []
        for facts in all_facts:
            if len(facts) == 1:
                all_facts.append(facts.string)
            else:
                atrasts = facts.findChildren("span")
                for i in atrasts:
                    all_facts.append(i.string)

        item_array.append(all_facts)
        info.append(item_array)
    for ieraksts in info:
        print(ieraksts)
