from westom.feednut.models import *
from westom.feednut.libs import OPMLSubscription as opml
from westom.feednut.utils import feed_accomplice
from westom.feednut.utils import user as user_utils
from westom.feednut.utils.lucene_utils import FeedSearcher
from westom.feednut.utils import djangojson
from westom.feednut import mail
from westom.settings import URL_HOST
from django.shortcuts import render_to_response, get_object_or_404
from django.http import *
from django.template import loader, RequestContext
from django.db.models.query import Q
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.cache import cache_page
import urllib
import StringIO
import datetime
import md5
import random
import logging


def get_user_or_404(username):
    return(get_object_or_404(User, username__iexact=username.strip()))

    
def forgot_password(request):
    if request.has_key('email'):
        email = request['email'].strip()
        try:
            user = User.objects.get(email__iexact=email)
        except:
            return HttpResponseNotFound('Email does not exist for any users.')
        else:
            hash = md5.new('%s-%s-%s' % (email, datetime.datetime.now(), random.randint(0, 1000))).hexdigest()
            fpass = ForgotPassword(email=email, hash=hash)
            fpass.save()
            mail.send_password_reset(email, hash)
            return HttpResponse('An email has been sent to \'%s\'.' % email)
    else:
        return render_to_response('forgot_password.html', RequestContext(request))

def reset_password(request):
    if request.has_key('id'):
        id = request['id']
        print id
        try:
            fpass = ForgotPassword.objects.get(hash=id)
        except:
            return HttpResponseRedirect("/")
        else:
            context = RequestContext(request)
            context['email'] = fpass.email
            context['hash'] = fpass.hash
            try:
                context['username'] = User.objects.get(email__iexact=fpass.email)
            except:
                return HttpResponseRedirect("/")
            return render_to_response('reset_password.html', context)
    elif request.has_key('new_pass1') and request.has_key('new_pass2') and \
        request.has_key('hash') and request.has_key('email') and request.has_key('username'):
        new_pass1 = request['new_pass1']
        new_pass2 = request['new_pass2']
        hash = request['hash']
        email = request['email']
        username = request['username']
        
        error = None
        #make sure the user exists
        try:
            user = User.objects.get(username__iexact=username)
        except:
            error = 'Invalid request - no username "%s"' % username
        else:
            #make sure the forgot password request exists
            try:
                forgotPass = ForgotPassword.objects.get(email=email, hash=hash)
            except:
                error = 'Invalid request - this password reset request is no longer valid'
            else:
                #make sure the two new passwords are ok
                if len(new_pass1) < 5:
                    error = 'Password too short. Must be at least 5 characters'
                elif new_pass1 != new_pass2:
                    error = 'Passwords do not match'
                else:
                    #if all is OK, then set the password and save!
                    user.set_password(new_pass1)
                    user.save()
                    #might as well just send us to the login view then take us home
                    post = request.POST.copy()
                    post['username'] = username
                    post['password'] = new_pass1
                    request.POST = post
                    login(request)
                    #delete all forgot password requests for this email
                    ForgotPassword.objects.filter(email__iexact=email).delete()
                    return HttpResponseRedirect('/%s/' % username)
        context = RequestContext(request)
        context['error'] = error
        context['username'] = username
        context['hash'] = hash
        context['email'] = email
        return render_to_response('reset_password.html', context)
        
    return HttpResponseRedirect("/")


def index(request):
    context = RequestContext(request)
    if not request.GET.has_key('script') and not request.session.get('script', False):
        return render_to_response('base.html', context)
    elif not request.session.get('script', False):
        request.session['script'] = True
        return HttpResponseRedirect('/')

    if not request.user.is_authenticated():
        #return render_to_response('index.html', context)
        return HttpResponseRedirect('/guest/')
    else:
        return HttpResponseRedirect('/%s/' % request.user.username)

def login(request):
    retvals = {}
    user = None
    
    context = RequestContext(request)
    if 'next' in request.GET:
        context['next'] = request.GET['next']
    
    if request.POST.has_key('username') and request.POST.has_key('password'):
        username = request.POST.get('username').strip()
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            user.last_login = datetime.datetime.now()
            user.save()
            # Redirect to a success page.
        else:
            retvals['bad_user'] = 'Invalid username or password'
    elif 'lb' in request.GET:
        return render_to_response('login.html', context)
    else:
        #have an actual login page
        return render_to_response('index.html', context)
    #check to see if somebody else was already logged in. if so, we need to log them out
    if not user:
        logout(request)
    else:
        retvals['ok'] = True
    
    if 'next' in request.POST:
        retvals['next'] = urllib.unquote(request.POST['next'])
    
    return HttpResponse(djangojson.write(retvals), 'text/javascript')

