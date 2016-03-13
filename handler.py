import logging

import webapp2

app = webapp2.WSGIApplication([
        routes.RedirectRoute(
            '/articlesgi',
            handler=blog.ArticleHandler, name='article', strict_slash=True),
        routes.RedirectRoute(
            '/subscribers',
            handler=blog.SubscriberHandler,
            name='subscriber', strict_slash=True),
        routes.RedirectRoute(
            '/tags',
            handler=blog.TagHandler, name='tag', strict_slash=True),
        routes.RedirectRoute(
            '/auth',
            handler=blog.AuthHandler, name='auth', strict_slash=True),
    ])
