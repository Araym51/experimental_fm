from framework.server_launcher import run_wsgi
from framework.main import Application
from views import routes
from middleware import fronts

application = Application(routes, fronts)
run_wsgi(application, 8000)
