import webapp2

from controllers import server
from controllers import blog
from webapp2_extras import routes

app = webapp2.WSGIApplication([
    routes.DomainRoute('blog.vikash.me', [
        routes.RedirectRoute(
            '/write',
            handler=blog.BlogHandler,
            name='authentication',
            handler_method='authentication', strict_slash=True),
        routes.RedirectRoute(
            '/write/<token>/',
            handler=blog.WriteHandler, name='write', strict_slash=True),
        routes.RedirectRoute(
            '/<article_url>/',
            handler=blog.ArticleHandler, name='article', strict_slash=True),
        routes.RedirectRoute(
            '/write/resend_mail',
            handler=blog.BlogHandler, name='resend_mail',
            handler_method='resend_mail', strict_slash=True),
        routes.RedirectRoute(
            '/dashboard/',
            handler=blog.DashboardHandler, name='dashboard',
            strict_slash=True),
        routes.RedirectRoute(
            '/',
            handler=blog.ArticlesListHandler, name='blog',
            strict_slash=True),
    ]),
    routes.RedirectRoute(
        '/about',
        handler=server.AboutHandler, name='about', strict_slash=True),
    routes.RedirectRoute(
        '/blog',
        handler=blog.ArticlesListHandler, name='blog', strict_slash=True),
    routes.RedirectRoute(
        '/write',
        handler=blog.BlogHandler, name='authentication',
        handler_method='authentication', strict_slash=True),
    routes.RedirectRoute(
        '/write/resend_mail',
        handler=blog.BlogHandler, name='resend_mail',
        handler_method='resend_mail', strict_slash=True),
    routes.RedirectRoute(
        '/blog/write/<token>',
        handler=blog.WriteHandler, name='write', strict_slash=True),
    routes.RedirectRoute(
        '/blog/<article_url>/',
        handler=blog.ArticleHandler, name='article', strict_slash=True),
    routes.RedirectRoute(
        '/blog/dashboard/',
        handler=blog.DashboardHandler, name='dashboard', strict_slash=True),
    routes.RedirectRoute(
        '/', handler=server.HomeHandler, name='home', strict_slash=True),
    routes.RedirectRoute(
        '/_ah/warmup', handler=server.BaseHandler,
        name='warmup', handler_method='warmup')
])

# errors
app.error_handlers[404] = server.error_handlar
app.error_handlers[500] = server.error_handlar
