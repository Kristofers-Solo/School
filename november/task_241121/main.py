from bs4 import BeautifulSoup
import requests

url = "https://en.wikipedia.org/wiki/Husky"
all_page = requests.get(url)

# print(all_page)

if all_page.status_code == 200:
    print(":)")
    page = BeautifulSoup(all_page.content, 'html.parser')
    found = page.find(id="Etymology")
    # print(found)
    # print(found.constents)
    # print(found.string)
    found = page.find_all(class_="mw-headline")
    # print(found)
    found = page.find_all("li", class_="interlanguage-link")
    # print(found)
    found = page.find_all("a", class_="interlanguage-link-target")
    # print(found)
    for i in found:
        # 	print(i.prettify())
        if i.attrs["lang"] == "ru":
            print(
                f"{i.attrs['lang']} \t {i.attrs['title']} \n {i.attrs['href']}")
else:
    print(":(")
