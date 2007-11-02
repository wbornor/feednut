import os, logging
from PyLucene import FSDirectory, IndexReader, IndexModifier, StandardAnalyzer, \
                     IndexSearcher, Document, Term, Field, Sort, MultiFieldQueryParser, \
                     QueryParser
from dateutil import parser
import cPickle as pickle
from westom.settings import DOCUMENT_ROOT


class IndexSupport:
    indexDirectories = {}
    readers = {}
    modifiers = {}
    searchers = {}
    
    def __init__(self, indexPath, batchMode=False, analyzer=None):
        self.batchMode = batchMode
        self.indexPath = indexPath
        self.analyzer = analyzer or StandardAnalyzer()
    
    
    def getIndexDirectory(self):
        if not IndexSupport.indexDirectories.has_key(self.indexPath):
            if not os.path.exists(self.indexPath):
                os.makedirs(self.indexPath)
            IndexSupport.indexDirectories[self.indexPath] = FSDirectory.getDirectory(self.indexPath, False)
        return IndexSupport.indexDirectories[self.indexPath]
    
    
    def getIndexReader(self):
        if IndexSupport.readers.has_key(self.indexPath):
            if not IndexSupport.readers[self.indexPath].isCurrent() and not self.batchMode:
                logging.debug('Refreshing reader...')
                IndexSupport.readers[self.indexPath] = IndexReader.open(self.indexPath)
        else:
            logging.debug('Creating reader...')
            IndexSupport.readers[self.indexPath] = IndexReader.open(self.indexPath)
        return IndexSupport.readers[self.indexPath]
    
    
    def getIndexModifier(self):
        if IndexSupport.modifiers.has_key(self.indexPath):
            return IndexSupport.modifiers[self.indexPath]
        logging.debug("Creating an IndexModifier...")
        try:
            IndexSupport.modifiers[self.indexPath] = IndexModifier(self.indexPath, self.analyzer, False)
        except:
            # a failure opening a non-existent index causes it to be locked anyway
            logging.debug('unlocking indexreader and creating new index')
            IndexReader.unlock(self.getIndexDirectory())
            IndexSupport.modifiers[self.indexPath] = self.createIndex()
        return IndexSupport.modifiers[self.indexPath]
    
    
    def getIndexSearcher(self):
#        if not IndexSupport.searchers.has_key(self.indexPath) or not IndexSupport.searchers[self.indexPath].getIndexReader().isCurrent():
#            IndexSupport.searchers[self.indexPath] = IndexSearcher(self.getIndexReader())
#        return IndexSupport.searchers[self.indexPath]
        return IndexSearcher(self.getIndexReader())

        
    def createIndex(self):
        logging.debug('Creating index: %s' % self.indexPath)
        if IndexSupport.modifiers.has_key(self.indexPath):
            IndexSupport.modifiers[self.indexPath].close()
        IndexSupport.modifiers[self.indexPath] = IndexModifier(self.indexPath, self.analyzer, True)
        return IndexSupport.modifiers[self.indexPath]
    
    
    def optimizeIndex(self):
        logging.debug('optimizing index: %s' % self.indexPath)
        self.getIndexModifier().optimize()
    
    
    def close(self):
        #TODO flush if batch
        self.optimizeIndex()
        if IndexSupport.readers.has_key(self.indexPath):
            IndexSupport.readers[self.indexPath].close()
            del IndexSupport.readers[self.indexPath]
        if IndexSupport.modifiers.has_key(self.indexPath):
            IndexSupport.modifiers[self.indexPath].close()
            del IndexSupport.modifiers[self.indexPath]
    
    
#    def __del__(self):
#        try:
#            self.close()
#        except:{}
#        



STORE_DIR = os.path.join(DOCUMENT_ROOT, '../index')
FEED_FIELDS = ['url', 'link', 'title', 'subtitle']
FEED_ENTRY_FIELDS = ['feed_url', 'link', 'title', 'summary', 'updated']


