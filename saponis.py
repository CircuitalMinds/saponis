from flask import Flask, render_template, send_from_directory, request, redirect, url_for
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import os
import yaml
from saponis_config import server_app


os.environ['SECRET'] = "saponis"
saponis = Flask(__name__, template_folder='./templates', static_folder='./static')
saponis.config['SECRET_KEY'] = "saponis"
saponis.config['SESSION_TYPE'] = 'filesystem'
saponis.config['STORAGE'] = "./storage"

CORS(saponis)
cross_origin(CORS)
login = LoginManager(app=saponis)
session = saponis.session_interface
socketio = SocketIO(saponis, manage_session=False)

server_app = server_app(app=saponis)
_config = yaml.load(open("./saponis_config/_config.yml"), Loader=yaml.FullLoader)
host, port, debug = _config["HOST"], _config["PORT"], _config["DEBUG"]


def upload_template():
    allowed_file = lambda filename: '.' in filename and filename.rsplit('.', 1)[1].lower() in {
        'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', "mp4", "mp3"}
    _template = '''<!doctype html>\n'''
    _template += '''<title>Upload File</title>\n'''
    _template += '''<h1>Upload File</h1>\n'''
    _template += '''<form method=post enctype=multipart/form-data>\n'''
    _template += '''<input type=file name=file>\n'''
    _template += '''<input type=submit value=Upload>\n'''
    _template += '''</form>\n'''
    response_template = lambda response="": f'''{_template}<p>{response}</p>'''
    return response_template, allowed_file


@saponis.route("/", methods=["GET", "POST"])
@saponis.route("/<path>", methods=["GET", "POST"])
def home(path=None):
    if path == "storage":
        return redirect(url_for("storage_files"))    
    else:
        products_path = "./storage/products"
        config_files = {"path": "./storage", "products":
            [f"{products_path}/{product}" for product in os.listdir(f"{products_path}")]}
        return render_template("saponis.html", config_files=config_files)


@saponis.route("/storage/<data>/<file_dir>", methods=["GET", "POST"])
def storage_files(data=None, file_dir=None):
    sections = ["products", "banners", "images"]
    if data in sections:
        files = os.listdir(f"./storage/{data}")
        print(files[files.index(file_dir)])
        return send_from_directory(saponis.config['STORAGE'] + "/" + data, files[files.index(file_dir)])
    filename = request.args.get("filename")
    response_template, allowed_file = upload_template()
    if request.method == 'POST':
        if 'file' not in request.files:
            response = "No file part"
            return response_template(response=response)
        file = request.files['file']
        if file.filename == '':
            response = 'No selected file'
            return response_template(response=response)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(saponis.config['STORAGE'], filename))
            response = f"{filename} uploaded"
            return response_template(response=response)
    elif filename is not None:
        if filename not in os.listdir("./storage"):
            response = f"filename with {filename} not exist, please upload file before"
            return response_template(response=response)
        else:
            return send_from_directory(saponis.config['STORAGE'], filename)
    else:
        return response_template()


if __name__ == '__main__':

    socketio.run(saponis,
                 host=host,
                 port=port,
                 debug=debug)
