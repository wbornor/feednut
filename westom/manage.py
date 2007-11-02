#!/usr/bin/env python
from django.core.management import execute_manager
try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
    sys.exit(1)


import MySQLdb, sys
def freshen():
    """
    Helper function that deletes and creates the database
    """
    
    #let's delete the database
    db=MySQLdb.connect(db=settings.DATABASE_NAME,
                       user=settings.DATABASE_USER, 
                       passwd=settings.DATABASE_PASSWORD)
    c=db.cursor()
    c.execute("DROP DATABASE " + settings.DATABASE_NAME)
    print 'Dropped database: ' + settings.DATABASE_NAME
    c.execute("CREATE DATABASE " + settings.DATABASE_NAME)
    print 'Created database: ' + settings.DATABASE_NAME
    
    sys.argv.remove('fresh')
    #first, let's init it
    sys.argv = [sys.argv[0], 'syncdb']
    execute_manager(settings)
    
    #now, update some fields that should be blobs
    c.execute("USE %s" % settings.DATABASE_NAME)
#    c.execute("ALTER TABLE FEEDNUT_FEED MODIFY FEED_DATA BLOB NOT NULL")
    c.execute("ALTER TABLE FEEDNUT_FEED CONVERT TO CHARACTER SET utf8")
    c.execute("ALTER TABLE FEEDNUT_FEEDENTRY CONVERT TO CHARACTER SET utf8")
    db.close()
    
    print 'Synced database'
    

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'fresh':
        freshen()
    elif len(sys.argv) > 1 and sys.argv[1] == 'compress':
        #compresses the javascripts
        import os, subprocess
        os.chdir('scripts')
        p = subprocess.Popen(
                             ['python', 'compressJS.py'],
                             stdout=subprocess.PIPE,
                             )
    #otherwise, process normally...
    else:
        execute_manager(settings)
