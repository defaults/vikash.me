import json
import logging
import random
import re
import string
import datetime
import types

from google.appengine.api import images
from google.appengine.ext import ndb


class JsonifiableEncoder(json.JSONEncoder):
    """JSON encoder"""
    def default(self, obj):
        if isinstance(obj, Jsonifiable):
            result = json.loads(obj.to_json())
            return result
            return json.JSONEncoder.default(self, obj)

class Jsonifiable:
    """JSON encoder which provides a convenient extension point for custom JSON
    encoding of Jsonifiable subclasses.
    """

    @staticmethod
    def lower_first(key):
        """Make the first letter of a string lower case."""
        return key[:1].lower() + key[1:] if key else ''

    @staticmethod
    def transform_to_camelcase(key):
        """Transform a string underscore separated words to concatenated camel case.
        """
        return Jsonifiable.lower_first(
            ''.join(c.capitalize() or '_' for c in key.split('_')))

    @staticmethod
    def transform_from_camelcase(key):
        """Tranform a string from concatenated camel case to underscore separated
        words.
        """
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', key)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def to_json(self):
        result = {}
        a = self
        properties = self.to_dict()
        # properties = dict(properties, **dict(id=self.key.id()))
        if isinstance(self, ndb.Model):
            properties['id'] = unicode(self.key.id())
        for key, value in properties.iteritems():
            if isinstance(value, datetime.datetime):
                value = value.strftime("%Y-%m-%d")
            result[Jsonifiable.transform_to_camelcase(key)] = value
        return json.dumps(result)

    def from_json(self, json_string):
        """Sets properties on this object based on the JSON string supplied."""
        o = json.loads(json_string)
        properties = {}
        if isinstance(self, ndb.Model):
            properties = self._properties
        for key, value in o.iteritems():
            property_value = value
            property_key = Jsonifiable.transform_from_camelcase(key)
            if property_key in properties.keys():
                if isinstance(properties[property_key], ndb.IntegerProperty):
                    property_value = int(value)
            self.__setattr__(property_key, property_value)

class Article(ndb.Model, Jsonifiable):
    """Represents article written"""
    url = ndb.StringProperty()
    tittle = ndb.StringProperty()
    date = ndb.DateTimeProperty()
    content = ndb.TextProperty()
    short_url = ndb.StringProperty()
    stars = ndb.IntegerProperty(default=0)
    tags = ndb.StringProperty(repeated=True)
    published = ndb.BooleanProperty(default=True)
    created_on = ndb.DateTimeProperty(auto_now_add=True)
    modified_on = ndb.DateTimeProperty()
    soft_deleted = ndb.BooleanProperty(default=False)


class Subscriber(ndb.Model, Jsonifiable):
    """Represents subscribers of blog"""
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    created_on = ndb.DateTimeProperty(auto_now_add=True)
    modified_on = ndb.DateTimeProperty()
    soft_deleted = ndb.BooleanProperty(default=False)


class Auth(ndb.Model, Jsonifiable):
    """Represents Authorisation token for verifing user"""
    token = ndb.StringProperty()
    created_on = ndb.DateTimeProperty(auto_now_add=True)
    modified_on = ndb.DateTimeProperty()
    soft_deleted = ndb.BooleanProperty(default=False)


class ShortUrl(ndb.Model, Jsonifiable):
    """Represents short url for blog"""
    full_url = ndb.StringProperty()
    Short_url = ndb.StringProperty()
    created_on = ndb.DateTimeProperty(auto_now_add=True)
    modified_on = ndb.DateTimeProperty()
    soft_deleted = ndb.BooleanProperty(default=False)


class Tag(ndb.Model):
    """Represents tags for blog"""
    tag = ndb.StringProperty()
    created_on = ndb.DateTimeProperty(auto_now_add=True)
    modified_on = ndb.DateTimeProperty()
    soft_deleted = ndb.BooleanProperty(default=False)
