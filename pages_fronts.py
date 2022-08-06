from datetime import date
from framework.template_render import render


# views
class IndexView:
    def __call__(self, request):
        return '200 OK', 'Index'
        #todo заменить на render('index.html', data=request.get('data', None))


class AboutView:
    def __call__(self, request):
        return '200 OK', 'About us'


# пути в приложении:
routes = {
    '/': IndexView,
    '/about/': AboutView,
}


# front controllers:

def secret_front(request):
    request['data'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]
