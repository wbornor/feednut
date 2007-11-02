#!/usr/bin/env python


"""
post to, repost to, or delete articles from a weblog via Blogger API
requires pyblogger and xmlrpclib

Copyright 2001 Adam Feuer

This is free software, distributed under the Python 2.1.1 license.
See http://www.python.org/2.1.1/license.html

---------------------------

reads name and password from ~/.bloggerrc
file should be formatted like:

username adamfeuer
password foo

"""


__author__ = "Adam Feuer <adamf at pobox dot com>"
__version__ = "0.3"
__date__ = "4 November 2001"
__copyright__ = "Copyright (c) 2001 Adam Feuer"
__license__ = "Python"




import sys, os, string
import Blog


##----------- global variables --------------------


debug = 0

BlogInfoFileName = "~/.bloggerrc"

ValidCommands = { 'delete'       : 2,
                  'd'            : 2,
                  'post'         : 3,
                  'p'            : 3,
                  'repost'       : 3,
                  'r'            : 3,
                  'gettemplate'  : 2,
                  'gt'           : 2,
                  'savetemplate' : 3,
                  'st'           : 3}

ProgramName = os.path.split(sys.argv[0])[-1]

##----------- utility functions --------------------

def Message(msg):
    if debug == 1:
        sys.stderr.write(msg)
        sys.stderr.write('\n')

def Error(msg):
    sys.stderr.write("Error: %s" % msg)
    sys.stderr.write('\n')
    sys.exit(0)


def ReadFile(filename):
    """read a post out of a file and into a string."""
    try:
        f = open(filename)
        contents = f.read()
        f.close()
    except:
        return None
    return contents


def SettingsDict(contents):
    """Convert a string to a dict containing name, value pairs.
         Splits name,value on first space or tab.
         Ignores blank lines or lines where first non-whitespace is '#'
         All names are returned lowercase."""

    lines = string.split(contents,'\n')
    dict = {}
    for line in lines:
        line = string.strip(line)

        # ignore blank lines and comments
        if len(line) == 0:
            continue
        if line[0] == '#':
            continue

        name, value = string.split(line,None,1)
        name = string.strip(string.lower(name))
        value = string.strip(value)
        dict[name] = value

    return dict


def GetUsernameAndPassword(contents):
    """parse username and password from a string"""

    settings = SettingsDict(contents)

    username = None
    password = None

    if settings.has_key('username'):
        username = settings['username']
    if settings.has_key('password'):
        password = settings['password']

    return username, password


def GetBlogUsernameAndPassword():
    """parse username and password from the ~/.bloggerrc file"""
    
    filename = os.path.expanduser(BlogInfoFileName)
    contents = ReadFile(filename)
    return GetUsernameAndPassword(contents)


##------------- blogger functions --------------


def Post(blog, PostContents):
    Message("Post: getting posts...")
    posts = blog.posts
    Message ("Post: doing posts...")
    posts.append(PostContents)
        
def Repost(blog, PostContents, PostID):
    posts = blog.posts    
    if PostID is None:
        posts[-1] = PostContents
    else:
        for post in posts:
            if post.id == PostID:
                post.content = PostContents
                sys.exit(0)
        Error("Did not find article '%s' in '%s'." % (PostID, blog.name))

def DeletePost(blog, PostID):
    posts = blog.posts
    if PostID is None:
        del posts[-1]
    else:
        for post in posts:
            if post.id == PostID:
                del post
                sys.exit(0)
        Error("did not find article '%s' in '%s'." % (PostID, blog.name))


def GetTemplate(blog):
    html = blog.template.main
    print html

def SaveTemplate(blog, FileContents):
    blog.template.main = FileContents


def Usage():
    print "Usage: %s [-d] <command> [<parameters>] " % ProgramName

    print "   -d:                               print debugging info to STDERR."
    print
    print "Commands:"
    print "   post   <filename>:                posts a file to a weblog"
    print "   p      <filename>:                same as post"
    print "   repost <filename> [<PostID>]:     reposts file to weblog as article <PostID>, or as most recent article if <PostID> is omitted."
    print "   r      <filename> [<PostID>]:     same as repost"
    print "   delete [<PostID>]:                deletes article with PostID, or most recent article if PostID is omitted."
    print "   d      [<PostID>]:                same as delete"
    print "   gettemplate:                      gets the HTML template and writes it to STDOUT."
    print "   gt:                               same as gettemplate."
    print "   savetemplate <filename>:          saves file as the HTML template for this blog."
    print "   st:                               same as savetemplate."
    print 
    print "Note: only operates on the first weblog."
    print 

##----------------------------

def main():
    global debug
    
    if len(sys.argv) < 2:
        Usage()
        sys.exit(0)

    if sys.argv[1] == '-d':
        del sys.argv[1]
        debug = 1
    else:
        debug = 0

    command = sys.argv[1]

    if not ValidCommands.has_key(command):
        Usage()
        Error("'%s' is not a valid command." % command)
        sys.exit(0)

    if len(sys.argv) < ValidCommands[command]:
        Usage()
        Error("%s requires at least %d parameter(s)." % (command, ValidCommands[command] - 1))

    FileName = None
    FileContents = None
    PostID = None

    if command in ['post', 'p', 'repost', 'r', 'savetemplate', 'st']:
        FileName = sys.argv[2]

    if command in ['post', 'p', 'repost', 'r']:
        if len(sys.argv) > 3:
            PostID = sys.argv[3]

    if command in ['delete', 'd']:
        if len(sys.argv) > 2:
            PostID = sys.argv[2]

    UserInfo = GetBlogUsernameAndPassword()
    if UserInfo is None:
        Error("could not read Username and Password.")
    else:
        Username, Password = UserInfo

    if FileName is not None:
        FileContents = ReadFile(FileName)
        if FileContents is None:
            Error("could not read from '%s'." % FileName)

    Message("Getting blog user info...")
    
    user = Blog.User(Username, Password)
    blogs = user.blogs
    
    # fixme: all operations are on the first blog
    blog = blogs[0]

    if command in ['post', 'p']:
        Message("Posting file '%s' to '%s'" % (FileName, blog.name))
        Post(blog, FileContents)
    elif command in ['repost', 'r']:
        if PostID is not None:
            Message("Reposting file '%s' to article '%s' of '%s'" % (FileName, PostID, blog.name))
        else:
            Message("Reposting file '%s' to '%s'" % (FileName, blog.name))
        Repost(blog, FileContents, PostID)
    elif command in ['delete', 'd']:
        if PostID is not None:
            Message("Deleting article '%s' from '%s'." % (PostID,blog.name))
        else:
            Message("Deleting most recent article from '%s'." % blog.name)
        DeletePost(blog, PostID)
    elif command in ['gettemplate','gt']:
        Message("Getting main template from '%s'" % blog.name)
        GetTemplate(blog)
    elif command in ['savetemplate','st']:
        Message("Saving file '%s' as main template of '%s'" % (FileName, blog.name))
        SaveTemplate(blog, FileContents)

##----------------------------


if __name__ == "__main__":

    main()
