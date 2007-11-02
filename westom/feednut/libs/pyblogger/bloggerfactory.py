"""Factory to output blogs in various formats

Currently supported formats:
- RSS: for syndication
- Scripting News XML: also for syndication
- minimal HTML: for text browsers and mobile devices
- Javascript: for dynamic inclusion in other HTML pages
"""

__author__ = "Mark Pilgrim (f8dy@diveintomark.org)"
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2006/03/04 10:07:32 $"
__copyright__ = "Copyright (c) 2001 Mark Pilgrim"
__license__ = "Python"

import blogger
import bloggerext
import re
import time
import xml.dom.minidom
import scriptingnews

class _Factory:
    postPattern = re.compile(r'(.*?)<Blogger>(.*?)</Blogger>(.*)', re.IGNORECASE | re.DOTALL)
    dateHeaderPattern = re.compile(r'(.*?)<BlogDateHeader>(.*?)</BlogDateHeader>(.*)', re.IGNORECASE | re.DOTALL)
    stripTagsPattern = re.compile(r'(<.*?>)(.*?)(</.*?>)')
    stripTagsReplace = r'\2'
    titlePattern = re.compile(r'(.*?)([.?!-]\s|\n)')
    descriptionPattern = re.compile(r'(.*?)([.?!-]\s|\n)\n*(.*?)(\n|$)')
    
    def __init__(self, blogID, username, password, maxposts=15):
        self.blogID = blogID
        self.username = username
        self.password = password
        self.maxposts = maxposts
        self.refresh()
        
    def refresh(self):
        self.posts = blogger.listPosts(self.blogID, self.username, self.password, self.maxposts)
        self.posts.reverse()
        self.blogTitle = bloggerext.getBlogSetting("blogTitle", self.blogID, self.username, self.password)
        self.blogURL = bloggerext.getBlogSetting("blogURL", self.blogID, self.username, self.password)
        self.blogDescription = bloggerext.getBlogSetting("blogDescription", self.blogID, self.username, self.password)
        info = blogger.getUserInfo(self.username, self.password)
        self.userID = info["userid"]
        self.userRealName = "%s %s" % (info["firstname"], info["lastname"])
        
    def striptags(self, text):
        return self.stripTagsPattern.sub(self.stripTagsReplace, text)
    
    def splittitle(self, post):
        text = self.striptags(post["content"])
        title = self.titlePattern.search(text)
        if title:
            title = title.group(1)
            description = self.descriptionPattern.search(text).group(3)
        else:
            title = text
            description = ""
        if len(title) > self.maxTitleLength:
            title = title[:self.maxTitleLength-3] + "..."
        if len(description) > self.maxPostLength:
            description = description[:self.maxPostLength-3] + "..."
        return (title, description)

class SimpleElement(xml.dom.minidom.Element):
    def __init__(self, tag, data):
        xml.dom.minidom.Element.__init__(self, tag)
        self.appendChild(xml.dom.minidom.Text(data))
        
class _XMLFactory(_Factory):
    maxTitleLength = 100
    maxPostLength = 500
    
class _RSSFactory(_XMLFactory):
    def get(self):
        doc = xml.dom.minidom.Document()
        rss = xml.dom.minidom.Element("rss")
        rss.attributes["version"] = "0.92"
        channel = xml.dom.minidom.Element("channel")
        channel.appendChild(SimpleElement("title", self.blogTitle))
        channel.appendChild(SimpleElement("link", self.blogURL))
        channel.appendChild(SimpleElement("description", self.blogDescription))
        for post in self.posts:
            item = xml.dom.minidom.Element("item")
            title, description = self.splittitle(post)
            item.appendChild(SimpleElement("title", title))
            item.appendChild(SimpleElement("description", description))
            item.appendChild(SimpleElement("link", "%s#%s" % (self.blogURL, post["postid"])))
            channel.appendChild(item)
        rss.appendChild(channel)
        doc.appendChild(rss)
        return doc.toxml()

class _ScriptingNewsFactory(_XMLFactory):
    headerDateTimeFormat = "%a, %d %b %Y %H:%M:%S GMT"
    
    def get(self):
        headers = {}
        if self.posts:
            lastBuildDate = self.posts[-1]["dateCreated"]
        else:
            lastBuildDate = time.localtime()
        gap = lastBuildDate[-1] and time.altzone or time.timezone
        lastBuildDate = time.localtime(time.mktime(lastBuildDate) + gap)
        headers["copyright"] = "Copyright %s %s" % (lastBuildDate[0], self.userRealName)
        headers["pubDate"] = time.strftime(self.headerDateTimeFormat, time.gmtime(time.time()))
        headers["lastBuildDate"] = time.strftime(self.headerDateTimeFormat, lastBuildDate)
        headers["channelDescription"] = self.blogDescription
        headers["channelLink"] = self.blogURL
        headers["channelTitle"] = self.blogTitle
        allposts = [p["content"].strip() for p in self.posts]
        return scriptingnews.textToXML(headers, "\n\n".join(allposts))
        
