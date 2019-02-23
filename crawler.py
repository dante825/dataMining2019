# import numpy as np
from lxml import html
import requests

class AppCrawler:
    def __init__(self, starting_url, depth):
        self.starting_url = starting_url
        self.depth = depth
        self.apps = []

    def crawl(self):
        self.get_app_from_link(self.starting_url)
        return

    def get_app_from_link(self, link):
        start_page = requests.get(link)
        tree = html.fromstring(start_page.text)

        name = tree.xpath('//h1[@class="stock-profile f16"]/text()')[0]
        open = tree.xpath('//td[@id="slcontent_0_ileft_0_opentext"]/text()')[0]
        high = tree.xpath('//td[@id="slcontent_0_ileft_0_hightext"]/text()')[0]
        low = tree.xpath('//td[@id="slcontent_0_ileft_0_lowtext"]/text()')[0]
        close = tree.xpath('//td[@id="slcontent_0_ileft_0_lastdonetext"]/text()')[0]
        code = tree.xpath('//li[@class="f14"]/text()')[1]

        print(name)
        print(open)
        print(high)
        print(low)
        print(close)
        print(code[3:])

        return

class App:

    def __init__(self, name, code, open, high, low, close, links):
        self.name = name
        self.code = code
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.links = links

    def __str__(self):
        return ("Name: " + self.name.encode('UTF-8') +
        "\r\nCode: " + self.developer.encode('UTF-8') +
        "\r\nOpen: " + self.open.encode('UTF-8') +
        "\r\nHigh: " + self.high.encode('UTF-8') +
        "\r\nLow: " + self.low.encode('UTF-8') +
        "\r\nClose: " + self.close.encode('UTF-8') + "\r\n")

crawler = AppCrawler("https://www.thestar.com.my/business/marketwatch/stocks/?qcounter=SAPNRG", 0)

crawler.crawl()

for app in crawler.apps:
    print(app)

# print('text' + '\n' + 'one')