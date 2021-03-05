import os
import yaml
import requests
import subprocess
import random
Loader_Requests = lambda path: yaml.load(requests.get(path).content, Loader=yaml.FullLoader)
Loader_YAML = lambda path: yaml.load(open(path), Loader=yaml.FullLoader)
os.environ["FILES_STORAGE"] = "https://raw.githubusercontent.com/CircuitalMinds/FractalMetric/localhost"
os.environ['PATH_DB'] = "/circuitalminds/databases/"
local_config = "./saponis/_config.yml"


class Settings:

    def __init__(self):
        config = Loader_YAML(local_config)
        self.database_path = os.environ.get("FILES_STORAGE") + os.environ.get("PATH_DB")
        self.root_path = "../root_server/"
        self.host, self.port, self.debug = config["HOST"], config["PORT"], config["DEBUG"]
        self.routes, self.libs, self.templates, self.index_builder, self.websites = self.config()
        self.url_server = self.apps("CircuitalMinds")
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
        websites = {"blog": "https://circuitalminds.github.io/blog/",
                    "pyfullstack": "https://circuitalminds.github.io/pyfullstack/",
                    "portfolio": "https://alanmatzumiya.github.io/",
                    "desktop": "https://circuitalminds.github.io/desktop"}
        return routes, libs, templates, index_builder, websites

    @staticmethod
    def apps(app):
        host = {"CircuitalMinds": "https://circuitalminds.herokuapp.com/",
                "jupyter": "https://jupyternbs.herokuapp.com/notebooks/"}
        return host[app]


    def get_music(self):
        return yaml.load(subprocess.getoutput("python3 ./saponis/get_music.py"), Loader=yaml.FullLoader)


    def get_notebooks(self, topic, module):
        notebooks = {}
        nbs = list(Loader_Requests(self.database_path + "db_yaml/" + topic + ".yml")[topic][module].values())
        for nb in nbs:
            notebooks[nb["name"]] = {"url": nb["url"], "app": nb["app"]}
        return notebooks

    def get_repos(self, user):
        data_repos = Loader_Requests(self.database_path + "db_yaml/repos.yml")
        repos = {}
        for repo in data_repos[user]:
            repos[repo] = data_repos[user][repo]
        return repos

    @staticmethod
    def covid19(country=None):
        API = "https://covid19.mathdro.id/api/"
        if country is None:
            data = requests.get(API).json()
            covid_data = {"lastUpdate": data["lastUpdate"][0:10].replace('-', '/'),
            "confirmed": data['confirmed']['value'],
            "recovered": data['recovered']['value'],
            "deaths": data["deaths"]['value'],
            "source": data["source"],
            "countries": [country['name'] for country in requests.get(
                API + "countries").json()['countries']]}
            return covid_data
        else:
            data = requests.get(API + "countries/" + country).json()
            return {"recovered": data['recovered']['value'],
                    "confirmed": data['confirmed']['value'],
                    "deaths": data['deaths']['value']}


class Blog:
    url = "https://raw.githubusercontent.com/CircuitalMinds/blog/main/"
    post = {1: dict(text="El tiempo cósmico es igual para todos, pero el tiempo humano difiere con cada persona. El tiempo corre de la misma manera para todos los seres humanos; pero todo ser humano flota de distinta manera en el tiempo. — Yasunari Kawabata",
                    date="2020/09/08 20:16:55",
                    title='How infinite can time be?',
                    pic="img/01.jpg"),
            2: dict(text="A veces, las cosas más sencillas y normales pueden convertirse en acontecimientos extraordinarios, simplemente si las llevaran a cabo con las personas adecuadas; y puedes ser solamente una persona para el mundo, pero para una persona tú eres el mundo.",
                    date="2020/09/14 13:45:55",
                    title="Birthdays",
                    pic="img/little-pigs2.png"),
            3: dict(text="Se repiten en multitud, liberandose en aparente anarquía preciosa estructura pintada en fragmentos disjuntos; El Infinito expresando su arte más auténtico.",
                    date="2020/10/08 10:30:55",
                    title="What does it mean to feel millions of dreams come real?",
                    pic="img/mandel-fractal-01.png"),
            4: dict(text="Dando vueltas, con gracia. Ir a ninguna parte, rápidamente Soy mayor; Día a día rapido envejezco pero regresando a mi infancia. Gira y gira pacientemente, perdiendose por el guía. Y estoy todo nervioso por nada.",
                    date="2021/01/01 12:00:00",
                    title="CircuitalMinds, their fractalized meaning.",
                    pic="img/circuital_post.jpg")}
    def __init__(self):
        IterPost = lambda data: list(self._post(data[key]) for key in list(data.keys()))
        self.posts =  IterPost(Blog.post)

    class _post(object):
        def __init__(cls, posdata):
            cls.text = posdata["text"]
            cls.date = posdata["date"]
            cls.title = posdata["title"]
            cls.pic = Blog.url + posdata["pic"]
