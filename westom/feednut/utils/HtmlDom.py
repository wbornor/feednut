#!/usr/bin/env python
'''
- requires Python 2.4, cElementTree, elementtree, and elementtidy.
- also uses Mark Pilgrim's openanything lib
- uses PyXML

see http://effbot.org/downloads/ to download the element* packages


Example usage:
    url = 'http://www.rssgov.com/rssparsers.html'
    dom = HtmlDom(url)
    print dom.evaluate('/html:html/html:head/html:title/text()')
    
    dom = HtmlDom('<html><head></head><body><div class="test">some text</div></body></html>')
    print dom.evaluate('//html:div/text()')

'''

from westom.feednut.libs.openanything import fetch
from elementtidy import TidyHTMLTreeBuilder as tidy
import cElementTree as _etree
from xml.dom.ext.reader import PyExpat
import sys, xml.xpath
    
MOZILLA_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.4) Gecko/20060508 Firefox/1.5.0.4'
XHTML_NAMESPACE = u'http://www.w3.org/1999/xhtml'

class HtmlDom:
    
    def __init__(self, url):
        try:
            f = file(url)
            data = f.read()
            f.close()
        except IOError, e:
            try:
                result = fetch(url, agent=MOZILLA_AGENT)
                data = result['data']
            except:
                raise IOError, 'invalid URL'
        
        # create parser
        parser = tidy.TreeBuilder()
        parser.feed(data)
        xmlText = _etree.tostring(parser.close())
        
        #create the DOM
        reader = PyExpat.Reader()
        self.dom = reader.fromString(xmlText)
        
        self.nss = {u'html': XHTML_NAMESPACE}
        self.context = xml.xpath.Context.Context(self.dom, processorNss=self.nss)
        
    def evaluate(self, expression, node=None):
        ''' evaluates the given xpath expression and returns the nodes '''
        if not node:
            return xml.xpath.Evaluate(expression, context=self.context)
        else:
            cxt = xml.xpath.Context.Context(node, processorNss=self.nss)
            return xml.xpath.Evaluate(expression, context=cxt)


def escapeHTML(s):
    ''' adapted from MochiKit '''
    return s.replace('&', '&amp;'). \
        replace('"', "&quot;"). \
        replace('<', "&lt;"). \
        replace('>', "&gt;")


def toHTML(dom):
    ''' adapted from MochiKit '''
    return ''.join(emitHTML(dom))


def emitHTML(dom):
    ''' adapted from MochiKit '''
    lst = [];
    # queue is the call stack, we're doing this non-recursively
    queue = [dom];
    while len(queue) > 0:
        dom = queue.pop();
        if not hasattr(dom, 'nodeType'):
            lst.append(dom)
        elif dom.nodeType == 1:
            lst.append('<' + dom.nodeName.lower())
            attributes = []
            for i in range(dom.attributes.length):
                attr = dom.attributes.item(i)
                attributes.append(' %s="%s"' % (attr.name, escapeHTML(attr.value)))
            attributes.sort()
            
            for attr in attributes:
                lst.append(attr)
            
            if dom.hasChildNodes():
                lst.append(">")
                # queue is the FILO call stack, so we put the close tag on first
                queue.append("</" + dom.nodeName.lower() + ">")
                cnodes = dom.childNodes
                cnodes.reverse()
                queue += cnodes
            else:
                lst.append('/>')
        elif dom.nodeType == 3:
            lst.append(escapeHTML(dom.nodeValue))
    return lst

    

if __name__ == '__main__':
    for arg in sys.argv[1:]:
        htmldom = HtmlDom(arg)
        from xml.dom.ext import PrettyPrint
        PrettyPrint(htmldom.dom)
    