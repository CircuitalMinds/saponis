import os
import yaml
import requests
Loader_Requests = lambda path: yaml.load(requests.get(path).content, Loader=yaml.FullLoader)
Loader_YAML = lambda path: yaml.load(open(path), Loader=yaml.FullLoader)
os.environ["FILES_STORAGE"] = "https://raw.githubusercontent.com/CircuitalMinds/FractalMetric/localhost"
os.environ['PATH_DB'] = "/circuitalminds/databases/"
local_config = "./saponis_server/_config.yml"


class Settings:

    def __init__(self):
        config = Loader_YAML(local_config)
        self.database_path = os.environ.get("FILES_STORAGE") + os.environ.get("PATH_DB")
        self.root_path = "../root_server/"
        self.host, self.port, self.debug = config["HOST"], config["PORT"], config["DEBUG"]
        self.routes, self.libs, self.templates, self.index_builder = self.config()
        self.path_index = "/list.html"
        self.index_title = 'FractalMetric'
        path_img = "static/images/saponis_img/"
        self.saponis_img = {img: "./" + path_img + img for img in os.listdir("./" + path_img)}

    @staticmethod
    def config():
        routes = {"base": "/"}
        libs = {"fractal-vendors": "./static/vendors", "fractal-css": "./static/css/index.css",
                "fractal-js": "./static/js", "fractal-img": "./static/images", "fractal-data": "./static/data"}
        templates = {
            f.replace('.html', ''): '/' + f.replace('.html', '') for f in os.listdir('./templates/subtemplates')}
        index_builder = {
            "head": "head.html",
            "header": "header.html",
            "navigation": "navigation.html",
            "footer": "footer.html",
            "navbar": "navbar.html",
            "javascripts": "javascripts.html"}
        return routes, libs, templates, index_builder
