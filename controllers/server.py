import datetime
import logging
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


# base handler
class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

    def render_response(self, _template, **params):
        # Renders a template and writes the result to the response.
        temp = self.jinja2.render_template(_template, **params)
        self.response.write(temp)

    def authentication(self):
        verify = model.Auth.query().get()
        if verify:
                params = {
                    'page': 'write',
                    'pending': 'pending'
                }
        else:
            gtoken = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
            save = model.Auth(token=gtoken)
            save.put()

            to = config.admin['admin_name'] + ' ' + '<' + config.admin['admin_mail'] + '>'
            subject = 'Link to write blog'
            body = 'https://blog.vikashkumar.me/write/{0}'.format(gtoken)

            self.sendEmail(to, subject, body)

            params = {
                'page': 'token'
            }

        self.render_response('write.html', **params)

    # function to resend blog mail
    def resendMail(self):
        verify = model.Auth.query().get()

        if not verify:
            verify = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
            save = model.Auth(token=verify)
            save.put()

        to = config.admin['admin_name'] + ' ' + '<' + config.admin['admin_mail'] + '>'
        subject = 'Link to write blog'
        body = 'https://blog.vikashkumar.me/write/{0}'.format(verify.token)

        self.sendEmail(to, subject, body)
        self.response.out.write(json.dumps({'status' : 'success'}))

    # funtion to send mail
    def sendEmail(self, emailTo, emailSubject, emailBody):
        mail.send_mail(sender="Vikash Kumar <mailkumarvikash@gmail.com>",
                       to=emailTo,
                       subject=emailSubject,
                       body=emailBody)

        return


# welcome page handler
class HomeHandler(BaseHandler):
    def get(self):
        params = {
            'page': 'Vikash Kumar'
        }
        self.render_response('home.html', **params)


# handler for blog
class BlogHandler(BaseHandler):
    def get(self):
        # code to search the database for blog posts
        article = model.Article.query().order(-model.Article.date)

        params = {
            'page': 'blog',
            'article': article
        }
        self.render_response('blog.html', **params)


# handler for serving article
class ArticleHandler(BaseHandler):
    def get(self, **kwargs):
        article_url = kwargs['article_url']
        article_content = model.Article.query(model.Article.url == article_url).fetch()

        if article_content:
            for article in article_content:
                content = markdown.markdown(article.content, extras=["code-friendly"])
                tittle = article.tittle
                date = article.date
                url = article.url

            params = {
                'page': 'article',
                'tittle': tittle,
                'content': content,
                'date': date,
                'url': url
            }
            self.render_response('article.html', **params)
        else:
            self.abort(404)
            return


# handler for writing blog
class WriteHandler(BaseHandler):
    # add function to authenticate user
    def get(self, **kwargs):
        auth = kwargs['token']
        verify = model.Auth.query(model.Auth.token == auth).get()
        if verify:
            params = {
                'page': 'write',
                'welcome': ''
            }

            self.render_response('zenpen.html', **params)
            return

        # else redirecting to generate token
        else:
            self.redirect('/write')
            return


    # first check authentication
    def post(self, **kwargs):
        auth = kwargs['token']
        verify = model.Auth.query(model.Auth.token == auth).get()
        if verify:
            header = self.request.get('header')
            content = self.request.get('text')
            url = re.sub(r'[/|!|"|:|;|.|%|^|&|*|(|)|@|,|{|}|+|=|_|?|<|>]', 'p', header).replace(' ', '-').lower()
            time = datetime.datetime(2015, 03, 02, hour=01, minute=25, second=55, microsecond=66)
            save = model.Article(tittle=header,
                                 content=content,
                                 url=url,
                                 date=time)
            save.put()
            token = model.Auth.query().get()
            token.key.delete()

        else:
            self.abort(404)
            return


# handler for about page
class AboutHandler(BaseHandler):
    def get(self):
        params = {
            'page': 'about'
        }
        self.render_response('about.html', **params)
