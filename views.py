from framework.template_render import render


# views
class IndexView:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date'))


class AboutView:
    def __call__(self, request):
        return '200 OK', render('about.html')


class ContactView:
    def __call__(self, request):
        return '200 OK', render('contact_us.html')

# пути в приложении:
routes = {
    '/': IndexView,
    '/about/': AboutView,
    '/contact_us/': ContactView,
}
