import logging

import webapp2
from webapp2_extras import routes

from controllers import blog_api


config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'some-secret-key',
}

app = webapp2.WSGIApplication([
        routes.RedirectRoute(
            '/api/articles',
            handler=blog_api.ArticleHandler,
            name='get_all_articles',
            handler_method='all_articles', methods=['GET'], strict_slash=True),
        routes.RedirectRoute(
            '/api/article',
            handler=blog_api.ArticleHandler, name='post_article',
            methods=['POST'], strict_slash=True),
        routes.RedirectRoute(
            '/api/article/<id>',
            handler=blog_api.ArticleHandler, name='article',
            methods=['GET', 'PUT', 'DELETE'], strict_slash=True),
        routes.RedirectRoute(
            '/api/subscribers',
            handler=blog_api.SubscriberHandler,
            name='get_all_subscribers', methods=['GET'], strict_slash=True),
        routes.RedirectRoute(
            '/api/subscriber',
            handler=blog_api.SubscriberHandler,
            name='post_subscriber', methods=['POST'], strict_slash=True),
        routes.RedirectRoute(
            '/api/subscriber/<id>',
            handler=blog_api.SubscriberHandler,
            name='subscriber', methods=['DELETE'], strict_slash=True),
        routes.RedirectRoute(
            '/api/tags',
            handler=blog_api.TagHandler, name='get_all_tags',
            methods=['GET'], strict_slash=True),
        routes.RedirectRoute(
            '/api/tag',
            handler=blog_api.TagHandler, name='post_tag',
            methods=['POST'], strict_slash=True),
        routes.RedirectRoute(
            '/api/tag/<id>',
            handler=blog_api.TagHandler, name='delete_tag',
            methods=['DELETE'], strict_slash=True),
        routes.RedirectRoute(
            '/api/short',
            handler=blog_api.UrlShortnerHandler, name='short',
            methods=['GET', 'POST'], strict_slash=True),
        routes.RedirectRoute(
            '/api/short/<id>',
            handler=blog_api.UrlShortnerHandler, name='delete_short',
            methods=['DELETE'], strict_slash=True),
        routes.RedirectRoute(
            '/auth',
            handler=blog_api.BlogHandler,
            name='auth', handler_method='authentication', strict_slash=True),
    ], config=config)
