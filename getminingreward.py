#!/usr/bin/env python

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
r = Render(url)
html = r.frame.toHtml()
ascii_html = str(html.toAscii())
soup = BeautifulSoup(ascii_html, 'html.parser')
print soup.prettify()
print soup.find_all("button", class_="dropdown-toggle")
