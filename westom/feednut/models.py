from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from westom.settings import FEEDS_DIR
from westom.feednut.utils import misc as misc_utils
import os
import cPickle as pickle


#Set up File locks in a system-independent manner
try:
    from fcntl import lockf as lockFile
    from fcntl import LOCK_EX, LOCK_SH
except:
    from msvcrt import locking as lockFile
    from msvcrt import LK_RLCK as LOCK_EX
    from msvcrt import LK_NBLCK as LOCK_SH


class Feed(models.Model):
    """
    This represents an individual RSS/etc. Feed in the system
    """
    
    xml_url = models.URLField(verify_exists=False, unique=True, db_index=True)
    channel_link = models.URLField(verify_exists=False, null=True)
    title = models.CharField(maxlength=128, null=False, db_index=True)
    subtitle = models.TextField(null=True, blank=True)
    icon_url = models.URLField(verify_exists=False, null=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    encoding = models.CharField(maxlength=64, default='us-ascii')
    
    #These next two deal with the HTTP headers of the feed
    last_modified = models.DateTimeField(null=True)
    etag = models.CharField(maxlength=128, null=True, blank=True)
    
    create_date = models.DateTimeField(auto_now_add=True)
    touch_date = models.DateTimeField(auto_now=True)
    
    suggested_tags = models.CharField(maxlength=255, db_index=True, default='')
    
    default_feed = models.BooleanField(default=False) #True if this should be a feed included in a new users first view
    system_feed = models.BooleanField(default=False)
    
    
    class Admin:
        list_display = ('xml_url', 'create_date', 'last_modified', 'touch_date', 'default_feed', 'system_feed')
        list_filter = ('default_feed', 'system_feed')
        search_fields = ('xml_url', 'title')
    
    def __str__(self):
        return self.xml_url
    
    def get_data_path(self):
        """ returns the full path to the data file """
        name = misc_utils.clean_string(self.xml_url)
        return os.path.abspath(os.path.join(FEEDS_DIR, 'feeds_%d/%s' % (self.id % 100, name)))
    
    def set_data(self, data):
        """ Set the feed data, which gets pickled and stored """
        path = self.get_data_path()
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:{}
        f = open(path, 'wb')
        try:
            #lock the file and write it
            lockFile(f.fileno(), LOCK_EX, 0)
        except:{}
        pickle.dump(data, f)
        f.close()
    
    def get_data(self):
        """ Unpickles the data and returns the stored object """
        f = open(self.get_data_path(), 'rb')
        try:
            #lock the file and read it
            lockFile(f.fileno(), LOCK_SH, 0)
        except:{}
        data = pickle.load(f)
        f.close()
        return data
    
    def get_xml_data(self):
        """ Returns the stored XML data """
        data = self.get_data()
        return data.get('xml_data', None)

    def get_entries(self, limit=10):
        """ returns a list of entries associated with the feed """
#        return self.feedentry_set.all()[:limit]
        #get the feed data that got pickled on disk
        return self.get_data()['entries'][:limit]
    
    def get_suggested_tags(self):
        """ returns list of the suggested tags """
        return self.suggested_tags.split()



class FeedEntry(models.Model):
    """ An Entry for a Feed """
    entry_id = models.CharField(maxlength=255)
    title = models.TextField()
    link = models.URLField(verify_exists=False, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    
    feed = models.ForeignKey(Feed)

    create_date = models.DateTimeField(auto_now_add=True)
    touch_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Feed entries"
        ordering = ['-touch_date', '-id']
    
    class Admin:
        list_display = ('entry_id', 'title', 'link', 'updated_date',)
        search_fields = ('title', 'link')
    
    def __str__(self):
        return self.entry_id



      
class UserFeed(models.Model):
    """Each item is a feed for the specified user, with its rating """
    class Meta:
        unique_together = (("user", "feed"),)
    
    user = models.ForeignKey(User)
    feed = models.ForeignKey(Feed)
    
    create_date = models.DateTimeField(auto_now_add=True)
    position = models.IntegerField(default=0, db_index=True)
    is_anchored = models.BooleanField(default=False)
    
    access_count = models.IntegerField(default=0)
    is_public = models.BooleanField(default=True)
    is_hidden = models.BooleanField(default=False)
    num_items = models.IntegerField(default=10)
    permanent_feed = models.BooleanField(default=False)
    
    class Admin:
        list_display = ('user', 'feed', 'create_date')
        list_filter = ('is_public', 'permanent_feed')
    
    def __str__(self):
        return '%s, %s' % (self.user.username, self.feed.xml_url)
    
    def get_tags_string(self):
        st = ' '.join(self.get_tags())
        if len(st) > 0:
            st += ' '
        return st
    
    def get_tags(self):
        items = self.userfeedtag_set.all()
        return [item.tag.tag for item in items]
    
    def get_feed(self):
        return self.feed
    
    def get_entries(self):
        return self.feed.get_entries(limit=self.num_items)



class Tag(models.Model):
    """ Tags """
    tag = models.CharField(maxlength=32, unique=True, db_index=True)
    
    class Admin:
        search_fields = ('tag',)
    
    def __str__(self):
        return self.tag



class Entry(models.Model):
    """ An Entry for a Feed"""
    feed = models.ForeignKey(Feed)
    title = models.CharField(maxlength=128, null=False)
    link = models.URLField(verify_exists=False, null=False)
    description = models.TextField(default='')
    
    #the xml_url of the originating feed where the article came from
    xml_url = models.URLField(verify_exists=False, null=True)
 
    create_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Entries"
    
    class Admin:
        list_display = ('title', 'link', 'create_date')
    
    def __str__(self):
        return self.link



class FeedTag(models.Model):
    """ A tag for a Feed as a whole. Entries could be 'suggested tags' or something of that sort. """
    create_date = models.DateTimeField(auto_now_add=True)
    feed = models.ForeignKey(Feed)
    tag = models.ForeignKey(Tag)
    
    class Meta:
        unique_together = (("feed", "tag"),)
    
    class Admin:
        pass
    
    def __str__(self):
        return '%s, %s' % (self.feed, self.tag.tag)



class UserFeedTag(models.Model):
    """ A user's tag for one of their subscribed feeds """
    create_date = models.DateTimeField(auto_now_add=True)
    user_feed = models.ForeignKey(UserFeed)
    tag = models.ForeignKey(Tag)
    
    class Meta:
        unique_together = (("user_feed", "tag"),)
    
    class Admin:
        list_display = ('user_feed', 'tag', 'create_date')
    
    def __str__(self):
        return '%s, %s' % (self.user_feed, self.tag.tag)




class UserReadEntry(models.Model):
    """ Articles read by users """
    user = models.ForeignKey(User)
    title = models.CharField(maxlength=128, null=False)
    link = models.URLField(verify_exists=False)
    description = models.TextField(default='')
    read_date = models.DateTimeField(auto_now=True)
    xml_url = models.URLField(verify_exists=False, null=True)
    
    class Admin:
        list_display = ('title', 'user', 'read_date')
    
    def __str__(self):
        return self.title


class UserBuddy(models.Model):
    """ maps members to a User's network """
    user = models.ForeignKey(User, related_name='user')
    buddy = models.ForeignKey(User, related_name='buddy')
    create_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = (("user", "buddy"),)
        ordering = ['buddy']
        verbose_name_plural = "User Buddies"
    
    class Admin:
        list_display = ('user', 'buddy', 'create_date')

class ForgotPassword(models.Model):
    """ keeps track of requests to reset a password """
    request_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True)
    hash = models.CharField(maxlength=32, unique=True)
    #set expired to true whenever they request the URL... maybe?
    expired = models.BooleanField(default=False)
    
    class Admin:
        pass


User._meta.admin.list_display = User._meta.admin.list_display + ('date_joined', 'last_login',)


#class Blacklist(models.Model):
#    """ maps members to a User's network """
#    ipaddress = models.IPAdressField(_('ipaddress'),  blank=False, null=False)
#    create_date = models.DateTimeField(auto_now_add=True)
#    touch_date = models.DateTimeField(auto_now=True)
#    
#    class Meta:
#        verbose_name = _('blacklist')
#        verbose_name_plural = _('blacklists')
##        ordering = ('-touch_date',)
#    class Admin:
#        #fields = (
##        #    (None, {'fields': ('content_type', 'object_id', 'site')}),
#        #    ('Content', {'fields': ('user', 'headline', 'comment')}),
##        #    ('Ratings', {'fields': ('rating1', 'rating2', 'rating3', 'rating4', 'rating5', 'rating6', 'rating7', 'rating8', 'valid_rating')}),
##        #    ('Meta', {'fields': ('is_public', 'is_removed', 'ip_address')}),
#        #)
##        list_display = ('ipaddress', 'create_date', 'touch_date')
#        list_filter = ('create_date', 'touch_date')
#        date_hierarchy = 'create_date'
#        search_fields = ('ipaddress',)
#
#    def __repr__(self):
#        return "%s: %s %s" % (self.ipaddress, self.create_date, self.touch_date)
