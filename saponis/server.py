from flask import redirect, render_template
from .config import Settings
import requests


class Server(Settings):
    """Class to build Server for using API.

    """

    def __init__(self, app):
        super(Server, self).__init__()
        # blog posts by CircuitalMinds
        requests.get("https://circuitaldb.herokuapp.com/api/message?name=circuitalminds&email=circuitalminds@gmail.com&category=2&message=Hello!+Alan")
        self.messages = requests.get("https://circuitaldb.herokuapp.com/api/query?book=messages").json()
        # app instance
        self.app = app
        self.app.config["data"] = {"searches": {}}
        self.app.config["data"]["select"] = []

    def base(self, path):
        if path in list(self.websites.keys()):
            return redirect(self.websites[path])
        elif path in list(self.templates.keys()):
            return self.add_subpath(path)
        else:
            return self.error404(404)

    def home(self):
        return render_template(self.path_index, index_parts=self.index_builder, title=self.index_title,
                               libs=self.libs, routes=self.routes, subroutes=self.templates,
                               saponis_img=self.saponis_img)

    def error404(self, e):
        title = "Error404"
        routes = self.routes
        libs = self.back(self.libs)
        template = "./views/404.html"
        return render_template(template, index_parts=self.index_builder, title=title,
                               libs=libs, routes=routes, subroutes=self.templates)

    def error500(self, e):
        title = "Error500"
        routes = self.routes
        libs = self.back(self.libs)
        template = "./views/500.html"
        return render_template(template, index_parts=self.index_builder, title=title,
                                libs=libs, routes=routes, subroutes=self.templates)

    def add_subpath(self, path=None):
        template = "./subtemplates/" + path + '.html'
        return render_template(
            template,
            index_parts=self.index_builder,
            libs=self.back(self.libs),
            routes=self.routes,
            subroutes=self.templates,
            messages=self.messages
        )
        
    def get_song(self, song_id):
        if not self.playlist:
            self.playlist = self.get_music()
        return self.playlist[int(song_id)]

    @staticmethod
    def back(lib):
        return {name: '../' + lib[name] for name in list(lib.keys())}
