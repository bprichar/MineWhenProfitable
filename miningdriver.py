#!/usr/bin/env python

import json
import urllib2
from datetime import datetime, timedelta
from selenium import webdriver
from bs4 import BeautifulSoup
import re
from time import sleep

TRANSMISSION_CHARGE = 0.04 # $/kWh
POWER_CONSUMPTION = 95.0 # W
HASH_RATE = 120.0 # H/s

def getElectricityPrice():
    baseaddress = 'https://rrtp.comed.com/api?type=5minutefeed&datestart='
    starttime = datetime.strftime(datetime.now() - timedelta(minutes=10), '%Y%m%d%H%M')
    endtime = datetime.strftime(datetime.now(), '%Y%m%d%H%M')
    address = baseaddress + starttime + '&dateend=' + endtime
    return float(json.loads(urllib2.urlopen(address).read())[-1]['price']) / 100 + TRANSMISSION_CHARGE # $/kWh

def getMiningRewards():
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
        rewards[symbols[i]] = float(rate_list[i]) / (60 * 60) # $/kH

    driver.close()

    return rewards

def getMaxReward():
    rewards = getMiningRewards()
    max_currency = ''
    max_rate = 0.0
    for currency in rewards.keys():
        if rewards[currency] > max_rate:
            max_currency = currency
            max_rate = rewards[currency]
    return max_currency, max_rate

electricity_price = getElectricityPrice()
cost_rate = electricity_price * (POWER_CONSUMPTION / HASH_RATE) / 3600 # $/kH
currency, reward_rate = getMaxReward()
profit = reward_rate - cost_rate # $/kH

print "Cost Rate = $", cost_rate, "/kH"
print "Reward Rate = $", reward_rate, "/kH, mining", currency
print "Profit = $", profit, "/kH"
