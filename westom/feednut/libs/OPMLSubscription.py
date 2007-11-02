from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from xml.sax import handler
from westom.feednut.utils.misc import storage 
import xml.parsers.expat

class SubscriptionHandler(handler.ContentHandler):
    """
    SubscriptionHandler creates a list of subscriptions from an OPML file
    Subscriptions are represented by a Storage object containing subscription attributes
    
    OPML subscriptions are a xml list of outline elements wrapped 
    in an catagory outline element.
    
    Here is an example from bloglines:
        <outline title="Subscriptions">
            <outline title="Bloglines | News" htmlUrl="http://www.bloglines.com" type="rss" xmlUrl="http://www.bloglines.com/rss/about/news" />
            <outline title="Fodor's Travel Wire" htmlUrl="http://www.fodors.com/wire/" type="rss" xmlUrl="http://www.fodors.com/blog/index.rdf" />
            <outline title="NASA Breaking News" htmlUrl="http://www.nasa.gov/audience/formedia/features/index.html" type="rss" xmlUrl="http://www.nasa.gov/rss/breaking_news.rss" />
            <outline title="Nature" htmlUrl="http://www.nature.com/nature/current_issue/" type="rss" xmlUrl="http://www.nature.com/nature/journal/v428/n6985/rss.rdf" />
            <outline title="Slashdot" htmlUrl="http://slashdot.org/" type="rss" xmlUrl="http://rss.slashdot.org/slashdot/eqWf" />
            <outline title="SPACE.com" htmlUrl="http://www.space.com/" type="rss" xmlUrl="http://feeds.feedburner.com/spaceheadlines" />
        </outline>    
    """
            
    def __init__(self):
        self.subscriptions = []
        self.inSubscriptionRootOutline = False
        self.inSubscriptionChildOutline = False
        self.valid_subscription_text = ['subscription', 'subscriptions']
        
    def getSubscriptions(self):
        return self.subscriptions
    
    def startElement(self, name, attrs):
        if (name and name.lower() == 'outline'): 
            text = attrs.get('text', None)
            title = attrs.get('title', None)
                        
            if (text and text.lower() in self.valid_subscription_text) or (title and title.lower() in self.valid_subscription_text):
                 self.inSubscriptionRootOutline = True
                 return
 
            if self.inSubscriptionRootOutline:
                #if you are here, you must be in a child outline element 
                #under a subscription outline element 
                self.inSubscriptionChildOutline = True
                type = attrs.get('type', None)
                xmlUrl = attrs.get('xmlUrl', None)
                self.subscriptions.append(storage({'text':text, 'title':title, 'type':type, 'xmlUrl':xmlUrl}))
    
    def endElement(self, name):
        if (name and name.lower() == 'outline') and self.inSubscriptionRootOutline:
            if self.inSubscriptionChildOutline:
                self.inSubscriptionChildOutline = False
            else:
                self.inSubscriptionRootOutline = False
                
            
        
def parseOpml(opml):
    """
    Parse some OPML and return its Subscriptions in a list of Storage objects
    """
    parser = make_parser()
    parser.setFeature(feature_namespaces, 0)
    dh = SubscriptionHandler()
    parser.setContentHandler(dh)
    parser.parse(opml)
    
    return dh.getSubscriptions()