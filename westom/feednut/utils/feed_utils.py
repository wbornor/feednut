import sys, os, re, logging, time, shutil, threading
import cPickle as pickle
from string import letters, digits
from datetime import datetime
from dateutil import parser
import PyLucene as lucene

from django.db.models import Q
from westom.feednut.libs import feedparser
from westom.feednut.libs import uuid
from westom.feednut.models import *
from westom.settings import DOCUMENT_ROOT
from westom.feednut.libs import yahoo_terms
from westom.feednut.utils.misc import clean_string, Singleton


def salvage_feed(feed):
    """
    Pass in a feedparser result here for feeds that had problems
    If it is salvageable, we remove the Exception (keeping the bozo status though)
    If not, return None
    """
    ex = feed.get('bozo_exception', None)
    bozo = feed.get('bozo', 0)
    
    if feed.has_key('feed') and feed['feed'].has_key('title') and len(feed.get('entries', [])) > 0:
        if ex:
            feed['bozo_exception'] = str(ex)
        return feed
    
    return None




class FeedDownloader:
    """
    This class can be used to download feeds. It contains disk cacheing
    which can be ignored if you wish.
    
    """
    CACHE_DIR = os.path.join(DOCUMENT_ROOT, '../feedcache')
    
    def __init__(self):
        self._feed_cache = {}
        
    def get_feeds(self, urls, **kwargs):
        feeds = {}
        for url in urls:
            feed = self.get_feed(url, **kwargs)
            if feed:
                feeds[url] = feed
        return feeds
    
    
    def get_cached_feeds(self):
        return self._feed_cache
    
    
    @staticmethod
    def fetch_feed(url, last_modified=None, etag=None):
        """ Does the actual fetching """
        logging.debug('Fetching %s' % url)
        result = feedparser.parse(url, etag=etag, modified=last_modified, agent=None, referrer=None, handlers=[])
        if result and result.get('bozo', 0) == 1:
            result = salvage_feed(result)
        if not result:
            raise Exception, 'Invalid result from feedparser'
        return result
    
    
    def get_feed(self, url, last_modified=None, etag=None, use_cache=False):
        """
        Fetches the feed by url, and returns the FeedParser result object.
        If the feed has problems, we try to salvage it if we can. Otherwise,
        None is returned.
        
        @param last_modified    specify a last_modified date
        @param etag             specify an etag
        @param use_cache        if this is True, will use the disk cache (only use for testing purposes)
        """
        
        if use_cache:
            if url in self._feed_cache:
                return self.feeds[url]
        
            clean_url = clean_string(url)
            save_path = os.path.join(self.CACHE_DIR, clean_url)
            if not os.path.exists(os.path.dirname(save_path)):
                try:
                    os.makedirs(os.path.dirname(save_path))
                except:{}
            
            try:
                if os.path.exists(save_path):
                    f = open(save_path, 'rb')
                    result = pickle.load(f)
                    f.close()
                else:
                    result = self.fetch_feed(url, last_modified, etag)
                    if result.get('status', 200) == 200:
                        f = open(save_path, 'wb')
                        pickle.dump(result, f)
                        f.close()
            except Exception, e:
                logging.error('Problem with %s, %s' % (url, e))
                try:
                    f.close()
                    os.unlink(save_path)
                except:{}
                return None
            else:
                self._feed_cache[url] = result
                return result
                    
        else:
            try:
                return self.fetch_feed(url, last_modified, etag)
            except Exception, e:
                logging.error(e)
                return None


def encode(val, encoding):
    """ encodes the string with the given codec """
    if val:
        val = val.encode(encoding)
    return val


def parse_date(date_str):
    """ attempts to parse a date string """
    if date_str:
        try:
            return parser.parse(entry.get('updated', None), ignoretz=True)
        except:{}
    return None


def make_entryid(link=None):
    """ tries to make a unique entryID """
    if link:
        return link[:255]
    else:
        return str(uuid.uuid4())



