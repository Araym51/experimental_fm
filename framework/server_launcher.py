from wsgiref.simple_server import make_server


# функция для запуска сервера
def run_wsgi(host, port, app):
    """
    :param host: адрес на которм запускается сервер
    :param port: порт на котором запускается сервер
    :param app: приложение
    """
    with make_server(host=host, port=port, app=app) as httpd:
        print(f'Running server at http://{host}:{port}')
        httpd.serve_forever()
