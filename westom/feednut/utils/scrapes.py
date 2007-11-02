import urllib, re
from westom.feednut.libs import syndic8
from westom.feednut.utils import feed_accomplice

URL_TECHNORATI = 'http://www.technorati.com/pop/blogs/?faves=1'

def scrape_technorati_top100():
    """ Returns a list of URLs representing the top 100 blogs """
    lines = urllib.urlopen(URL_TECHNORATI).read().split('\n')
    urls = []
    for line in lines:
        if re.match(r'.*h2><a href.*', line):
            line = line.strip()
            in1 = line.find('http')
            in2 = line.find('"', in1)
            urls.append(line[in1:in2])
    return urls


def load_technorati_top100():
    urls = scrape_technorati_top100()
    sites = []
    for url in urls:
        ids = syndic8.findsites('%s' % url)
        sites += syndic8.getfeedinfo(ids, ['dataurl'])
        
    for site in sites:
        print site['dataurl']
        newfeed = feed_accomplice.get_feed(site['dataurl'])
        if newfeed:
            print 'Saved Feed!: %s' % newfeed.title
    
        
        
            