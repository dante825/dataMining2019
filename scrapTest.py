# This works but when in loop, the second link cannot be rendered
# import bs4 as bs
import sys
import urllib.request
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from lxml import html

APP = QApplication(sys.argv)


class Page(QWebEnginePage):
    # def __init__(self):
    #     self.web_engine = QWebEnginePage.__init__(self)

    def __init__(self, url):
        self.app = QApplication.instance()
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    # def render(self, url):
    #     self.app = QApplication.instance()
    #     self.load(QUrl(url))
    #     self.app.exec_()


    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()


def main():
    # page = Page()
    urls = ['https://www.thestar.com.my/business/marketwatch/stock-list/?sector=main_energy',
            'https://www.thestar.com.my/business/marketwatch/stock-list/?sector=main_healthcare']
    for url in urls:
        print(url)
        page = Page(url)
        # page_html = page.render(url)
        # print(page_html)
        formatted_result = str(page.html.encode('UTF-8'))
        # print(len(formatted_result))
        # print(formatted_result)
        pageTree = html.fromstring(formatted_result)
        # Now using correct xpath we are fetching the URLs of the archive
        rawStocks = pageTree.xpath('//tbody/tr[@class="linedlist"]/td//text()')
        # print(rawStocks)
        rawStocks = rawStocks[:rawStocks.index('VSTECS')]
        rawStocks = rawStocks[:int(len(rawStocks) / 2)]
        rawLinks = pageTree.xpath('//tr[@class="linedlist"]/td/a/@href')

        # logging.info('Extracted symbols and links')
        cleanStocks = []
        for i in range(0, len(rawStocks)):
            if i % 8 == 0:
                cleanStocks.append(rawStocks[i])

        cleanLinks = rawLinks[:len(cleanStocks)]
        print(cleanStocks)
        print(cleanLinks)
        print(len(cleanStocks))

        # soup = bs.BeautifulSoup(page.html, 'html.parser')
        # js_test = soup.find('p', class_='jstest')
        # print js_test.text


if __name__ == '__main__': main()