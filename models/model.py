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


class Auth(ndb.Model):
    token = ndb.StringProperty()
