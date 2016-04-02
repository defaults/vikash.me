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

    # custom dispatch handler
    def handle_dispatch():
        # TODO: format return to JSON here
        pass

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

    # function to resend blog mail
    def resendMail(self):
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
        ShortUrl = ''.join(random.choice(string.ascii_lowercase +
                                         string.digits) for _ in range(5))
        save = model.ShortUrl(fullUrl=fullUrl,
                              shortURl=shortURl)
        save.put()
        return shortURl


# handler for serving article
class ArticleHandler(webapp2.RequestHandler):
    # GET method to retrive all articles
    def all_articles(self):
        limit = self.request.get('limit', default_value=2)
        # cookie = self.request.cookies
        time = datetime.datetime(2015, 03, 02, hour=01, minute=25,
                                     second=55, microsecond=66)
        articles = [article.to_dict() for article in model.Article.query()]
        self.response.write(json.dumps(articles))

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
