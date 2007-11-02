#!/usr/bin/env python
"""
Update all of the feeds

This is meant to be run on the server only
"""

import os, sys
import socket

DOC_ROOT = '/home/tzellman/webapps/feednut/'
sys.path.append(DOC_ROOT)
sys.path.append(os.path.join(os.getcwd(), '..'))

# Set DJANGO_SETTINGS_MODULE appropriately.
os.environ['DJANGO_SETTINGS_MODULE'] = 'westom.settings'
from westom.feednut.models import *
sys.path.pop()
from westom.feednut.utils import feed_accomplice

if __name__ == '__main__':
    
    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        args = arg.split('##')
        for arg in args:
            feed = feed_accomplice.updatefeed(arg)
            if feed:
                print 'Added feed: %s' % arg