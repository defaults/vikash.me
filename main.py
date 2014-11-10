import webapp2
import os
import logging
import urllib


from webapp2_extras import routes
from webapp2_extras import jinja2

#method for handling errors
def error(request, response, exception):
    logging.exception(exception)
    params = {
        'error' : exception.code
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

#welcome page handler
class HomeHandler(BaseHandler):
    def get(self):
        params = {

        }
        self.render_response('home.html',**params)
#handler for blog
class BlogHandler(BaseHandler):
    def get(self):
        params = {

        }
        self.render_response('blog.html',**params)

#handler for about page
class AboutHandler(BaseHandler):
    def get(self):
        params = {

        }
        self.render_response('about.html',**params)


#handler to redirect to naked domain
class WwwHandler(BaseHandler):
    def get(self):
        self.redirect('http://vikashkumar.me')


#error handler
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
    webapp2.Route('/about', handler=AboutHandler, name='about'),
    webapp2.Route('/', handler=HomeHandler, name='home'),
    ],
    debug=True)

#errors
app.error_handlers[404] = error
app.error_handlers[500] = error