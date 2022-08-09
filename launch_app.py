from framework.server_launcher import run_wsgi
from framework.main import Application
from views import routes
from middleware import fronts

application = Application(routes, fronts)
run_wsgi('127.0.0.1', 8000, application)
