from __future__ import unicode_literals
from django.db import models
from json import JSONEncoder
from uuid import UUID

# Create your models here.

JSONEncoder_olddefault = JSONEncoder.default

def JSONEncoder_newdefault(self, o):
    if isinstance(o, UUID): return str(o)
    return JSONEncoder_olddefault(self, o)

JSONEncoder.default = JSONEncoder_newdefault