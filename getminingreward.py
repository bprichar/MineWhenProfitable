#!/usr/bin/env python

from selenium import webdriver
from bs4 import BeautifulSoup
import re
from time import sleep

url = 'https://minergate.com/calculator/cryptonote'

driver = webdriver.Chrome('/home/brad/Downloads/chromedriver')
#driver = webdriver.PhantomJS()
driver.get(url)
the_button = driver.find_elements_by_css_selector('button.btn.dropdown-toggle') # find the Currency Dropdown
the_button[1].click() # And click it
dollars = driver.find_elements_by_class_name('dropdown-menu__entry')[1] # find Dollars
dollars.click() # and click it
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
