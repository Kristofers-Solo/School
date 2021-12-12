# Date - 11.12.2021
# Author - Kristiāns Francis Cagulis
# Title - Homework Selenium

import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

chromium = ["1", "chromium", "chrome"]
firefox = ["2", "firefox"]


def get_user_input():
	print("Choose which browser to use:")
	print("1 - chromium (chrome)")
	print("2 - firefox")
	browser = input("").lower()

	print("Choose from which pages you want to download files (1 4 7; 2-5; all)")
	pages = input("").lower()
	return browser, pages


def get_data():
	user_browser, user_pages = get_user_input()
	if user_browser in chromium:
		try:
			browser = webdriver.Chrome("chromedriver.exe")  # windows
		except:
			browser = webdriver.Chrome("chromedriver")  # gnu/linux
	elif user_browser in firefox:
		profile = webdriver.FirefoxProfile()
		profile.set_preference('browser.download.folderList', 2)  # custom location
		profile.set_preference('browser.download.manager.showWhenStarting', False)
		profile.set_preference('browser.download.dir', '/files')
		profile.set_preference('browser.helpApps.neverAsk.saveToDisk', 'text/csv')
		browser = webdriver.Firefox(profile)

	address = "https://www.riga.lv/lv"
	browser.get(address)
	# time.sleep(3)
	browser.find_element_by_class_name('cookie-accept-all').click()

	browser.find_element_by_class_name('search-link').click()

	delay = 0
	WebDriverWait(browser, delay).until(EC.presence_of_all_elements_located((By.ID, 'edit-search')))
	browser.find_element_by_id('edit-search').send_keys("dokum")  # writes in search line

	browser.find_element_by_id('search-header-button').click()

	browser.maximize_window()
	WebDriverWait(browser, delay).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'filter-content')))
	# delay = 3
	WebDriverWait(browser, delay).until(EC.presence_of_all_elements_located((By.ID, 'filter_type_file')))

	browser.find_element_by_css_selector('label[for="filter_type_file"]').click()

	browser.find_element_by_id('search-view-button').click()

	file = browser.find_element_by_class_name('file')


def main():
	get_data()


if __name__ == '__main__':
	main()