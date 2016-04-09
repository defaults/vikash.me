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

    def resend_mail(self):
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

        self.send_email(to, subject, body)
        self.response.out.write(json.dumps({'status': 'success'}))

    @staticmethod
    def url_shortner(full_url):
        """Method for sortning full URL and saving and returning short URL"""
        short_url = ''.join(random.choice(string.ascii_lowercase +
                                         string.digits) for _ in range(5))
        save = model.ShortUrl(full_url=fullUrl,
                              short_url=short_url)
        save.put()
        return short_url


# handler for serving article
class ArticleHandler(BlogHandler, JsonRestHandler):
    # GET method to retrive all articles
    def all_articles(self):
        limit = self.request.get('limit', default_value=2)
        # cookie = self.request.cookies
        articles = model.Article.query().order(model.Article.date).fetch()

        self.send_success(articles)

    # GET articles by id
    def get(self, **kwargs):
        try:
            # TODO get user from session and verify
            id = kwargs['id']
            if id:
                article = model.Article.get_by_id(long(id))
                self.send_success(article)
        except TypeError as te:
            self.send_error(404, 'Resource not found')
        except Exception as e:
            self.send_error(500, 'Server error')

    # POST article
    def post(self, **kwargs):
        tittle = self.request.get('header')
        content = self.request.get('text')

        url = re.sub(r'[/|!|"|:|;|.|%|^|&|*|(|)|@|,|{|}|+|=|_|?|<|>]',
                     'p', header).replace(' ', '-').lower()
        short_url = self.url_shortner(url)
        tags = self.request.get('tags')
        publish = self.request.get('publish', default_value=True)
        currentTime = self.request.get('date', default_value=datetime.datetime.now())
        article = model.Article(tittle=header,
                             content=content,
                             url=url,
                             short_url
                             date=currentTime
                             short_url=short_url,
                             published=publish,
                             tags=tags)
        article.put()
        send_success(article)

    # PATCH article
    def patch():
        id = id = kwargs['id']
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


    # DELETE article - sets softDeleted flag
    def delete():
        id = kwargs['id']
        if id:
            article = model.Article.get_by_id(long(id)).to_dict()
            article.soft_deleted = True
            article.put()

            self.send_success({'message' : 'sucess'})


# handler for writing blog
class SubscriberHandler(BlogHandler, JsonRestHandler):
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
        self.send_success(save)

    # PATCH an existing subscriber detail
    def patch():
        pass

    # DELETE subscriber - sets softDeleted flag
    def delete():
        pass


# handler for blog tags
class TagHandler(BlogHandler, JsonRestHandler):
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
class UrlShortnerHandler(BlogHandler, JsonRestHandler):
    def get():
        pass

    def post():
        pass

    def delete():
        pass
