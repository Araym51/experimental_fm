from wsgiref.util import setup_testing_defaults


class PageNotFoundView:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Application:
    """основной класс для работы фреймворка"""
    def __init__(self, routes_lst, front_list):
        """
        :param routes_lst: переменная хранит все адреса сайта
        :param front_list: переменная хранит middleware
        """
        self.routes_lst = routes_lst
        self.front_list = front_list

    def __call__(self, environ, start_response):
        # получаем путь от пользователя
        path = environ['PATH_INFO']
        # проверяем, заканчивается ли на / адрес
        if not path.endswith('/'):
            path += '/'

        # ищем нужный контроллер
        if path in self.routes_lst:
            view = self.routes_lst[path]()  # получаем view, потом передаем аргументы.
        else:
            view = PageNotFoundView()
        request = {}
        for front in self.front_list:
            front(request)

        # получаем код ответа из созданного view
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
