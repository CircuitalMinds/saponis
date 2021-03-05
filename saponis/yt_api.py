import requests
from bs4 import BeautifulSoup
import yaml


class YoutubeApi:

    def __init__(self, song):
        self.contents = self.secure_search(song)
        self.data = {"search": song, "search_data": self.get_basic_data()}

    def get_basic_data(self):
        search_data = []
        for content in self.contents:
            video_id = self.finder("videoId", content)
            if video_id != {}:
                find_title = self.finder("title", content)
                text_title = self.finder("text", find_title)
                if "text" in list(text_title.keys()):
                    title = text_title["text"]
                else:
                    title = self.finder("simpleText", find_title)["simpleText"]
                data = {"video_title": title, "video_url": 'https://www.youtube.com/watch?v=' + video_id["videoId"]}
                search_data.append(data)
        return search_data

    def search(self, song):
        f = requests.get("https://www.youtube.com/results?search_query=" + song).content
        s = BeautifulSoup(f, "html.parser")
        texto = s.findAll("script")
        x = {}
        for t in texto:
            try:
                if "var ytInitialData" in t.string:
                    xp = t.string.replace("var ytInitialData = ", "")
                    xp = xp.replace(";", "")
                    x.update(yaml.load(xp, Loader=yaml.FullLoader))
                    break
            except (IndexError, TypeError):
                continue
        contents = self.finder("contents", x)
        for j in range(2):
            contents = self.finder("contents", contents)
        return contents

    def secure_search(self, song):
        contents = self.search(song)
        for trying in range(3):
            try:
                itemsection = contents[0]['itemSectionRenderer']
                contents = itemsection['contents']
                break
            except KeyError:
                pass
            contents = self.search(song)
        return contents

    def finder(self, key, data):
        keys = list(data.keys())
        value = None
        test = False
        if key in keys:
            value = data[key]
        else:
            test = True
        while test:
            test, data = self.match_wrapper(key, data)
            value = data
            if data == {}:
                test = False
        return value

    @staticmethod
    def match_wrapper(key, data):
        def check(target, data_dict):
            if target in list(data_dict.keys()):
                return True, data_dict[target]
            else:
                return False, {k: data_dict[k] for k in list(data_dict.keys())}
        test = True
        values = {}
        for word in data:
            value = data[word]
            if type(value) == dict:
                cheking = check(key, value)
                if cheking[0]:
                    test = False
                    values = {key: cheking[1]}
                    break
                else:
                    values.update(cheking[1])
            elif type(value) == list:
                for v in value:
                    if type(v) == dict:
                        cheking = check(key, v)
                        if cheking[0]:
                            test = False
                            values = {key: cheking[1]}
                            break
                        else:
                            values.update(cheking[1])
                    elif type(v) == list:
                        for k in v:
                            if type(k) == dict:
                                values.update(k)
        return test, values
