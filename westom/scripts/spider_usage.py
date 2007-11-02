import sys
from string import join, strip

from time import sleep


import os, sys
import md5
import urllib2
import logging
sys.path.append(os.path.join(os.getcwd(), '..'))
sys.path.append(os.getcwd())

# Set DJANGO_SETTINGS_MODULE appropriately.
os.environ['DJANGO_SETTINGS_MODULE'] = 'westom.settings'

sys.path.pop()


from westom.feednut.utils import search, feed_accomplice
from westom.feednut.libs.spider import Spider
inc = 0

class myspider(Spider):
    global inc
    def handle(self,  html, urllist):
    	try:
    	    logging.debug('increment: %s, url: %s, length of html: %s' % (inc, self.url, len(html)))
            feeds = search.scrape_for_feeds(self.url)
            logging.debug('feeds: %s' % (feeds))

            for feed in feeds:            
                logging.debug('added/updated feed: %s' % (feed_accomplice.get_feed(str(feed))))

    	except Exception, e:
            raise e
            
	return urllist

    def _webparser(self, html):
	   return Spider._webparser(self, html)

    def _webopen(self, base):
    	global inc
    	t = self
        sleep(2)
    	self.url = base[0]
    	inc = inc + 1
    	return	Spider._webopen(self, base)

if __name__ == '__main__':
    if len(sys.argv) > 1:
       url = sys.argv[1]
       s = myspider().weburls( base=url, width=10000, depth=10 )
       print s
    
    else:
       print "you need to call this with a url like this, >>python mycrawler.py http://www.othermedia.com"