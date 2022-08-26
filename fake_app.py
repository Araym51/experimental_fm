from framework.main import Application
"""
Добавить фейковый (на все запросы пользователя отвечает: 200 OK, Hello from Fake).
"""


class FakeApp(Application):
    def __init__(self, routes_lst, front_list):
        self.app = Application(routes_lst, front_list)
        super().__init__(routes_lst, front_list)

    def __call__(self, env, response):
        response('200 OK', [('Content-Type', 'text/html')])
        return ['Hello from Fake']
