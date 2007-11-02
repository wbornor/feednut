# simpletest
print "Testing some rss calls"

import pydelicious as p
r = []
result = p.getrss(tag="python", popular=0)
r.append(result)
result = p.getrss(tag="python ajax", popular=0)
r.append(result)
result = p.getrss(tag="python", popular=1)
r.append(result)
result = p.getrss(tag="python ajax", popular=1)
r.append(result)
result = p.getrss(tag="python", user="delpy")
r.append(result)
result = p.getrss(user="delpy")
r.append(result)
result = p.getrss(tag="python ajax", user="pydelicious")
r.append(result)
result = p.getrss()
r.append(result)
result = p.getrss(url="http://www.heise.de/")
r.append(result)
result = p.get_userposts("delpy")
r.append(result)
result = p.get_tagposts("python")
r.append(result)
result = p.get_urlposts("http://www.heise.de/")
r.append(result)
result = p.get_popular()
r.append(result)
result = p.get_popular(tag="python")
r.append(result)

for i in range(len(r)):
    if r[i].bozo == 1:
        print "Catched a exception"
        print i
        print r[i]["debug"]
        print "Exception", r[i].bozo_exception
        print dir(r[i].bozo_exception)
    elif type(r[i]["result"]) != type(p.posts()) and r[i]["result"] != p.posts():
        print 
        print "Error with posts"
        print i
        print r[i]["debug"]
        print "result", r[i]["result"]
        print "type", type(r[i]["result"])
        print "Exception", r[i].bozo_exception
print "done"
