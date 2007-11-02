from django.template import Library
from westom.feednut.utils import misc as misc_utils
import re
register = Library()

def split_seq(list, num):
    """
    Splits the given list into the given number of lists

    Argument: optional, number of lists to return (default=2)
    """
    return misc_utils.split_seq(list, int(num))
register.filter(split_seq)


def feedid(prefix, args):
    """
    Returns prefix + feedId + itemId
    """
    parts = args.split()
    itemId = parts[1]
    if len(parts) > 2:
        for i in range(1, len(parts)):
            if parts[i]:
                itemId = parts[i]
                break
    return '%s_%s_%s' % (prefix, parts[0], itemId)
register.filter(feedid)


ANCHOR_RE = re.compile(r'<\s*a.*>(.*)</a>')
def strip_anchors_and_images(html):
    """ Strip links from html """
    return ANCHOR_RE.sub(r'\1', html)
    
register.filter(strip_anchors_and_images)

def page_owner(name1, name2):
    """
    Takes in two usernames. If equal, returns 'my', otherwise
    it returns the second user's name.
    
    Returns an ownership string
    """
    if cmp(name1, name2) == 0 and name2 is not None:
        return 'my'
    elif name2:
        return "%s's" % name2
    else:
        return name2
register.filter(page_owner)

def stripws(value):
    """ strips whitespace """
    if value:
        value = str(value).strip()
    return value
register.filter(stripws)

def split_word(word, limit):
    """ splits an individual word into space seperated words with maximum length of "limit" """
    
    limit = int(limit)
    word_length = len(word)
    
    if word_length <= limit:
        return word
    
    one_word = word[:limit]
    return ' '.join([one_word, split_word(word[limit:], limit)])

def split_phrase(phrase, limit):
    """ make sure that no word in a phrase has length greater than limit """
    
    words = phrase.split(" ")
    return_phrase = []
    
    for word in words:
        return_phrase.append(split_word(word, limit))
        
    return(' '.join(return_phrase))
register.filter(split_phrase)


def range_list(end, start=0, step=1):
    return range(int(start), int(end), int(step))
register.filter(range_list)

