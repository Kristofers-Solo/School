from bs4 import BeautifulSoup
import requests

HEADERS = {
    "User-Agent":
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Vivaldi/4.1.2369.21'
}

url = "https://www.ss.com/lv/real-estate/flats/riga/all/sell/page61.html"

page = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(page.content, 'html.parser')

# print(soup.find_all(class_="navi"))

ids = [tag['id'] for tag in soup.select('tr[id]')]

ids.pop(0)
ids = [x for x in ids if "tr_bnr" not in x]

print(ids)
