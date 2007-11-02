from westom.feednut.models import *
from django.db.models import Q
from westom.feednut.libs.pybloglines import pybloglines
from westom.feednut.libs.pyblogger import blogger
import re


def get_user_blogs(user, type=None):
    """
    This returns a list of tuples (size 2).
    
    Each tuple consists of the Account (see the models), and
    a list of blogs for that account
    """
    query = Q(type__exact='blog')
    if type:
        query &= Q(source__exact=type)
    accounts = user.get_account_list(query)
    
    blog_tuples = []
    for account in accounts:
        blogs = blogger.listBlogs(account.username, account.password)
        blog_tuples.append((account, blogs))
    return blog_tuples

#list any system names here, so people can't use them
INVALID_NAMES = ['static', 'register', 'feed', 'login', 'logout', 'help', 'captcha', 'check', 'gpalert',
                  'tag', 'tags', 'feeds', 'feednut', 'root', 'admin', 'api', 'readentry', 'feeds', 'read', 'form']
INVALID_NAME_DICT = {}
for val in INVALID_NAMES:
    INVALID_NAME_DICT['val'] = val

def is_valid_username(username):
    """
    Checks if the input username is valid by:
        -seeing if it is long enough
        -seeing if it is too long
        -seeing if it is a system name
        -seeing if someone already has it
    If nothing is wrong, an empty string is returned.
    Otherwise, it returns an error message.
    """
    message = None
    if username is not None:
        username = username.strip().rstrip('/')
        if len(username) < 3:
            message = 'Username too short. Must be at least 3 characters'
        elif len(username) > 20:
            message = 'Username too long. Must be at at most 20 characters'
        elif not re.match('^\w+$', username):
            message = 'Username can only be comprised of letters, digits, or the underscore.'
        elif username in INVALID_NAME_DICT:
            message = 'Username already in use'
        else:
            try:
                user = User.objects.get(username__iexact=username)
            except:
                pass
            else:
                message = "Username already exists"
    return message


EMAIL_RE = re.compile(r"^([0-9a-zA-Z_&.+-]+!)*[0-9a-zA-Z_&.+-]+@(([0-9a-z]([0-9a-z-]*[0-9a-z])?\.)+[a-z]{2,6}|([0-9]{1,3}\.){3}[0-9]{1,3})$")
def is_valid_email(email):
    """ checks if the email is valid """
    #an empty string if the address is valid
    if email is not None and len(email.strip()) >= 3 and len(EMAIL_RE.sub('', email)) == 0:
        return None
    else:
        return 'Invalid email format'


def get_user_feeds(user, only_public=True, limit=-1):
    """ Returns a list of UserFeed objects owned by user """
    query = Q(user__id__exact=user.id)
    if only_public:
        query &= Q(is_public=1)
    if limit >= 0:
        return UserFeed.objects.select_related().filter(query, limit=limit).order_by('position')
    else:
        return UserFeed.objects.select_related().filter(query).order_by('position')


def get_feeds(user, only_public=True):
    """ Returns a list of Feed objects owned by user """
    feedlist = []
    for uf in get_user_feeds(user, only_public=only_public):
        feedlist.append(uf.get_feed())
    return feedlist


def get_tags(user, only_public=None):
    """
    Returns a list of tags for this user
    
    Also returns a count as part of each tag
    """
    where=['feednut_userfeed.user_id=' + str(user.id), 'feednut_userfeedtag.tag_id=feednut_tag.id', 'feednut_userfeedtag.user_feed_id=feednut_userfeed.id']
    if(only_public):
        where.append('feednut_tag.tag <> "fn:private"')
        where.append('feednut_userfeed.is_public = True')
    tables=['feednut_userfeed', 'feednut_userfeedtag']
    select={'count' : 'select count(*) from feednut_userfeedtag, feednut_userfeed where feednut_userfeedtag.tag_id=feednut_tag.id and feednut_userfeed.id=feednut_userfeedtag.user_feed_id and feednut_userfeed.user_id=' + str(user.id)}
    tags = Tag.objects.extra(where=where, tables=tables, select=select).distinct().order_by('tag')
#    usertags = UserFeedTag.objects.filter(user_feed__user__exact=user.id).values('tag').distinct()
#    usertags = list(tag['tag'] for tag in usertags)
#    tags = Tag.objects.in_bulk(usertags).values()
#    tags.sort(lambda x, y:cmp(x.tag,(y.tag)))
    return tags
    
def get_accounts(user, type):
    """ returns a list of accounts of a specific type """
    query = Q()
    if type:
        query &= Q(type=type)
    accounts = user.account_set.filter(query)
    return accounts

def read_this_entry(user, url, title, description, xml_url):
    """ keep a list of the last 50 articles that the user read """
    limit = 50
    count = UserReadEntry.objects.count()
    if count >= limit:
        for entry in UserReadEntry.objects.filter(user=user.id).order_by('-read_date')[limit - 1:count]:
            entry.delete()
    ure = UserReadEntry(user=user, link=url, title=title, description=description, xml_url=xml_url)
    ure.save()
    return ure
#    uf = UserFeed.objects.get(id=userFeedId)
#    uf.touch()


#def bookmark(user, url, title, description):
#    """ keep a list of the last 50 articles that the user read """
#    try:
#        bookmark = Bookmark.objects.get(link__iexact=url)
#    except:
#        bookmark = Bookmark(user=user, link=url, title=title, description=description)
#        bookmark.save()
#        return bookmark
#    else:
#        return None

    
def get_latest_read_entries(user):
    """ return a list of UserReadEntry objects of lastest read entries """
    return UserReadEntry.objects.filter(user__id__exact=user.id).order_by('-read_date')

def has_feed(user, feed):
    """ returns True if the user has a userfeed for the given feed, otherwise false """
    return UserFeed.objects.filter(user__id__exact=user.id, feed__id__exact=feed.id).count() > 0

def get_user_buddies(user):
    where=['feednut_userbuddy.user_id=%s' % user.id, 'feednut_userbuddy.buddy_id=auth_user.id']
    tables = ['feednut_userbuddy']
    return User.objects.extra(where=where, tables=tables).distinct()
