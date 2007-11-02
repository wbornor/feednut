"""
postObject model for Blogger

This is a high-level object-oriented interface for blogger.py,
which defines all the available functions exposed by Blogger.com's
XML-RPC API.  

This code was originally written by Mark Pilgrim
(f8dy@diveintomark.org).  I have added objects to allow interface with the added
methods available in Movable Type's XML-RPC API.

Example:
>>> user = Blog.User("YOUR_BLOGGER_USERNAME", "YOUR_BLOGGER_PASSWORD")
>>> blogs = user.blogs                # list of all blogs
>>> for blog in blogs:
...     print "Blog ID:", blog.id     # internal Blogger.com blog ID
...     print "Blog name:", blog.name # title of blog
...     print "Blog URL:", blog.url   # base URL of blog

>>> blog = blogs[0]                   # get reference to user's first blog
>>> posts = blog.posts                # list of most recent posts (up to 20)
>>> for post in blog.posts:
...     print "Post ID:", post.postid        # internal Blogger.com post ID
...     print "Post date:", post.dateCreated # date created, in tuple format
...     print "Posted by:", post.userid      # internal Blogger.com user ID
...     print "Post text:", post.content     # text of post

>>> posts.append("Ping.")             # post new entry to blog
>>> len(posts)                        # count posts
>>> posts[-1].content = "Pong."       # edit text of most recent post
>>> del posts[-1]                     # delete most recent post

>>> html = blog.template.main         # get HTML of main blog entry template
>>> blog.template.main = html         # set HTML template for main blog entries
>>> html = blog.template.archiveIndex # get HTML of archive index template
>>> blog.template.archiveIndex = html # set HTML template for archive index

Movable Type Example:

>>> user = Blog.user ("YOUR_MT_USERNAME", "YOUR_MT_PASSWORD")
>>> blogs = user.blogs
>>> for blog in blogs:
...     print "Blog ID:", blog.id     # internal Blogger.com blog ID
...     print "Blog name:", blog.name # title of blog
...     print "Blog URL:", blog.url   # base URL of blog

>>> blog = blogs[0]                   # get reference to user's first blog
>>> posts = blog.mtposts              # list of most recent posts (up to 20)
>>> for post in blog.posts:
...     print "Post ID:", post.postid        # internal Blogger.com post ID
...     print "Post date:", post.dateCreated # date created, in tuple format
...     print "Posted by:", post.userid      # internal Blogger.com user ID
...     print "Post text:", post.content     # text of post

>>> content = {}                      # fill dictionary with info for new post
>>> content ["title"] = "New Post Title"
>>> content ["description"] = "Ping."A
>>> mtposts.append (content)
>>> len(posts)                        # count posts
>>> posts[-1].content = "Pong."       # edit text of most recent post
>>> del posts[-1]                     # delete most recent post

Compatibility note:
There are several weblog services that offer an XML-RPC interface
with varying levels of compatibility with Blogger.com's API.  These
generally will not work with this high-level API, due to missing
support for key functions.  For instance, Manila does not implement
the getUsersBlogs API, so blogger.listBlogs() will not work, so trying
to access the Blog.User.blogs attribute will not work.  The other
lower-level functions in blogger.py will work with Manila; I suggest
you use those directly if you wish to talk to a Manila server.
"""

__author__ = "Brent Loertscher (blurch@cbtlsl.com)"
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2006/03/04 10:07:32 $"
__copyright__ = "Copyright (c) 2001-2 Mark Pilgrim, 2003 Brent Loertscher"
__license__ = "Python"

import blogger

