import datetime
import string
import os

import webapp2
import jinja2
import logging
from google.appengine.api import mail

from config import config

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(
        'public/build/')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


# method for handling errors
def error_handlar(request, response, exception):
    logging.exception(exception)
    params = {
        'error': exception
    }
    template = JINJA_ENVIRONMENT.get_template('templates/error.html')
    response.write(template.render(params))


class BaseHandler(webapp2.RequestHandler):
    """Base handler for webpage"""

    def render_response(self, _template, **params):
        print os.path
        """Renders a template and writes the result to the response."""
        template = JINJA_ENVIRONMENT.get_template('templates/' + _template)
        self.response.write(template.render(**params))

    def send_email(self, emailTo, emailSubject, emailBody):
        """method to send mail"""
        mail.send_mail(sender=config.admin['admin_mail'],
                       to=emailTo,
                       subject=emailSubject,
                       body=emailBody)

        return

    def warmup(self):
        pass


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
