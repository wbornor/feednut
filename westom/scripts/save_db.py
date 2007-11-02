#!/usr/bin/env python
"""
Saves the database to a pickled file
"""

import os, sys
sys.path.append(os.path.join(os.getcwd(), '..'))
sys.path.append(os.getcwd())

# Set DJANGO_SETTINGS_MODULE appropriately.
os.environ['DJANGO_SETTINGS_MODULE'] = 'westom.settings'
import westom.feednut.models as DB
sys.path.pop()
import cPickle, re
from datetime import datetime
from django.db.models.base import ModelBase
from westom.feednut.utils import djangojson

def save_db(filename):
    
    #first, let's figure out what tables we want to save
    #by default, if no args are given, we save all
    tables = []
    if len(sys.argv) > 1:
        tables = sys.argv[1].strip().lower().split(',')
    else:
        for item in dir(DB):
            obj = getattr(DB, item)
            if isinstance(obj, ModelBase) and item.find('Middle') == -1:
                tables.append(item)
    
    db_dict = {}
    for item in tables:
        if hasattr(DB, item):
            obj = getattr(DB, item)
            if isinstance(obj, ModelBase):
                rows = obj.objects.all()
                db_dict[obj.__name__] = rows

    try:
        os.makedirs(os.path.dirname(filename))
    except:{}
    
    file = open(filename, 'wb')
#    cPickle.dump(djangojson.write(db_dict), file)
    cPickle.dump(db_dict, file)
    file.close()


if __name__ == '__main__':
    filename = os.path.join(os.getcwd(), 'westom_%s.dmp' % (datetime.strftime(datetime.now(), '%Y-%m-%d-%M-%S')))
    save_db(filename)