class FeedIndexer:
    
    def __init__(self, store_dir=STORE_DIR, destroy=False, analyzer=None):
        self.feedSupport = IndexSupport(os.path.join(store_dir, 'feeds'), analyzer=analyzer)
        self.entrySupport = IndexSupport(os.path.join(store_dir, 'entries'), analyzer=analyzer)
    
    
    def delete_existing_feed_docs(self, docs=None):
        """ deletes existing documents relating to the given feed """
        numDeleted = 0
        try:
            reader = self.feedSupport.getIndexReader()
            for doc in docs or []:
                try:
                    numDeleted += reader.deleteDocuments(Term('url', doc.get('url')))
                except:{}
            reader.close()
        except Exception, e:
            logging.error(e)
        logging.debug('deleted %d existing feed documents' % numDeleted)
    
    
    def delete_existing_entry_docs(self, docs=None):
        numDeleted = 0
        try:
            reader = self.entrySupport.getIndexReader()
            for doc in docs or []:
                try:
                    numDeleted += reader.deleteDocuments(Term('id', doc.get('id')))
                except:{}
            reader.close()
        except Exception, e:
            logging.error(e)
        logging.debug('deleted %d feed entry documents' % numDeleted)
    
    
    def create_feed_document(self, feed):
        doc = Document()
        doc.add(Field('id', str(feed.id), Field.Store.YES, Field.Index.UN_TOKENIZED))
        doc.add(Field('url', feed.xml_url, Field.Store.YES, Field.Index.UN_TOKENIZED))
        if feed.channel_link:
            doc.add(Field('link', feed.channel_link, Field.Store.YES, Field.Index.UN_TOKENIZED))
        if feed.title:
            doc.add(Field('title', feed.title, Field.Store.YES, Field.Index.TOKENIZED))
        if feed.subtitle:
            doc.add(Field('subtitle', feed.subtitle, Field.Store.YES, Field.Index.TOKENIZED))
        return doc
    
    
    def create_entry_documents(self, feed):
        docs = []
        for entry in feed.get_entries():
            try:
                doc = Document()
                id = '%s:%s' % (feed.xml_url, entry.get('id', None))
                doc.add(Field('id', id, Field.Store.YES, Field.Index.UN_TOKENIZED))
                doc.add(Field('feed_url', feed.xml_url, Field.Store.YES, Field.Index.UN_TOKENIZED))
                if entry.get('title', None):
                    doc.add(Field('title', entry['title'], Field.Store.YES, Field.Index.TOKENIZED))
                if entry.get('summary', None):
                    doc.add(Field('summary', entry['summary'], Field.Store.YES, Field.Index.TOKENIZED))
                if entry.get('link', None):
                    doc.add(Field('link', entry['link'], Field.Store.YES, Field.Index.UN_TOKENIZED))
                try:
                    updated = parser.parse(entry.get('updated', None), ignoretz=True)
                    doc.add(Field('updated', updated.isoformat(' '), Field.Store.YES, Field.Index.NO))
                except:{}
                try:
                    doc.add(Field('pickle', pickle.dumps(entry), Field.Store.YES, Field.Index.NO))
                except Exception, e:
                    logging.error('Unable to store pickled entry: %s' % e)
                docs.append(doc)
            except Exception, e:
                logging.error(e)
        return docs
    
    
    def index_feed(self, feed):
        """ Indexes the given feed """
        logging.debug('Attempting to index feed: %s' % feed.xml_url)
        self.index_feeds([feed,])
    
    
    def index_feeds(self, feeds=None):
        if not feeds:
            return
        
        feed_docs = []
        entry_docs = []
        for feed in feeds:
            doc = self.create_feed_document(feed)
            if doc:
                feed_docs.append(doc)
            docs = self.create_entry_documents(feed)
            if docs:
                entry_docs.extend(docs)
        
        if len(feed_docs):
            self.delete_existing_feed_docs(feed_docs)
            for doc in feed_docs:
                try:
                    modifier = self.feedSupport.getIndexModifier()
                    modifier.addDocument(doc)
                    logging.debug('Indexed Feed: %s' % doc.get('url'))
                    modifier.flush()
                except Exception, e:
                    logging.error(e)
        
        if len(entry_docs):
            self.delete_existing_entry_docs(entry_docs)
            for doc in entry_docs:
                try:
                    modifier = self.entrySupport.getIndexModifier()
                    modifier.addDocument(doc)
                    logging.debug('Indexed Feed Entry: %s' % doc.get('title') or doc.get('id'))
                    modifier.flush()
                except Exception, e:
                    logging.error(e)
    

class FeedSearcher:
    
    def __init__(self, store_dir=STORE_DIR, analyzer=None):
        self.feedSupport = IndexSupport(os.path.join(store_dir, 'feeds'), analyzer=analyzer)
        self.entrySupport = IndexSupport(os.path.join(store_dir, 'entries'), analyzer=analyzer)
    
    
    def search(self, query, fields=FEED_ENTRY_FIELDS, analyzer=None, support=None):
        if not query or len(query.strip()) == 0 or len(fields) == 0:
            return None
        if not support:
            support=self.entrySupport
        analyzer = analyzer or support.analyzer
        
        if len(fields) > 1:
            qp = MultiFieldQueryParser(fields, analyzer)
        else:
            qp = QueryParser(fields[0], analyzer)
        q = qp.parse(query)
        
        searcher = support.getIndexSearcher()
        hits = searcher.search(q, Sort.RELEVANCE)
        return HitHolder(hits, searcher)

    
    def search_entries(self, query, fields=FEED_ENTRY_FIELDS, analyzer=None):
        return self.search(query, fields=fields, analyzer=analyzer, support=self.entrySupport)
    
    def search_feeds(self, query, fields=FEED_FIELDS, analyzer=None):
        return self.search(query, fields=fields, analyzer=analyzer, support=self.feedSupport)
        


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
    
    def close(self):
        try:
            logging.debug('Closing Searcher handle...')
            self.searcher.close()
        except:{}
    
    def __getitem__(self, index):
        if type(index) == slice:
            return [self.doc_dict(i) for i in range(max(index.start, 0), min(index.stop, self.hits.length()))]
        else:
            return self.doc_dict(index)
    
    def __iter__(self):
        return [self.doc_dict(i) for i in range(self.hits.length())].__iter__()
        







