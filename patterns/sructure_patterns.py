from time import time


# декоратор для путей в приложении
class Routes:
    def __init__(self, routes, url):
        """
        :param routes: словарь в котором содержатся пути
        :param url: путь для страницы
        """
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        """принимает класс который будет вызывать"""
        self.routes[self.url] = cls()


class Debug: # todo ДОКУМЕНТАЦИЯ!
    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def timeit(method):
            def timed(*args, **kwargs):
                begin = time()
                res = method(*args, **kwargs)
                end = time()
                delta = end - begin

                print(f'debug => {self.name} выполнялся {delta:2.2f} ms')
                return res
            return timed
        return timeit(cls)
