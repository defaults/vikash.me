from google.appengine.ext import ndb


class Article(ndb.Model):
    url = ndb.StringProperty()
    tittle = ndb.StringProperty()
    date = ndb.DateTimeProperty()
    content = ndb.TextProperty()
    shortUrl = ndb.StringProperty()
    stars = ndb.IntegerProperty(default=0)
    tags = ndb.StringProperty(repeated=True)
    published = ndb.BooleanProperty(default=True)


class Subscribers(object):
    name = ndb.StringProperty()
    email = ndb.StringProperty()


class Auth(ndb.Model):
    token = ndb.StringProperty()