class User:
    """Blogger user
    
    .username (read-only) - Blogger login
    .password (read-only) - Blogger password
    .nickname (read-only) - user's nickname
    .userid (read-only) - internal Blogger user ID
    .url (read-only) - user's URL
    .email (read-only) - user's email
    .lastname (read-only) - user's last name
    .firstname (read-only) - user's first name
    .blogs - list of Blog objects to access this user's blogs
    """
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.__blogs = None
        self.__info = {}

    def __getattr__(self, key):
        if key in ("nickname", "userid", "url", "email", "lastname", "firstname"):
            if not self.__info:
                self.__info = blogger.getUserInfo(self.username, self.password)
            return self.__info[key]
        if key == "blogs":
            if not self.__blogs:
                self.__blogs = [Blog(self, b) for b in blogger.listBlogs(self.username, self.password)]
            return self.__blogs
        else:
            raise AttributeError, key

class Blog:
    """weblog
    
    .id (read-only) - internal ID of this blog
    .name (read-only) - title of this blog
    .url (read-only) - base web address of this blog
    .template - Template object to access this blog's HTML templates
    .posts - Posts object to access this blog's recent posts
    .posttitles - PostTitles object to access title information for this blogs
                  recent posts
    .mtposts - Posts object designed for use with metaWeblog blogs.
    .categories - Categories object for use with Movable Type blogs.
    .filters - Filters object for use with Movable Type blogs.

    Notes:
    the .posttitles, mtposts, categories, and filters objects are designed to
    work exclusively with Movable Type.
    """
    def __init__(self, user, params):
        self.user = user
        self.id = params["blogid"]
        self.name = params["blogName"]
        self.url = params["url"]
        self.template = Template(self)
        self.__posts = None
        self.__posttitles = None
        self.__categories = None
        self.__filters = None
        self.__mtposts = None
        
    def __getattr__(self, key):
        if key == "posts":
            if not self.__posts:
                allPosts = blogger.listPosts(self.id, self.user.username, self.user.password)
                self.__posts = Posts(self, [Post(self, p) for p in allPosts])
            return self.__posts
        if key == "mtposts":
            if not self.__mtposts:
                allMTPosts = blogger.listMetaWeblogPosts(self.id, self.user.username, self.user.password)
                self.__mtposts = MTPosts(self, [MTPost(self, p) for p in allMTPosts])
                self.__mtposts.count = len (allMTPosts)
            return self.__mtposts
        if key == "posttitles":
            if not self.__posttitles:
               allPostTitles = blogger.listPostTitles(self.id, self.user.username, self.user.password)
               self.__posttitles = PostTitles (self, [PostTitle(self, p) for p in allPostTitles])
               self.__posttitles.count = len(allPostTitles)
            return self.__posttitles
        if key == "categories":
            if not self.__categories:
               allCategories = blogger.listCategories(self.id, self.user.username, self.user.password)
               self.__categories = Categories (self, [Category(self, p) for p in allCategories])
               self.__categories.count = len(allCategories)
            return self.__categories
        if key == "filters":
            if not self.__filters:
               allFilters = blogger.listTextFilters()
               self.__filters = Filters (self, [Filter(self, p) for p in allFilters])
               self.__filters.count = len(allFilters)
            return self.__filters
        else:
            raise AttributeError, key

class Template:
    """blog template
    
    .main (read/write) - HTML template for blog entries
    .archiveIndex (read/write) - HTML template for blog archive index
    """
    def __init__(self, blog):
        self.blog = blog
        self.__template = {}
        
    def __getattr__(self, key):
        if key in blogger.TemplateType.acceptableTypes:
            if not self.__template.has_key(key):
                self.__template[key] = blogger.getTemplate(self.blog.id,
                                                           self.blog.user.username,
                                                           self.blog.user.password,
                                                           key)
            return self.__template[key]
        else:
            raise AttributeError, key

    def __setattr__(self, key, value):
        if key in blogger.TemplateType.acceptableTypes:
            self.__template[key] = value
            blogger.setTemplate(self.blog.id,
                                self.blog.user.username,
                                self.blog.user.password,
                                value,
                                key)
        else:
            self.__dict__[key] = value