def unauthenticated(request):
    context = RequestContext(request)
    if 'next' in request.GET:
        if 'async' in request.GET['next'] or 'json' in request.GET['next']:
            #Only return the 403. 
            #The client (browser parsing the ajax response) MUST take care of redirecting to the login page.
            return HttpResponseForbidden("Error - You must be logged in to do that.")
            
        else:
            return HttpResponseRedirect("/login/?next=%s" % urllib.quote(request.GET['next']))
            
    else:
        return HttpResponseRedirect("/login/")
        

def logout(request):
    """ Logs the user out, and removes cookies if necessary """
    response = HttpResponseRedirect("/")
    auth_logout(request)
    
    try:
        for key in request.session.keys():
            del request.session[key]
    except:{}
    
    if request.session.get('cookiesAllowed', '') == 'true':
        for key in request.COOKIES.keys():
            print 'trying to delete cookie:', key
            response.delete_cookie(key)
        request.COOKIES = {}
    
    for key in request.session.__dict__['_session_cache'].keys():
        del request.session[key]
    
    return response

def pass_through(request, page, require_user=False):
    context = RequestContext(request)
    user = request.user
    if require_user and not request.user.is_authenticated():
        raise Http404
    return render_to_response(page, context)

def register(request, captcha_error):
    user = None
    retvals = {}
    
    if len(captcha_error) > 0:
        retvals['bad_captcha'] = 'Invalid security word'
    if request.POST.has_key('new_username') and request.POST.has_key('new_password') and request.POST.has_key('new_email'):
        username = request.POST['new_username'].strip()
        password = request.POST['new_password']
        email = request.POST['new_email'].strip()
        
        user_msg = user_utils.is_valid_username(username)
        if user_msg:
            retvals['bad_user'] = user_msg
        email_msg = user_utils.is_valid_email(email)
        if email_msg:
            retvals['bad_email'] = email_msg
        if len(password) < 5:
            retvals['bad_pass'] = 'Password too short. Must be at least 5 characters'
        
        #see if the user already exists
        try:
            user = User.objects.get(username__iexact=username)
        except:
            if len(retvals) == 0:
                try:
                    user = User.objects.create_user(username, email, password)
                    user = authenticate(username=username, password=password)
                    auth_login(request, user)
                    retvals['ok'] = True
                    
                    #send the welcome email
                    mail.send_welcome_email(user)

                    for feed in feed_accomplice.get_feeds(default_feed=True):
                        userfeed = feed_accomplice.add_userfeed(user, feed, ['fn:home'])
                    
                    feed_accomplice.add_permanent_feeds(user)
                    

                    if request.has_key('next'):
                        retvals['next'] = urllib.unquote(request['next'])

                except Exception, e:
                    logging.error(e)
                    retvals['bad_user'] = 'Unable to create account'
        else:
            retvals['bad_user'] = 'Username already exists'
    else:
        raise Http404
    return HttpResponse(djangojson.write(retvals), 'text/javascript')

def get_user_page(request, username, tags=None):
    """ Returns a user page """
    
    context = RequestContext(request)
    
    page_user = get_object_or_404(User, username__iexact=username.strip())
    context['page_user'] = page_user

    if(request.user == page_user):
        only_public=None
    else:
        only_public=True
    
    
    if not tags:
        tags = ['fn:home']
    else:
        tags = tags.split('+')
        
    context['feeds'] = feed_accomplice.get_feeds(user=page_user, tags=tags, only_public=only_public)
    
    if 'async' in request.GET:
        return render_to_response('feeds.html', context)
    else:
        return render_to_response('user_page.html', context)
#do this so that IE doesn't load the same page again... protects against logouts/logins
#user_page = cache_page(user_page, 1)


#@cache_page(60 * 1)
def get_feed(request, id):
    feed = get_object_or_404(Feed, id=id)
    context = RequestContext(request)
    context['feed_id'] = id
    context['json'] = True
    if request.GET.has_key('json'):
        feedobj = {'description':feed.subtitle, 'channel_link':feed.channel_link, 'icon_url':feed.icon_url, 'title':feed.title, 'id':feed.id}
        obj = {'feed': feedobj}
        entrylist = []
        entries = feed.get_entries()
        for i, entry in zip(range(len(entries)), entries):
            context['entry'] = entry
            context['index'] = i
            entrylist.append(loader.render_to_string('feed_entry.html', context))
        obj['entries'] = entrylist
        obj['suggest_tags'] = feed.get_suggested_tags()
        return HttpResponse(djangojson.write(obj), 'text/javascript')
    else:
        data = feed.get_xml_data()
        if data is not None:
            response = HttpResponse(mimetype='text/xml')
            response['Content-Type'] = 'text/xml'
            response.write(data)
            return response
        else:
            return HttpResponseRedirect(feed.xml_url)       
