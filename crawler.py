from lxml import html
import requests


class AppCrawler:
    def __init__(self, depth):
        # self.starting_url = starting_url
        self.depth = depth
        self.apps = []

    def crawl(self, url_param):
        return self.get_app_from_link(url_param)

    def get_app_from_link(self, link):
        start_page = requests.get(link)
        tree = html.fromstring(start_page.text)

        date = tree.xpath('//*[@id="slcontent_0_ileft_0_datetxt"]/text()')[0]
        name = tree.xpath('//h1[@class="stock-profile f16"]/text()')[0]
        open_price = tree.xpath('//td[@id="slcontent_0_ileft_0_opentext"]/text()')[0]
        high = tree.xpath('//td[@id="slcontent_0_ileft_0_hightext"]/text()')[0]
        low = tree.xpath('//td[@id="slcontent_0_ileft_0_lowtext"]/text()')[0]
        close = tree.xpath('//td[@id="slcontent_0_ileft_0_lastdonetext"]/text()')[0]
        code = tree.xpath('//li[@class="f14"]/text()')[1]
        vol = tree.xpath('//*[@id="slcontent_0_ileft_0_voltext"]/text()')[0]
        buy_vol = tree.xpath('//*[@id="slcontent_0_ileft_0_buyvol"]/text()')[0]
        sell_vol = tree.xpath('//*[@id="slcontent_0_ileft_0_sellvol"]/text()')[0]

        stock = Stock(date[10: -2], name, code[3:], open_price, high, low, close, vol, buy_vol, sell_vol)
        return stock


class Stock:
    def __init__(self, date, name, code, open, high, low, close, vol, buy_vol, sell_vol):
        self.date = date
        self.name = name
        self.code = code
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.vol = vol
        self.buy_vol = buy_vol
        self.sell_vol = sell_vol

    def __str__(self):
        return "Stock: " + str(self.name) + "\n" + "Stock Code: " + str(self.code) + "\n" + "Open: " + \
               str(self.open) + "\n" + "High: " + str(self.high) + "\n" + "Low: " + str(self.low) + "\n" + \
               "Close: " + str(self.close) + "\n" + "Volume: " + str(self.vol) + "\n" + "Buy vol: " + \
               str(self.buy_vol) + "\n" + "Sell vol: " + str(self.sell_vol) + "\n" + "Date: " + str(self.date) + "\n"


urls = ['https://www.thestar.com.my/business/marketwatch/stocks/?qcounter=ALAM',
        'https://www.thestar.com.my/Business/Marketwatch/Stocks?qcounter=RSENA',
        'https://www.thestar.com.my/Business/Marketwatch/Stocks?qcounter=CLIQ']

crawler = AppCrawler(0)
for url in urls:
    s = crawler.crawl(url)
    print(s.__str__())
