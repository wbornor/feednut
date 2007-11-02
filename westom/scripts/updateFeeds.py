#!/usr/bin/env python
"""
Update all of the feeds

This is meant to be run on the server only
"""

import os, sys
import socket


DOC_ROOT = '/home/tzellman/webapps/feednut/'
sys.path.append(DOC_ROOT)

# Set DJANGO_SETTINGS_MODULE appropriately.
os.environ['DJANGO_SETTINGS_MODULE'] = 'westom.settings'
from westom.feednut.models import *
sys.path.pop()
from westom.feednut.utils import feed_accomplice

if __name__ == '__main__':
    # make a short timeout so dead feeds don't cause crawler to have a long runtime
    if hasattr(socket, 'setdefaulttimeout'):
        socket.setdefaulttimeout(5)
    
    feed_accomplice.update_feeds()