from google.appengine.ext import ndb

class Article(ndb.Model):
    url = ndb.StringProperty()
    tittle = ndb.StringProperty()
    date = ndb.DateTimeProperty()                        # has to be depricated
    content = ndb.TextProperty()
    shortUrl = ndb.StringProperty()
    stars = ndb.IntegerProperty(default=0)
    tags = ndb.StringProperty(repeated=True)
    published = ndb.BooleanProperty(default=True)
    createdOn = ndb.DateTimeProperty()
    modifiedOn = ndb.DateTimeProperty()
    softDeleted = ndb.BooleanProperty(default=False)


class Subscribers(object):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    createdOn = ndb.DateTimeProperty()
    modifiedOn = ndb.DateTimeProperty()
    softDeleted = ndb.BooleanProperty(default=False)


class Auth(ndb.Model):
    token = ndb.StringProperty()
    createdOn = ndb.DateTimeProperty()
    modifiedOn = ndb.DateTimeProperty()
    softDeleted = ndb.BooleanProperty(default=False)

class ShortUrl(ndb.Model):
    fullUrl = ndb.StringProperty()
    ShortUrl = ndb.StringProperty()
