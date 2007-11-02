"""Unit tests for blogger.py

These require PyUnit (unittest.py), which is part of the standard library
starting with Python 2.1.
"""

__author__ = "Mark Pilgrim (f8dy@diveintomark.org)"
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2006/03/04 10:07:32 $"
__copyright__ = "Copyright (c) 2001 Mark Pilgrim"
__license__ = "Python"

import unittest
import blogger
import xmlrpclib
import new
import time
import copy
import random
from xml.dom import minidom

class constants:
    blogID = "1000"
    title = "Fake blog"
    url = "http://localhost/default.ida"
    email = "me@mydomain.org"
    userID = "999"
    nickname = "nicky"
    firstname = "first"
    lastname = "last"
    username = "username"
    password = "password"
    invalidUsername = "wrong username"
    invalidPassword = "wrong password"
    template = {"main":"main template",
                "archiveIndex":"archive index template"}
    autoPostText = "This post intentionally contains the following random number: %s"
c = constants()

# utility functions to insert into minidom.Node class
def _all(self, tagname):
    return self.getElementsByTagName(tagname)
minidom.Node.all = new.instancemethod(_all, None, minidom.Node)

def _first(self, path):
    node = self
    for name in path.split("/"):
        node = node.all(name)[0]
    return node
minidom.Node.first = new.instancemethod(_first, None, minidom.Node)

def _text(self):
    try:
        return str(self.firstChild.data)
    except:
        return ""
minidom.Node.text = new.instancemethod(_text, None, minidom.Node)

def text(element):
    return element.text()

# fake XML-RPC server to facilitate local testing;
# this acts just like the Blogger.com server, but with a hard-coded blog
class FakeTransport:
    authFailed = "Error: User authentication failed: %s"
    postNotFound = "Post %s not found"
    noPerms = "ERROR: User does not have permission to post to this blog."
    
    def __init__(self):
        self.posts = [{"dateCreated":xmlrpclib.DateTime(time.time()),
                       "userid":c.userID,
                       "postid":'3',
                       "content":"Third post!"},
                      {"dateCreated":xmlrpclib.DateTime(time.time()),
                       "userid":c.userID,
                       "postid":'2',
                       "content":"Second post!"},
                      {"dateCreated":xmlrpclib.DateTime(time.time()),
                       "userid":c.userID,
                       "postid":'1',
                       "content":"First post!"}]
        self.template = copy.deepcopy(c.template)
        self.nextPostID = len(self.posts) + 1
        
    def request(self, host, handler, request_body, verbose=0):
        xmldoc = minidom.parseString(request_body)
        methodName = xmldoc.first("methodName").text().replace("blogger.", "")
        return getattr(self, "do_%s" % methodName)(xmldoc)

    def _err(self, message="error"):
        raise xmlrpclib.Fault(0, message)
    
    def do_getUserInfo(self, doc):
        appkey, username, password = map(text, doc.all("string"))
        if (username <> c.username) or (password <> c.password):
            self._err(self.authFailed % username)
        return ({"nickname":c.nickname,
                 "userid":c.userID,
                 "url":c.url,
                 "email":c.email,
                 "lastname":c.lastname,
                 "firstname":c.firstname},)
    
    def do_getUsersBlogs(self, doc):
        appkey, username, password = map(text, doc.all("string"))
        if (username <> c.username) or (password <> c.password):
            self._err(self.authFailed % username)
        return ([{"blogid":c.blogID,
                  "blogName":c.title,
                  "blogURL":c.url}],)

    def do_getPost(self, doc):
        appkey, postID, username, password = map(text, doc.all("string"))
        if (username <> c.username) or (password <> c.password):
            self._err(self.authFailed % username)
        findPost = lambda d, p=postID: d["postid"]==p
        found = filter(findPost, self.posts)
        if found:
            return copy.deepcopy(found)
        else:
            self._err(self.postNotFound % postID)
        
    def do_getRecentPosts(self, doc):
        appkey, blogID, username, password = map(text, doc.all("string"))
        maxposts = int(doc.first("int").text())
        if blogID <> c.blogID:
            self._err(self.noPerms)
        if (username <> c.username) or (password <> c.password):
            self._err(self.authFailed % username)
        return copy.deepcopy(self.posts)[:maxposts]

    def do_newPost(self, doc):
        appkey, blogID, username, password, content = map(text, doc.all("string"))
        if blogID <> c.blogID:
            self._err(self.noPerms)
        if (username <> c.username) or (password <> c.password):
            self._err(self.authFailed % username)
        postID = str(self.nextPostID)
        self.nextPostID += 1
        self.posts.insert(0, {"dateCreated":xmlrpclib.DateTime(time.time()),
                              "userid":c.userID,
                              "postid":postID,
                              "content":content})
        return postID

    def do_editPost(self, doc):
        appkey, postID, username, password, content = map(text, doc.all("string"))
        if (username <> c.username) or (password <> c.password):
            self._err(self.authFailed % username)
        findPost = lambda d, p=postID: d["postid"]==p
        found = filter(findPost, self.posts)
        if found:
            found[0]["content"] = content
            return (xmlrpclib.True,)
        else:
            self._err(self.postNotFound % postID)

    def do_deletePost(self, doc):
        appkey, postID, username, password = map(text, doc.all("string"))
        if (username <> c.username) or (password <> c.password):
            self._err(self.authFailed % username)
        for i in range(len(self.posts)):
            if self.posts[i]["postid"] == postID:
                del self.posts[i]
                return (xmlrpclib.True,)
        self._err("Post %s not found" % postID)

    def do_getTemplate(self, doc):
        appkey, blogID, username, password, templatetype = map(text, doc.all("string"))
        if blogID <> c.blogID:
            self._err(self.noPerms)
        if (username <> c.username) or (password <> c.password):
            self._err(self.authFailed % username)
        return self.template[templatetype]

    def do_setTemplate(self, doc):
        appkey, blogID, username, password, html, templatetype = map(text, doc.all("string"))
        if blogID <> c.blogID:
            self._err(self.noPerms)
        if (username <> c.username) or (password <> c.password):
            self._err(self.authFailed % username)
        self.template[templatetype] = html
        return (xmlrpclib.True,)

