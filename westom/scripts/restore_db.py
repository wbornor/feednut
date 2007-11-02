#!/usr/bin/env python
"""
Restores the database from a pickled file
"""

import os, sys
sys.path.append(os.path.join(os.getcwd(), '..'))
sys.path.append(os.getcwd())

# Set DJANGO_SETTINGS_MODULE appropriately.
os.environ['DJANGO_SETTINGS_MODULE'] = 'westom.settings'
import westom.feednut.models as DB
sys.path.pop()
import cPickle


def restore_db(filename):
    if os.path.exists(filename):
        file = open(filename, 'r')
        db_dict = cPickle.load(file)
        for table, rows in db_dict.iteritems():
            for row in rows:
                try:
                    row.save()
                except:{}
        file.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print 'Restoring...'
        restore_db(sys.argv[1])