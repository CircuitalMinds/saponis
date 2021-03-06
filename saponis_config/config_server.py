from flask import render_template

import os
import yaml


class ServerApp:
    """Class to build Server for using API.

    """

    def __init__(self, app):
        super(ServerApp, self).__init__()
        # app instance
        self.app = app
        self.router = self.app.add_url_rule
        self.routes, self.libs, self.templates, self.index_builder = None, None, None, None
        self.template = {}

    def base(self, path=None):
        if path is None or path == "/":
            return render_template(self.template, **self.template)
        elif path in list(self.templates.keys()):
            return self.add_subpath(path)
        else:
            return self.error(404)

    def api_router(self, query):
        query = self.index_builder
        return "ok"

    def error(self, e):
        self.template["title"] = f"Error{e}"
        self.template["libs"] = self.back(self.libs)
        template = f"./views/{e}.html"
        return render_template(template, **self.template)

    def add_subpath(self, path=None):
        template = "./subtemplates/" + path + '.html'
        return render_template(template, **self.template)

    @staticmethod
    def back(lib):
        return {name: '../' + lib[name] for name in list(lib.keys())}
