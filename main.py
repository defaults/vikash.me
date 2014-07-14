import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    autoescape=True,
    extensions=['jinja2.ext.autoescape'])

class MainHandler(webapp2.RequestHandler):

    template = JINJA_ENVIRONMENT.get_template('home.html')
    self.response.write(template.render())


app = webapp2.WSGIApplication(
    [
     ('/', MainHandler),
     ],
    debug=True)