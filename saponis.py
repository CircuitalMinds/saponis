from saponis import server, get_db, YoutubeApi
from flask import Flask, jsonify, request, Response
from flask_login import LoginManager
from flask.helpers import BadRequest
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
import os
from jinja2.exceptions import TemplateNotFound
import requests


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
saponis_server = server(saponis)

# server routes
routes = saponis_server.routes

# main and subtemplates views
saponis.add_url_rule(
    routes['base'], 'home', saponis_server.home, methods=['GET', 'POST'])
saponis.add_url_rule(
    routes['base'] + '<path>', 'routes', saponis_server.base, methods=['GET', 'POST'])

# error handlers
saponis.register_error_handler(TemplateNotFound, saponis_server.error404)
saponis.register_error_handler(BadRequest, saponis_server.error500)

@saponis.route("/music/play")
def play_song():
    song_id = request.args.get("song_id")
    return jsonify(saponis_server.get_song(song_id))

@saponis.route("/repos/<user>")
def repos(user):
    return jsonify(saponis_server.get_repos(user))

@saponis.route("/notebooks/<topic>")
def notebooks(topic):
    module = request.args.get("module")
    return jsonify(saponis_server.get_notebooks(topic, module))

@saponis.route("/covid/<country>")
def covid(country):
    return jsonify(saponis_server.covid19(country[0].upper() + country[1:]))

def search_data(data=None):
    url = "https://circuitaldb.herokuapp.com/api/"
    if data is None:
        return requests.get(url + "query?book=searches").json()
    else:
        requests.get(url + "search?video_title=" + data["video_title"] + "&video_id=" + data["video_id"])

@saponis.route("/youtube/search/<search>")
def yt_search(search):
    searches = saponis_server.app.config["data"]["searches"]
    if list(searches.keys()) == [] or search not in list(searches.keys()):
        data = YoutubeApi(song=search).data["search_data"]
        saponis_server.app.config["data"]["searches"][search] = data
        search_data(data={"video_title": data["video_title"],
                          "video_id": data["video_url"].replace("https://www.youtube.com/watch?v=", "")})
        return jsonify({"search": data})
    else:
        return jsonify({"search": searches[search]})

@saponis.route("/check_data/<option>")
def check_data(option):
    if option == "get":
        return jsonify(saponis_server.app.config["data"])
    elif option == "delete":
        saponis_server.app.config["data"]["searches"]["select"] = []
        return jsonify(saponis_server.app.config["data"])
    elif option == "select":
        url = request.args.get("url")
        saponis_server.app.config["data"]["searches"]["select"].append(url)
        return jsonify({"select": saponis_server.app.config["data"]["searches"]["select"]})


if __name__ == '__main__':

    socketio.run(saponis,
                 host=saponis_server.host,
                 port=saponis_server.port,
                 debug=saponis_server.debug)
