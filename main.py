import webapp2
import os
import logging
import urllib


from webapp2_extras import routes
from webapp2_extras import jinja2


def error(request, response, exception):
    logging.exception(exception)
    params = {
        'error' : exception.code
    }
    jinja = jinja2.get_jinja2()
    response.write(jinja.render_template('error.html', **params))

class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

    def render_response(self, _template, **params):
        # Renders a template and writes the result to the response.
        temp = self.jinja2.render_template(_template, **params)
        self.response.write(temp)


class HomeHandler(BaseHandler):
    def get(self):
        params = {

        }
        self.render_response('home.html',**params)

class BlogHandler(BaseHandler):
    def get(self):
        params = {

        }
        self.render_response('blog.html',**params)

class WwwHandler(BaseHandler):
    def get(self):
        self.redirect('http://vikashkumar.me')

class ErrorHandler(BaseHandler):
    def get(self,*args):
        params = {
            'error' : error
        }
        self.response.write(error)


app = webapp2.WSGIApplication([
    routes.DomainRoute('blog.vikashkumar.me', [
        webapp2.Route('/', handler=BlogHandler, name='blog'),
    ]),
    routes.DomainRoute('www.vikashkumar.me', [
        webapp2.Route('/', handler=WwwHandler, name='www'),
    ]),
    webapp2.Route('/', handler=HomeHandler, name='home'),
    ],
    debug=True)


app.error_handlers[404] = error
app.error_handlers[500] = error