def store_feed(feed, url=None, update=True):
    """
    This stores a FeedParser feed object into the database
    Also, stores the feed entries in the database
    
    If update is set to True, will update existing feeds and entries
    Returns a database Feed object
    """
    
    #get the encoding
    encoding = feed.get('encoding', 'utf-8')
    
    kwargs = {
        'xml_url' : url or feed.get('href', None),
        'channel_link' : feed.get('feed', None) and feed['feed'].get('link', None),
        'title' : feed.get('feed', None) and encode(feed['feed'].get('title', None), encoding),
        'subtitle' : feed.get('feed', None) and encode(feed['feed'].get('subtitle', None), encoding),
        'icon_url' : feed.get('feed', None) and feed['feed'].get('image', None) and feed['feed']['image'].get('href', None),
        'etag' : feed.get('headers', None) and encode(feed['headers'].get('etag', None), encoding),
        'updated_date' : feed.get('feed', None) and parse_date(feed['feed'].get('updated', None)),
        'last_modified' : feed.get('headers', None) and parse_date(feed['headers'].get('last-modified', None)),
        'encoding' : encoding,
    }
    
    #TODO do some error checking here to punt if certain fields dont exist (href, title)
    if type(kwargs['title']) is not str:
        logging.error('Invalid feedparser response')
        return None
    
    
    # see if the feed already exists
    try:
        db_feed = Feed.objects.get(xml_url__iexact=kwargs['xml_url'])
    except:
        logging.debug('creating new feed: %s', kwargs['xml_url'])
        # it doesn't exist, so create a new one
        try:
            try:
                suggest_text = '%s %s ' % (kwargs['title'], kwargs['subtitle'])
                kwargs['suggested_tags'] = ' '.join(yahoo_terms.extract_terms(suggest_text, limit=10))
            except:{}
            db_feed = Feed(**kwargs)
            db_feed.save()
        except Exception, e:
            logging.error('Error Creating Feed: %s' % e)
            return None
    else:
        if update:
            # loop through the args and update the feed item...
            logging.debug('updating feed: %s', db_feed.xml_url)
            for arg, val in kwargs.iteritems():
                setattr(db_feed, arg, val)
            try:
                db_feed.save()
            except Exception, e:
                logging.error('Could not update feed: %s, %s' % (kwargs['xml_url'], e))
                return db_feed

    #loop through and make sure each entry has an ID field
    #this way, we can more easily lookup by ID later on if we need
    entries = feed.get('entries', [])
    for entry in entries:
        if not entry.has_key('id') or entry['id'] is None:
            entry['id'] = make_entryid(entry.get('link', None))
    
    #TODO should probably put this in a try block
    db_feed.set_data(feed)
    
    
    ################################################################
    ################################################################
    # Anything dealing with storing entries in the database is for
    # pure testing purposes. For now, we will just return the feed
    # without storing feed entries in the database. This is fine as
    # long as the Feed.get_entries() method returns the entries from
    # disk
    ################################################################
    ################################################################
    
    return db_feed
    #was going to reverse the entries in order to make the newest ones have the newest timestamp
    #    entries.reverse() 
    #was going to reverse the entries in order to make the newest ones have the newest timestamp
    #    entries.reverse()
    for entry in entries:
        kwargs = {
            'entry_id' : encode(entry.get('id', None), encoding),
            'title' : encode(entry.get('title', None), encoding),
            'link' : entry.get('link', None),
            'summary' : encode(entry.get('summary', None), encoding),
            'updated_date' : parse_date(entry.get('updated', None)),
        }

        #TODO check to see if this already exists in the database
        # if it does, then just touch it
        try:
            q = Q(entry_id=kwargs['entry_id']) | Q(title=kwargs['title'])
            if kwargs['link']:
                q |= Q(link=kwargs['link'])
            q = (q) & Q(feed__id__exact=feed.id)
            db_entry = FeedEntry.objects.get(q)
        except:{}
        else:
            if update:
                logging.debug('updating feed entry: %s', db_entry.entry_id)
                for arg, val in kwargs.iteritems():
                    setattr(db_entry, arg, val)
                try:
                    db_entry.save()
                except Exception, e:
                    print 'Could not update an Entry', kwargs['entry_id'], e
            continue
        
        #try to save the NEW entry
        try:
            logging.debug('creating feed entry: %s', db_entry.entry_id)
            db_entry = FeedEntry(feed=db_feed, **kwargs)
            db_entry.save()
        except Exception, e:
            logging.error('Error creating FeedEntry: %s, %s', (kwargs.get('entry_id', None), e))
    
    return db_feed
            


