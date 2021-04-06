import requests
from bs4 import BeautifulSoup
import yaml


class YoutubeApi:
    yt_url = "https://www.youtube.com/"
    search_query = yt_url + "results?search_query="
    watch = yt_url + "watch?v="

    def __init__(self):
        self.data_search = {}

    def scraper(self, tag, video_id=None, video_title=None, recursion=False):
        url = str
        if video_id is None:
            url = f"{YoutubeApi.search_query}{video_title}"
        elif video_title is None:
            url = f"{YoutubeApi.watch}{video_id}"
        data = requests.get(url).text
        return self.filter_tag(string=data, tag=tag, recursion=recursion)

    def get_search_list(self, video_title, max_search_results=20):
        if video_title in list(self.data_search.keys()):
            return self.data_search[video_title]
        else:
            video_ids = self.scraper(tag="videoId", video_title=video_title, recursion=True)
            self.data_search[video_title] = {}
            self.data_search[video_title]["search_list"] = []
            stop_results = 0
            for video_id in video_ids:
                video_data = self.scraper(tag="title", video_id=video_id)
                soup = BeautifulSoup(video_data, "html.parser")
                meta_tags = soup.findAll("meta")
                tags, keys = ["og:title", "og:url", "og:image"], ["video_title", "video_url", "video_image"]
                data = {"video_title": "", "video_url": "", "video_image": ""}
                stop = 0
                for meta in meta_tags:
                    meta_keys = list(meta.attrs.keys())
                    if "property" in meta_keys and meta.get("property") in tags:
                        stop += 1
                        key = keys[tags.index(meta.get("property"))]
                        data[key] = meta["content"]
                    if stop == 3:
                        break
                if list(data.values()).count("") != 3:
                    self.data_search[video_title]["search_list"].append(data)
                    stop_results += 1
                if stop_results == max_search_results:
                    break
            return {"search_list": self.data_search[video_title]["search_list"]}

    def get_search_song(self, video_title):
        if video_title in list(self.data_search.keys()):
            return self.data_search[video_title]
        else:
            self.data_search[video_title] = {}
            video_id = self.scraper(tag="videoId", video_title=video_title)
            video_data = self.scraper(tag="title", video_id=video_id)
            self.data_search[video_title]["video_id"] = video_id
            soup = BeautifulSoup(video_data, "html.parser")
            meta_tags = soup.findAll("meta")
            self.data_search[video_title]["meta_tags"] = {"name": {}, "property": {}, "itemprop": {}}
            _tags = ["name", "property", "itemprop"]
            for meta in meta_tags:
                _keys = list(meta.attrs.keys())
                if "name" in _keys:
                    self.data_search[video_title]["meta_tags"]["name"][meta.attrs["name"]] = meta.attrs["content"]
                elif "property" in _keys:
                    self.data_search[video_title]["meta_tags"]["property"][meta.attrs["property"]] = meta.attrs["content"]
                elif "itemprop" in _keys:
                    self.data_search[video_title]["meta_tags"]["itemprop"][meta.attrs["itemprop"]] = meta.attrs["content"]
            return {"search_song": self.data_search[video_title]}

    @staticmethod
    def select_meta_tags(meta_tags):
        data = {}
        def try_key(item, key):
            value = ""
            try:
                value = item[key]
            except KeyError:
                pass
            return value
        items = ["name", "property", "itemprop"]
        name = ["title", "description", "keywords", "twitter:card",
                "twitter:site", "twitter:url", "twitter:title",
                "twitter:description", "twitter:image"]
        property = ["og:site_name", "og:url", "og:title", "og:image",
                    "og:image:width", "og:image:height", "og:description",
                    "og:video:type", "og:video:width", "og:video:height",
                    "al:android:app_name", "al:android:package", "og:video:tag"]
        itemprop = ["name", "description", "videoId", "duration",
                    "unlisted", "width", "height", "playerType",
                    "interactionCount", "datePublished", "uploadDate", "genre"]
        select_tags = {"name": name, "property": property, "itemprop": itemprop}
        for item_name in items:
            item = meta_tags[item_name]
            for key in select_tags[item_name]:
                data[item_name + "_" + key.replace(":", "_")] = try_key(item=item, key=key)
        return data

    @staticmethod
    def get_base_data(meta_tags):
        def try_key(item, key):
            value = ""
            try:
                value = item[key]
            except KeyError:
                pass
            return value
        data = {}
        keys = ["og:title", "og:image", "og:url"]
        for key in keys:
            data[key.replace("og:", "video_")] = try_key(item=meta_tags["property"], key=key)
        return data

    @staticmethod
    def filter_tag(string, tag, recursion=False):
        _fix = tag
        stop = " "
        if tag in ["title", "meta", "head", "link", "div"]:
            tag = '<' + tag + ''
            stop = "\n"
        elif tag == "videoId":
            tag = '"' + tag + '":'
            stop = ','

        def new_string(_string, _tag, l, r):
                data = _string[l: l + r]
                if _fix == "videoId":
                    data = data.split(":")[-1][1:-1][0:11]
                _new_string = _string[l + r:]
                return data, _new_string
        if recursion:
            test = True
            data_collect = []
            while test:
                try:
                    l = string.index(tag)
                    r = string[l:].index(stop)
                    data, string = new_string(_string=string, _tag=tag, l=l, r=r)
                    if data not in data_collect:
                        data_collect.append(data)
                except ValueError:
                    test = False
                    pass
            return data_collect
        else:
            data = ""
            try:
                l = string.index(tag)
                r = string[l:].index(stop)
                data, string = new_string(_string=string, _tag=tag, l=l, r=r)
            except ValueError:
                pass
            return data


def get_playlist():
    url_API = "https://circuitalminds.herokuapp.com/api/"
    data = requests.get(url_API + "get_music_data").json()
    with open("playlist.yml", "w") as outfile:
        yaml.dump(data, outfile, default_flow_style=False)

def save_data(data, name):
    with open(f"{name}.yml", "w") as outfile:
        yaml.dump(data, outfile, default_flow_style=False)

def load_data(data):
    return yaml.load(open(f"{data}.yml"), Loader=yaml.FullLoader)

def get_playlist_meta_tags(list_names):
    yt_api = YoutubeApi()
    data = {}
    for song in list_names:
        _data = yt_api.get_search_song(video_title=song)["search_song"]
        _meta_tags = yt_api.select_meta_tags(meta_tags=_data["meta_tags"])
        _basic_data = yt_api.get_base_data(meta_tags=_data["meta_tags"])
        data[song] = {}
        data[song].update(_basic_data)
        data[song].update(_meta_tags)
        save_data(data=data, name="playlist_meta_tags")

def send_data_to_db():
    list_names = load_data(data="playlist")["list_names"]
    yt_api = YoutubeApi()
    for song in list_names:
        meta_tags = yt_api.select_meta_tags(meta_tags=yt_api.data_search[list_names[0]]["meta_tags"])
    base_data = yt_api.get_base_data(meta_tags=yt_api.data_search[list_names[0]]["meta_tags"])
    data = {"option": "add", "book": "searches"}
    data.update(base_data)
    data.update()
    f = requests.get("http://127.0.0.1:4000/api/query", data).json()
    print(f)

get_playlist_meta_tags(list_names=load_data(data="playlist")["list_names"])
