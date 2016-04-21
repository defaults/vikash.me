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


class BlogHandler(server.BaseHandler):
    """Base handler for blog"""

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
        short_url = ''.join(random.choice(string.ascii_letters +
                                         string.digits) for _ in range(10))
        save = model.ShortUrl(full_url=full_url,
                              short_url=short_url)
        save.put()
        return short_url


class ArticleHandler(BlogHandler, JsonRestHandler):
    """Article handler - Provides an api for working with articles"""

    def all_articles(self):
        """GET request to get all articles - Exposed as `GET /api/articles`"""
        limit = self.request.get('limit', default_value=2)
        articles = model.Article.query().order(model.Article.date).fetch()

        self.send_success(articles)

    def get(self, **kwargs):
        """GET request to get article by id - Exposed as `GET /api/article/<id>`"""
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

    def post(self, **kwargs):
        """POST method for articles - Exposed as `POST /api/article`"""
        article = model.Article()
        article.from_json(self.request.body)
        article.url = re.sub(r'[/|!|"|:|;|.|%|^|&|*|(|)|@|,|{|}|+|=|_|?|<|>]',
                             'p', article.tittle).replace(' ', '-').lower()
        article.short_url = self.url_shortner(article.url)

        article.put()
        self.send_success(article)

    def patch():
        """PATCH method for article - Exposed as `PATCH /api/article/<id>`"""
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


    def delete():
        """DELETE method for articles - Exposed as `DELETE /api/article/<id>`"""
        id = kwargs['id']
        if id:
            article = model.Article.get_by_id(long(id)).to_dict()
            article.soft_deleted = True
            article.put()

            self.send_success({'message' : 'sucess'})


class SubscriberHandler(BlogHandler, JsonRestHandler):
    """Handler for subscribers - Exposes GET, POST, PATCH,
    DELETE for `/api/subscriber`
    """

    def get():
        """GET method for subscribers - Exposed as `GET /api/subscribers`"""
        article = model.Subscriber.query()
        self.send_response(article)

    def post():
        """POST method for subscribers - Exposed as `POST /api/subscriber`"""
        name = self.request.get('name')
        email = self.request.get('email')

        save = model.Subscriber(name=name,
                                email=email)
        save.put()
        self.send_success(save)

    def patch():
        """PATCH method for subscribers -
        Exposed as `PATCH /api/subscriber/<id>`
        """
        pass

    def delete():
        """DELETE method for subscribers -
        Exposed as `DELETE /api/subscriber/<id>`
        """
        pass


class TagHandler(BlogHandler, JsonRestHandler):
    """Blog tag handler -
    Exposes api for GET, POST, DELETE
    """
    def get():
        """GET method for all tags - Exposed as `GET /api/tag`"""
        pass

    def post():
        """POST method for all tags - Exposed as `POST /api/tag`"""
        pass

    def delete():
        """DELETE method for all tags - Exposed as `DELETE /api/tag/<id>`"""
        pass


class UrlShortnerHandler(BlogHandler, JsonRestHandler):
    """URL shortner API handler -
    Exposes GET and POST API
    """

    def get():
        """GET method for url shortner -
        Exposed as `GET /api/short?short_url=<shortUrl>`
        """
        short_url = self.request.get('shortUrl')
        url = model.shortUrl.query(short_url=short_url).get()
        send_success(url)

    def post():
        """POST method for url shortner -
        Exposed as `POST /api/short>`
        """
        short_url = model.ShortUrl()
        short_url.from_json(self.request.body)
        short_url.put()
        send_success(short_url)


    def delete():
        """DELETE method for url shortner -
        Exposed as `DELETE /api/short/<id>`
        """
        pass
