#!/usr/bin/env python

from selenium import webdriver
import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebPage
from bs4 import BeautifulSoup

class Render(QWebPage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()

    def _loadFinished(self, result):
        self.frame = self.mainFrame()
        self.app.quit()

url = 'https://minergate.com/calculator/cryptonote'
#r = Render(url)
#html = r.frame.toHtml()
#ascii_html = str(html.toAscii())
#soup = BeautifulSoup(ascii_html, 'html.parser')
#print soup.prettify()
#print soup.find_all("button", class_="dropdown-toggle")

driver = webdriver.Chrome('/home/brad/Downloads/chromedriver')
driver.get(url)
the_button = driver.find_elements_by_css_selector('button.btn.dropdown-toggle') # find the Currency Dropdown
the_button[1].click() # And click it
dollars = driver.find_elements_by_class_name('dropdown-menu__entry')[1] # find Dollars
dollars.click() # and click it
