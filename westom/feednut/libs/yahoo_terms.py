"""
FYI: Yahoo puts a limit of 5000 requests per day...
"""
import urllib, string, re

APP_ID = 'yahoo_feednut'
YAHOO_URL = 'http://api.search.yahoo.com/ContentAnalysisService/V1/termExtraction'
RESULT_RE = re.compile('<Result>([\w\s]+)<\/Result>')

#filter out some words we don't want back
FILTER_LIST = ['a', 'for', 'the', 'of', 'or', 'and', 'in']
FILTER_DICT = dict((val, val) for val in FILTER_LIST)

def extract_terms(text, query='', appid = APP_ID, limit=0):
    """ calls the Yahoo! term extraction service and returns a list of the results """
    params = urllib.urlencode([('appid',appid), ('context',text), ('query',query)])
    f = urllib.urlopen(YAHOO_URL, params)
    content = string.join(f.readlines()).strip()
    f.close()
    results = RESULT_RE.findall(content)
    tags = {}
    for result in results:
        words = result.split()
        for word in words:
            if word not in FILTER_DICT and word not in tags and len(word) > 2:
                tags[word] = word
    tags = list((tag) for tag in tags.keys())
    if limit:
        tags = tags[:limit]
    return tags
    
if __name__ == '__main__':
    """ example usage """
#    print extract_terms('Alice in Wonderland is a great book!')
#    print extract_terms('Italian sculptors and painters of the renaissance favored the Virgin Mary for inspiration.')
    print extract_terms('www.slashdot.org')
    
