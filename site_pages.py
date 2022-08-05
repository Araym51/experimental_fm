from .framework.server_launcher import run_wsgi


# views
class IndexView:
    def __call__(self):
        return '200 OK', [b'Index']


class AboutView:
    def __call__(self):
        return '200 OK', [b'About us']


routes = {
    '/': IndexView,
    'about': AboutView,
}


