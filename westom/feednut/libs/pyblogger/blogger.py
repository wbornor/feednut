"""Blogger interface for Python

http://sourceforge.net/projects/pyblogger/

This module allows you to post to a weblog and manipulate its
settings.  It was originally designed to work with Blogger
(http://www.blogger.com/), but other weblog systems have since
implemented this API, and this module can talk to any of them.
Whichever system you use, you'll need an account.
- Blogger: http://www.blogger.com/
- Manila: http://www.manilasites.com/
- LiveJournal: http://www.livejournal.com/

Note that LiveJournal does not support this API directly; you'll
need to use a Blogger-to-LiveJournal gateway, described here:
  http://www.tswoam.co.uk/index.php?n_go=14

Many functions take the following common arguments:
- blogID:
  - If connecting to Blogger, this is your blog's ID number on
    blogger.com; to get this, log in on blogger.com, click on your blog
    to edit it, and look in the query string of the URL.
  - For Manila, this is the base URL of your weblog.
  - For LiveJournal, this is the journal name.  Can be left blank
    and the user's default journal will be used.
- username: your weblog system username.
- password: your weblog system password.

This code was originally written by Mark Pilgrim (f8dy@diveintomark.org).  I
have added the interface for the added methods available in Movable Type's
XML-RPC API.

Example:
>>> import blogger
>>> username = "YOUR_BLOGGER_USERNAME"
>>> password = "YOUR_BLOGGER_PASSWORD"
>>> blogs = blogger.listBlogs(username, password)
>>> myFirstBlog = blogs[0]
>>> url = myFirstBlog["url"]
>>> blogID = myFirstBlog["blogid"]
>>> postID = blogger.newPost(blogID, username, password, "First post!", 1)
>>> print "New post is available at %s#%s" % (url, postID)
"""

__author__ = "Brent Loertscher (blurch@cbtlsl.com)"
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2006/03/04 10:07:32 $"
__copyright__ = "Copyright (c) 2001-2 Mark Pilgrim, 2003 Brent Loertscher"
__license__ = "Python"

# Requires Pythonware's XML-RPC library
# This comes standard in Python 2.2
# Users of earlier versions must download and install from
# http://www.pythonware.com/products/xmlrpc/
import xmlrpclib

class TemplateType:
    main = "main"
    archiveIndex = "archiveIndex"
    acceptableTypes = (main, archiveIndex)

class constants:
    # XML-RPC server.  We default to Blogger's server, but you
    # can set this to any Blogger-compatible server
    # - Manila: set to your base URL + "/RPC2"
    # - LiveJournal: set to your Blogger-LiveJournal gateway
    # - Movable Type: set to the location of your mt-xmlrpc.cgi script
    # Alternatively, you can pass the server to any of the
    # functions as the last parameter to override this setting.
    xmlrpcServer = "http://www.blogger.com/api"
    
    # The application key is required by Blogger;
    # other weblog systems ignore it
    applicationKey = "1973FAF4B76FC60D35E266310C6F0605456798"
    
    # Transport is only used for testing; should be None for production
    transport = None

def getUserInfo(username, password, serverURL=None):
    """Get information about a user
    
    Returns: dictionary
        {"nickname": "user's nickname",
         "userid": "user ID",
         "url": "user's URL",
         "email": "user's email",
         "lastname": "user's last name",
         "firstname": "user's first name"}
    
    Arguments:
    - username: your weblog username
    - password: your weblog password
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    
    Example:
    >>> info = blogger.getUserInfo("my_blogger_username", "my_secret_password")
    >>> for k, v in info.items():
    ...     print k, v
    """
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    info = server.blogger.getUserInfo(constants.applicationKey,
        username,
        password)
    return info

def listBlogs(username, password, serverURL=None):
    """Get a list of your blogs
    
    Returns: list of dictionaries
        [{"blogid": ID_of_this_blog,
          "blogName": "name_of_this_blog",
          "url": "URL_of_this_blog"}, ...]
    
    Arguments:
    - username: your weblog username
    - password: your weblog password
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    
    Example:
    >>> blogList = blogger.listBlogs("my_blogger_username", "my_secret_password")
    >>> for blog in blogList:
    ...     print "ID:", blog["blogid"]
    ...     print "Name:, blog["blogName"]
    ...     print "URL:", blog["url"]
    ...     print
    
    Manila notes:
    - Manila does not support this method, because it does not keep a centralized
      database of a user's blogs.
    """
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    response = server.blogger.getUsersBlogs(constants.applicationKey,
        username,
        password)
    return response
