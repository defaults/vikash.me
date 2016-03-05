from google.appengine.ext import ndb


class Article(ndb.Model):
    url = ndb.StringProperty()
    tittle = ndb.StringProperty()
    content = ndb.TextProperty()
    date = ndb.DateTimeProperty()
    # image = ndb.


class Auth(ndb.Model):
    token = ndb.StringProperty()
