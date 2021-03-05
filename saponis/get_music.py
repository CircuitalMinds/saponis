import yaml
import requests
from multiprocessing import Pool


db = "https://raw.githubusercontent.com/CircuitalMinds/FractalMetric/localhost/circuitalminds/databases/"
music = {"branches": ["music_" + str(b) for b in range(1, 11)],
         "sections": ["part_" + str(j) for j in range(1, 11)]}
music_data = []
processes = tuple(music['branches'])
Loader_Requests = lambda path: yaml.load(requests.get(path).content, Loader=yaml.FullLoader)


def run_process(branch):
    data = []
    branch_songs = list(Loader_Requests(db + "db_yaml/" + branch + ".yml").values())
    for song in branch_songs:
        data.append({"name": requests.utils.unquote(song["video_title"]), "url": song["url"]})
    return data


pool = Pool(processes=len(music['branches']))
data = pool.map(run_process, music['branches'])
for f in data:
    music_data.extend(f)

print(music_data)