STORE_DIR = os.path.join(DOCUMENT_ROOT, '../index')
FEED_FIELDS = ['url', 'link', 'title', 'subtitle']
FEED_ENTRY_FIELDS = ['feed_url', 'link', 'title', 'summary', 'updated']


class IndexModifier:
    def __init__(self, store_dir=STORE_DIR, destroy=False, analyzer=None):
        self.store_dir = store_dir
        self.create = False
        
        if os.path.exists(self.store_dir) and destroy:
            shutil.rmtree(self.store_dir)
        
        if not os.path.exists(self.store_dir):
            try:
                os.makedirs(self.store_dir)
            except:{}
            self.create = True
        
        self.store = lucene.FSDirectory.getDirectory(self.store_dir, self.create)
        self.analyzer = analyzer or lucene.StandardAnalyzer()
        if self.create:
            self.get_writer(self.create).close() #this inits the segment

    
    def get_writer(self, create=False):
        writer = None
        while writer is None:
            try:
                writer = lucene.IndexWriter(self.store, self.analyzer, create)
                writer.setMaxFieldLength(1048576)
            except Exception, e:
                print e
                time.sleep(.1)
        return writer
    
    
    def get_reader(self):
        reader = None
        while reader is None:
            try:
                reader = lucene.IndexReader.open(self.store)
            except Exception, e:
                print e
                time.sleep(.1)
        return reader
    

class HitHolder:
    def __init__(self, hits, searcher):
        self.hits = hits
        self.searcher = searcher
    
    def doc(self, index):
        return self.hits.doc(index)
    
    def doc_dict(self, index):
        holder = {} 
        doc = self.doc(index)
        fields = doc.fields()
        while fields.hasMoreElements():
            field = fields.nextElement()
            holder[field.name()] = unicode(field.stringValue())
        return holder
    
    def __len__(self):
        return self.hits.length()
    
    def __del__(self):
        try:
            self.searcher.close()
        except:{}
    
    def __getitem__(self, index):
        if type(index) == slice:
            return [self.doc_dict(i) for i in range(max(index.start, 0), min(index.stop, self.hits.length()))]
        else:
            return self.doc_dict(index)
    
    def __iter__(self):
        return [self.doc_dict(i) for i in range(self.hits.length())].__iter__()
        


