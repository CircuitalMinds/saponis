import os
import yaml
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import requests

class DataUpdaters:

    def __init__(self, url_git=None, path=None):
        self.path = path
        self.url_git = url_git

    def update(self, container, path_output):
        url = container["url"]
        sub_url = container["sub_url"]
        url_extend = container["url_extend"]
        extension = container["extension"]
        for repo in list(container["repos"]):
            file_data = self.search(url, sub_url, url_extend, self.path, repo, extension)
            print(file_data)
            if file_data != {}:
                print("good test")
                self.save(file_data, path_output + repo)

    @staticmethod
    def search(url, sub_url, url_extend, root, path, extension):
        data = {}

        for sub_path, dirs, files in os.walk(root + path, topdown=False):
            for name in files:
                if name.endswith(extension):
                    data[name] = url + sub_path.replace(root + path, path + sub_url) + "/" + name + url_extend
            for name in dirs:
                if name.endswith(extension):
                    data[name] = url + sub_path.replace(root + path, path + sub_url) + "/" + name + url_extend
        return data

    @staticmethod
    def save(file_data, path_output, format_output="yml"):

        if format_output == "json":
            with open(path_output + ".json", "w") as outfile:
                json_file = json.dumps(file_data, indent=4, sort_keys=True)
                outfile.write(json_file)
                outfile.close()
        else:
            with open(path_output + ".yml", "w") as outfile:
                yaml.dump(file_data, outfile, default_flow_style=False)

    @staticmethod
    def mp4converter(path, extension):

        target_path = "cd " + path
        converter = '"$(for i in * .' + extension + '; do ffmpeg -i "$i" "${i%.*}.mp4"; done)"'
        os.system(target_path + " && " + converter)

    def music_db(self, subpath, url_root, repo, branch, out_path):
        data = {}
        for j in range(1, 11):
            dirs = os.listdir(self.path + subpath + "/" + "part_" + str(j))
            url_target = self.url_git + repo + "/tree/" + branch + "/part_" + str(j)
            tag = ".mp4"
            urls = requests.get(url_root + "?url=" + url_target + "&tag=" + tag).json()["urls"]
            for f in dirs:
                sample = []
                url = url_target.replace("/tree/", "/blob/") + "/" + f.replace(" ", "%20")
                for test in urls:
                    test += "https://github.com" + test
                    sample.append(self.checking(url, test))
                data.update(
                    {
                        f: "https://github.com" + urls[sample.index(max(sample))] + "?raw=true"
                    }
                )
        with open(out_path + branch + ".yml", "w") as outfile:
            yaml.dump(data, outfile, default_flow_style=False)

    @staticmethod
    def checking(x, y):
        nltk.download("all")
        x_list, y_list = word_tokenize(x), word_tokenize(y)
        sw = stopwords.words('english')
        l1, l2 = [], []
        x_set = {w for w in x_list if w not in sw}
        y_set = {w for w in y_list if w not in sw}
        r_vector = x_set.union(y_set)
        c = 0
        for w in r_vector:
            if w in x_set:
                l1.append(1)
            else:
                l1.append(0)
            if w in y_set:
                l2.append(1)
            else:
                l2.append(0)
        for i in range(len(r_vector)):
            c += l1[i] * l2[i]
        cosine = c / float((sum(l1) * sum(l2)) ** 0.5)
        return cosine
