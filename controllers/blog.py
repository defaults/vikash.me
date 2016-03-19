import datetime
import random
import re
import string
import json

import webapp2
from google.appengine.api import mail
from webapp2_extras import jinja2
from webapp2_extras import routes

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


# handler for serving article
class ArticleHandler(webapp2.RequestHandler):
    # GET method to retrive all articles
    def all_articles():
        limit
        offset
        article = model.Article.query().order(-model.Article.date)
        return article

    # GET articles by id
    def get(self):
        self.response.out.write('Hii')

    # POST article
    def post(self, **kwargs):
        pass

    # PATCH article
    def patch():
        pass

    # DELETE article - sets softDeleted flag
    def delete():
        pass


# handler for writing blog
class SubscriberHandler(BlogHandler):
    # GET all subscribers
    def get():
        pass

    # POST subscriber
    def post():
        pass

    # PATCH an existing subscriber detail
    def patch():
        pass

    # DELETE subscriber - sets softDeleted flag
    def delete():
        pass
