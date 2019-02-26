
from PySide import QtCore, QtGui, QtWebKit
from lxml import html
import sys


def load_page(url):
    page = QtWebKit.QWebPage()
    loop = QtCore.QEventLoop() # Create event loop
    page.mainFrame().loadFinished.connect(loop.quit) # Connect loadFinished to loop quit
    page.mainFrame().load(url)
    loop.exec_() # Run event loop, it will end on loadFinished
    return page.mainFrame().toHtml()


app = QtGui.QApplication(sys.argv)

urls = ['https://www.thestar.com.my/business/marketwatch/stock-list/?sector=main_healthcare',
        'https://www.thestar.com.my/business/marketwatch/stock-list/?sector=main_energy']
for url in urls:
    print('Loading ' + url)
    result = load_page(url)
    formatted_result = str(result.encode('UTF-8'))
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

app.exit()
