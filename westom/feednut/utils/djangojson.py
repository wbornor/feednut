import string, types, datetime
from django.db.models.base import ModelBase
from django.db import models
from westom.feednut.models import *
from westom.feednut.libs import json
from django.db.models.query import QuerySet

class DjangoJsonWriter(json.JsonWriter):
    
    def write(self, obj, escaped_forward_slash=False):
        self._escaped_forward_slash = escaped_forward_slash
        self._results = []
        self._write(obj)
        return "".join(self._results)
    
    def _write(self, obj):
        if isinstance(obj, QuerySet):
            self._write(list(item for item in obj))
        elif isinstance(obj, models.Model):
            j={}
            for i in obj._meta.fields:
                if i.attname != 'id':
                    j[i.attname] = obj.__getattribute__(i.attname)
                    #even return the foreign objects
#                    if isinstance(i, models.ForeignKey):
#                        j[i.name] = apply(obj.__getattribute__("get_" + i.name))
            self._write( j )
        elif isinstance(obj, datetime.datetime):
            self._write(obj.isoformat() )
        else:
            json.JsonWriter._write(self, obj)

def write(obj, escaped_forward_slash=False):
    return DjangoJsonWriter().write(obj, escaped_forward_slash)
