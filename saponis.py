from flask import Flask, render_template
from flask_login import LoginManager
from flask.helpers import BadRequest
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
import os
import yaml
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

_config = yaml.load(open("./saponis_server/_config.yml"), Loader=yaml.FullLoader)
host, port, debug = _config["HOST"], _config["PORT"], _config["DEBUG"]

# main and subtemplates views
@saponis.route("/", methods=["GET", "POST"])
def home():
    path = "./static/images/saponis"
    config = {"images": f"../{path}",
    "products": [f"../{path}/products/{product}" for product in os.listdir(f"{path}/products")]}
    return render_template("saponis.html", config=config)



if __name__ == '__main__':

    socketio.run(saponis,
                 host=host,
                 port=port,
                 debug=debug)
