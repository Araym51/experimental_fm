import quopri
from wsgiref.util import setup_testing_defaults
from .requests_separator import PostRequest, GetRequest
from .template_render import render_template


class PageNotFoundView:
    def __call__(self, request):
        return '404 WHAT', render_template('404_not_found.html')


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
        request = {}
        # получаем метод запроса из environ
        method = environ['REQUEST_METHOD']
        request['method'] = method
        # обработка GET и POST запросов:
        if method == 'POST':
            data = PostRequest().request_params(environ)
            request['data'] = data
            print(f'Пришёл post запрос: {Application.decode_value(data)}')
        if method == 'GET':
            request_parametrs = GetRequest.get_req_params(environ)
            request['request_params'] = request_parametrs
            print(f'Пришел get запрос {request_parametrs}')

        # ищем нужный контроллер
        if path in self.routes_lst:
            view = self.routes_lst[path]  # получаем view, потом передаем аргументы.
        else:
            view = PageNotFoundView()

        for front in self.front_list:
            front(request)

        # получаем код ответа из созданного view
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        """метод для исправления декодирования строки из ASCII в UTF-8"""
        fixed_data = {}
        for key, value in data.items():
            fixed_value = bytes(value.replace('%', '=').replace('+', ' '), 'UTF-8')
            fixed_value_str = quopri.decodestring(fixed_value).decode('UTF-8')
            fixed_data[key] = fixed_value_str
        return fixed_data
