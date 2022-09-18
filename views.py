from framework.template_render import render_template


# views
class IndexView:
    def __call__(self, request):
        return '200 OK', render_template('index.html', date=request.get('date'))


class AboutView:
    def __call__(self, request):
        return '200 OK', render_template('about.html')


class ContactView:
    def __call__(self, request):
        return '200 OK', render_template('contact_us.html')

# пути в приложении:
routes = {
    '/': IndexView,
    '/about/': AboutView,
    '/contact_us/': ContactView,
}