class _HTMLFactory(_Factory):
    maxTitleLength = 80
    maxPostLength = 255
    itemDateFormat = "%m/%d, %I:%M%p"

    def get(self):
        if not self.template:
            raise ValueError, "no template defined"
        pagetext = self.template
        pagetext = pagetext.replace('<$BlogTitle$>', self.blogTitle)
        pagetext = pagetext.replace('<$BlogDescription$>', self.blogDescription)
        postTemplate = self.postPattern.search(pagetext).group(2)
        posttexts = []
        for post in self.posts:
            posttext = postTemplate
            title, description = self.splittitle(post)
            posttext = posttext.replace("<$BlogItemTitle$>", title)
            posttext = posttext.replace("<$BlogItemBody$>", description)
            posttext = posttext.replace("<$BlogItemAuthor$>", self.userRealName)
            posttext = posttext.replace("<$BlogItemDateTime$>",
                time.strftime(self.itemDateFormat, post["dateCreated"]))
            posttext = posttext.replace("<$BlogItemArchiveFileName$>", self.blogURL)
            posttext = posttext.replace("<$BlogItemNumber$>", post["postid"])
            posttexts.append(posttext)
        return self.postPattern.sub(r'\1%s\3' % ''.join(posttexts), pagetext)

class _MinimalFactory(_HTMLFactory):
    template = """<html>
<head>
<title><$BlogTitle$></title>
</head>
<body>
<p><b><u><$BlogDescription$></u></b></p>
<p>
<Blogger>
<p>
<b><a href="<$BlogItemArchiveFileName$>#<$BlogItemNumber$>"><$BlogItemTitle$></a></b>
<br>
<$BlogItemBody$>
<br>
<i><$BlogItemAuthor$>, <$BlogItemDateTime$></i>
</p>
</Blogger>
</body>
</html>"""

class _JavascriptFactory(_HTMLFactory):
    template = """document.writeln("<p><span class="blogdescription"><$BlogDescription$></span></p>");
<Blogger>document.writeln("<p><span class='blogitemtitle'><$BlogItemTitle$></span>");
document.writeln("<br />");
document.writeln("<span class='blogitembody'><$BlogItemBody$></span>");
document.writeln("<br />");
document.writeln("<span class='blogitemauthor'><$BlogItemAuthor$></span>,");
document.writeln("<span class='blogitemdatetime'><$BlogItemDateTime$></span>");
document.writeln("</p>");
</Blogger>"""

def getBlogAsRSS(blogID, username, password, maxposts=15):
    """output blog in RSS format
    
    Returns: string
    
    Arguments:
    - blogID: your weblog ID
    - username: your weblog username
    - password: your weblog password
    - maxposts: maximum number of posts to include in output
    """
    return getBlogAs("RSS", blogID, username, password, maxposts)

def getBlogAsScriptingNews(blogID, username, password, maxposts=20):
    """output blog in Scripting News XML format
    
    Returns: string
    
    Arguments:
    - blogID: your weblog ID
    - username: your weblog username
    - password: your weblog password
    - maxposts: maximum number of posts to include in output
    """
    return getBlogAs("ScriptingNews", blogID, username, password, maxposts)

def getBlogAsMinimal(blogID, username, password, maxposts=20):
    """output blog as minimal HTML, suitable for reading on text browsers
    
    Returns: string
    
    Arguments:
    - blogID: your weblog ID
    - username: your weblog username
    - password: your weblog password
    - maxposts: maximum number of posts to include in output
    """
    return getBlogAs("Minimal", blogID, username, password, maxposts)

def getBlogAsJavascript(blogID, username, password, maxposts=20):
    """output blog as Javascript code
    
    Returns: string
    
    Arguments:
    - blogID: your weblog ID
    - username: your weblog username
    - password: your weblog password
    - maxposts: maximum number of posts to include in output
    
    Usage:
    - <script language="JavaScript">OUTPUT_OF_THIS_FUNCTION</script>
    - <script language="JavaScript" src="FILE_CONTAINING_OUTPUT_OF_THIS_FUNCTION"></script>
    - <script language="JavaScript" src="URL_CONTAINING_OUTPUT_OF_THIS_FUNCTION"></script>
    - <script language="JavaScript" src="URL_THAT_DYNAMICALLY_CALLS_THIS_FUNCTION"></script>
    
    Presumably you would only be able to do that last one if you control your
    own web server.
    """
    return getBlogAs("Javascript", blogID, username, password, maxposts)

def getBlogAs(format, blogID, username, password, maxposts=20):
    """output blog in given format
    
    Returns: string
    
    Arguments:
    - format: in ('RSS', 'ScriptingNews', 'Minimal', 'Javascript')
    - blogID: your weblog ID
    - username: your weblog username
    - password: your weblog password
    - maxposts: maximum number of posts to include in output
    """
    factory = globals()["_%sFactory" % format]
    return factory(blogID, username, password, maxposts).get()
