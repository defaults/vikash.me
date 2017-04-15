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
from controllers import blog_api


# base handler
class BlogHandler(server.BaseHandler):

    def authentication(self):
        verify = model.Auth.query().get()
        if verify:
                params = {
                    'page': 'write',
                    'pending': 'pending'
                }
        else:
            gtoken = ''.join(random.choice(string.ascii_uppercase +
                                           string.digits) for _ in range(20))
            save = model.Auth(token=gtoken)
            save.put()

            to = config.admin['admin_name'] + ' ' + '<' + \
                config.admin['admin_mail'] + '>'
            subject = 'Link to write blog'
            body = 'https://blog.vikashkumar.me/write/{0}'.format(gtoken)

            self.send_email(to, subject, body)

            params = {
                'page': 'token'
            }

        self.render_response('write.html', **params)

    # function to resend blog mail
    def resendMail(self):
        verify = model.Auth.query().get()

        if not verify:
            verify = ''.join(random.choice(string.ascii_uppercase +
                                           string.digits) for _ in range(20))
            save = model.Auth(token=verify)
            save.put()

        to = config.admin['admin_name'] + ' ' + '<' + \
            config.admin['admin_mail'] + '>'
        subject = 'Link to write blog'
        body = 'https://blog.vikashkumar.me/write/{0}'.format(verify.token)

        self.sendEmail(to, subject, body)
        self.response.out.write(json.dumps({'status': 'success'}))


# handler for blog
class ArticlesListHandler(BlogHandler):
    def get(self):
        # code to search the database for blog posts
        article = model.Article.query().order(-model.Article.date)

        params = {
            'page': 'blog',
            'article': article
        }
        self.render_response('blog.html', **params)


# handler for serving article
class ArticleHandler(BlogHandler):
    def get(self, **kwargs):
        article_url = kwargs['article_url']
        article_content = model.Article.query(
            model.Article.url == article_url).fetch()

        if article_content:
            for article in article_content:
                content = markdown.markdown(article.content,
                                            extras=["code-friendly"])
                tittle = article.tittle
                date = article.date
                url = article.url
                tags = article.tags

            params = {
                'page': 'article',
                'tittle': tittle,
                'content': content,
                'date': date,
                'url': url,
                'tags': tags
            }
            self.render_response('article.html', **params)
        else:
            self.abort(404)
            return


# handler for writing blog
class WriteHandler(BlogHandler):
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
            url = re.sub(r'[/|!|"|:|;|.|%|^|&|*|(|)|@|,|{|}|+|=|_|?|<|>]',
                         'p', header).replace(' ', '-').lower()
            time = datetime.datetime(2015, 03, 02, hour=01, minute=25,
                                     second=55, microsecond=66)
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


class DashboardHandler(BlogHandler):
    def get(self):
        pass
