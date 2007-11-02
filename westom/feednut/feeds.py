from django.contrib.syndication.feeds import Feed as FEED
from django.contrib.syndication.feeds import ObjectDoesNotExist
from django.contrib.syndication.views import feed as feed_func
from django.views.decorators.cache import cache_page
from westom.feednut.utils import user as user_utils
from westom.feednut.utils import feed_accomplice
from westom.feednut.models import *
from westom.settings import URL_HOST

class HottestFeed(FEED):
    """
    The Hottest Feeds on FeedNut
    
    Returns the most popular, both site-wide, and user-based
    """
    def get_object(self, bits):
        if len(bits) > 1:
            raise ObjectDoesNotExist
        if len(bits) == 1:
            return User.objects.get(username__iexact=bits[0].lower())
        return None

    def title(self, obj):
        if obj:
            return "FeedNut.com | %s's Hottest Feeds" % obj.username
        else:
            return "FeedNut.com | Hottest Feeds"

    def link(self, obj):
        if obj:
            return "http://feednut.com/%s/" % obj.username
        else:
            return "http://feednut.com/"

    def description(self, obj):
        if obj:
            return "%s's Hottest Feeds at feednut.com" % obj.username
        else:
            return "The most popular feeds at feednut.com"

    def items(self, obj):
        """
        Returns the top 25 most popular feeds
        Popularity is based on how many people are subscribed to the feeds
        OR
        the position of the feed in the users list
        """
        if obj:
            where = ['feednut_userfeed.user_id=' + str(obj.id), 'feednut_feed.id=feednut_userfeed.feed_id']
            tables = ['feednut_userfeed']
            select = {'uf_pos' : 'select position from feednut_userfeed where feed_id=feednut_feed.id and feednut_userfeed.user_id=' + str(obj.id)}
            return Feed.objects.extra(where=where, tables=tables, select=select).order_by('uf_pos')[:25]
        else:
            return Feed.objects.extra(select={'feed_count': 'SELECT COUNT(*) FROM feednut_userfeed WHERE feed_id = feednut_feed.id'}).order_by('-feed_count', '-create_date')[:25]
    
    def item_link(self, item):
        return item.xml_url


class RecentRead(FEED):
    """
    Returns the user's or system's most recently read articles
    """
    def get_object(self, bits):
        if len(bits) > 1:
            raise ObjectDoesNotExist
        if len(bits) == 1:
            return User.objects.get(username__iexact=bits[0].lower())
        return None

    def title(self, obj):
        if obj:
            return "FeedNut.com | %s's Recent Reads" % obj.username
        else:
            return "FeedNut.com | Recent Reads"
        

    def link(self, obj):
        if obj:
            return "http://feednut.com/%s/" % obj.username
        else:
            return "http://feednut.com/"

    def description(self, obj):
        if obj:
            return "%s's recent reads at feednut.com" % obj.username
        else:
            return "Recent reads at feednut.com"

    def items(self, obj):
        if obj:
            #return user_utils.get_latest_read_entries(obj) 
            feed = feed_accomplice.get_system_feed("%s/%s/latest.rss" % (URL_HOST, obj.username))
        else:
            feed = feed_accomplice.get_system_feed("%s/latest.rss" % URL_HOST)
            
        return feed_accomplice.get_entries(feed)
        
    def item_link(self, item):
        return item.link
    
class ReadLater(FEED):
    """
    Returns the entries the user's has flagged to read later
    """
    def get_object(self, bits):
        if len(bits) > 1:
            raise ObjectDoesNotExist
        if len(bits) == 1:
            return User.objects.get(username__iexact=bits[0].lower())
        return None

    def title(self, obj):
        if obj:
            return "FeedNut.com | %s's Read Later List" % obj.username
        

    def link(self, obj):
        if obj:
            return "http://feednut.com/%s/" % obj.username

    def description(self, obj):
        if obj:
            return "%s's entries to read later on FeedNut.com" % obj.username

    def items(self, obj):
        if obj:
            feed = feed_accomplice.get_system_feed("%s/%s/readlater.rss" % (URL_HOST, obj.username))

        return feed_accomplice.get_entries(feed)
        
    def item_link(self, item):
        return item.link

#copied from the contrib area, so we can change the response
#might want to move thisinto the views.py file
def feed(request, url, feed_dict=None):
    response = feed_func(request, url, feed_dict)
    response['Content-Type'] = 'text/xml'
    return response
#let's cache it for 2 minutes
feed = cache_page(feed, 120)

def user_feed(request, username, url, feed_dict=None):
    return feed(request, '%s/%s' % (url, username), feed_dict=feed_dict)
