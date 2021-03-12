from flask import render_template
from .config import Settings


class Server(Settings):
    """Class to build Server for using API.

    """

    def __init__(self, app):
        super(Server, self).__init__()
        # app instance
        self.app = app

    def base(self, path):
        if path in list(self.templates.keys()):
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
            subroutes=self.templates
        )

    @staticmethod
    def back(lib):
        return {name: '../' + lib[name] for name in list(lib.keys())}
