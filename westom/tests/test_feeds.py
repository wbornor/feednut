import sys, os, logging

sys.path.append(os.path.join(os.getcwd(), '../..'))
sys.path.append(os.getcwd())

# Set DJANGO_SETTINGS_MODULE appropriately.
os.environ['DJANGO_SETTINGS_MODULE'] = 'westom.settings'
from westom.feednut.utils.feed_utils import get_feed, store_feed, FeedDownloader, FeedIndex, FEED_FIELDS, FEED_ENTRY_FIELDS
from westom.feednut.models import *

#some test feeds
FEEDS = [
    'http://www.bloglines.com/rss/about/news', 
    'http://distrowatch.com/news/dw.xml', 
    'http://sports.espn.go.com/espn/rss/news', 
    'http://new.linuxjournal.com/node/feed', 
    'http://www.fool.com/xml/foolnews_rss091.xml', 
    'http://rss.slashdot.org/slashdot/eqWf', 
    'http://feeds.feedburner.com/spaceheadlines', 
    'http://www.wired.com/news_drop/netcenter/netcenter.rdf', 
    'http://rssfeeds.webmd.com/rss/rss.aspx?RSSSource=RSS_PUBLIC', 
    'http://rss.people.com/web/people/rss/ataol/topheadlines/index.xml', 
    'http://rss.people.com/web/people/rss/ataol/photogalleries/index.xml', 
    'http://googleblog.blogspot.com/atom.xml', 
    'http://del.icio.us/rss/', 
    'http://api.flickr.com/services/feeds/photos_public.gne?id=51934166@N00&format=rss_200', 
    'http://www.feednut.com/latest.rss', 
]

def test_fetch_feeds(feeds=FEEDS, cache=False, update=True):
    
    #this way demonstrates how to customize things
    if cache:
        mgr = FeedDownloader()
        feeds = mgr.get_feeds(feeds, use_cache=cache)

        #loop through each feedparser object, add to the database, and index it
        for url, feed in feeds.iteritems():
            db_feed = store_feed(feed, update=update)
            FeedIndex().index_feed(db_feed, feed)
        indexer.optimize()
    else:
        #this way shows the quick-n-dirty way of fetching and storing the feed
        for url in FEEDS:
            feed = get_feed(url, update=update)


def test_search_entries(query='feednut', fields=FEED_ENTRY_FIELDS):
    print 'SEARCHING FOR: "%s"' % query
    #let's do a search
    result = FeedIndex().search_entries(query, fields=fields)
    print 'FOUND %s RESULTS' % len(result)
    for i, doc in zip(range(len(result)), result):
        print 'Result %d' % i
        print '============================================='
        print 'Title:', doc.get('title', None)
        print 'Link:', doc.get('link', None)
        print 'Summary:', doc.get('summary', None)
        print '=============================================\n'

def test_search_feeds(query='feednut', fields=FEED_FIELDS):
    print 'SEARCHING FOR: "%s"' % query
    #let's do a search
    result = FeedIndex().search_feeds(query, fields=fields)
    print 'FOUND %s RESULTS' % len(result)
    for i, hit in zip(range(len(result)), result.hits):
        print 'Result %d' % i
        doc = result.doc_dict(i)
        print '============================================='
        print 'XML:', doc.get('url', None)
        print 'Title:', doc.get('title', None)
        print 'Subtitle:', doc.get('subtitle', None)
        print '=============================================\n'
    

if __name__ == '__main__':
#    FeedIndex(destroy=True)
#    test_fetch_feeds(feeds=Feed.objects.all(), cache=False, update=False)
    
    search_str = ' '.join(sys.argv[1:] or ['late*']).strip()
    print 'SEARCHING: "%s"' % search_str

    print '###################################################'
    print '###################################################'
    print 'SEARCHING FEEDS'
    print '###################################################'
    print '###################################################\n'
    test_search_feeds(search_str)
    
    print '\n\n###################################################'
    print '###################################################'
    print 'SEARCHING ENTRIES'
    print '###################################################'
    print '###################################################\n'
    test_search_entries(search_str)


#        print '\nHREF:', feed.get('href', None)
#        print 'Keys:', feed.keys()
#        print 'Version:', feed.get('version', None)
#        print 'Updated:', feed.get('updated', 'NEVER')
#        print 'Headers:', feed.get('headers', None)
#        print 'Status:', feed.get('status', None)
#        print 'Etag:', feed.get('etag', None)
#        print 'Feed Keys:', feed.get('feed', {}).keys()
#        print 'Header Keys:', feed.get('header', {}).keys()
#        print 'Entries:', len(feed.get('entries', []))
#        for entry in feed.get('entries', []):
#            print entry.keys()
#            print 'ID:', entry.get('id', None)
#            if entry.has_key('tags'):
#                print entry.get('tags', None)


        
