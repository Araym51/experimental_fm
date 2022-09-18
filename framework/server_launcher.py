from wsgiref.simple_server import make_server


# функция для запуска сервера
def run_wsgi(app, port):
    with make_server('', port, app) as httpd:
        print(f'Running server on port {port}')
        httpd.serve_forever()
