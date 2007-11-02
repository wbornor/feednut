from westom.feednut.libs.ScrapeNFeed import ScrapedFeed
from westom.feednut.libs.PyRSS2Gen import RSSItem, Guid

class SimpleFeed(ScrapedFeed):
    def __init__(self, title, url, description, rssItems, 
                 rssFile=None, pickleFile=None, maxItems=20, **kwargs):
        ScrapedFeed.__init__(self, 
                             title, 
                             url, 
                             description, 
                             rssFile, 
                             pickleFile, 
                             maxItems=maxItems, 
                             generator = None, 
                             docs = None, 
                             **kwargs)
        self.rssItems = rssItems
    
    def HTML2RSS(self, headers, body):
        self.addRSSItems(self.rssItems)
        
    def refresh(self):
        ''' override the parent implementation '''
        self.HTML2RSS(None, None)
        #if self.rssFile:
        #    self.writeRSS()
        #if self.pickleFile:
        #    self.pickle()        
        


def main():
    from westom.feednut.utils.HtmlDom import HtmlDom, toHTML
    import sys
    
    #another example... python job board
    job_board = 'http://www.python.org/community/jobs/'
    dom = HtmlDom(job_board)
    rssItems = []
    title = dom.evaluate("/html:html/html:head/html:title/text()")[0].nodeValue
    description = 'Feed generated for %s by FeedNut' % job_board
    job_ops = dom.evaluate("//html:div[@class='section'][@id][position()>2]")
    for i, job_op in zip(range(len(job_ops)), job_ops):
        try: itemTitle = dom.evaluate("html:h2/html:a[@class='reference']/text()", node=job_op)[0].nodeValue
        except: continue
        try: link = dom.evaluate("html:h2/html:a[@class='reference']/@href", node=job_op)[0].nodeValue
        except: link = None
        try: itemDesc = toHTML(job_op).replace('html:', '')
        except: itemDesc = None
        
        item = RSSItem(title=itemTitle, description=itemDesc, link=link, guid=Guid(link and ('%s#%s' % (link, i)) or itemTitle))
        rssItems.append(item)
    feed = SimpleFeed(title, job_board, description, rssItems)
    feed.refresh()
    print feed.to_xml()
    
    
    #one example... top40 dance hits
    top40 = 'http://www.bbc.co.uk/radio1/chart/top40.shtml'
    dom = HtmlDom(top40)
    rssItems = []
    title = dom.evaluate("/html:html/html:head/html:title/text()")[0].nodeValue
    description = 'Feed generated for %s by FeedNut' % top40
    songs = dom.evaluate("//html:td[@class='col4']")
    for song in songs:
        try: artist = dom.evaluate("html:h4/text()", node=song)[0].nodeValue
        except: continue
        try: track = dom.evaluate("html:h5/text()", node=song)[0].nodeValue
        except: continue
        try: link = dom.evaluate("html:a/@href", node=song)[0].nodeValue
        except: link = None
        try: img = dom.evaluate("html:img/@src", node=song)[0].nodeValue
        except: img = None
        
        itemTitle = '%s - %s' % (artist, track)
        itemDesc = '<p>%s</p>%s' % (itemTitle, img and ('<img src="%s"/>' % img) or '')
        item = RSSItem(title=itemTitle, description=itemDesc, link=link, guid=Guid(link or itemTitle))
        rssItems.append(item)
    feed = SimpleFeed(title, top40, description, rssItems)
    feed.refresh()
    print feed.to_xml()
    
    
    
if __name__ == '__main__':
    main()
    
    
    

