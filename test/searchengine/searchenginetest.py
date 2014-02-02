import unittest
import urllib2
from BeautifulSoup import BeautifulSoup
from searchengine import searchengine
from searchengine.database import database
from mock import MagicMock
from searchengine.searchengine import crawler


class SearchEngineTestCase(unittest.TestCase):
    def test_crawler(self):
        pagelist = ['http://en.wikipedia.org/wiki/Main_Page']
        mockDb = MagicMock()
        crawler = searchengine.crawler(mockDb)
        crawler.crawl(pagelist,1)
        mockDb.dbcommit.assert_called_with()

    def test_seperateWords(self):
        mockDb = MagicMock()
        crawler = searchengine.crawler(mockDb)
        crawler_seperatewords = crawler.seperatewords("hello how aer you")
        print crawler_seperatewords