class Posts:
    """list of posts in a blog
    
    You can use *some* standard list operations to manipulate this:
    posts.append(text) - adds a new post
    posts[n] - returns Post object containing information about a single post
    posts[n] = text - edits the text of a post
    del posts[n] - deletes a post
    """
    
    def __init__(self, blog, data):
        self.blog = blog
        self.data = data

    def append(self, text):
        import time
        username = self.blog.user.username
        postID = blogger.newPost(self.blog.id, username, self.blog.user.password, text, 1)
        params = {"dateCreated": time.localtime(),
                  "userid": username,
                  "postid": postID,
                  "content": text}
        self.data.append(Post(self.blog, params))

    def _appendMultiple(self, postList):
        for p in postList:
            self.append(p)
    
    def __getitem__(self, index):
        return self.data[index]
    
    def __setitem__(self, index, text):
        self.data[index].content = text

    def __delitem__(self, index):
        postID = self.data[index].id
        blogger.deletePost(postID, self.blog.user.username, self.blog.user.password, 1)
        del self.data[index]

    def __contains__(self, item):
        return item in [post.content for post in self.data]

    def __add__(self, other):
        self._appendMultiple(other)

    def extend(self, other):
        self._appendMultiple(other)

    def __repr__(self):
        return repr(self.data)

class MTPosts:
    """list of posts in a blog
    
    You can use *some* standard list operations to manipulate this:
    posts.append(text) - adds a new post
    posts[n] - returns Post object containing information about a single post
    posts[n] = text - edits the text of a post
    del posts[n] - deletes a post
    """
    
    def __init__(self, blog, data):
        self.blog = blog
        self.data = data

    def append (self, content, publish=1):
        import time
        postID = blogger.newMetaWeblogPost (self.blog.id, self.blog.user.username, self.blog.user.password, content, publish)
        content["dateCreated"] = time.localtime()
        content["userid"] = self.blog.user.username
        content["postid"] = postID
        self.data.append(MTPost(self.blog, content))

    def _appendMultiple (self, postList):
        for p in postList:
           self.append(p)

    def __getitem__(self, index):
        return self.data[index]
    
    def __setitem__(self, index, text):
        self.data[index].content = text

    def __delitem__(self, index, publish=1):
        postID = self.data[index].id
        blogger.deletePost(postID, self.blog.user.username, self.blog.user.password, publish)
        del self.data[index]

    def __contains__(self, item):
        return item in [mtpost.content for mtpost in self.data]

    def __add__(self, other):
        self._appendMultiple(other)

    def extend(self, other):
        self._appendMultiple(other)

    def __repr__(self):
        return repr(self.data)

    def __len__(self):
        return self.count

class PostTitles:
    """list of post titles in a blog
    
    You can use *some* standard list operations to manipulate this:
    posts[n] - returns Post object containing information about a single post
    """
    
    def __init__(self, blog, data):
        self.blog = blog
        self.data = data
        self.count = 0

    def __getitem__(self, index):
        return self.data[index]
    
    def __contains__(self, item):
        return item in [posttitle.title for posttitle in self.data]

    def __repr__(self):
        return repr(self.data)

    def __len__(self):
        return self.count

class Categories:
    """list of categories in a blog
    
    You can use *some* standard list operations to manipulate this:
    categories[n] - returns Post object containing information about a single post
    """
    
    def __init__(self, blog, data):
        self.blog = blog
        self.data = data
        self.count = 0

    def __getitem__(self, index):
        return self.data[index]
    
    def __contains__(self, item):
        return item in [category.content for category in self.data]

    def __repr__(self):
        return repr(self.data)

    def __len__(self):
        return self.count
        
