import logging

import webapp2

from controllers import server
from controllers import blog
from webapp2_extras import jinja2
from webapp2_extras import routes


# method for handling errors
def error(request, response, exception):
    logging.exception(exception)
    params = {
        'error': exception
    }
    jinja = jinja2.get_jinja2()
    response.write(jinja.render_template('error.html', **params))


app = webapp2.WSGIApplication([
    routes.DomainRoute('blog.vikashkumar.me', [
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
        '/', handler=server.HomeHandler, name='home', strict_slash=True),
])

# errors
app.error_handlers[404] = error
app.error_handlers[500] = error