##----------------------- unit tests -----------------------##

def getRandomNumber():
    return str(random.randint(0, 100000))

class BaseTest(unittest.TestCase):
    def setUp(self):
        blogger.constants.transport = FakeTransport()
        self.checkPosts = blogger.constants.transport.posts
        self.checkTemplate = blogger.constants.transport.template

class GetUserInfoTest(BaseTest):
    def testNickname(self):
        """getUserInfo returns known nickname"""
        info = blogger.getUserInfo(c.username, c.password)
        self.assertEqual(info["nickname"], c.nickname)
        
    def testUserID(self):
        """getUserInfo returns known user ID"""
        info = blogger.getUserInfo(c.username, c.password)
        self.assertEqual(info["userid"], c.userID)
        
    def testURL(self):
        """getUserInfo returns known URL"""
        info = blogger.getUserInfo(c.username, c.password)
        self.assertEqual(info["url"], c.url)
        
    def testEmail(self):
        """getUserInfo returns known email"""
        info = blogger.getUserInfo(c.username, c.password)
        self.assertEqual(info["email"], c.email)
        
    def testLastName(self):
        """getUserInfo returns known last name"""
        info = blogger.getUserInfo(c.username, c.password)
        self.assertEqual(info["lastname"], c.lastname)
        
    def testFirstName(self):
        """getUserInfo returns known first name"""
        info = blogger.getUserInfo(c.username, c.password)
        self.assertEqual(info["firstname"], c.firstname)
        
    def testNoOtherReturnValues(self):
        """getUserInfo returns only known keys"""
        info = blogger.getUserInfo(c.username, c.password)
        self.assertEqual(len(info.keys()), 6)
        
    def testFailsWithInvalidUsername(self):
        """getUserInfo fails with invalid username"""
        self.assertRaises(blogger.xmlrpclib.Fault, blogger.getUserInfo, c.invalidUsername, c.password)

    def testFailsWithInvalidPassword(self):
        """getUserInfo fails with invalid password"""
        self.assertRaises(blogger.xmlrpclib.Fault, blogger.getUserInfo, c.username, c.invalidPassword)

class ListBlogsTest(BaseTest):
    def testCount(self):
        """listBlogs says I have 1 blog"""
        blogs = blogger.listBlogs(c.username, c.password)
        self.assertEqual(len(blogs), 1)

    def testBlogID(self):
        """listBlogs returns known blog ID"""
        blogs = blogger.listBlogs(c.username, c.password)
        self.assertEqual(blogs[0]["blogid"], c.blogID)

    def testBlogName(self):
        """listBlogs returns known blog name"""
        blogs = blogger.listBlogs(c.username, c.password)
        self.assertEqual(blogs[0]["blogName"], c.title)

    def testBlogURL(self):
        """listBlogs returns known blog URL"""
        blogs = blogger.listBlogs(c.username, c.password)
        self.assertEqual(blogs[0]["blogURL"], c.url)

    def testFailsWithInvalidUsername(self):
        """listBlogs fails with invalid username"""
        self.assertRaises(blogger.xmlrpclib.Fault, blogger.listBlogs, c.invalidUsername, c.password)

    def testFailsWithInvalidPassword(self):
        """listBlogs fails with invalid password"""
        self.assertRaises(blogger.xmlrpclib.Fault, blogger.listBlogs, c.username, c.invalidPassword)

