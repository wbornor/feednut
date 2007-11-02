# PyBloglines $Id: pybloglines.py,v 1.2 2006/03/04 10:10:47 tzellman Exp $
# Module for accessing the Bloglines Web Services
# See <http://www.josephson.org/projects/pybloglines/>

# Suggestion to add BloglinesUnread to OPML parsing by Erik Bryn

import urllib
import urllib2
import string
import re
import base64
import xml.parsers.expat
import westom.feednut.libs.feedparser as feedparser# http://sourceforge.net/projects/feedparser/

class BloglinesException(Exception): pass
class Subscription: pass

class BloglinesWebServices:

    BWS_HOSTNAME = "rpc.bloglines.com"
    BWS_REALM = "Bloglines RPC"

    def __init__(self, user, password = None):
        """Initialises for the specified user. If just the
        update() method is being used then password is optional.
        Other methods will require authentication."""
        if user == None:
            raise BloglinesException("user must be specified")
        else:    
            self.user = user
            self.password = password
    
    def getContent(self, url, requiresAuth = False):
        request = urllib2.Request(url)
        if requiresAuth:
            b64 = base64.encodestring("%s:%s" % (self.user, self.password))[:-1]
            request.add_header("Authorization", "Basic %s" % b64)
        f = urllib2.urlopen(request)
        content = string.join(f.readlines()).strip()
        f.close()
        return content
        
    def checkPasswordSpecified(self):
        if self.password == None:
            raise BloglinesException("password must be specified to call this method")

    def update(self):
        """Returns the unread count for the Bloglines account."""
        # http://www.bloglines.com/services/api/notifier
        params = urllib.urlencode([("user", self.user), ("ver", "1")])
        url ="http://%s/update?%s" % (self.BWS_HOSTNAME, params)
        content = self.getContent(url)
        m = re.match("\|(\-{0,1}[0-9]+)\|([^|]*)\|", content)
        if m:
            unreadCount = int(m.group(1))
            if unreadCount != -1:
                return unreadCount
            else:
                raise BloglinesException("user does not exist")
        else:
            raise BloglinesException("response did not match expected pattern")
            
    def listsubs(self):
        """Returns a list of subscriptions for the Bloglines account.
        This is returned as a list of Subscription objects where each
        entry has title, htmlUrl, type, xmlUrl, bloglinesSubId and
        bloglinesIgnore."""
        # http://www.bloglines.com/services/api/listsubs
        self.checkPasswordSpecified()
        url = "http://%s/listsubs" % self.BWS_HOSTNAME
        content = self.getContent(url, True)
        opmlParser = OpmlParser()
        feedlist = opmlParser.parse(content)
        return feedlist
            
    def getitems(self, bloglinesSubId, markAsRead = False, date = None):
        """For the specified subscription, returns either a list of unread items
        or all items since the data specified, optionally marking the selected
        items as read.
        This is returned as the result of parsing the response using Mark Pilgrim's
        feedparser. See http://www.feedparser.org for details."""
        # http://www.bloglines.com/services/api/getitems
        self.checkPasswordSpecified()
        paramList = [("s", str(bloglinesSubId))]
        if markAsRead:
            paramList.append(("n", "1"))
        else:
            paramList.append(("n", "0"))
        if date != None:
            paramList.append(("d", str(date)))
        params = urllib.urlencode(paramList)
        url = "http://%s/getitems?%s" % (self.BWS_HOSTNAME, params)
        auth = urllib2.HTTPBasicAuthHandler()
        auth.add_password(self.BWS_REALM, self.BWS_HOSTNAME, self.user, self.password)
        parsedData = feedparser.parse(url, handlers = [auth])
        return parsedData
        
class OpmlParser:

    def __init__(self):
        self.parser = xml.parsers.expat.ParserCreate()
        self.parser.StartElementHandler = self.start_element
        self.parser.EndElementHandler = self.end_element
    
    def parse(self, opml):
        self.feedlist = []
        self.parser.Parse(opml)
        return self.feedlist
    
    def start_element(self, name, attrs):
        if name == "outline":
            if attrs.has_key('title') and attrs.has_key('xmlUrl'):
                sub = Subscription()
                sub.title = attrs["title"]
                sub.htmlUrl = attrs["htmlUrl"]
                sub.type = attrs["type"]
                sub.xmlUrl = attrs["xmlUrl"]
                sub.bloglinesSubId = int(attrs["BloglinesSubId"])
                sub.bloglinesIgnore = int(attrs["BloglinesIgnore"])
                sub.bloglinesUnread = int(attrs["BloglinesUnread"])
                self.feedlist.append(sub)
    
    def end_element(self, name):
        pass

        
if __name__ == '__main__':
    service = BloglinesWebServices('tom@zematek.com', 'bloglinespass')
    for item in service.listsubs():
        print item.title
        items = service.getitems(item.bloglinesSubId)
        for key, val in items.iteritems():
            print key, val