#user_page = cache_page(user_page, 1)

@login_required
def form_subscribe(request):
    context = RequestContext(request)
    
    if 'calling_link' in request.GET:
        context['calling_link'] = request.GET['calling_link'] #for hiding the add_feed button after subscribing
        
    if 'page_user_id' in request.GET:
        context['on_my_page'] = int(request.GET['page_user_id']) == int(request.user.id)
    
    if request.has_key('url'):
        context['feed'] = feed_accomplice.get_feed(url=request.REQUEST['url'])
    else:
        raise Http404
    
    context['tags'] = user_utils.get_tags(user=request.user)
    
    if 'async' in request.GET:
        context['async'] = True
        return render_to_response('form_subscribe.html', context)  
    else:
        return render_to_response('subscribe.html', context)     
    
@login_required
def subscribe(request):
   
    if 'feed_id' in request.POST:
        feed_id = request.POST['feed_id']
    elif request.has_key('url'):
        feed_id = feed_accomplice.get_feed(request.REQUEST['url']).id
        if not feed_id:
            raise Http404
    else:
        raise Http404
    
    tags = []
    if 'tags' in request.POST:
        tags = request.POST['tags'].strip().split()
    else:
        tags = ['fn:home']
    
    #see if the user already has this feed
    try:
        userfeed = UserFeed.objects.get(user__id__exact=request.user.id, feed__id__exact=feed_id)
        return HttpResponse('') #already has userfeed, return empty string
    except:
        userfeed = feed_accomplice.add_userfeed(request.user, feed_id, tags=tags)
    
    context = RequestContext(request)
    context['page_user'] = request.user
    context['userfeed'] = userfeed
    context['feed'] = userfeed.feed
    
    #render just this new feed page and return it
    return render_to_response('feed.html', context)


def search_feeds(request):
    if 'query' in request.GET:
        query = request.GET['query'].strip()
        feeds = []
        
        offset = 0
        limit = 10
        total = 0
        if 'o' in request.GET:
            try:
                offset = int(request.GET['o'])
            except:{}
            if offset < 0:
                offset = 0
        if 'l' in request.GET:
            try:
                limit = int(request.GET['l'])
            except:{}
            if limit < 0:
                limit = 10
        
        if len(query) < 2:
            results = []
        else:
#            results = FeedSearcher().search_feeds(query)
            type = 'desc'
            if query.startswith('tags:'):
                query = query.replace('tag:', '')
                type = 'tag'
            elif query.startswith('url:'):
                query = query.replace('url:', '')
                type = 'url'
            
            if len(query) < 2:
                feedlist = []
            elif type == 'tag':
                where = ['feednut_userfeed.feed_id=feednut_feed.id', 
                           'feednut_userfeedtag.user_feed_id=feednut_userfeed.id', 
                           'feednut_userfeedtag.tag_id=feednut_tag.id', 
                           'feednut_tag.tag="' + query + '"']
                tables=['feednut_tag', 'feednut_userfeed', 'feednut_userfeedtag']
                total = Feed.objects.extra(where=where, tables=tables).distinct().count()
                results = Feed.objects.extra(where=where, tables=tables).distinct()[offset:offset+limit]
            elif type == 'url':
                q = (Q(xml_url__icontains=query) | Q(channel_link__icontains=query))
                filter = Feed.objects.filter(q)
                total = filter.count()
                results = filter[offset:offset+limit]
            else:
                q = (Q(title__icontains=query) | Q(subtitle__icontains=query))
                total = Feed.objects.filter(q).count()
                results = Feed.objects.filter(q)[offset:offset+limit]
            
        
        context = RequestContext(request)
        context['results'] = results #[offset:offset+limit]
        context['query'] = query
        context['total'] = total #len(results)
        context['prevoffset'] = max(0, offset - limit)
        context['offset'] = offset + 1
        context['endoffset'] = offset + len(results)
        context['limit'] = limit
        try:
            context['page_user'] = User.objects.get(username__iexact=request.GET['page_user'])
        except:{}
        return render_to_response('search_results.html', context)
    raise Http404

