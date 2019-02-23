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
# This does the magic. Loads everything
r = Render(url)
# result if a QString
result = r.frame.toHtml()

# QString should be converted to string before processed by lxml
formatted_result = str(result.encode('UTF-8'))

# Next build lxml tree from formatted result
tree = html.fromstring(formatted_result)

# Now using correct xpath we are fetching the URLs of the archive
archive_links = tree.xpath('//tbody/tr[@class="linedlist"]/td//text()')
print(archive_links)

# ------------------------------------
# class AppCrawler:
#     def __init__(self, starting_url, depth):
#         self.starting_url = starting_url
#         self.depth = depth
#         self.apps = []
#
#     def crawl(self):
#         self.get_app_from_link(self.starting_url)
#         return
#
#     def get_app_from_link(self, link):
#         start_page = requests.get(link)
#         tree = html.fromstring(start_page.text)
#         print(start_page.text)
#
#         table = tree.xpath('//tbody/tr[@class="linedlist"]/td//text()')
#         # name = tree.xpath('//h1[@class="stock-profile f16"]/text()')[0]
#         # open = tree.xpath('//td[@id="slcontent_0_ileft_0_opentext"]/text()')[0]
#         # high = tree.xpath('//td[@id="slcontent_0_ileft_0_hightext"]/text()')[0]
#         # low = tree.xpath('//td[@id="slcontent_0_ileft_0_lowtext"]/text()')[0]
#         # close = tree.xpath('//td[@id="slcontent_0_ileft_0_lastdonetext"]/text()')[0]
#         # code = tree.xpath('//li[@class="f14"]/text()')[1]
#
#         # print(name)
#         # print(open)
#         # print(high)
#         # print(low)
#         # print(close)
#         # print(code[3:])
#         print(table)
#
#         return
#
#
# class App:
#
#     def __init__(self, shortName, link, table):
#         # self.name = name
#         # self.code = code
#         # self.open = open
#         # self.high = high
#         # self.low = low
#         # self.close = close
#         # self.links = links
#         self.table = table
#
#     def __str__(self):
#         # return ("tbody: " + self.root.encode('UTF-8') + "\r\n")
#         return table
#         # return ("Name: " + self.name.encode('UTF-8') +
#         #         "\r\nCode: " + self.developer.encode('UTF-8') +
#         #         "\r\nOpen: " + self.open.encode('UTF-8') +
#         #         "\r\nHigh: " + self.high.encode('UTF-8') +
#         #         "\r\nLow: " + self.low.encode('UTF-8') +
#         #         "\r\nClose: " + self.close.encode('UTF-8') + "\r\n")
#
#
# crawler = AppCrawler("https://www.thestar.com.my/business/marketwatch/stock-list/?sector=main_healthcare", 0)
#
# crawler.crawl()
#
# for app in crawler.apps:
#     print(app)