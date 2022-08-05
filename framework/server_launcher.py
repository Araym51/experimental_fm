from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server

def application(environ, start_response):
    setup_testing_defaults(environ)
    print(type(environ))
    print(environ)
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'hello wsgi!']

with make_server('', 8000, application) as  httpd:
    print('Running server on port 8000')
    httpd.serve_forever()