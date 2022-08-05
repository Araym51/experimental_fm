from wsgiref.util import setup_testing_defaults


class PageNotFoundView:
    def __call__(self):
        return '404 WHAT', [b'404 PAGE Not Found']


class Application:
    """основной класс для работы фреймворка"""
    def __init__(self, routes):
        """
        :param routes: переменная хранит все адреса сайта
        """
        self.routes = routes

    def __call__(self, environ, start_response):
        # для запуска сервера применяем значения uwsgi по умолчанию
        setup_testing_defaults(environ)
        # получаем путь от пользователя
        path = environ['PATH_INFO']
        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFoundView

        # получаем код ответа из созданного view
        code, body = view()
        start_response(code, body)
        return body



