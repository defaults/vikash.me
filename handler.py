import logging

import webapp2
from webapp2_extras import routes

from controllers import blog


config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'some-secret-key',
}

app = webapp2.WSGIApplication([
        routes.RedirectRoute(
            '/api/articles',
            handler=blog.ArticleHandler,
            name='article',
            handler_method='all_articles', strict_slash=True, methods=['GET']),
        routes.RedirectRoute(
            '/api/article',
            handler=blog.ArticleHandler, name='article', strict_slash=True),
        routes.RedirectRoute(
            '/api/subscribers',
            handler=blog.SubscriberHandler,
            name='subscriber', strict_slash=True),
        routes.RedirectRoute(
            '/api/tag',
            handler=blog.TagHandler, name='tag', strict_slash=True),
        routes.RedirectRoute(
            '/api/short',
            handler=blog.UrlShortnerHandler, name='short', strict_slash=True),
        routes.RedirectRoute(
            '/auth',
            handler=blog.BlogHandler,
            name='auth', handler_method='authentication', strict_slash=True),
    ], config=config, debug=True)