@login_required
def tag_feed(request):
    if request.POST.has_key('id'):
        id = request.POST['id'].strip()
        try:
            userfeed = UserFeed.objects.get(id=id, user__id__exact=request.user.id)
        except:
            raise HttpResponseServerError()
        tags = []
        if 'tags' in request.POST:
            tags = request.POST['tags'].strip().split()
        feed_accomplice.tag_feed(userfeed, tagnames=tags)
        return HttpResponse(djangojson.write(userfeed.get_tags_string()), 'text/javascript')
    raise Http404


@login_required
def remove_feed(request):
    if request.POST.has_key('id'):
        id = request.POST['id'].strip()
        try:
            userfeed = UserFeed.objects.get(feed__id__exact=id, user__id__exact=request.user.id)
        except: {}
        else:
            if userfeed.permanent_feed:
                return HttpServerError("Cannot remove a permanent feed.")
            else:
                userfeed.delete()
                return HttpResponse('')
    raise Http404
    
        
def read_article(request):
    if request.has_key('url') and request.has_key('title') and request.has_key('feed'):
        if request.has_key('summary'):
            summary = request['summary']
        else:
            summary = 'Read full article for more details'
        link = request['url'].strip()
        xml_url = request['feed'].strip()
        title = request['title'].strip()
        if request.user.is_authenticated():
            users_feed = feed_accomplice.get_system_feed('%s/%s/latest.rss' % (URL_HOST, request.user.username))
            feed_accomplice.push_entry(users_feed, title=title, link=link, description=summary, xml_url=xml_url)
        system_feed = feed_accomplice.get_system_feed('%s/latest.rss' % URL_HOST)
        feed_accomplice.push_entry(system_feed, title=title, link=link, description=summary, xml_url=xml_url)
        
        if request.user.is_authenticated():
            uname = request.user.username
        else:
            uname = 'Anonymous User'
        logging.info("%s is reading this entry's link: %s" % (uname, link))
        
        return HttpResponseRedirect(link)
    raise Http404

@login_required 
def read_later(request):   
    if 'url' in request.POST and 'title' in request.POST and 'summary' in request.POST and 'xml_url' in request.POST:
        users_feed = feed_accomplice.get_system_feed('%s/%s/readlater.rss' % (URL_HOST, request.user.username))

        feed_accomplice.push_entry(users_feed, title=request.POST['title'], link=request.POST['url'].strip(), description=request.POST['summary'], xml_url=request.POST['xml_url'])
    return HttpResponse("")
    
def new_captcha(request):
    user = request.user
    if not request.user.is_authenticated():
        raise Http404
    
    from westom.settings import SITE_ID
    from Captcha.Visual import Tests
    import Captcha
    import tempfile
    name = Tests.__all__[0]
    fact = Captcha.PersistentFactory(tempfile.gettempdir() + "/pycaptcha_%d" % SITE_ID)
    test = fact.new(getattr(Tests, name))
    vals = {'captcha_image': '/captcha/i/?id=%s' % test.id, 'captcha_id' : test.id}
    return HttpResponse(djangojson.write(vals), 'text/javascript')


def get_user_tags(request, username):
    page_user = get_user_or_404(username)
    
    if page_user != request.user:
        only_public = True
    else:
        only_public = False
        
    tags = user_utils.get_tags(page_user, only_public=only_public)
    return HttpResponse(djangojson.write([(tag.tag, tag.count) for tag in tags]), 'text/javascript')


def page_not_found(request):
    context = RequestContext(request)
    response = render_to_response('404.html', context)
    response.status_code = 404
    return response

@login_required
def import_subscriptions(request, username):
    """ Request to import a list of feeds in OPML Subscription format"""
    
    #this is causing firefox to crash when an un-authenticated user trys to import subs. Should redirect to error page. Not sure why.
    try:
        xmlData= StringIO.StringIO(request.FILES['opmlfile']['content'])
        subscriptions = opml.parseOpml(xmlData)
    except:
        return HttpResponseServerError('An error occurred parsing the input file')
    
    for sub in subscriptions:
        url = sub.xmlUrl.strip().lower()
        try:
            feed = feed_accomplice.get_feed(url)
            feed_accomplice.add_userfeed(request.user, feed)
        except:{}
    return HttpResponseRedirect("/%s/" % request.user.username)