class MTPostCategories:
    """list of categories in a blog
    
    You can use *some* standard list operations to manipulate this:
    categories[n] - returns Post object containing information about a single post
    """
    
    def __init__(self, post, data):
        self.post = post
        self.data = data
        self.count = 0

    def append (self, content):
       self.data.append(MTPostCategory(self.post, content))

    def _appendMultiple (self, postList):
       for p in postList:
          self.append(p)

    def __getitem__(self, index):
        return self.data[index]

    def __delitem__(self, index):
        del self.data[index]
    
    def __contains__(self, item):
        return item in [mtpostcategory.content for mtpostcategory in self.data]

    def __add__(self, other):
        self._appendMultiple(other)

    def extend(self, other):
        self._appendMultiple(other)

    def __repr__(self):
        return repr(self.data)

    def __len__(self):
        return self.count

    def apply (self):
       content = []
       for p in self.data:
          content.append ({"categoryId": p.id })
       blogger.setPostCategories (self.post.id, self.post.blog.user.username, self.post.blog.user.password, content)
       blogger.publishPost(self.post.id, self.post.blog.user.username, self.post.blog.user.password)
        
class Filters:
    """list of filters in a blog
    
    You can use *some* standard list operations to manipulate this:
    filters[n] - returns Post object containing information about a single post
    """
    
    def __init__(self, blog, data):
        self.blog = blog
        self.data = data
        self.count = 0

    def __getitem__(self, index):
        return self.data[index]
    
    def __contains__(self, item):
        return item in [filter.content for filter in self.data]

    def __repr__(self):
        return repr(self.data)

    def __len__(self):
        return self.count
        

class Post:
    """information about a blog post
    
    .id (read-only) - internal post ID
    .dateCreated (read-only) - tuple representing date/time this post was first created
    .userid (read-only) - internal user ID of user who posted this post
    .content (read/write) - text of post
    """
    def __init__(self, blog, params):
        self.blog = blog
        self.id = params["postid"]
        self.dateCreated = params["dateCreated"]
        self.userid = params["userid"]
        self.__content = params["content"]

    def __getattr__(self, key):
        if key == "content":
            return self.__content
        else:
            raise AttributeError, key
        
    def __setattr__(self, key, value):
        if key == "content":
            self.__content = value
            blogger.editPost(self.id, self.blog.user.username, self.blog.user.password, value, 1)
        else:
            self.__dict__[key] = value

if __name__ == "__main__":
    try:
        import pydoc
        pydoc.help("Blog")
    except ImportError:
        print __doc__

class MTPost:
    """information about a MT blog post
    
    .id (read-only) - internal post ID
    .dateCreated (read-only) - tuple representing date/time this post was first created
    .userid (read-only) - internal user ID of user who posted this post
    .description - post description,
    .title - post title,
    .link - post link,
    .permaLink - post permalink,
    .mt_excerpt - post excerpt,
    .mt_text_more - post more,
    .mt_allow_comments - if open for comments,
    .mt_allow_pings - if open for pings,
    .mt_convert_breaks - text filter id,
    .mt_keywords - post keywords
    """
    def __init__(self, blog, params):
        self.blog = blog
        self.id = params["postid"]
        self.dateCreated = params["dateCreated"]
        self.userid = params["userid"]
        self.__description = params["description"]
        self.__title = params["title"]
        if params.has_key("link"):
           self.__link = params["link"]
        if params.has_key("permaLink"):
           self.__permaLink = params["permaLink"]
        if params.has_key("mt_excerpt"):
           self.__mt_excerpt = params["mt_excerpt"]
        if params.has_key("mt_text_more"):
           self.__mt_text_more = params["mt_text_more"]
        if params.has_key("mt_allow_comments"):
           self.__mt_allow_comments = params["mt_allow_comments"]
        if params.has_key("mt_allow_pings"):
           self.__mt_allow_pings = params["mt_allow_pings"]
        if params.has_key("mt_convert_breaks"):
           self.__mt_convert_breaks = params["mt_convert_breaks"]
        if params.has_key("mt_keywords"):
           self.__mt_keywords = params["mt_keywords"]
        self.__postcategories = None

    def __getattr__(self, key):
        if key == "postcategories":
           if not self.__postcategories:
              allMTPostCategories = blogger.listPostCategories (self.id, self.blog.user.username, self.blog.user.password)
              self.__postcategories = MTPostCategories (self, [MTPostCategory(self, p) for p in allMTPostCategories])
              self.__postcategories.count = len (allMTPostCategories)
           return self.__postcategories
        if key == "description":
            return self.__description
        if key == "title":
            return self.__title
        if key == "link":
            return self.__link
        if key == "permaLink":
            return self.__permaLink
        if key == "mt_excerpt":
            return self.__mt_excerpt
        if key == "mt_text_more":
            return self.__mt_text_more
        if key == "mt_allow_comments":
            return self.__mt_allow_comments
        if key == "mt_allow_pings":
            return self.__mt_allow_pings
        if key == "mt_convert_breaks":
            return self.__mt_convert_breaks
        if key == "mt_keywords":
            return self.__mt_keywords
        else:
           raise AttributeError, key
    
    def __setattr__(self, key, value):
        if key == "description":
            self.__description = value
            content = {}
            content ['description'] = self.__description
            blogger.editMetaWeblogPost(self.id, self.blog.user.username, self.blog.user.password, content, 1)
        if key == "mt_excerpt":
            self.__mt_excerpt = value
            content = {}
            content ['mt_excerpt'] = self.__mt_excerpt
            blogger.editMetaWeblogPost(self.id, self.blog.user.username, self.blog.user.password, content, 1)
        if key == "mt_text_more":
            self.__mt_text_more = value
            content = {}
            content ['mt_text_more'] = self.__mt_text_more
            blogger.editMetaWeblogPost(self.id, self.blog.user.username, self.blog.user.password, content, 1)
        if key == "title":
            self.__title = value
            content = {}
            content ['title'] = self.__title
            blogger.editMetaWeblogPost(self.id, self.blog.user.username, self.blog.user.password, content, 1)
        else:
            self.__dict__[key] = value

