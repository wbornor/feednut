from django.template import Library, Node
from django import template
from westom.feednut.utils import user as user_utils
from westom.feednut.utils import misc as misc_utils
from westom.feednut.utils import feed_accomplice
from westom.feednut.models import *

register = Library()


def get_entries(parser, token):
    try:
        # Splitting by None == splitting by spaces.
        tag_name, feed = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires an argument" % token.contents[0]
    return GetEntriesNode(feed)


class GetEntriesNode(template.Node):
    def __init__(self, feed):
        self.feed = feed 
    def render(self, context):
        feed = template.resolve_variable(self.feed, context)
        context['entries'] = feed.get_entries()
        return ''
register.tag('get_entries', get_entries)


def get_user_tag_tuples(parser, token):
    """ This assumes you have 'page_user' in the current context"""
    try:
        # Splitting by None == splitting by spaces.
        tag_name, var = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires an argument" % token.contents[0]
    return GetUserTagTuplesNode(var)

class GetUserTagTuplesNode(template.Node):
    def __init__(self, var):
        self.var = var
    def render(self, context):
        if context.has_key('user') and context['page_user'] == context['user']:
            only_public = False
        else:
            only_public = True
  
        context[self.var] = user_utils.get_tags(context['page_user'], only_public=only_public)
        return ''
register.tag('get_user_tag_tuples', get_user_tag_tuples)

def get_user_buddies(parser, token):
    try:
        # Splitting by None == splitting by spaces.
        tag_name, var = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires an argument" % token.contents[0]
    return GetUserBuddies(var)

class GetUserBuddies(template.Node):
    def __init__(self, var):
        self.var = var
    def render(self, context):
        page_user = context['page_user']
        context[self.var] = user_utils.get_user_buddies(page_user)
        return ''
register.tag('get_user_buddies', get_user_buddies)

def get_permanent_feeds(parser, token):
    try:
        # Splitting by None == splitting by spaces.
        tag_name, var = token.contents.split(None, 1)
        print "in here"
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires an argument" % token.contents[0]
    return GetPermanentFeeds(var)

class GetPermanentFeeds(template.Node):
    def __init__(self, var):
        self.var = var
    def render(self, context):
        page_user = context['page_user']
        context[self.var] = feed_accomplice.get_feeds(user=page_user, permanent_feed=True)
        print context[self.var]
        return ''
register.tag('get_permanent_feeds', get_permanent_feeds)

