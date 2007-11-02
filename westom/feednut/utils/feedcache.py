from westom.feednut.cache import Cache, ExpiredError
from westom.settings import FEEDS_DIR
import os, cPickle


class FeedCache(Cache):
    
    def get_full_path(self, key):
        """ returns the full path to the data file """
        return os.path.abspath(os.path.join(FEEDS_DIR, key))
    
    def get_feed_data(self, key):
        """ Unpickles the data and returns the stored object """
#        print 'HAD TO FETCH DATA FROM DISK!!!!!'
        #TODO read-lock the file?
        obj = None
        try:
            file = open(self.get_full_path(key), 'r')
            obj = cPickle.load(file)
        except Exception, e:
            print e
        else:
            file.close()
        return obj
    
    def __getitem__(self, key):
        try:
            item = Cache.__getitem__(self, key)
        except KeyError, e:
            #need to try to fetch it and update the cache
            try:
                item = self.get_feed_data(key)
            except:
                raise KeyError
            self[key] = item
        return item

FEED_CACHE = FeedCache(age='5m')
