import datetime
import string

import webapp2
from google.appengine.api import mail
from webapp2_extras import jinja2

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


# handler for about page
class AboutHandler(BaseHandler):
    def get(self):
        params = {
            'page': 'about'
        }
        self.render_response('about.html', **params)
