import logging

import webapp2
from webapp2_extras import routes

from controllers import blog

app = webapp2.WSGIApplication([
        routes.RedirectRoute(
            '/api/articles',
            handler=blog.ArticleHandler, name='article', strict_slash=True),
        routes.RedirectRoute(
            '/api/subscribers',
            handler=blog.SubscriberHandler,
            name='subscriber', strict_slash=True),
        routes.RedirectRoute(
            '/api/tags',
            handler=blog.TagHandler, name='tag', strict_slash=True),
        routes.RedirectRoute(
            '/auth',
            handler=blog.AuthHandler, name='auth', strict_slash=True),
    ], debug=True)
