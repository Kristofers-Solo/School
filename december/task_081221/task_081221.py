# Date - 08.12.2021
# Author - Kristiāns Francis Cagulis
# Title - Class work 081221 Selenium

import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

firefox = True

if firefox:
	browser = webdriver.Firefox()
else:
	browser = webdriver.Chrome("chromedriver")

address = "https://www.riga.lv/lv"
browser.get(address)
time.sleep(3)
agreement = browser.find_element_by_class_name('cookie-accept-all')
agreement.click()

search = browser.find_element_by_class_name('search-link')
search.click()

delay = 2
WebDriverWait(browser, delay).until(EC.presence_of_all_elements_located((By.ID, 'edit-search')))
search = browser.find_element_by_id('edit-search')
search.send_keys("dokum")  # writes in search line

search = browser.find_element_by_id('search-header-button')
search.click()

browser.maximize_window()
WebDriverWait(browser, delay).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'filter-content')))
delay = 3
WebDriverWait(browser, delay).until(EC.presence_of_all_elements_located((By.ID, 'filter_type_content')))

filter = browser.find_element_by_css_selector("label[for='filter_type_file']")
filter.click()

search = browser.find_element_by_id('search-view-button')
search.click()