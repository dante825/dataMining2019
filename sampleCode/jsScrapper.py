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

url = 'http://pycoders.com/archive'
# This does the magic. Loads everything
r = Render(url)
# result if a QString
result = r.frame.toHtml()

# QString should be converted to string before processed by lxml
formatted_result = str(result.encode('UTF-8'))

# Next build lxml tree from formatted result
tree = html.fromstring(formatted_result)

# Now using correct xpath we are fetching the URLs of the archive
archive_links = tree.xpath('//div[@class="mb-3"]/h2/a/@href')
print(archive_links)