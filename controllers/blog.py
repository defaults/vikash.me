import datetime
import random
import re
import string
import json

import webapp2
from google.appengine.api import mail
from webapp2_extras import jinja2
from webapp2_extras import routes
from webapp2_extras import sessions

from vendors import markdown
from models import model
from config import config
from controllers import server


# base handler
class BlogHandler(server.BaseHandler):
    def __init__(self, request, response):
        # Set self.request, self.response and self.app.
        self.initialize(request, response)

    # def handle_dispatch():
    #     """custom dispatch handler"""
    #     # TODO: format return to JSON here
    #     pass

    def authentication(self):
        gtoken = ''.join(random.choice(string.ascii_uppercase +
                                       string.digits) for _ in range(20))
        save = model.Auth(token=gtoken)
        save.put()

        to = config.admin['admin_name'] + ' ' + '<' + config.admin['admin_mail'] + '>'
        subject = 'Link to write blog'
        body = 'https://blog.vikashkumar.me/write/{0}'.format(gtoken)

        self.sendEmail(to, subject, body)

        self.render_response('write.html', **params)

    def resendMail(self):
        """Method to resend mail for login to admin"""
        verify = model.Auth.query().get()

        if not verify:
            verify = ''.join(random.choice(string.ascii_uppercase +
                                           string.digits) for _ in range(20))
            save = model.Auth(token=verify)
            save.put()

        to = config.admin['admin_name'] + ' ' + '<' + config.admin['admin_mail'] + '>'
        subject = 'Link to write blog'
        body = 'https://blog.vikashkumar.me/write/{0}'.format(verify.token)

        self.sendEmail(to, subject, body)
        self.response.out.write(json.dumps({'status': 'success'}))

    def urlShortner(self, fullUrl):
        """Method for sortning full URL and saving and returning short URL"""
        ShortUrl = ''.join(random.choice(string.ascii_lowercase +
                                         string.digits) for _ in range(5))
        save = model.ShortUrl(fullUrl=fullUrl,
                              shortURl=shortURl)
        save.put()
        return shortURl


class JsonRestHandler(webapp2.RequestHandler):
  """Base RequestHandler type which provides convenience methods for writing
  JSON HTTP responses.
  """
  JSON_MIMETYPE = "application/json"

  def send_error(self, code, message):
    """Convenience method to format an HTTP error response in a standard format.
    """
    self.response.set_status(code, message)
    self.response.out.write(message)
    return

  def send_success(self, obj=None):
    """Convenience method to format a PhotoHunt JSON HTTP response in a standard
    format.
    """
    self.response.headers["Content-Type"] = "application/json"
    if obj is not None:
      if isinstance(obj, basestring):
        self.response.out.write(obj)
      else:
        self.response.out.write(json.dumps(obj, cls=model.JsonifiableEncoder))


# handler for serving article
class ArticleHandler(BlogHandler, JsonRestHandler):
    # GET method to retrive all articles
    def all_articles(self):
        limit = self.request.get('limit', default_value=2)
        # cookie = self.request.cookies
        time = datetime.datetime(2015, 03, 02, hour=01, minute=25,
                                     second=55, microsecond=66)
        # save = model.Article(tittle='hii',
        #                      content='hii how are you',
        #                      url='/url',
        #                      date=time)
        # save.put()
        articles = model.Article.query().fetch()
        # self.response.headers["Content-Type"] = "application/json"
        # self.response.write(json.dumps(articles, cls=MyJsonEncoder))
        self.send_success(articles)

    # GET articles by id
    def get(self, **kwargs):
        id = kwargs['id']
        article = model.Article.query(id=id)
        self.send_response(article)

    # POST article
    def post(self, **kwargs):
        header = self.request.get('header')
        content = self.request.get('text')
        url = re.sub(r'[/|!|"|:|;|.|%|^|&|*|(|)|@|,|{|}|+|=|_|?|<|>]',
                     'p', header).replace(' ', '-').lower()
        time = datetime.datetime()
        save = model.Article(tittle=header,
                             content=content,
                             url=url,
                             date=time)
        save.put()
        return

    # PATCH article
    def patch():
        id = self.request.get('id')
        header = self.request.get('header')
        content = self.request.get('text')
        url = re.sub(r'[/|!|"|:|;|.|%|^|&|*|(|)|@|,|{|}|+|=|_|?|<|>]',
                     'p', header).replace(' ', '-').lower()
        time = datetime.datetime()
        save = model.Article(tittle=header,
                             content=content,
                             url=url,
                             date=time)
        save.put()
        return

    # DELETE article - sets softDeleted flag
    def delete():
        id = self.request.get('id')


# handler for writing blog
class SubscriberHandler(BlogHandler):
    # GET all subscribers
    def get():
        article = model.Subscriber.query()
        self.send_response(article)

    # POST subscriber
    def post():
        name = self.request.get('name')
        email = self.request.get('email')

        save = model.Subscriber(name=name,
                                email=email)
        save.put()

    # PATCH an existing subscriber detail
    def patch():
        pass

    # DELETE subscriber - sets softDeleted flag
    def delete():
        pass


# handler for blog tags
class TagHandler(BlogHandler):
    # GET all tags
    def get():
        pass

    # add a new tag
    def post():
        pass

    # delete a tag
    def delete():
        pass


# Handler for URL shortner
class UrlShortnerHandler(BlogHandler):
    def get():
        pass

    def post():
        pass

    def delete():
        pass


class MyJsonEncoder(json.JSONEncoder):
   def default(self, obj):
      if isinstance(obj, datetime.datetime):
         # format however you like/need
         return obj.strftime("%Y-%m-%d")
      # pass any other unknown types to the base class handler, probably
      # to raise a TypeError.
      return json.JSONEncoder.default(self, obj)
