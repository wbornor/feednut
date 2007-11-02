import sys, os, logging

sys.path.append(os.path.join(os.getcwd(), '../..'))
sys.path.append(os.getcwd())

# Set DJANGO_SETTINGS_MODULE appropriately.
os.environ['DJANGO_SETTINGS_MODULE'] = 'westom.settings'
from westom.feednut.utils.feed_utils import FeedIndex, FEED_FIELDS, FEED_ENTRY_FIELDS

from westom.feednut.models import *
from westom.settings import DOCUMENT_ROOT
from threading import Thread
import logging

from westom.feednut.utils.lucene_utils import FeedIndexer, IndexSupport, FeedSearcher
from PyLucene import FSDirectory, IndexReader, IndexModifier, StandardAnalyzer, IndexSearcher


import unittest

class TestLucene(unittest.TestCase):
    
    
    def xtestsupport(self):
        self.store_dir = os.path.join(DOCUMENT_ROOT, '../index')
        self.support = IndexSupport(self.store_dir)
        fsdir = self.support.getIndexDirectory()
        self.assertTrue(os.path.exists(self.store_dir))
        
#        print self.support.createIndex()
        print self.support.getIndexModifier()
        print self.support.getIndexReader()
        print self.support.getIndexSearcher()
    
    
    def xtestFeedIndexer(self):
        indexer = FeedIndexer()
        indexer.index_feeds(Feed.objects.all())
#        indexer.index_feeds(Feed.objects.all()[0:5])

    def testSearchEntries(self):
        searcher = FeedSearcher()
        result = searcher.search('feednut')
        print 'FOUND %s RESULTS' % len(result)
        for i, doc in zip(range(len(result)), result):
            print 'Result %d' % i
            print '============================================='
            print 'Title:', doc.get('title', None)
            print 'Link:', doc.get('link', None)
            print 'Summary:', doc.get('summary', None)
            print '=============================================\n'
        del result
    
    def testSearchFeeds(self):
        searcher = FeedSearcher()
        result = searcher.search_feeds('late*')
        print 'FOUND %s RESULTS' % len(result)
        for i, doc in zip(range(len(result)), result):
            print 'Result %d' % i
            print '============================================='
            print 'URL:', doc.get('url', None)
            print 'Title:', doc.get('title', None)
            print 'Subtitle:', doc.get('subtitle', None)
            print '=============================================\n'
        del result
        


if __name__ == '__main__':
    unittest.main()

