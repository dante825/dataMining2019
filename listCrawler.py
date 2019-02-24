import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebKitWidgets import QWebPage
from PyQt5.QtCore import QUrl
from lxml import html, etree
import requests

# Render class renders the web page. QWebPage is the input URL of the web page to scrape
# Render object loads everything and creates a frame containing all information about the web page
class Render(QWebPage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        self.mainFrame().load(QUrl(url))
        self.app.exec()

    def _loadFinished(self, result):
        self.frame = self.mainFrame()
        self.app.quit()

url = 'https://www.thestar.com.my/business/marketwatch/stock-list/?sector=main_healthcare'
# url = 'https://www.thestar.com.my/business/marketwatch/stock-list/?sector=main_finance'
# This does the magic. Loads everything
r = Render(url)
# result is a QString
result = r.frame.toHtml()

# QString should be converted to string before processed by lxml
formatted_result = str(result.encode('UTF-8'))

# print(formatted_result)

# Next build lxml tree from formatted result
tree = html.fromstring(formatted_result)

# Now using correct xpath we are fetching the URLs of the archive
rawStocks = tree.xpath('//tbody/tr[@class="linedlist"]/td//text()')
rawStocks = rawStocks[:rawStocks.index('CAB')]
rawStocks = rawStocks[:int(len(rawStocks) / 2)]

rawLinks = tree.xpath('//tr[@class="linedlist"]/td/a/@href')

cleanStocks = []
for i in range(0, len(rawStocks)):
    if i % 8 == 0:
        cleanStocks.append(rawStocks[i])

cleanLinks = rawLinks[:len(cleanStocks)]
print(cleanStocks)
print(cleanLinks)