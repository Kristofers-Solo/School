# Date - 14.12.2021
# Author - Kristiāns Francis Cagulis
# Title - Homework Selenium

import os
from os.path import exists
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

debug = False

chromium = ["1", "chromium", "chrome"]
firefox = ["2", "firefox"]


def get_data():
	user_browser, user_pages, search_word = get_user_input()

	for page in user_pages:
		if user_browser in chromium:
			if os.name in ('nt', 'dos'):
				browser = webdriver.Chrome("chromedriver.exe")  # windows
			else:
				browser = webdriver.Chrome("chromedriver")  # gnu/linux
		elif user_browser in firefox:
			browser = webdriver.Firefox()

		url = f"https://www.riga.lv/lv/search?q={search_word}&types=file&page={page - 1}"
		browser.get(url)
		browser.find_element(By.CLASS_NAME, 'cookie-accept-all').click()

		files = browser.find_elements(By.CLASS_NAME, 'file')
		for file in files:
			file_name = file.text
			file_url = file.get_attribute('href')
			file_download(file_name, file_url)
		browser.quit()


def get_user_input():
	if debug == True:
		search_word = "dokum"
	else:
		search_word = input("Choose keyword to search: ")

	last_page = get_max_page_amount(search_word)
	print("\nChoose which browser to use:")
	print("1 - chromium (chrome)")
	print("2 - firefox")

	if debug == True:
		browser = "firefox"
	else:
		browser = input("").lower()

	print(f"\nChoose from which pages you want to download files (1 4 7; 2-5; all). Maximum is {last_page} pages.")
	try:
		if debug == True:
			user_input = "1"
		else:
			user_input = input("").lower()

		if user_input == "all":
			pages = list(map(int, range(1, last_page + 1)))  # creates list with all pages
		else:
			user_page_list = user_input.split(" ")
			for page_range in user_page_list:
				if "-" in page_range:

					first_num = int(page_range[:page_range.find("-")])  # gets first number
					second_num = int(page_range[page_range.find("-") + 1:]) + 1  # gets second number

					if second_num > last_page:  # reduces user input to max page amount
						second_num = last_page

					user_page_list = user_page_list + list(map(str, range(first_num, second_num)))  # creates list with str range
			pages = [elem for elem in user_page_list if not "-" in elem]  # removes all elements containing "-"
			pages = list(map(int, pages))  # convers str to int
			pages.sort()  # sorts list
			pages = list(set(pages))  # removes duplicates from list
	except:
		print("Enered incorrect number/s. Try again.")
	return browser, pages, search_word


def get_max_page_amount(keyword: str):
	url = f"https://www.riga.lv/lv/search?q={keyword}&types=file"
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	try:
		last_page = soup.find(class_='pager__item--last').get_text().strip()
	except:
		try:
			last_page = soup.find_all(class_='pager__item page-item')
			last_page = last_page[-1].get_text().strip()[-1]  # gets last number from navigation bar
		except:
			print("Something went wrong. Please try again or try another keyword.")
	return int(last_page)


def file_download(file_name, file_url):
	print(f"\nNAME: {file_name}")
	print(f"URL: {file_url}")

	path = "files"
	if not exists(path):
		os.mkdir(path)

	response = requests.get(file_url)
	if ".pdf" in file_name:
		open(f"{path}/{file_name}", "wb").write(response.content)
	else:
		open(f"{path}/{file_name}.pdf", "wb").write(response.content)


def main():
	get_data()


if __name__ == '__main__':
	main()