class FeedIndexModifier:
    """ This needs help -- should do something like the searchable code at
    http://mojodna.net/searchable/
    
    """
    
    def __init__(self, store_dir=STORE_DIR, destroy=False, analyzer=None):
        self.store_dir = store_dir
        self.analyzer = analyzer or lucene.StandardAnalyzer()
        
        self.feed_modifier = IndexModifier(store_dir=os.path.join(store_dir, 'feeds'), destroy=destroy, analyzer=analyzer)
        self.entry_modifier = IndexModifier(store_dir=os.path.join(store_dir, 'entries'), destroy=destroy, analyzer=analyzer)
        
    
    def delete_existing_feed_docs(self, feed):
        """ deletes existing documents relating to the given feed """
        reader = lucene.IndexReader.open(self.feed_modifier.store)
        numDeleted = reader.deleteDocuments(lucene.Term('url', feed.xml_url))
        logging.info('deleted %d existing index documents' % numDeleted)
        reader.close()
        
        reader = lucene.IndexReader.open(self.entry_modifier.store)
        for entry in feed.get_entries():
            try:
                id = '%s:%s' % (feed.xml_url, entry.get('id', None))
                numDeleted = reader.deleteDocuments(lucene.Term('id', id))
                if numDeleted:
                    logging.info('deleted %d feed entry docyments' % numDeleted)
            except:{}
        reader.close()
    
    
    def index_feed(self, feed, feed_data=None):
        """ Indexes the given feed """
        #remove any existing entries for this feed
        self.delete_existing_feed_docs(feed)
        
        writer = self.feed_modifier.get_writer()
        doc = lucene.Document()
        doc.add(lucene.Field('id', str(feed.id), lucene.Field.Store.YES, lucene.Field.Index.UN_TOKENIZED))
        doc.add(lucene.Field('url', feed.xml_url, lucene.Field.Store.YES, lucene.Field.Index.UN_TOKENIZED))
        if feed.channel_link:
            doc.add(lucene.Field('link', feed.channel_link, lucene.Field.Store.YES, lucene.Field.Index.UN_TOKENIZED))
        if feed.title:
            doc.add(lucene.Field('title', feed.title, lucene.Field.Store.YES, lucene.Field.Index.TOKENIZED))
        if feed.subtitle:
            doc.add(lucene.Field('subtitle', feed.subtitle, lucene.Field.Store.YES, lucene.Field.Index.TOKENIZED))
        writer.addDocument(doc)
        writer.close()
        logging.info('Indexed Feed: %s' % feed.xml_url)
        
        writer = self.entry_modifier.get_writer()
        for entry in feed.get_entries():
            try:
                doc = lucene.Document()
                id = '%s:%s' % (feed.xml_url, entry.get('id', None))
                doc.add(lucene.Field('id', id, lucene.Field.Store.YES, lucene.Field.Index.UN_TOKENIZED))
                doc.add(lucene.Field('feed_url', feed.xml_url, lucene.Field.Store.YES, lucene.Field.Index.UN_TOKENIZED))
                if entry.get('title', None):
                    doc.add(lucene.Field('title', entry['title'], lucene.Field.Store.YES, lucene.Field.Index.TOKENIZED))
                if entry.get('summary', None):
                    doc.add(lucene.Field('summary', entry['summary'], lucene.Field.Store.YES, lucene.Field.Index.TOKENIZED))
                if entry.get('link', None):
                    doc.add(lucene.Field('link', entry['link'], lucene.Field.Store.YES, lucene.Field.Index.UN_TOKENIZED))
                updated = parse_date(entry.get('updated', None))
                if updated:
                    doc.add(lucene.Field('updated', updated.isoformat(' '), lucene.Field.Store.YES, lucene.Field.Index.NO))
                doc.add(lucene.Field('pickle', pickle.dumps(entry), lucene.Field.Store.YES, lucene.Field.Index.NO))
                writer.addDocument(doc)
                logging.info('Indexed Feed Entry: %s' % entry.get('title', None) or id)
            except:{}
        writer.close()
    
    
    def search(self, query, fields=FEED_ENTRY_FIELDS, analyzer=None, store=None):
        if not query or len(query.strip()) == 0 or len(fields) == 0:
            return None
        analyzer = analyzer or self.analyzer
        if store is None:
            store = self.entry_modifier.store
        
        if len(fields) > 1:
            qp = lucene.MultiFieldQueryParser(fields, analyzer)
        else:
            qp = lucene.QueryParser(fields[0], analyzer)
        q = qp.parse(query)
        
        searcher = lucene.IndexSearcher(store)
        hits = searcher.search(q, lucene.Sort.RELEVANCE)
        return HitHolder(hits, searcher)

    
    def search_entries(self, query, fields=FEED_ENTRY_FIELDS, analyzer=None):
        return self.search(query, fields=fields, analyzer=analyzer, store=self.entry_modifier.store)
    
    def search_feeds(self, query, fields=FEED_FIELDS, analyzer=None):
        return self.search(query, fields=fields, analyzer=analyzer, store=self.feed_modifier.store)
        

FeedIndex = FeedIndexModifier


from westom.feednut.utils.lucene_utils import FeedIndexer
def get_feed(url, last_modified=None, etag=None, index=True, update=False):
    """ Fetches the feed and stores it in the database. Also, indexes it by default """
    try:
        db_feed = Feed.objects.get(xml_url__iexact=url)
    except:
        db_feed = None
    if update or not db_feed:
        feed_data = FeedDownloader().get_feed(url, last_modified, etag, use_cache=False)
        if feed_data:
            db_feed = store_feed(feed_data, url=url, update=update)
#    if index and db_feed:
#        FeedIndex().index_feed(db_feed)
    return db_feed


def update_feeds(urls, index=True):
    feedMap = FeedDownloader().get_feeds(urls, use_cache=False)
    feeds = []
    for url, feed_data in feedMap.iteritems():
        feeds.append(store_feed(feed_data, url=url, update=True))
#    if index:
#        FeedIndexer().index_feeds(feeds)
    return feeds
    

#def get_feeds(urls, index=True, update=False):
#    """ returns dict of (url, db_feed) of all feeds that were fetched and stored """
#    feeds = {}
#    for url in urls:
#        feed = FeedDownloader().get_feed(url, use_cache=False)
#        if feed:
#            db_feed = store_feed(feed, update=update)
#            feeds[url] = db_feed
#            .index_feed(feed)
#        indexer = FeedIndexer()
#    return feeds

