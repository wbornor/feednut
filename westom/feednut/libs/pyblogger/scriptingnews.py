"""Text to Scripting News XML

This module converts loosely structured text into XML that conforms to
the Scripting News XML format.

About the Scripting News XML format:
  http://my.userland.com/stories/storyReader$11

Specification for text to XML translation:
  http://my.userland.com/stories/storyReader$14
"""

__author__ = "Mark Pilgrim (f8dy@diveintomark.org)"
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2006/03/04 10:07:32 $"
__copyright__ = "Copyright (c) 2001 Mark Pilgrim"
__license__ = "Python"

import re
import cgi
from xml.dom.minidom import Document, Element, Text

_link = re.compile(r'(.*?)<a href=["''](.*?)["''].*?>(.*?)</a>(.*)', re.IGNORECASE + re.DOTALL)

class _TextElement(Element):
    def __init__(self, tag, text):
        Element.__init__(self, tag)
        self.appendChild(Text(text))
        
def _parseItem(itemtext):
    links = []
    while 1:
        match = _link.search(itemtext)
        if not match: break
        prefix, url, linetext, suffix = match.groups()
        links.append((url, linetext))
        itemtext = "%s%s%s" % (prefix, linetext, suffix)
    itemtext = cgi.escape(itemtext)
    return (itemtext, links)

def textToXML(headers, text):
    """convert text to Scripting News XML
    
    Returns: string, complete XML output as single string
    
    Arguments:
    - headers: dictionary of additional headers for <header> node;
      some of these are required, see http://my.userland.com/stories/storyReader$11
    - text: text to convert
    """
    scriptingNewsNode = Element("scriptingNews")
    headernode = Element("header")
    headernode.appendChild(_TextElement("scriptingNewsVersion", "2.0b1"))
    headernode.appendChild(_TextElement("docs", "http://my.userland.com/stories/storyReader$11"))
    for k, v in headers.items():
        headernode.appendChild(_TextElement(k, v))
    scriptingNewsNode.appendChild(headernode)
    itemlist = text.split("\n\n")
    for itemtext in itemlist:
        itemnode = Element("item")
        itemtext, linklist = _parseItem(itemtext)
        itemnode.appendChild(_TextElement("text", itemtext))
        for link in linklist:
            linknode = Element("link")
            url, linetext = link
            linknode.appendChild(_TextElement("url", url))
            linknode.appendChild(_TextElement("linetext", linetext))
            itemnode.appendChild(linknode)
        scriptingNewsNode.appendChild(itemnode)
    doc = Document()
    doc.appendChild(scriptingNewsNode)
    return doc.toxml()