def export_subscriptions(request, username):
    """Export the users list of feeds in OPML Subscription format """
    context = RequestContext(request)
    #load the user, if they are logged in
    username = username.strip()
    page_user = get_object_or_404(User, username__iexact=username)
    try:
        only_public = (request.user.id != page_user.id)
    except:
        user = None
        only_public = True
    
    context['page_user'] = page_user
    #context['feeds'] = page_user.get_feeds(only_public=only_public)
    #context['feeds'] = user_utils.get_user_feeds(page_user, only_public=only_public)
    context['feeds'] = user_utils.get_feeds(page_user, only_public=only_public)
    response = render_to_response("export_opml.html", context)
    response['Content-Type'] = 'text/xml'
    response['Content-Disposition'] = 'attachment; filename=%s_feeds.opml' % page_user.username
    return response

@login_required
def add_user_buddy(request, username):   
    if request.user.username.lower() != username.lower():
        return HttpResponseServerError()
    
    if request.has_key('buddy'):
        buddy_name = request['buddy']
        buddy = get_object_or_404(User, username__iexact=buddy_name)
        try:
            UserBuddy.objects.get(user__id__exact=request.user.id, buddy__id__exact=buddy.id)
        except:
            userbuddy = UserBuddy(user=request.user, buddy=buddy)
            userbuddy.save()
            return HttpResponse('')
        else:
            return HttpResponse('Already have buddy!')
    raise Http404

@login_required  
def remove_user_buddy(request, username):
    if request.user.username.lower() != username.lower():
        raise HttpResponseServerError()
    
    if request.has_key('buddy'):
        buddy_name = request['buddy']
        print buddy_name
        try:
            buddy = UserBuddy.objects.get(user__id__exact=request.user.id, buddy__username__iexact=buddy_name)
        except: {}
        else:
            buddy.delete()
    #for now, we just always return a valid http response... basically, failing silently
    return HttpResponse('')
            
            
def get_user_buddies(request, username):
    #TODO only select the username to make it quicker
    user = get_object_or_404(User, username__iexact=username)
    buddies = user_utils.get_user_buddies(user)
    return HttpResponse(djangojson.write([buddy.username for buddy in buddies]), 'text/javascript')



def generate_feed(request):
    ''' having a little fun generating feeds... so might as well let users see them '''
    from westom.feednut.utils.HtmlDom import HtmlDom, toHTML
    from westom.feednut.libs.ScrapeNFeed import ScrapedFeed
    from westom.feednut.libs.PyRSS2Gen import RSSItem, Guid
    from westom.feednut.utils.rssgen import SimpleFeed
    
    if request.has_key('url'):
        url = request['url'].lower()
        
        job_board = 'http://www.python.org/community/jobs/'
        top40 = 'http://www.bbc.co.uk/radio1/chart/top40.shtml'
        
        feed = None
        if url == job_board.lower():
            dom = HtmlDom(job_board)
            rssItems = []
            title = dom.evaluate("/html:html/html:head/html:title/text()")[0].nodeValue
            description = 'Feed generated for %s by FeedNut' % job_board
            job_ops = dom.evaluate("//html:div[@class='section'][@id][position()>0]")
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
        
        elif url == top40.lower():
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
        
        if feed is not None:
            response = HttpResponse(mimetype='text/xml')
            response['Content-Type'] = 'text/xml'
            response.write(feed.to_xml())
            return response
        
    raise Http404
generate_feed = cache_page(generate_feed, 120)


def userfeed_action(request, username, id):
    
    try:
        userfeed = UserFeed.objects.filter(feed__id__exact=id, user__username__iexact=username)[0]
    except:
        return HttpResponseServerError('Invalid UserFeed')
    
    if request.REQUEST.has_key('a'):
        action = request.REQUEST['a'].strip()
        if action == 'items' and request.POST.has_key('numitems'):
            #make sure the user requesting is the owner
            if username.lower() != request.user.username.lower():
                return HttpResponseServerError('Invalid user')
            numitems = max(int(request.POST.get('numitems')), 0)
            userfeed.num_items = numitems
            userfeed.save()
            return HttpResponse('')
        elif action == 'entries':
            context = RequestContext(request)
            feed = userfeed.feed
            context['feed_id'] = feed.id
            context['json'] = True
            feedobj = {'description':feed.subtitle, 'channel_link':feed.channel_link, 'icon_url':feed.icon_url, 'title':feed.title, 'id':feed.id}
            obj = {'feed': feedobj}
            entrylist = []
            entries = userfeed.get_entries()
            for i, entry in zip(range(len(entries)), entries):
                context['entry'] = entry
                context['index'] = i
                entrylist.append(loader.render_to_string('feed_entry.html', context))
            obj['entries'] = entrylist
            obj['suggest_tags'] = feed.get_suggested_tags()
            return HttpResponse(djangojson.write(obj), 'text/javascript')
    
    return HttpResponseServerError('No valid action requested')

