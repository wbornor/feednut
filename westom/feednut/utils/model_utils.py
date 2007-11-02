# -*- coding: utf-8 -*-
from django.db.models.base import ModelBase
from django.db import models
import types

def _filter_bases(bases, filter_key): 
    """ Remove all classes descendants of ``filter_key`` from ``bases`` """
    new_bases = tuple([base for base in bases \
                       if ((not (base is filter_key)) and (not issubclass(base, filter_key)))])
    
    # ensure that we don't end up with an orphan class - it must be
    # parented by at least models.Model
    if len(new_bases) == 0: new_bases = (models.Model,)
    return new_bases

class Hooks(object):
    _pre_saves = {}
    _post_saves = {}
    _pre_deletes = {}
    _post_deletes = {}

class MetaModelMiddleware(ModelBase):
    
    # pre and post hooks for save() will be temporarily stored in these
    #pre_saves = {}
    #post_saves = {}
    # pre and post hooks for delete()
    #pre_deletes = {}
    #post_deletes = {}
    def __new__(cls, name, bases, attrs):
        
        # whether base classes should be filtered
        cls.hide_bases = False
        # only filter bases if this wasn't invoked by the ModelMiddleware
        # class, which is a super class for all custom middleware, and the
        # one we are using as a filter key
        if not (name == 'ModelMiddleware'):
            if not (ModelMiddleware in bases):
                cls.hide_bases = True
        if cls.hide_bases:
            # replace the original bases with filtered ones to fool Django's inheritance
            bases = _filter_bases(bases, ModelMiddleware)
        # set the middleware options under Klass._middle
        if attrs.has_key('Middle'):
            midopts = attrs['Middle']
            assert type(midopts) == types.ClassType, "Middle attribute of %s model must be a class, not a %s object" % (name, type(midopts))
            opts = {}
            opts.update([(k,v) for k,v in midopts.__dict__.items() if not k.startswith('_')])
            attrs["_middle"] = opts
            attrs.pop('Middle')
        return ModelBase.__new__(cls, name, bases, attrs)
    
    def __init__(cls,name,bases,attrs):
        # provide a wrapper func for save()
        def new_save(func):
            def wrapper(*args, **kwargs):
                if hasattr(cls, 'pre_saves'):
                    [pre(args[0]) for pre in cls.pre_saves]
                func(*args, **kwargs)
                if hasattr(cls, 'post_saves'):
                    [post(args[0]) for post in cls.post_saves]
            return wrapper
        # provide a wrapper func for delete()
        def new_delete(func):
            def wrapper(*args, **kwargs):
                if hasattr(cls, 'pre_deletes'):
                    [pre(args[0]) for pre in cls.pre_deletes]
                func(*args, **kwargs)
                if hasattr(cls, 'post_deletes') > 0:
                    [post(args[0]) for post in cls.post_deletes]
            return wrapper
        
        # if this is a descendant of ModelMiddleware, but not ModelMiddleware itself
        if name != 'ModelMiddleware':
            # if this class inherits directly from ModelMiddleware then save its hooks
            if ModelMiddleware in bases:
                if attrs.has_key('pre_save'):
                    Hooks._pre_saves[name] = attrs['pre_save']
                if attrs.has_key('post_save'):
                    Hooks._post_saves[name] = attrs['post_save']
                if attrs.has_key('pre_delete'):
                    Hooks._pre_deletes[name] = attrs['pre_delete']
                if attrs.has_key('post_delete'):
                    Hooks._post_deletes[name] = attrs['post_delete']
        

            # if this is NOT a direct descendant of ModelMiddleware - not a holder of callbacks
            if ModelMiddleware not in bases:
                orig_save = cls.save
                orig_delete = cls.delete
                for base in bases:
                    base_pre_save = Hooks._pre_saves.get(base.__name__, False)
                    if base_pre_save:
                        if not hasattr(cls,'pre_saves'):
                            cls.pre_saves = []
                        cls.pre_saves.append(base_pre_save)
                    base_post_save = Hooks._post_saves.get(base.__name__, False)
                    if base_post_save:
                        if not hasattr(cls, 'post_saves'):
                            cls.post_saves = []
                        cls.post_saves.append(base_post_saves)
                    base_pre_delete = Hooks._pre_deletes.get(base.__name__, False)
                    if base_pre_delete:
                        if not hasattr(cls, 'pre_deletes'):
                            cls.pre_deletes = []
                        cls.pre_deletes.append(base_pre_deletes)
                    base_post_delete = Hooks._post_deletes.get(base.__name__, False)
                    if base_post_delete:
                        if not hasattr(cls, 'post_deletes'):
                            cls.post_deletes = []
                        cls.post_deletes.append(base_post_deletes)
                cls.save = new_save(orig_save)
                cls.delete = new_delete(orig_delete)
                # replace original bases with filtered ones
                bases = _filter_bases(bases,ModelMiddleware)
        new_class = super(ModelBase,cls).__init__(name,bases,attrs)
        return new_class
    

class ModelMiddleware(models.Model):
    """
    Custom model middleware components should subclass this and never
    use the MetaModelMiddleware metaclass directly.
    """
    __metaclass__ = MetaModelMiddleware
    
    
class ReSTMiddleware(ModelMiddleware):
    def pre_save(self):
        try:
            opts = self.__class__._middle["ReST"] # individual options are saved in a dict
        except (AttributeError, KeyError):
            return  # just fail silently, though it might not be a very good idea in practice

        # parse for as many fields as we have options for
        for opt in opts:  
            # lets be nice to ourselves and provide a default value for the initial header level
            if not opt.has_key("init_header"):
                opt["init_header"] = 1 
            try:
                cont = getattr(self, opt["field"]).decode("utf_8")
                parts = build_document(cont, initial_header_level=opt["init_header"])
                setattr(self, opt["save_body"], parts["html_body"].encode('utf_8'))
                setattr(self, opt["save_toc"], parts["toc"].encode('utf_8'))
            except:
                pass # another silent fail, needs fixing        d = datetime.now()

from datetime import datetime

class TimestampMiddleware(ModelMiddleware):
    """
    This class can record a timestamp (down to one second precision) into any fields you specify.
    There are two types of timestamps: 'always' and 'once'. 'always' means that record must be
    made on every save(), while 'once' fields will be timestamped once on the first save() of this
    object.
    
    A default set of options (used if none are provided by the model) is provided, which presume
    the existance of 'pub_date' and 'last_modified' fields.  The 'pub_date' field is of type "once",
    and 'last_modified' is of type "always". This lets you timestamp the object's creation and modification
    times.
    
    Example options (also the default ones):
    
    class Middle:
        Timestamp = ({'field' : 'pub_date', 'type' : 'once'},
            {'field' : 'last_modified', 'type' : 'always'})
    """
    def pre_save(self):
        try:
            opts = self.__class__._middle["Timestamp"]
        except (AttributeError, KeyError):
            opts = ({'field' : 'pub_date', 'type' : 'once'},
                {'field' : 'last_modified', 'type' : 'always'})
        
        for opt in opts:
            if not opt.has_key('type'):
                opt['type'] = 'always'
            d = datetime.now()
            pdate = datetime(d.year, d.month, d.day, d.hour, d.minute)
            # if this is a "set once" type of field, then we check whether
            # it's been filled in and if not - do so
            if opt['type'] == 'once':
                if getattr(self, opt['field']) is None:
                    setattr(self, opt['field'], pdate)
            elif opt['type'] == 'always':
                setattr(self, opt['field'], pdate)