getUsersBlogs = listBlogs

def listPosts(blogID, username, password, maxPosts=20, serverURL=None):
    """List recent posts in your blog
    
    Returns: list of dictionaries
        [{"dateCreated": date/time of this post in tuple format (see http://python.org/doc/lib/module-time.html)
          "userid": user who posted this entry,
          "postid": ID of this post,
          "content": text of this post
         }, ...]
        
        Posts are listed in chronological order, oldest to newest, so
        listPosts(...)[-1] is the newest post
    
    Arguments:
    - blogID: your weblog's ID number (see module docs for details)
    - username: your weblog username
    - password: your weblog password
    - maxPosts: maximum number of posts to return
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    
    Example:
    >>> blogger.listPosts(my_blog_ID, "my_blogger_username", "my_blogger_password", 1)
    # returns the most recent post
    
    Notes:
    - The Blogger server will only return the 20 most recent posts.
    """
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    response = server.blogger.getRecentPosts(constants.applicationKey,
        str(blogID),
        str(username),
        str(password),
        maxPosts)
    response.reverse()
    for i in range(len(response)):
        v = response[i]["dateCreated"].value
        response[i]["dateCreated"] = (int(v[:4]), int(v[4:6]), int(v[6:8]), int(v[9:11]), int(v[12:14]), int(v[15:17]), 0, 0, 0)
    return response
getRecentPosts = listPosts

def listMetaWeblogPosts(blogID, username, password, maxPosts=20, serverURL=None):
    """List recent posts in your blog
    
    Returns: list of dictionaries
        [{"dateCreated": date/time of this post in tuple format (see http://python.org/doc/lib/module-time.html)
         "userid": user who posted this entry,
         "postid": ID of this post,
         "description": post description,
         "title": post title,
         "link": post link,
         "permaLink": post permalink,
         "mt_excerpt": post excerpt,
         "mt_text_more": post more,
         "mt_allow_comments": if open for comments,
         "mt_allow_pings": if open for pings,
         "mt_convert_breaks": text filter id,
         "mt_keywords": post keywords}
         }, ...]
        
        Posts are listed in chronological order, oldest to newest, so
        listPosts(...)[-1] is the newest post
    
    Arguments:
    - blogID: your weblog's ID number (see module docs for details)
    - username: your weblog username
    - password: your weblog password
    - maxPosts: maximum number of posts to return
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    
    Example:
    >>> blogger.listMetaWeblogPosts(my_blog_ID, "my_blogger_username", "my_blogger_password", 1)
    # returns the most recent post
    
    Notes:
    - Blogger does not recognize this method.  Only servers such as Movable Type
      that support metaWeblog methods will accept this.
   
    """
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    response = server.metaWeblog.getRecentPosts(str(blogID),
        str(username),
        str(password),
        maxPosts)
    response.reverse()
    for i in range(len(response)):
        v = response[i]["dateCreated"].value
        response[i]["dateCreated"] = (int(v[:4]), int(v[4:6]), int(v[6:8]), int(v[9:11]), int(v[12:14]), int(v[15:17]), 0, 0, 0)
    return response

def listPostTitles(blogID, username, password, maxPosts=20, serverURL=None):
    """List recent posts in your blog
    
    Returns: list of dictionaries
        [{"dateCreated": date/time of this post in tuple format (see http://python.org/doc/lib/module-time.html)
          "userid": user who posted this entry,
          "postid": ID of this post,
          "title": title of post
         }, ...]
        
        Posts are listed in chronological order, oldest to newest, so
        listPosts(...)[-1] is the newest post
    
    Arguments:
    - blogID: your weblog's ID number (see module docs for details)
    - username: your weblog username
    - password: your weblog password
    - maxPosts: maximum number of posts to return
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    
    Example:
    >>> blogger.listPosts(my_blog_ID, "my_blogger_username", "my_blogger_password", 1)
    # returns the most recent post
    
    Notes:
    - Blogger does not recognize this method.  Only servers such as Movable Type
      that support metaWeblog methods will accept this.
    - This is a bandwidth friendly way to get a list of post titles from your
      blog.
    """
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    response = server.mt.getRecentPostTitles(str(blogID),
        str(username),
        str(password),
        maxPosts)
    response.reverse()
    for i in range(len(response)):
        v = response[i]["dateCreated"].value
        response[i]["dateCreated"] = (int(v[:4]), int(v[4:6]), int(v[6:8]), int(v[9:11]), int(v[12:14]), int(v[15:17]), 0, 0, 0)
    return response

