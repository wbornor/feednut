# -*- coding: cp1252 -*-
import sys
import unittest
import new
import types
import pydelicious as p
reload(p)

#---------- old test cases taken from original pydelicioustest ----------
class TestHelperFunctions(unittest.TestCase):

    def teststr2uni(self):
        t = {'a':u'a', u'a':u'a', 'ä':u'\xe4', u'ä':u'\xe4'}
        [self.assert_(p.str2uni(i) == t[i]) for i in t]

    def teststr2utf8(self):
        t = {'a':'a', u'a':'a', 'ä':'\xc3\xa4', u'ä':'\xc3\xa4'}
        [self.assert_(p.str2utf8(i) == t[i]) for i in t]

    def testdict0(self):
        t0 = [{"a":"a", "b":"", "c":"c", "d":"", "e":" "}]
        t1 = [{"a":"a", "c":"c", "e":" "}]
        [self.assert_(p.dict0(t0[i]) == t1[i]) for i in range(len(t0))]

    def testxdict(self):
        xdict = p.xdict
        t0 = [xdict(a=1).a,xdict(a="1").a, xdict(a="").a, xdict(a="a").a]
        t1 = [1, "1","","a"]
        [self.assertEqual(t0[i],t1[i]) for i in range(len(t0))]


class TestPost(unittest.TestCase):

    def testpost1(self):
        t0 = [dict(href = "h"), dict(dt = "dt"), dict(time = "time"), dict(tag = "tag"), dict(tags = "tags")]
        t1 = [{'count': '', 'extended': '', 'hash': '', 'description': '', 'href': 'h', 'tags': '', 'user': '', 'dt': ''},
              {'count': '', 'extended': '', 'hash': '', 'description': '', 'href': '', 'tags': '', 'user': '', 'dt': 'dt'},
              {'count': '', 'extended': '', 'hash': '', 'description': '', 'href': '', 'tags': '', 'user': '', 'dt': 'time'},
              {'count': '', 'extended': '', 'hash': '', 'description': '', 'href': '', 'tags': 'tag', 'user': '', 'dt': ''},
              {'count': '', 'extended': '', 'hash': '', 'description': '', 'href': '', 'tags': 'tags', 'user': '', 'dt': ''}]
        for i in range(len(t0)):
            self.assert_(p.post(**t0[i]) == t1[i])

    def testpost2(self):
        t0 = [dict(href = "h"), dict(dt = "dt"), dict(time = "time"), dict(tag = "tag"), dict(tags = "tags")]
        t2 = [dict(href = "h"), dict(dt = "dt"), dict(dt = "time"), dict(tags = "tag"), dict(tags = "tags")]
        for i in range(len(t0)):
            self.assert_(p.dict0(p.post(**t0[i])) == t2[i])

    def testpost3(self):
        t0 = [p.post(href="href").href, p.post(href="href")["href"],
              p.post(user="user").user, p.post(user="user")["user"],
              p.post().user, p.post()["user"]]
        t1 = ["href", "href", "user", "user", "", ""]
        for i in range(len(t0)):
              self.assert_(t0[i] == t1[i])

class TestPosts(unittest.TestCase):

    def testposts1(self):
        p_  = p.post
        pp = p.posts
        t0 = [pp(p_(href="href"), p_(href="href2"))]
        t1 = [['href', 'href2']]
        for i in range(len(t0)):
            self.assert_(t0[i].href == t1[i])

#---------- old test cases for the API calls taken from original pydelicioustest ----------

class TestApiCalls(unittest.TestCase):

    def setUp(self):
        self.a = p.apiNew(user, passwd)
        
    def test_tags_get(self):
        r = self.a.tags_get()
        if r.bozo: print "test_tags_get",r.bozo_exception
        
    def test_tags_rename(self):
        r = self.a.tags_rename("tag", "taag")        
        if r.bozo: print "test_tags_rename",r.bozo_exception
        r = self.a.tags_rename("taag", "tag")        
        if r.bozo: print "test_tags_rename",r.bozo_exception

    def test_posts_update(self):
        r = self.a.posts_update()
        if r.bozo: print "test_posts_update",r.bozo_exception

    def test_posts_dates(self):
        r = self.a.posts_dates()
        if r.bozo: print "test_posts_dates",r.bozo_exception

    def test_post_get(self):
        r = self.a.posts_get(tag="akjs")
        if r.bozo: print "test_post_get",r.bozo_exception

    def test_posts_recent(self):
        r = self.a.posts_recent()
        if r.bozo: print "test_posts_recent",r.bozo_exception

    def test_posts_all(self):
        r = self.a.posts_all()
        if r.bozo: print "test_posts_all",r.bozo_exception

    def test_posts_add(self):
        r = self.a.posts_add("http://url.de/", "desc")
        if r.bozo: print "test_posts_add",r.bozo_exception
        r = self.a.posts_delete("http://url.de/")
        if r.bozo: print "test_posts_add",r.bozo_exception

    def test_post_via_api_has_user(self):
        r = self.a.posts_get()
        if r.bozo:
            print "test_post_via_api_has_user", r.bozo_exception
            return ""
        user = r["result"][0]['user']
        if self.a.user != "" and r != []:
            self.assertEqual(self.a.user, user)
    
