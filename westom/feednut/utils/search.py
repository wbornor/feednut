"""
Searchp utility functions
"""
from westom.feednut.models import *
from westom.feednut.libs import feedparser
import time
from datetime import datetime
from westom.feednut.utils import misc as misc_utils
from westom.feednut.libs import yahoo_terms
from westom.feednut.libs.BeautifulSoup import BeautifulSoup
from westom.settings import URL_HOST
import re, random
import urllib2
import logging

#unit test
#text="<html><head><link rel='alternate' type='application/rss+xml' href='http://example.com/feed.rss'></link></head></html>"
#links = get_html_alternate_links(text=text, types=['application/rss+xml'])
#assert(links[0] == 'http://example.com/feed.rss')
def get_html_alternate_links(html=None, types=[]):
    """
    Returns a list of xml_url links
    """
    
    links = []
    if not types:
        types=['application/rss+xml', 'application/atom+xml']
        
    try:
        for type in types:
            soup = BeautifulSoup(html)
            for alternate in soup.findAll('link', attrs={'rel':"alternate", 'type':type}):
                links.append(alternate['href'])

        return links

    except Exception:
        return []

def scrape_alternates(html=None, types=[]):
    """
    Returns a list of xml_url links
    """
    
    links = []
    if not types:
        types=['application/rss+xml', 'application/atom+xml']
        
    try:
        for type in types:
            soup = BeautifulSoup(html)
            for alternate in soup.findAll('link', attrs={'rel':"alternate", 'type':type}):
                links.append(alternate['href'])

        return links

    except Exception:
        return []

def scrape_alternates(html=None, types=[]):
    """
    Returns a list of xml_url links
    """
    
    links = []
    if not types:
        types=['application/rss+xml', 'application/atom+xml']
        
    try:
        for type in types:
            soup = BeautifulSoup(html)
            for alternate in soup.findAll('link', attrs={'rel':"alternate", 'type':type}):
                links.append(alternate['href'])

        return links

    except Exception:
        return []

def scrape_anchors(html=None, extensions=['.rss', '.xml', '.atom']):
    """
    Returns a list of xml_url links
    """
    
    links = []
        
    try:

        soup = BeautifulSoup(html)
        for anchor in soup.findAll('a'):
            if any(map(anchor['href'].endswith, ['.rss', '.xml', '.atom'])):
                links.append(anchor['href'])

        return links

    except Exception, e:
#        return []
         raise e
    
#def scrape_alternates(url=None):
#    page = urllib2.urlopen(url)
#    return get_html_alternate_links(page.read())

def scrape_for_feeds(url=None):
    
    html = urllib2.urlopen(url).read()
    url_host = urllib2.Request(url).get_host()
    
    try:
        links = scrape_alternates(html)
        links.extend(scrape_anchors(html))
        
        for link in links:
            try:
                if link.startswith('/'):
                    link = url_host + link
                    
            except:
                pass   
                        
        return links

    except Exception, e:
        #return []
        raise e




def generate_feed(context=None, seed=None):
    
    logging.debug("seed: %s" % seed)
    
    tokens = []
    
    for seedling in seed:
        #logging.debug("seedling: %s" % seedling)
        #logging.debug("context: %s" % context)
        index = context.find(seedling)
        #logging.debug("index: %s" % index)
        token = context[:index]
        #logging.debug("token: %s" % token)
        tokens.append(token)
        context = context[index+len(seedling):]
    
    
    logging.debug("final tokens: %s" % tokens)
    for token in tokens:    
        print token
    return tokens

    
#return a list of Feed objects
#query('http://cnn.com')
#query('http://del.icio.us/rss/wbornor/')
#query('health')
#query('health cnn')
#query('tags:entertainment')
#query('title:health cnn')
#query('description:News for geeks')
def query(query=None):
#
#search first from our database
#    if its a normal url, search through all the channel links
#
#    if its a xml_url, search through all the xml_urls
#
#    if its plain text, search through the titles, descriptions, and tags
#
#if not in our database, and its a url, pull it from the actual page
#    if its an xml_url pull the actual feed into the database
#
#    if its a normal url use get_feed_urls_from_html() and pull those feeds into the database

    pass
