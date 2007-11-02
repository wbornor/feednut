"""
Create some pucking sweet data for testing
"""

import os, sys
import md5
sys.path.append(os.path.join(os.getcwd(), '..'))
sys.path.append(os.getcwd())

# Set DJANGO_SETTINGS_MODULE appropriately.
os.environ['DJANGO_SETTINGS_MODULE'] = 'westom.settings'

from westom.feednut.models import *
sys.path.pop()
from westom.feednut.utils import feed_accomplice
from westom.feednut.utils import misc
import random


def clean():
    User.objects.all().delete()
    for feed in Feed.objects.all():
        if os.path.exists(feed.get_data_path()):
            os.unlink(feed.get_data_path())
        feed.delete()
    Tag.objects.all().delete()

def make_data():
    #make some users
    user1 = User.objects.create_user('tom', "tom@zellmania.com", 'password')
    user2 = User.objects.create_user('wes', "wbornor@splaysh.com", 'password')
    user3 = User.objects.create_user('slayer', "slayer@zellmania.com", 'slayer')
    user4 = User.objects.create_user('guest', "guest@zellmania.com", 'slayer')
    
    user1.is_staff=True
    user2.is_staff=True
    user2.is_superuser=True
    user2.is_superuser=True
    user1.save()
    user2.save()
    
    users = (user1, user2, user3, user4)
    #for user in users:
        #user.set_password(user.password)
        #user.save()
        #print 'Saved', user
        #feed_accomplice.add_default_feeds(user)
    
    #some feeds to add
    feeds = [
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
        'http://jquery.com/blog/feed/',
        'http://feeds.feedburner.com/jquery/',
    ]
    
    #some random tags to possibly add
    randomTags = ['cool', 'tech', 'fun', 'pr0n', 'work', 'splaysh', 'web']
    
    for i, url in zip(range(len(feeds)), feeds):
        print url
        feed = feed_accomplice.get_feed(url)
        if feed:
            #randomly get some tags to tag this feed with
            tags = random.sample(randomTags, random.randint(0, len(randomTags)-1))
            user = users[random.randint(0, len(users) - 1)]
            userfeed = feed_accomplice.add_userfeed(user, feed, tags=tags + ['fn:home'])

if __name__ == '__main__':
    clean()
    make_data()
#    feed_accomplice.update_feeds()
    