class TestAdd(unittest.TestCase):

    def testadd1(self):
        if user == '' or passwd == '': return ''
        r=p.get(user,passwd)
        if r.bozo:
            print "testadd1",r.bozo_exception
            return ""
        pa = p.add
        self.assertEqual(pa(user, passwd, "http://www.testurl.de/", "description", tags="täg tag tuck", replace="yes")["result"],1)
        self.assertEqual(pa(user, passwd, "http://www.testurl.de/", "description", tags="täg tag tuck")["result"],0)

class TestDelete(unittest.TestCase):

    def testdelete1(self):
        if user == '' or passwd == '': return ''
        pd = p.delete
        r=p.get(user,passwd)
        if r.bozo:
            print "testdelete1",r.bozo_exception
            return ""
        self.assertEqual(pd(user, passwd, "http://www.testurl.de/")["result"],1)
        self.assertEqual(pd(user, passwd, "http://www.testurl.de/")["result"],1)

class TestGet(unittest.TestCase):

    def testget(self):
        if user == '' or passwd == '': return ''
        r1 = p.get(user, passwd)
        r2 = p.get(user, passwd, count = 2)
        if r1.bozo:
            print "testget:",r1.bozo_exception
            return ""
        if len(r1.result) > 2: self.assertEqual(len(r2.result),2)
        else: self.assertEqual(len(r1.result), len(r2.result))
        
#---------- a simple bug testing testcase ----------

class TestBug(unittest.TestCase):

    def test_bug_missing_http_request_showData(self):
        if user == '': return ''
        a = p.apiNew(user, passwd)
        r = a.posts_add("http://11833/", "D", "aws","sla")
        r2 = a.posts_delete("http://11833/")
        if r.bozo:
            print r.bozo_exception
            return ""
        self.assert_(r.http_request.showData() != '')
        self.assert_(r.http_request.showData() != '')


#---------- dummy test case class (test methods are added dynamically) ----------

class TestCase(unittest.TestCase):
    pass


#---------- testfunction for the postObject ----------

def checkPostObject(postObject):
    if postObject.bozo == 0 and type(postObject["result"]) == type(p.posts()):
        return 1
    elif postObject.bozo == 1:
        l = "ERROR REASON: " + str(postObject.bozo_exception)
        e = postObject.bozo_exception
        if "reason" in dir(e) and e.reason[0] == 11001:
            print "No Connection to the server available", 
            return 1
        return l
    elif type(postObject["result"]) == type(p.posts()):
        l = "EROOR POSTOBJECT:" + repr(postObject["result"])
        return l
#---------- testing all the possible calls to the rss interface ----------
testrss = [checkPostObject,
           dict(func = p.getrss,
                args = [ dict(tag="python", popular=0),
                         dict(tag="python ajax", popular=0),
                         dict(tag="python", popular=1),
                         dict(tag="python ajax", popular=1),
                         dict(tag="python", user="delpy"),
                         dict(user="delpy"),
                         dict(tag="python ajax", user="pydelicious"),
                         dict(url="http://www.heise.de/"),
                         dict() ],),
           dict(func = p.get_userposts,
                args = [ dict(user="delpy") ] ) ,
           dict(func = p.get_tagposts,
                args = [ dict(tag = "python") ] ),
           dict(func = p.get_urlposts,
                args = [ dict(url = "http://www.heise.de/") ] ),
           dict(func = p.get_popular,
                args = [ dict(),
                         dict(tag = "python" ) ] ) ]


testbugs = [dict(func = p.getrss,
                  args = [ dict(tag="read", user="deepakjois")],
                  doc = "this refers to an email I got from an user. thnx to him."), ]


#---------- putting all the testcases together ----------
__tests__ = [testrss, testbugs]

if __name__ == '__main__':
    if len(sys.argv)>1 and sys.argv[1][0:4]=="--p=":
        user, passwd = sys.argv[1][4:].split(":")
        if passwd =="": passwd = user
        sys.argv.pop(1)
    else:
        user = raw_input("Username (hit return to skip api test):")
        if user:  passwd = raw_input("Passwd (hit return to skip api test):")
        else: passwd = ""
    print "running with username '%s' and passwd '%s'"%(user, passwd)
    # buildcases 2
    for testarea in __tests__:
        for t in testarea:
            if type(t) == types.FunctionType:
                checkFunc = t
                continue
            i = 0
            method = t["func"]
            for kkwargs in t["args"]:
                i = i + 1
                testName = "test_%s_%s_%s" % (testarea, method.__name__,i)
                testFunc = lambda self, method=method, kkwargs=kkwargs: self.assertEqual(checkFunc(method(**kkwargs)),1)  
                instanceMethod = new.instancemethod(testFunc, None, TestCase)
                setattr(TestCase, testName, instanceMethod)
                
    unittest.main()
