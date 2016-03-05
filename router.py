import logging

import webapp2

from controllers import server
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
        routes.RedirectRoute('/write', handler=server.BaseHandler, name='authentication', handler_method='authentication', strict_slash=True),
        routes.RedirectRoute('/write/<token>/', handler=server.WriteHandler, name='write', strict_slash=True),
        routes.RedirectRoute('/<article_url>/', handler=server.ArticleHandler, name='article', strict_slash=True),
        routes.RedirectRoute('/', handler=server.BlogHandler, name='blog', strict_slash=True),
    ]),
    routes.RedirectRoute('/about', handler=server.AboutHandler, name='about', strict_slash=True),
    routes.RedirectRoute('/blog', handler=server.BlogHandler, name='blog', strict_slash=True),
    routes.RedirectRoute('/write', handler=server.BaseHandler, name='authentication', handler_method='authentication', strict_slash=True),
    routes.RedirectRoute('/blog/write/<token>', handler=server.WriteHandler, name='write', strict_slash=True),
    routes.RedirectRoute('/blog/<article_url>/', handler=server.ArticleHandler, name='article', strict_slash=True),
    routes.RedirectRoute('/', handler=server.HomeHandler, name='home', strict_slash=True),
])

# errors
app.error_handlers[404] = error
app.error_handlers[500] = error
