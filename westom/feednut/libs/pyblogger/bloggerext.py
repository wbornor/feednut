"""Extensions to the Blogger XML-RPC interface

This module implements some useful functions which ought
to be part of Blogger's XML-RPC interface, but aren't.
These functions are Blogger.com-specific and do not use
XML-RPC, so they will not work with weblog servers that
are otherwise compatible with the Blogger XML-RPC interface.

The hope is that Blogger (and other servers) will eventually
implement these functions in a consistent manner via XML-RPC,
and all this nastiness can disappear.  But I need them sooner
than that, so here we are.
"""

__author__ = "Mark Pilgrim (f8dy@diveintomark.org)"
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2006/03/04 10:07:32 $"
__copyright__ = "Copyright (c) 2001 Mark Pilgrim"
__license__ = "Python"

import urllib
import Cookie
import re

_opener = None
_pid = None
_settings = {}
_info = {}

def _getHTML(url, params=None):
    global _opener
    if not _opener:
        _opener = urllib.FancyURLopener()
        _opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 4.0)')]
    if params:
        data = urllib.urlencode(params)
        usock = _opener.open(url, data)
    else:
        usock = _opener.open(url)
    cookies = Cookie.SmartCookie()
    for c in usock.headers.getallmatchingheaders("set-cookie"):
        cookies.load(c)
    html = usock.read()
    usock.close()
    _opener.addheaders.extend([('Cookie', c) for c in cookies.output().replace("\n", "").split("Set-Cookie: ")[1:]])
    return html

def _login(username, password):
    global _pid
    if _opener: return
    _getHTML("http://www.blogger.com/")
    params = {"username":username,
              "password":password,
              "remember":"1"}
    _getHTML("http://www.blogger.com/login-action.pyra", params)
    cookies = [v for k, v in _opener.addheaders if k == "Cookie"]
    userid = re.compile("^PyraID=(.*?);")
    _pid = [userid.search(v).group(1) for v in cookies if userid.search(v)][0]

def _getSettings(blogID):
    global _settings
    blogID = str(blogID)
    if not _settings.has_key(blogID):
        _settings[blogID] = {}
        s = _getHTML("http://www.blogger.com/blog_edit.pyra?blogID=%s" % blogID)
        _settings[blogID]["blogTitle"] = re.search(r'"txtTitle".*?value="(.*?)">', s).group(1)
        _settings[blogID]["blogDescription"] = re.search(r'"txaBody".*?>(.*?)</textarea', s).group(1)
        _settings[blogID]["blogURL"] = re.search(r'"txtBlogURL".*?value="(.*?)">', s).group(1)
        _settings[blogID]["ftpServer"] = re.search(r'"txtFTPServer".*?value="(.*?)">', s).group(1)
        _settings[blogID]["ftpPath"] = re.search(r'"txtFTPPath".*?value="(.*?)">', s).group(1)
        _settings[blogID]["ftpFileName"] = re.search(r'"txtFTPFileName".*?value="(.*?)">', s).group(1)
        _settings[blogID]["ftpUserName"] = re.search(r'"txtFTPUserName".*?value="(.*?)">', s).group(1)
        _settings[blogID]["ftpPassword"] = re.search(r'"txtFTPPassword".*?value="(.*?)">', s).group(1)

def getBlogSetting(settingName, blogID, username, password):
    """Get blog setting
    
    Returns: string
    
    Arguments:
    - settingName: in ('blogTitle', 'blogDescription', 'blogURL',
                       'ftpServer', 'ftpPath', 'ftpFileName',
                       'ftpUserName', 'ftpPassword')
    - blog ID: your weblog ID
    - username: your weblog username
    - password: your weblog password
    """
    blogID = str(blogID)
    _login(username, password)
    _getSettings(blogID)
    return _settings[blogID][settingName]
    