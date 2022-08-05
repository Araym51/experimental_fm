from framework.server_launcher import run_wsgi
from framework.main import Application
from pages_fronts import routes, fronts

application = Application(routes, fronts)
run_wsgi(application, 8000)