def cmp_categories (x, y):
    return cmp (x["categoryName"], y["categoryName"])

def listCategories(blogID, username, password, serverURL=None):
    """List all categories defined in weblog
    
    Returns: list of dictionaries
        [{"categoryId": string containing the category id,
          "categoryName": name of category
         }, ...]
        
    Arguments:
    - blogID: your weblog's ID number (see module docs for details)
    - username: your weblog username
    - password: your weblog password
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    
    Example:
    >>> blogger.listCategories(my_blog_ID, "my_blogger_username", "my_blogger_password")
    # returns categories

    Notes:
    - This method will only work with Movable Type.
    """
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    response = server.mt.getCategoryList(str(blogID),
        str(username),
        str(password))
    response.sort(cmp_categories)
    return response

def listPostCategories(postID, username, password, serverURL=None):
    """List all categories selected for a given post
    
    Returns: list of dictionaries
        [{"categoryId": string containing the category id,
          "categoryName": name of category
          "isPrimary": is category primary?
         }, ...]
        
    Arguments:
    - postID: the post ID for the post
    - username: your weblog username
    - password: your weblog password
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    
    Example:
    >>> blogger.listPostCategories(my_post_ID, "my_blogger_username", "my_blogger_password")
    # returns categories

    Notes:
    - This method will only work with Movable Type.
    """
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    response = server.mt.getPostCategories(str(postID),
        str(username),
        str(password))
    response.sort(cmp_categories)
    return response

def setPostCategories(postID, username, password, categories, serverURL=None):
    """Sets the categories for a given post.
    
    Returns: boolean TRUE or FALSE
       
    Arguments:
    - postID: the post ID for the post
    - username: your weblog username
    - password: your weblog password
    - categories: list of dictionaries
       [{"categoryID": string containing the category is,
         "isPrimary": is categor primary?
       }, ...]
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    
    Example:
    >>> blogger.listCategories(my_post_ID, "my_blogger_username", "my_blogger_password")
    # returns categories

    Notes:
    - isPrimary is optional.  If omitted, the first categoryID is the primary
    category.
    - This method will only work with Movable Type.
    """
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    response = server.mt.setPostCategories(str(postID),
        str(username),
        str(password),
        categories)
    return response

def cmp_filters (x, y):
    return cmp (x["label"], y["label"])

def listTextFilters(serverURL=None):
    """List all available text filters for blog
    
    Returns: list of dictionaries
        [{"filterKey": string containing the category id,
          "filterLabel": name of category
         }, ...]
        
    Arguments:
       none
    
    Example:
    >>> blogger.listTextFilters()
    # returns filters

    Notes:
    - This method will only work with Movable Type.
    """
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    response = server.mt.supportedTextFilters()
    response.sort(cmp_filters)
    return response

def getPost(postID, username, password, serverURL=None):
    """Get a single post by ID
    
    Returns: dictionary
        {"dateCreated": date/time of this post in tuple format (see http://python.org/doc/lib/module-time.html)
         "userid": user who posted this entry,
         "postid": ID of this post,
         "content": text of this post}
        
    Arguments:
    - postID: the ID of the post to get
    - username: your weblog username
    - password: your weblog password
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    
    Example:
    >>> blogger.getPost(postID, "my_blogger_username", "my_blogger_password")
    """
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    response = server.blogger.getPost(constants.applicationKey,
        str(postID),
        str(username),
        str(password))
    v = response["dateCreated"].value
    response["dateCreated"] = (int(v[:4]), int(v[4:6]), int(v[6:8]), int(v[9:11]), int(v[12:14]), int(v[15:17]), 0, 0, 0)
    return response

def getMetaWeblogPost(postID, username, password, serverURL=None):
    """Get a single post by ID
    
    Returns: dictionary
        {"dateCreated": date/time of this post in tuple format (see http://python.org/doc/lib/module-time.html)
         "userid": user who posted this entry,
         "postid": ID of this post,
         "description": post description,
         "title": post title,
         "link": post link,
         "permaLink": post permalink,
         "mt_excerpt": post excerpt,
         "mt_text_more": post more,
         "mt_allow_comments": if open for comments,
         "mt_allow_pings": if open for pings,
         "mt_convert_breaks": text filter id,
         "mt_keywords": post keywords}
        
    Arguments:
    - postID: the ID of the post to get
    - username: your weblog username
    - password: your weblog password
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    
    Example:
    >>> blogger.getPost(postID, "my_blogger_username", "my_blogger_password")
    
    Notes:
    - Blogger does not recognize this method.  Only servers such as Movable Type
      that support metaWeblog methods will accept this.
    """
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    response = server.metaWeblog.getPost(str(postID),
        str(username),
        str(password))
    v = response["dateCreated"].value
    response["dateCreated"] = (int(v[:4]), int(v[4:6]), int(v[6:8]), int(v[9:11]), int(v[12:14]), int(v[15:17]), 0, 0, 0)
    return response

