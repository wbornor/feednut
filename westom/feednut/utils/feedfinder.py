from HTMLParser import HTMLParser
from westom.feednut.libs.openanything import fetch

MOZILLA_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.4) Gecko/20060508 Firefox/1.5.0.4'

class FeedFinder(HTMLParser):
    
    def reset(self):
        self.links = []
        self.result = None #will be dict containing data, url, status
        HTMLParser.reset(self)
        
    def feed_url(self, url):
        """ feed it a URL to download data and parse """
        result = fetch(url, agent=MOZILLA_AGENT)
        self.result = result
        return self.feed(result['data'])
        
    def handle_starttag(self, tag, attrs):
        d_attrs = self._attrs_to_dict(attrs)
        if tag == 'link':
            if d_attrs.has_key('type') and d_attrs.has_key('href') and \
                (d_attrs['type'] == 'application/rss+xml' or d_attrs['type'] == 'application/atom+xml'):
                self.links.append(d_attrs['href'])
    
    def _attrs_to_dict(self, attrs):
        """ just converts the html parser's attribute array of tuples to a dict """
        d = {}
        for item in attrs:
            d[item[0]] = item[1]
        return d

if __name__ == '__main__':
    p = FeedFinder()
#    p.feed(file('tom.html').read())
    p.feed_url('http://www.msnbc.com')
    print p.links
    print p.result['status'], p.result['url']
    print p.result['data']
    
#    p.reset()
#    p.feed_url('http://www.slashdot.org')
#    print p.links
#    print p.url
    