if __name__ == "__main__":
    try:
        import pydoc
        pydoc.help("Blog")
    except ImportError:
        print __doc__

class PostTitle:
    """information about a blog post title
    
    .id (read-only) - internal post ID
    .dateCreated (read-only) - tuple representing date/time this post was first created
    .userid (read-only) - internal user ID of user who posted this post
    .title (read-only) - text of post
    """
    def __init__(self, blog, params):
        self.blog = blog
        self.id = params["postid"]
        self.dateCreated = params["dateCreated"]
        self.userid = params["userid"]
        self.__title = params["title"]

    def __getattr__(self, key):
        if key == "title":
            return self.__title
        else:
            raise AttributeError, key
        
class Category:
    """information about a blog category
    
    .id (read-only) - internal category ID
    .category (read-only) - category name
    """
    def __init__(self, blog, params):
        self.blog = blog
        self.id = params["categoryId"]
        self.__category = params["categoryName"]

    def __getattr__(self, key):
        if key == "category":
            return self.__category
        else:
            raise AttributeError, key
        
class MTPostCategory:
    """information about a post category
    
    .id (read-only) - internal category ID
    .category - category name
    .primary - whether category is primary category or not
    """
    def __init__(self, post, params):
        self.post = post
        self.id = params["categoryId"]
        if params.has_key("categoryName"):
           self.__categoryname = params["categoryName"]
        if params.has_key("isPrimary"):
           self.__primary = params["isPrimary"]

    def __getattr__(self, key):
        if key == "categoryname":
            return self.__categoryname
        if key == "primary":
            return self.__primary
        else:
            raise AttributeError, key

    def __setattr__(self, key, value):
        self.__dict__[key] = value

class Filter:
    """information about a blog text filter
    
    .id (read-only) - internal category ID
    .filter (read-only) - text of post
    """
    def __init__(self, blog, params):
        self.blog = blog
        self.id = params["key"]
        self.__filter = params["label"]

    def __getattr__(self, key):
        if key == "filter":
            return self.__filter
        else:
            raise AttributeError, key
        
if __name__ == "__main__":
    try:
        import pydoc
        pydoc.help("Blog")
    except ImportError:
        print __doc__