def ifisme(parser, token):
    nodelist_true = parser.parse(('else', 'endifisme'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endifisme',))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()
    return IfIsMeNode(nodelist_true, nodelist_false)


class IfIsMeNode(template.Node):
    def __init__(self, nodelist_true, nodelist_false):
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
    
    def render(self, context):
        if context.has_key('page_user'):
            page_user = context['page_user']
            if context.has_key('user'):
                user = context['user']
                if user and page_user and page_user.id == user.id:
                    return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)
register.tag('ifisme', ifisme)        

def ifisnotme(parser, token):
    nodelist_true = parser.parse(('else', 'endifisnotme'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endifisnotme',))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()
    return IfIsNotMeNode(nodelist_true, nodelist_false)


class IfIsNotMeNode(template.Node):
    def __init__(self, nodelist_true, nodelist_false):
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
    
    def render(self, context):
        if context.has_key('page_user'):
            page_user = context['page_user']
            if context.has_key('user'):
                user = context['user']
                if user and page_user and page_user.id != user.id:
                    return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)
register.tag('ifisnotme', ifisnotme)  


def if_user_or_page_user(parser, token):
    nodelist_true = parser.parse(('else', 'endifuserorpageuser'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endifuserorpageuser',))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()
    return IfUserOrPageUserNode(nodelist_true, nodelist_false)


class IfUserOrPageUserNode(template.Node):
    def __init__(self, nodelist_true, nodelist_false):
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
    
    def render(self, context):
        ok = False
        if context.has_key('page_user'):
            page_user = context['page_user']
            if page_user and page_user.id:
                ok = True
        elif context.has_key('user'):
            user = context['user']
            if user and user.id:
                ok = True
        if ok:
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)
register.tag('ifuserorpageuser', if_user_or_page_user)        
        

def ifishottestfeed(parser, token):
    nodelist_true = parser.parse(('else', 'endifishottestfeed'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endifishottestfeed',))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()
    return IfIsHottestFeedNode(nodelist_true, nodelist_false)


class IfIsHottestFeedNode(template.Node):
    def __init__(self, nodelist_true, nodelist_false):
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
    
    def render(self, context):
        if context.has_key('feed'):
            feed = context['feed']
            if feed.title == "FeedNut.com - Hottest Feeds":
                return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)
register.tag('ifishottestfeed', ifishottestfeed)        

def ifhasfeed(parser, token):
    nodelist_true = parser.parse(('else', 'endifhasfeed'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endifhasfeed',))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()
    return IfHasFeedNode(nodelist_true, nodelist_false)


class IfHasFeedNode(template.Node):
    def __init__(self, nodelist_true, nodelist_false):
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
    
    def render(self, context):
        if (context.has_key('feed') or context.has_key('result')) and context.has_key('user'):
            feed = context.get('feed', None) or context.get('result', None)
            user = context['user']
            if type(feed) == dict:
                try:
                    feed = Feed.objects.get(id=feed['id'])
                except:{}
            if user_utils.has_feed(user, feed):
                return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)
register.tag('ifhasfeed', ifhasfeed)        
        

def first_not_none(parser, token):
    try:
        parts = token.contents.split(None)
        del parts[0]
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires an argument" % token.contents[0]
    return FirstNotNoneNode(parts)


class FirstNotNoneNode(template.Node):
    def __init__(self, parts):
        self.parts = parts
    def render(self, context):
        for part in self.parts:
            try:
                part = template.resolve_variable(part, context)
            except: {}
            else:
                if part:
                    return part
        return ''
register.tag('first_not_none', first_not_none)





def load_welcome_page(context):
    return context
load_welcome_page = register.inclusion_tag('welcome.html', takes_context=True)(load_welcome_page)

def load_account_settings_page(context):
    return context
load_account_settings_page = register.inclusion_tag('account_settings.html', takes_context=True)(load_account_settings_page)

def load_search_results_nav_page(context):
    return context
load_search_results_nav_page = register.inclusion_tag('search_results_nav.html', takes_context=True)(load_search_results_nav_page)

def load_feed_hdr_page(context):
    return context
load_feed_hdr_page = register.inclusion_tag('feed_hdr.html', takes_context=True)(load_feed_hdr_page)

def load_feed_options_page(context):
    return context
load_feed_options_page = register.inclusion_tag('feed_options.html', takes_context=True)(load_feed_options_page)

def load_noscript_page(context):
    return context
load_noscript_page = register.inclusion_tag('noscript.html', takes_context=True)(load_noscript_page)

def load_addsearch_page(context):
    return context
load_addsearch_page = register.inclusion_tag('add_search_feeds.html', takes_context=True)(load_addsearch_page)

def load_options_page(context):
    return context
load_options_page = register.inclusion_tag('options.html', takes_context=True)(load_options_page)

def load_login_page(context):
    return context
load_login_page = register.inclusion_tag('login.html', takes_context=True)(load_login_page)

def load_footer_page(context):
    return context
load_footer_page = register.inclusion_tag('footer.html', takes_context=True)(load_footer_page)

def load_main_page(context):
    return context
load_main_page = register.inclusion_tag('main.html', takes_context=True)(load_main_page)

def load_feeds_page(context):
    return context
load_feeds_page = register.inclusion_tag('feeds.html', takes_context=True)(load_feeds_page)

def load_tags_page(context):
    return context
load_tags_page = register.inclusion_tag('tags.html', takes_context=True)(load_tags_page)

def load_community_page(context):
    return context
load_community_page = register.inclusion_tag('communityTab.html', takes_context=True)(load_community_page)

def load_toolbar_page(context):
    return context
load_toolbar_page = register.inclusion_tag('toolbar.html', takes_context=True)(load_toolbar_page)

def load_rss_feeds_page(context):
    return context
load_rss_feeds_page = register.inclusion_tag('rss_feeds.html', takes_context=True)(load_rss_feeds_page)

def load_blogs_page(context):
    return context
load_blogs_page = register.inclusion_tag('blogs.html', takes_context=True)(load_blogs_page)

def load_tag_nav(context):
    return context
load_tag_nav = register.inclusion_tag('tag_nav.html', takes_context=True)(load_tag_nav)

def load_feed_nav(context):
    return context
load_feed_nav = register.inclusion_tag('feed_nav.html', takes_context=True)(load_feed_nav)

def load_bookmark_nav(context):
    return context
load_bookmark_nav = register.inclusion_tag('bookmark_nav.html', takes_context=True)(load_bookmark_nav)

def load_syndication_nav(context):
    return context
load_syndication_nav = register.inclusion_tag('syndication_nav.html', takes_context=True)(load_syndication_nav)

def load_header_page(context):
    return context
load_header_page = register.inclusion_tag('header.html', takes_context=True)(load_header_page)

def load_tabs_page(context):
    return context
load_tabs_page = register.inclusion_tag('tabs.html', takes_context=True)(load_tabs_page)

def load_search_display_page(context):
    return context
load_search_display_page = register.inclusion_tag('searchDisplay.html', takes_context=True)(load_search_display_page)

def load_feed_entry_page(context, feed_id, id):
    context['feed_id'] = feed_id
    context['index'] = id
    return context
load_feed_entry_page = register.inclusion_tag('feed_entry.html', takes_context=True)(load_feed_entry_page)

@register.inclusion_tag('feed.html', takes_context=True)
def load_feed_page(context):
    context['userfeed'] = UserFeed.objects.get(user__id__exact=context['page_user'].id, feed__id__exact=context['feed'].id)
    return context

@register.inclusion_tag('form_subscribe.html', takes_context=True)
def load_form_subscribe_page(context):
    return context

#copied from the django dev release
class SpacelessNode(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        return misc_utils.strip_spaces_between_tags(self.nodelist.render(context).strip())

def spaceless(parser, token):
    """
    Normalize whitespace between HTML tags to a single space. This includes tab
    characters and newlines.

    Example usage::

        {% spaceless %}
            <p>
                <a href="foo/">Foo</a>
            </p>
        {% endspaceless %}

    This example would return this HTML::

        <p> <a href="foo/">Foo</a> </p>

    Only space between *tags* is normalized -- not space between tags and text. In
    this example, the space around ``Hello`` won't be stripped::

        {% spaceless %}
            <strong>
                Hello
            </strong>
        {% endspaceless %}
    """
    nodelist = parser.parse(('endspaceless',))
    parser.delete_first_token()
    return SpacelessNode(nodelist)
spaceless = register.tag(spaceless)

