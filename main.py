import webapp2
import jinja2
import os
import datetime
import cgi
import json


class MainHandler(webapp2.RequestHandler):
    self.response.render('index.html')

app = webapp2.WSGIApplication(
    [
     ('/', MainHandler),
     ],
    debug=True)