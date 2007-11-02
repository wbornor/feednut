from string import letters, digits
import re

VALID_CHARS = letters + digits

def clean_string(s):
    """ cleans a string, removing any non-letters/digits """
    return ''.join([c in VALID_CHARS and c or '_' for c in s])

class Singleton(type):
    def __init__(cls,name,bases,dic):
        super(Singleton,cls).__init__(name,bases,dic)
        cls.instance=None
    
    def __call__(cls,*args,**kw):
       if cls.instance is None:
           cls.instance=super(Singleton,cls).__call__(*args,**kw)
       return cls.instance

#class Singleton(type):
#    """ Base class for creating a singleton """
#    def __init__(self, *args):
#        type.__init__(self, *args)
#        self._instances = {}
#
#    def __call__(self, *args):
#        if not args in self._instances:
#            self._instances[args] = type.__call__(self, *args)
#        return self._instances[args]


def split_seq(seq, p):
    """ Splits a sequence into equal parts """
    newseq = []
    n = len(seq) / p    # min items per subsequence
    r = len(seq) % p    # remaindered items
    b,e = 0, n + min(1, r)  # first split
    for i in range(p):
        newseq.append(seq[b:e])
        r = max(0, r-1)  # use up remainders
        b,e = e, e + n + min(1, r)  # min(1,r) is always 0 or 1
    return newseq


def split_every_other(seq):
    """ Returns an array of size two, composed of arrays containing the items, interleaved every other """
    newseq = [[], []]
    for i, item in zip(range(len(seq)), seq):
        newseq[i % 2].append(item)
    return newseq


def clean_string(s):
    """ cleans a string, removing any non-letters/digits """
    news = ''
    valid_chars = letters + digits
    for c in s:
        if c not in valid_chars:
            news += '_'
        else:
            news += c
    return news


#copied from the django dev release
STRIP_RE = re.compile(r'>\s+<')
def strip_spaces_between_tags(value):
    "Returns the given HTML with spaces between tags normalized to a single space"
    return STRIP_RE.sub('> <', value)


class Storage(dict):
    """
    A Storage object is like a dictionary except `obj.foo` can be used
    instead of `obj['foo']`. Create one by doing `storage({'a':1})`.
    
    Copied from web.py
    """
    def __getattr__(self, key): 
        if self.has_key(key): 
            return self[key]
        raise AttributeError, repr(key)
    def __setattr__(self, key, value): 
        self[key] = value
    def __repr__(self):     
        return '<Storage ' + dict.__repr__(self) + '>'

storage = Storage