class ListPostsTest(BaseTest):
    def testCount(self):
        """listPosts says I have 3 posts"""
        posts = blogger.listPosts(c.blogID, c.username, c.password)
        self.assertEqual(len(posts), 3)

    def testPostID(self):
        """listPosts returns known post ID"""
        posts = blogger.listPosts(c.blogID, c.username, c.password)
        self.assertEqual(posts[0]["postid"], "1")

    def testUserID(self):
        """listPosts returns known user ID"""
        posts = blogger.listPosts(c.blogID, c.username, c.password)
        self.assertEqual(posts[1]["userid"], c.userID)

    def testContent(self):
        """listPosts returns known content"""
        posts = blogger.listPosts(c.blogID, c.username, c.password)
        self.assertEqual(posts[2]["content"], "Third post!")

    def testPartialListing(self):
        """listPosts returns partial listing"""
        posts = blogger.listPosts(c.blogID, c.username, c.password, 2)
        self.assertEqual(len(posts), 2)

    def testFailsWithInvalidBlogID(self):
        """listPosts fails with invalid blog ID"""
        self.assertRaises(blogger.xmlrpclib.Fault, blogger.listPosts, 0, c.username, c.password)

    def testFailsWithInvalidUsername(self):
        """listPosts fails with invalid username"""
        self.assertRaises(blogger.xmlrpclib.Fault, blogger.listPosts, c.blogID, c.invalidUsername, c.password)

    def testFailsWithInvalidPassword(self):
        """listPosts fails with invalid password"""
        self.assertRaises(blogger.xmlrpclib.Fault, blogger.listPosts, c.blogID, c.username, c.invalidPassword)

class GetPostTest(BaseTest):
    def testUserID(self):
        """getPost returns known user ID"""
        post = blogger.getPost(1, c.username, c.password)
        self.assertEqual(post["userid"], c.userID)

    def testContent(self):
        """getPost returns known content"""
        post = blogger.getPost(3, c.username, c.password)
        self.assertEqual(post["content"], "Third post!")

    def testFailsWithInvalidPostID(self):
        """getPost fails with invalid post ID"""
        self.assertRaises(blogger.xmlrpclib.Fault, blogger.getPost, 0, c.username, c.password)
        
    def testFailsWithInvalidUsername(self):
        """getPost fails with invalid username"""
        self.assertRaises(blogger.xmlrpclib.Fault, blogger.getPost, 1, c.invalidUsername, c.password)

    def testFailsWithInvalidPassword(self):
        """getPost fails with invalid password"""
        self.assertRaises(blogger.xmlrpclib.Fault, blogger.getPost, 1, c.username, c.invalidPassword)
    
class NewPostTest(BaseTest):
    def testNewPost(self):
        """newPost happy path"""
        randomNumber = getRandomNumber()
        postText = c.autoPostText % randomNumber
        postID = blogger.newPost(c.blogID, c.username, c.password, postText, 1)
        self.assert_(self.checkPosts[0]["content"].find(randomNumber) >= 0)

    def testFailsWithInvalidBlogID(self):
        """newPost fails with invalid blog ID"""
        self.assertRaises(blogger.xmlrpclib.Fault, blogger.newPost, 0, c.username, c.password, "abc", 1)
        
    def testFailsWithInvalidUsername(self):
        """newPost fails with invalid username"""
        self.assertRaises(blogger.xmlrpclib.Fault, blogger.newPost, c.blogID, c.invalidUsername, c.password, "abc", 1)

    def testFailsWithInvalidPassword(self):
        """newPost fails with invalid password"""
        self.assertRaises(blogger.xmlrpclib.Fault, blogger.newPost, c.blogID, c.username, c.invalidPassword, "abc", 1)
        
class EditPostTest(BaseTest):
    def testEditPost(self):
        """edit post happy path"""
        randomNumber = getRandomNumber()
        postText = c.autoPostText % randomNumber
        blogger.editPost(2, c.username, c.password, postText, 1)
        self.assert_(self.checkPosts[-2]["content"].find(randomNumber) >= 0)

    def testFailsWithInvalidPostID(self):
        """editPost fails with invalid post ID"""
        self.assertRaises(blogger.xmlrpclib.Fault, blogger.editPost, 0, c.username, c.password, "abc", 1)
        
    def testFailsWithInvalidUsername(self):
        """editPost fails with invalid username"""
        self.assertRaises(blogger.xmlrpclib.Fault, blogger.editPost, c.blogID, c.invalidUsername, c.password, "abc", 1)

    def testFailsWithInvalidPassword(self):
        """editPost fails with invalid password"""
        self.assertRaises(blogger.xmlrpclib.Fault, blogger.editPost, c.blogID, c.username, c.invalidPassword, "abc", 1)

