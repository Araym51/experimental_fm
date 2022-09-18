from wsgiref.simple_server import make_server


# функция для запуска сервера
def run_wsgi(host, port, app):
    with make_server(host=host, port=port, app=app) as httpd:
        print(f'Running server at http://{host}:{port}')
        httpd.serve_forever()
