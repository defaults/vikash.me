import webapp2
import jinja2
import os


from webapp2_extras import routes

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    autoescape=True,
    extensions=['jinja2.ext.autoescape'])


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())

class SubdomainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("blogging")

app = webapp2.WSGIApplication([
    routes.DomainRoute('blog.vikashkumar.me', [
        webapp2.Route('/', handler=SubdomainHandler, name='home'),
    ]),
    routes.DomainRoute('www.vikashkumar.me', [
        webapp2.Route('/', handler=MainHandler, name='home'),
    ]),
    webapp2.Route('/', handler=MainHandler, name='home'),
    ],
    debug=True)