def newPost(blogID, username, password, text, publish=0, serverURL=None):
    """Post a new message to your blog
    
    Returns: string
        post ID: append this to your base blog URL to link to your new post
    
    Arguments:
    - blogID: your blog's ID number (see module docs for details)
    - username: your weblog username
    - password: your weblog password
    - text: the actual text you'd like to post
    - publish (optional): 0 = post but do not publish (default)
                          1 = post and publish
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    
    Example:
    >>> postID = blogger.newPost(my_blog_ID, "my_blogger_username", "my_blogger_password, "First post!", 1)
    >>> print postID
    
    Blogger notes:
    - Posts are limited to 65536 characters by the Blogger server.
    - If you want to publish, you must set up your blog to remember your
      FTP username and password.  You must do this through the web interface
      at blogger.com; there is currently no way to do it through this API.
    
    Manila notes:
    - Manila does not have the concept of "post but don't publish"; all
      posts are published immediately.  So the "publish" flag is used as
      an approval flag for multi-member weblogs.  See
      http://frontier.userland.com/emulatingBloggerInManila
      for details.
    """
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    postID = server.blogger.newPost(constants.applicationKey,
        str(blogID),
        str(username),
        str(password),
        str(text),
        publish and xmlrpclib.True or xmlrpclib.False)
    return postID

def newMetaWeblogPost(blogID, username, password, contents, publish=0, serverURL=None):
    """Post a new message to your blog
    
    Returns: string
        post ID: append this to your base blog URL to link to your new post
    
    Arguments:
    - blogID: your blog's ID number (see module docs for details)
    - username: your weblog username
    - password: your weblog password
    - content: dictionary containing content to post
    - publish (optional): 0 = post but do not publish (default)
                          1 = post and publish
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    
    Example:
    >>> postID = blogger.newMetaWeblogPost(my_blog_ID, "my_blogger_username", "my_blogger_password, post_content, 1)
    >>> print postID
    
    Notes:
    - Blogger does not recognize this method.  Only servers such as Movable Type
      that support metaWeblog methods will accept this.
    """
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    postID = server.metaWeblog.newPost( str(blogID),
        str(username),
        str(password),
        contents,
        publish and xmlrpclib.True or xmlrpclib.False)
    return postID

def editPost(postID, username, password, text, publish=0, serverURL=None):
    """Edit an existing message in your blog
    
    Returns: 1
    
    Arguments:
    - postID: ID of post to edit
    - username: your weblog username
    - password: your weblog password
    - text: the actual text you'd like to post
    - publish (optional): 0 = post but do not publish (default)
                          1 = post and publish
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    
    Example:
    >>> postID = blogger.newPost(my_blog_ID, "my_blogger_username", "my_blogger_password, "First post!", 1)
    >>> blogger.editPost(postID, "my_blogger_username", "my_blogger_password, "This text overwrites the old text completely.", 1)
    
    Blogger notes:
    - Posts are limited to 65536 characters by the Blogger server.
    - If you want to publish, you must set up your blog to remember your
      FTP username and password.  You must do this through the web interface
      at blogger.com; there is currently no way to do it through this API.
    
    Manila notes:
    - Manila does not have the concept of "post but don't publish"; all
      posts are published immediately.  So the "publish" flag is used as
      an approval flag for multi-member weblogs.  See
      http://frontier.userland.com/emulatingBloggerInManila
      for details.
    
    LiveJournal notes:
    - Post IDs (item IDs) are not guaranteed to be unique across all of a
      user's journals, so the default journal is always used.  There is
      currently no way of editing entries on a secondary journal.  See
      http://www.tswoam.co.uk/index.php?n_go=14
      for details.
    """
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    response = server.blogger.editPost(constants.applicationKey,
        str(postID),
        str(username),
        str(password),
        str(text),
        publish and xmlrpclib.True or xmlrpclib.False)
    return response == xmlrpclib.True