class DeletePostTest(BaseTest):
    def testDeletePost(self):
        """deletePost happy path"""
        blogger.deletePost(3, c.username, c.password, 1)
        self.assertEqual(len(self.checkPosts), 2)
        self.assertEqual(self.checkPosts[0]["postid"], "2")
        self.assertEqual(self.checkPosts[1]["postid"], "1")

    def testInvalidPostID(self):
        """deletePost fails with invalid post ID"""
        self.assertRaises(blogger.xmlrpclib.Fault, blogger.deletePost, 0, c.username, c.password, 1)

    def testInvalidUsername(self):
        """deletePost fails with invalid username"""
        self.assertRaises(blogger.xmlrpclib.Fault, blogger.deletePost, c.blogID, c.invalidUsername, c.password, 1)

    def testInvalidPassword(self):
        """deletePost fails with invalid password"""
        self.assertRaises(blogger.xmlrpclib.Fault, blogger.deletePost, c.blogID, c.username, c.invalidPassword, 1)

class GetTemplateTest(BaseTest):
    def testGetMainTemplate(self):
        """getTemplate happy path (main template)"""
        data = blogger.getTemplate(c.blogID, c.username, c.password, blogger.TemplateType.main)
        self.assertEqual(data, c.template["main"])

    def testGetArchiveIndexTemplate(self):
        """getTemplate happy path (archive index template)"""
        data = blogger.getTemplate(c.blogID, c.username, c.password, blogger.TemplateType.archiveIndex)
        self.assertEqual(data, c.template["archiveIndex"])

    def testFailsWithInvalidBlogID(self):
        """getTemplate fails with invalid blog ID"""
        self.assertRaises(blogger.xmlrpclib.Fault, blogger.getTemplate, 0, c.username, c.password)
        
    def testFailsWithInvalidTemplateType(self):
        """getTemplate fails with invalid template type"""
        self.assertRaises(ValueError, blogger.getTemplate, c.blogID, c.username, c.password, "abc")

    def testFailsWithInvalidUsername(self):
        """getTemplate fails with invalid username"""
        self.assertRaises(blogger.xmlrpclib.Fault, blogger.getTemplate, c.blogID, c.invalidUsername, c.password)

    def testFailsWithInvalidPassword(self):
        """getTemplate fails with invalid password"""
        self.assertRaises(blogger.xmlrpclib.Fault, blogger.getTemplate, c.blogID, c.username, c.invalidPassword)

class SetTemplateTest(BaseTest):
    def testSetMainTemplate(self):
        """setTemplate happy path (main template)"""
        randomNumber = getRandomNumber()
        blogger.setTemplate(c.blogID, c.username, c.password, randomNumber, blogger.TemplateType.main)
        self.assertEqual(self.checkTemplate["main"], randomNumber)
        
    def testSetArchiveIndexTemplate(self):
        """setTemplate happy path (archive index template)"""
        randomNumber = getRandomNumber()
        blogger.setTemplate(c.blogID, c.username, c.password, randomNumber, blogger.TemplateType.archiveIndex)
        self.assertEqual(self.checkTemplate["archiveIndex"], randomNumber)

    def testFailsWithInvalidBlogID(self):
        """setTemplate fails with invalid blog ID"""
        self.assertRaises(blogger.xmlrpclib.Fault, blogger.setTemplate, 0, c.username, c.password, "")
        
    def testFailsWithInvalidTemplateType(self):
        """setTemplate fails with invalid template type"""
        self.assertRaises(ValueError, blogger.setTemplate, c.blogID, c.username, c.password, "", "abc")

    def testFailsWithInvalidUsername(self):
        """setTemplate fails with invalid username"""
        self.assertRaises(blogger.xmlrpclib.Fault, blogger.setTemplate, c.blogID, c.invalidUsername, c.password, "abc")

    def testFailsWithInvalidPassword(self):
        """setTemplate fails with invalid password"""
        self.assertRaises(blogger.xmlrpclib.Fault, blogger.setTemplate, c.blogID, c.username, c.invalidPassword, "abc")

if __name__ == "__main__":
    unittest.main()
