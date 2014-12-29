import time

from google.appengine.ext import ndb
from webapp2_extras import security

class article(ndb.Model):
  key = ndb.IntegerProperty()
  tittle = ndb.StringProperty()
  content = ndb.BlobProperty()
  # date = ndb.DatetimeProperty(auto_update = true)
  # image = ndb.

class auth(ndb.Model):
  key = ndb.IntegerProperty()
  token = ndb.StringProperty()


