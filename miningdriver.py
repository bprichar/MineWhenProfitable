#!/usr/bin/env python

import json
import urllib2
from datetime import datetime, timedelta
from selenium import webdriver
from bs4 import BeautifulSoup
import re
from time import sleep
import thread
import os
from pyvirtualdisplay import Display

TRANSMISSION_CHARGE = 0.04 # $/kWh
POWER_CONSUMPTION = 95.0 # W
HASH_RATE = 120.0 # H/s
already_mining = False
current_currency = ""
mining_thread = None

def getElectricityPrice():
    return 0.22 # $/kWh

def getMiningRewards():
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

def mine_function(currency):
    mine_command = "/usr/bin/minergate-cli -user bprvxf@gmail.com -" + currency + " 3"
    print "Going to mine", currency
    print mine_command
    os.system(mine_command)

def mine(currency):
    global current_currency
    global mining_thread
    global already_mining
    if already_mining and currency == current_currency:
        return
    elif already_mining:
        mining_thread.exit()
        mining_thread = thread.start_new_thread(mine_function, currency)
        current_currency = currency
    else:
        mining_thread = thread.start_new_thread(mine_function, (currency,))
        already_mining = True
        current_currency = currency


def stop_mining():
    global mining_thread
    global already_mining
    if already_mining:
        mining_thread.exit()
        already_mining = False

display = Display()
display.start()
logfile = open('mining_log.txt', 'w')

while True:
    try:
        electricity_price = getElectricityPrice()
        cost_rate = electricity_price * (POWER_CONSUMPTION / HASH_RATE) / 3600 # $/kH
        currency, reward_rate = getMaxReward()
        profit = reward_rate - cost_rate # $/kH

        print "Cost Rate = $", cost_rate, "/kH"
        print "Reward Rate = $", reward_rate, "/kH, mining", currency
        print "Profit = $", profit, "/kH"

        if profit > 0:
            mine(currency)
        else:
            stop_mining()

        sleep(300)
    except KeyboardInterrupt:
        stop_mining()
        logfile.close()
        exit()
    except Exception as e:
        logfile.write(str(Exception.message) + '\n')
