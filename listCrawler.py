import sys
from PySide import QtCore, QtGui, QtWebKit
from lxml import html, etree
from DbOperations import *
import logging

# Setup the log level
logging.basicConfig(level = logging.DEBUG)

# The first of the dividend on the side table on the website, a point to subset the stocks
STOP_POINT = 'VSTECS'

# Hardcoded sector and links
SECTOR_LINK = {'Energy': 'https://www.thestar.com.my/business/marketwatch/stock-list/?sector=main_energy',}
               # 'Health care': 'https://www.thestar.com.my/business/marketwatch/stock-list/?sector=main_healthcare',
               # 'Technology': 'https://www.thestar.com.my/business/marketwatch/stock-list/?sector=main_technology',
               # 'Property': 'https://www.thestar.com.my/business/marketwatch/stock-list/?sector=main_property',
               # 'Utilities': 'https://www.thestar.com.my/business/marketwatch/stock-list/?sector=main_utilities',
               # 'Finance services': 'https://www.thestar.com.my/business/marketwatch/stock-list/?sector=main_finance',
               # 'Telecommunication and media': 'https://www.thestar.com.my/business/marketwatch/stock-list/?sector=main_telcomedia',
               # 'Consumer product and services': 'https://www.thestar.com.my/business/marketwatch/stock-list/?sector=main_consumer',
               # 'Construction': 'https://www.thestar.com.my/business/marketwatch/stock-list/?sector=main_construction',
               # 'Real Estate Investment Trust': 'https://www.thestar.com.my/business/marketwatch/stock-list/?sector=main_reits',
               # 'Industrial product and services': 'https://www.thestar.com.my/business/marketwatch/stock-list/?sector=main_indprod',
               # 'Plantation': 'https://www.thestar.com.my/business/marketwatch/stock-list/?sector=main_plantation',
               # 'Transportation and logistics': 'https://www.thestar.com.my/business/marketwatch/stock-list/?sector=main_transport',
               # 'Special purpose acquisition company': 'https://www.thestar.com.my/business/marketwatch/stock-list/?sector=main_specialpurposeact',
               # 'Closed end fund': 'https://www.thestar.com.my/business/marketwatch/stock-list/?sector=main_closedfund'}

PREFIX_URL = 'https://www.thestar.com.my'


# The MAGIC!
def load_page(page_url):
    page = QtWebKit.QWebPage()
    loop = QtCore.QEventLoop() # Create event loop
    page.mainFrame().loadFinished.connect(loop.quit) # Connect loadFinished to loop quit
    page.mainFrame().load(page_url)
    loop.exec_() # Run event loop, it will end on loadFinished
    return page.mainFrame().toHtml()


app = QtGui.QApplication(sys.argv)

# Render class renders the web page. QWebPage is the input URL of the web page to scrape
# Render object loads everything and creates a frame containing all information about the web page
# class Render(QWebPage):
#     def __init__(self, url):
#         self.app = QApplication(sys.argv)
#         QWebPage.__init__(self)
#         self.loadFinished.connect(self._loadFinished)
#         self.mainFrame().load(QUrl(url))
#         self.app.exec()
#
#     def _loadFinished(self, result):
#         self.frame = self.mainFrame()
#         self.app.quit()


def cleanStocks(stocksList):
    """
    Subset the extracted list into the list of stocks
    :param stocksList: extracted list of stocks
    :return: a clean list of stocks
    """
    logging.info('Cleansing the stocks')
    cleanStocks = []
    for i in range(0, len(stocksList)):
        if i % 8 == 0:
            cleanStocks.append(stocksList[i])

    return cleanStocks

def cleanLinks(linksList, length):
    """
    Clean or subset the extracted list of links into the needed list of links
    :param linksList: the extracted list of links
    :param length: the length of the clean stock list
    :return: a clean list of links
    """
    logging.info('Cleansing the links')
    cleanLinks = linksList[:length]
    return cleanLinks


def main():
    # stocks_list = []
    # stocks_link = []
    # stocks_sector = []

    # Loop the dictionary to crawl the list of stocks
    for sector, url in SECTOR_LINK.items():
        logging.info('Extracting %s with %s', sector, url)
        # This does the magic. Loads everything
        # r = Render(url)
        result = load_page(url)
        # result is a QString
        # result = r.frame.toHtml()
        # QString should be converted to string before processed by lxml
        formatted_result = str(result.encode('UTF-8'))
        # Next build lxml tree from formatted result
        tree = html.fromstring(formatted_result)

        # Now using correct xpath we are fetching the URLs of the archive
        rawStocks = tree.xpath('//tbody/tr[@class="linedlist"]/td//text()')
        rawStocks = rawStocks[:rawStocks.index(STOP_POINT)]
        rawStocks = rawStocks[:int(len(rawStocks) / 2)]
        rawLinks = tree.xpath('//tr[@class="linedlist"]/td/a/@href')

        stocks_list = cleanStocks(rawStocks)
        stocks_link = cleanLinks(rawLinks, len(stocks_list))

        logging.info('Inserting into Database table')
        db_op = DbOperations()
        for sym, page_link in zip(stocks_list, stocks_link):
            db_op.insert_symlink(sym, PREFIX_URL + page_link, sector)
        db_op.close_conn()


if __name__ == '__main__':
    main()
