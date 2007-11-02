from django.conf.urls.defaults import *
from westom.settings import DOCUMENT_ROOT
import os
from westom.feednut.feeds import HottestFeed, RecentRead, ReadLater

handler404 = 'westom.feednut.views.page_not_found'

#register these two feeds
feeds = {
    'hottest': HottestFeed,
    'latest': RecentRead,
    'readlater': ReadLater,
}

urlpatterns = patterns('', 
    (r'^$', 'westom.feednut.views.index'),
    (r'^gpalert/', include('django.contrib.admin.urls')),

#these deal with registration/login
    (r'^login/$', 'westom.feednut.views.login'), 
    (r'^login/forgot/$', 'westom.feednut.views.forgot_password'),
    (r'^login/reset/$', 'westom.feednut.views.reset_password'),
    (r'^accounts/login/$', 'westom.feednut.views.unauthenticated'), #required for django's @login_required decorator
    (r'^logout/$', 'westom.feednut.views.logout'), 
    (r'^register/$','westom.feednut.captcha.verify', 
        dict( forward_to='westom.feednut.views.register', )),
    (r'^captcha/i/$', 'westom.feednut.captcha.image'),
    (r'^captcha/g/$', 'westom.feednut.views.new_captcha'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(DOCUMENT_ROOT, 'feednut/media/')}), 

    (r'^form/subscribe/$', 'westom.feednut.views.form_subscribe'),
    
    (r'^feed/subscribe/$', 'westom.feednut.views.subscribe'), 
    (r'^feed/search/$', 'westom.feednut.views.search_feeds'),
    (r'^feed/tag/$', 'westom.feednut.views.tag_feed'),
    (r'^feed/remove/$', 'westom.feednut.views.remove_feed'),
    (r'^feed/read/$', 'westom.feednut.views.read_article'),
    (r'^feed/readlater/$', 'westom.feednut.views.read_later'),
    (r'^feed/generated/$', 'westom.feednut.views.generate_feed'),
    (r'^feed/(?P<id>\w+)/$', 'westom.feednut.views.get_feed'),
                       
    (r'^help/terms/$', 'westom.feednut.views.pass_through', {'page': 'terms.html'}),
    (r'^help/faq/$', 'westom.feednut.views.pass_through', {'page': 'faq.html'}),

#site-wide RSS feeds
    (r'^.rss$', 'westom.feednut.feeds.feed', {'url' : 'hottest', 'feed_dict': feeds}),
    (r'^hottest.rss$', 'westom.feednut.feeds.feed', {'url' : 'hottest', 'feed_dict': feeds}),
    (r'^latest.rss$', 'westom.feednut.feeds.feed', {'url' : 'latest', 'feed_dict': feeds}),
    
#User endpoints  
    (r'^(?P<username>\w+)/$', 'westom.feednut.views.get_user_page'),
    (r'^(?P<username>\w+)/tags/$', 'westom.feednut.views.get_user_tags'),
    (r'^(?P<username>\w+)/feed/(?P<id>\w+)/$', 'westom.feednut.views.userfeed_action'),
    (r'^(?P<username>\w+)/tags/(?P<tags>[fn:]*\w+[-\w]*)/$', 'westom.feednut.views.get_user_page'),
    
#    (r'^(?P<username>\w+)/(?P<tag>fn:?\w+)/$', 'westom.feednut.views.get_user_page_with_tag'),
#    (r'^(?P<username>\w+)/update/$', 'westom.feednut.views.update_account'),
#    (r'^(?P<username>\w+)/bookmark/$', 'westom.feednut.views.bookmark'),
    (r'^(?P<username>\w+)/.rss$', 'westom.feednut.feeds.user_feed', {'url' : 'hottest', 'feed_dict': feeds}),
    (r'^(?P<username>\w+)/hottest.rss$', 'westom.feednut.feeds.user_feed', {'url' : 'hottest', 'feed_dict': feeds}),
    (r'^(?P<username>\w+)/latest.rss$', 'westom.feednut.feeds.user_feed', {'url' : 'latest', 'feed_dict': feeds}),
    (r'^(?P<username>\w+)/readlater.rss$', 'westom.feednut.feeds.user_feed', {'url' : 'readlater', 'feed_dict': feeds}),
    (r'^(?P<username>\w+)/subscriptions/import/$', 'westom.feednut.views.import_subscriptions'),
    (r'^(?P<username>\w+)/subscriptions/export/$', 'westom.feednut.views.export_subscriptions'),
    (r'^(?P<username>\w+)/buddies/add/$', 'westom.feednut.views.add_user_buddy'),
    (r'^(?P<username>\w+)/buddies/del/$', 'westom.feednut.views.remove_user_buddy'),
    (r'^(?P<username>\w+)/buddies/$', 'westom.feednut.views.get_user_buddies'),
    

#these are misc. functionalities
   
    # Uncomment this for admin:
    #(r'^admin/', include('django.contrib.admin.urls')),
)
