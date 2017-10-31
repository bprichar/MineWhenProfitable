#!/usr/bin/env python

from selenium import webdriver
from bs4 import BeautifulSoup
import re
from time import sleep

url = 'https://minergate.com/calculator/cryptonote'

driver = webdriver.Chrome('/home/brad/Downloads/chromedriver')
#driver = webdriver.PhantomJS()
driver.get(url)
speed_menu = driver.find_elements_by_class_name('intervals-dropdown')[0] # find the Speed Dropdown
options = speed_menu.find_elements_by_tag_name('option')
options[1].click() # And click on kH/s
rates_menu = driver.find_elements_by_class_name('rates')[0] # find the currency dropdown
currencies = rates_menu.find_elements_by_tag_name('option')
currencies[1].click() # and click on USD
sleep(10)

the_page = driver.page_source
soup = BeautifulSoup(the_page, 'html.parser')
titles = soup.find_all("th", class_="currency-title")
symbols = []
for title in titles:
    symbol = title.find_all("span", class_="muted")[0].get_text().encode('ascii').lower()
    symbols.append(symbol)

conversion_row = soup.find_all("tr", class_="conversion-row")[0]
rate_list = conversion_row.find_all(string=re.compile("[0-9]"))

rewards = {}
for i in xrange(len(symbols)):
    rewards[symbols[i]] = rate_list[i]

print rewards

driver.close()
