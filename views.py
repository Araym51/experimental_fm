from framework.template_render import render


# views
class IndexView:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date'))


class AboutView:
    def __call__(self, request):
        return '200 OK', 'About us'


# пути в приложении:
routes = {
    '/': IndexView,
    '/about/': AboutView,
}
