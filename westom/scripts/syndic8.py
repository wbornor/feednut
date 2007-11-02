#!/usr/bin/env python
"""
Saves the Syndic8 feeds to our DB
"""

import os, sys
sys.path.append(os.path.join(os.getcwd(), '..'))
sys.path.append(os.getcwd())

# Set DJANGO_SETTINGS_MODULE appropriately.
os.environ['DJANGO_SETTINGS_MODULE'] = 'westom.settings'
from westom.feednut.models import *
sys.path.pop()
import xmlrpclib
import cPickle
from westom.feednut.utils import feed_accomplice


#FEED_KEYS = ['python', 'cnn', 'espn', 'yahoo']
FEED_KEYS = ['cnn']


def find_feeds(query):
    server = xmlrpclib.ServerProxy("http://www.syndic8.com/xmlrpc.php")
    syndic8 = server.syndic8
    ids = syndic8.FindFeeds(query)
#    fields = ['feedid', 'sitename', 'siteurl', 'dataurl', 'description']
    return syndic8.GetFeedInfo(ids)


def search_site(query):
    server = xmlrpclib.ServerProxy("http://www.syndic8.com/xmlrpc.php")
    syndic8 = server.syndic8
    ids = syndic8.FindSites(query)
    return syndic8.GetFeedInfo(ids)


if __name__ == '__main__':
    
    if len(sys.argv) > 2:
        if sys.argv[1] == 'find':
            for key in sys.argv[2:]:
                print 'Searching for %s' % key
                feeds = find_feeds(key)
                for feed in feeds:
                    newfeed = feed_accomplice.get_feed(feed['dataurl'])
                    if newfeed:
                        print 'Saved Feed!: %s' % newfeed.title

        elif sys.argv[1] == 'site':
            for key in sys.argv[2:]:
                print 'Searching for %s' % key
                feeds = search_site(key)
                for feed in feeds:
                    newfeed = feed_accomplice.get_feed(feed['dataurl'])
                    if newfeed:
                        print 'Saved Feed!: %s' % newfeed.title
                    
#        file = open(os.path.join(os.getcwd(), 'syndic8Feeds.dmp'), 'wb')
#        cPickle.dump(feeds, file)
#        file.close()
#        for feed in feeds:
#            print feed
    
    
#    server = xmlrpclib.ServerProxy("http://www.syndic8.com/xmlrpc.php")
#    syndic8 = server.syndic8
##    print syndic8.GetFeedCount()
#    fields = syndic8.GetFeedFields()
#    print fields
#    ids = syndic8.QueryFeeds('feedid', '>', '0')
#    print len(ids)
#    print ids
#    
    