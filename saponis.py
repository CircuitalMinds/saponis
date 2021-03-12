from saponis_server import sapon_server
from flask import Flask
from flask_login import LoginManager
from flask.helpers import BadRequest
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
import os
from jinja2.exceptions import TemplateNotFound


# environ
os.environ['SECRET'] = "saponis"

# load configuration
saponis = Flask(__name__, template_folder='./templates', static_folder='./static')
saponis.config['SECRET_KEY'] = "saponis"
saponis.config['SESSION_TYPE'] = 'filesystem'
CORS(saponis)
login = LoginManager(app=saponis)
session = saponis.session_interface

socketio = SocketIO(saponis, manage_session=False)

# server instance
sapon = sapon_server(saponis)

# server routes
routes = sapon.routes

# main and subtemplates views
saponis.add_url_rule(
    routes['base'], 'home', sapon.home, methods=['GET', 'POST'])
saponis.add_url_rule(
    routes['base'] + '<path>', 'routes', sapon.base, methods=['GET', 'POST'])

# error handlers
saponis.register_error_handler(TemplateNotFound, sapon.error404)
saponis.register_error_handler(BadRequest, sapon.error500)


if __name__ == '__main__':

    socketio.run(saponis,
                 host=sapon.host,
                 port=sapon.port,
                 debug=sapon.debug)