def editMetaWeblogPost(postID, username, password, contents, publish=0, serverURL=None):
    """Edit an existing message in your blog
    
    Returns: 1
    
    Arguments:
    - postID: ID of post to edit
    - username: your weblog username
    - password: your weblog password
    - contents: a dictionary containing the contents of the post
    - publish (optional): 0 = post but do not publish (default)
                          1 = post and publish
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    
    Example:
    >>> postID = blogger.newMetaWeblogPost(my_blog_ID, "my_blogger_username", "my_blogger_password", contents, 1)
    >>> blogger.editPost(postID, "my_blogger_username", "my_blogger_password, contents, 1)
    
    Notes:
    - Blogger does not recognize this method.  Only servers such as Movable Type
      that support metaWeblog methods will accept this.
    """
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    response = server.metaWeblog.editPost(str(postID),
        str(username),
        str(password),
        contents,
        publish and xmlrpclib.True or xmlrpclib.False)
    return response == xmlrpclib.True

def publishPost(postID, username, password, serverURL=None):
    """Sends signal to regenerate static files assoctiated with a given
       post.  This is done without sending HTTP pings.
    
    Returns: 1
    
    Arguments:
    - postID: ID of post to edit
    - username: your weblog username
    - password: your weblog password
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    
    Example:
    >>> postID = blogger.newMetaWeblogPost(my_blog_ID, "my_blogger_username", "my_blogger_password", contents, 1)
    >>> blogger.editPost(postID, "my_blogger_username", "my_blogger_password, contents, 1)

    Notes:
    - This method will only work with Movable Type.
    """
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    response = server.mt.publishPost(str(postID),
        str(username),
        str(password))
    return response == xmlrpclib.True

def deletePost(postID, username, password, publish=0, serverURL=None):
    """Delete an existing message in your blog
    
    Returns: 1
    
    Arguments:
    - postID: ID of post to edit
    - username: your weblog username
    - password: your weblog password
    - publish (optional): 0 = delete but do not publish (default)
                          1 = delete and publish
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    
    Example:
    >>> postID = blogger.newPost(my_blog_ID, "my_blogger_username", "my_blogger_password, "First post!", 1)
    >>> blogger.deletePost(postID, "my_blogger_username", "my_blogger_password, 1)
    
    Blogger notes:
    - Posts are limited to 7200 characters by the Blogger server.
    - If you want to publish, you must set up your blog to remember your
      FTP username and password.  You must do this through the web interface
      at blogger.com; there is currently no way to do it through this API.
    
    LiveJournal notes:
    - Post IDs (item IDs) are not guaranteed to be unique across all of a
      user's journals, so the default journal is always used.  There is
      currently no way of deleting entries on a secondary journal.  See
      http://www.tswoam.co.uk/index.php?n_go=14
      for details.
    """
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    response = server.blogger.deletePost(constants.applicationKey,
        str(postID),
        str(username),
        str(password),
        publish and xmlrpclib.True or xmlrpclib.False)
    return response == xmlrpclib.True

def getTemplate(blogID, username, password, templateType="main", serverURL=None):
    """Get HTML template for your blog
    
    Returns: string
        specified HTML template
    
    Arguments:
    - blogID: your blog's ID number
    - username: your blogger.com username
    - password: your blogger.com password
    - templateType: 'main' = get main page template (default)
                    'archiveIndex' = get archive index template
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    """
    if templateType not in TemplateType.acceptableTypes:
        raise ValueError, "invalid template type: %s" % templateType
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    htmlTemplate = server.blogger.getTemplate(constants.applicationKey,
        str(blogID),
        str(username),
        str(password),
        templateType)
    return htmlTemplate

def setTemplate(blogID, username, password, text, templateType="main", serverURL=None):
    """Set HTML template for your blog
    
    Returns: 1
    
    Arguments:
    - blogID: your blog's ID number
    - username: your blogger.com username
    - password: your blogger.com password
    - text: complete HTML text of template
    - templateType: 'main' = set main page template (default)
                    'archiveIndex' = set archive index template
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    
    Notes:
    - The given username must be marked as an administrator on the blog in order to
      set the template.  This is the default if you created the blog, but
      not the default if somebody else added you to a team blog.  Administrators
      can add other users to their blog and give them administrative access,
      but they need to do it through the web interface at blogger.com.
    """
    if templateType not in TemplateType.acceptableTypes:
        raise ValueError, "invalid template type: %s" % templateType
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    server.blogger.setTemplate(constants.applicationKey,
        str(blogID),
        str(username),
        str(password),
        text,
        templateType)

if __name__ == "__main__":
    try:
        import pydoc
        pydoc.help("blogger")
    except ImportError:
        print __doc__
