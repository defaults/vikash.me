import webapp2
import os
import logging
import urllib
import random
import string
import json

import model
import markdown

from google.appengine.api import mail
from webapp2_extras import routes
from webapp2_extras import jinja2

#method for handling errors
def error(request, response, exception):
    logging.exception(exception)
    params = {
        'error' : exception
    }
    jinja = jinja2.get_jinja2()
    response.write(jinja.render_template('error.html', **params))


#base handler
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
        if verify :
                params = {
                'page' : 'write',
                'pending' :  'pending'
                }
        else :
            gtoken =  ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
            save = model.Auth(token = gtoken)
            save.put()

            # in production
            mail.send_mail(sender="Vikash Kumar <mailkumarvikash@gmail.com>",
              to="Vikash Kumar <mailkumarvikash@gmail.com>",
              subject="Link to write blog",
              body="""
                https://blog.vikashkumar.me/write/%s
            """, %(gtoken))
            params = {
                'page' : 'token'
                'message' : 'check your mail for link to write'
            }

            # for test
            # url = 'http://localhost:8080/blog/write/' + gtoken
            params = {
                'page' : 'token',
                'url' : ''
            }

        self.render_response('write.html',**params)


#welcome page handler
class HomeHandler(BaseHandler):
    def get(self):
        params = {
            'page' : 'home'
        }
        self.render_response('home.html',**params)

#handler for blog
class BlogHandler(BaseHandler):
    def get(self):
        #code to search the database for blog posts
        article = model.Article.query().order(-model.Article.date)

        params = {
            'page' : 'blog',
            'article' : article
        }
        self.render_response('blog.html',**params)

#handler for serving article
class ArticleHandler(BaseHandler):
    def get(self, **kwargs):
        article_url = kwargs['article_url']
        article_content = model.Article.query(model.Article.url == article_url).fetch()

        if article_content:
            for article in article_content:
                content =  markdown.markdown(article.content, extras=["code-friendly"])
                tittle = article.tittle
                date = article.date
            params = {
                'page' : 'article',
                'tittle' : tittle,
                'content' : content,
                'date' : date
            }
            self.render_response('article.html',**params)
        else:
            self.abort(404)
            return


#handler for writing blog
class WriteHandler(BaseHandler):
    # add function to authenticate user
    def get(self, **kwargs):
        auth = kwargs['token']
        verify = model.Auth.query(model.Auth.token == auth).get()
        if verify :
            params = {
                'page' : 'write',
                'welcome' : ''
            }

            self.render_response('zenpen.html',**params)
            return

        else:
            self.redirect('/write')
            return

        #code for redirecting to generate token

        #first check authentication
    def post(self, **kwargs):
        auth = kwargs['token']
        verify = model.Auth.query(model.Auth.token == auth).get()
        if verify :
            header = self.request.get('header')
            content = self.request.get('text')
            url = header.replace(' ','-').lower()
            save = model.Article(tittle = header,
                                content = content,
                                url = url)
            save.put()
            token = model.Auth.query().get()
            token.key.delete()

        else :
            self.abort(404)
            return


#handler for about page
class AboutHandler(BaseHandler):
    def get(self):
        params = {
            'page' : 'about'
        }
        self.render_response('about.html',**params)

#error handler
class ErrorHandler(BaseHandler):
    def get(self,*args):
        params = {
            'error' : error
        }
        self.response.write(error)


app = webapp2.WSGIApplication([
    routes.DomainRoute('blog.vikashkumar.me', [
    routes.RedirectRoute('/write', handler=BaseHandler, name='authentication', handler_method='authentication', strict_slash=True),
        routes.RedirectRoute('/write/<token>', handler=WriteHandler, name='write', strict_slash=True),
        routes.RedirectRoute('/<article_url>', handler=ArticleHandler, name='article', strict_slash=True),
        routes.RedirectRoute('/', handler=BlogHandler, name='blog', strict_slash=True),
    ]),
    routes.RedirectRoute('/about', handler=AboutHandler, name='about', strict_slash=True),
    routes.RedirectRoute('/blog/<article_url>', handler=ArticleHandler, name='article', strict_slash=True),
    routes.RedirectRoute('/', handler=HomeHandler, name='home', strict_slash=True),
    ],
    debug=True)

#errors
app.error_handlers[404] = error
app.error_handlers[500] = error
