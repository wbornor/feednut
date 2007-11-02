""" Library for the syndic8 RPC API """
import xmlrpclib
import time

PROXY = "http://www.syndic8.com/xmlrpc.php"

def _new_instance():
    """ Returns a new instance of the syndic8 proxy server """
    server = xmlrpclib.ServerProxy(PROXY)
    return server.syndic8

def findfeeds(pattern, sortfield='feedid', offset=0, limit=10):
    """ Returns Array of FeedIDs of matching feeds """
    syndic8 = _new_instance()
    if offset < 0:
        offset = 0
    if limit < 0:
        limit = 10
    return syndic8.FindFeeds(pattern, sortfield, limit, offset)

def findsites(pattern):
    """ Returns Array of FeedIDs of matching feeds """
    return _new_instance().FindSites(pattern)

def getfeedfields():
    """ Returns Array of feed field names """
    return _new_instance().GetFeedFields()

def getfeedcount():
    """ Returns Number of feeds """
    return _new_instance().GetFeedCount()

def getfeedinfo(ids, fields=[]):
    """ Returns Array of structures containing all feed fields (or requested fields only) from database, plus faultCode and faultMessage."""
    return _new_instance().GetFeedInfo(ids, fields)

def getlastfeed():
    """ Returns Highest assigned FeedID. """
    return _new_instance().GetLastFeed()

def gettaggedfeeds(tag):
    """ Returns Array of FeedIDs of all feeds with the given tag. """
    return _new_instance().GetTaggedFeeds(tag)

def getchangedfeeds(fields, startdate, enddate, returnfields):
    """ Returns Array of structures, each containing the requested fields from feeds with changes in the given date range. """
    syndic8 = _new_instance()
    return syndic8.GetChangedFeeds(fields, time.strftime('%Y-%m-%d', startdate), 
        time.strftime('%Y-%m-%d', enddate), returnfields)
