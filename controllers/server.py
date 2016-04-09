import datetime
import string

import webapp2
from google.appengine.api import mail
from webapp2_extras import jinja2

from config import config


class BaseHandler(webapp2.RequestHandler):
    """Base handler for webpage"""

    @webapp2.cached_property
    def jinja2(self):
        """Returns a Jinja2 renderer cached in the app registry."""
        return jinja2.get_jinja2(app=self.app)

    def render_response(self, _template, **params):
        """Renders a template and writes the result to the response."""
        temp = self.jinja2.render_template(_template, **params)
        self.response.write(temp)

    def send_email(self, emailTo, emailSubject, emailBody):
        """method to send mail"""
        mail.send_mail(sender=config.admin['admin_mail'],
                       to=emailTo,
                       subject=emailSubject,
                       body=emailBody)

        return


class HomeHandler(BaseHandler):
    """Welcome page handler"""

    def get(self):
        params = {
            'page': 'Vikash Kumar'
        }
        self.render_response('home.html', **params)


class AboutHandler(BaseHandler):
    """About page handler"""

    def get(self):
        params = {
            'page': 'about'
        }
        self.render_response('about.html', **params)
