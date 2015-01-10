import time

from google.appengine.ext import ndb
from webapp2_extras import security

class article(ndb.Model):
  tittle = ndb.StringProperty()
  content = ndb.BlobProperty()
  date = ndb.DateTimeProperty(auto_now = True)
  # image = ndb.

class auth(ndb.Model):
  token = ndb.StringProperty()

