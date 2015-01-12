import time

from google.appengine.ext import ndb
from webapp2_extras import security

class Article(ndb.Model):
  tittle = ndb.StringProperty()
  content = ndb.TextProperty()
  date = ndb.DateTimeProperty(auto_now = True)
  # image = ndb.

class Auth(ndb.Model):
  token = ndb.StringProperty()

