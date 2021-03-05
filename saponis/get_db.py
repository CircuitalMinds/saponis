from bs4 import BeautifulSoup
import requests
import yaml
import json

_db = "./circuitalminds/databases"


def save_data(data, name):
    with open(_db + "/db_json/" + name + ".json", "w") as outfile:
        json_file = json.dumps(data, indent=4, sort_keys=False)
        outfile.write(json_file)
        outfile.close()
    with open(_db + "/db_yaml/" + name + ".yml", "w") as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


def scrapper(request_url):
    soup = BeautifulSoup(requests.get(request_url).content, "html.parser")
    list_tags = soup.find_all(class_="js-navigation-open Link--primary")
    data = {}
    i = 1
    for tag in list_tags:
        info = tag.get("href")
        file_info = {"name": info.split("/")[-1], "url": "https://github.com" + info + "?raw=true"}
        data["id=" + str(i)] = file_info
        i += 1
    return data


def scrapper_music(request_url):
    soup = BeautifulSoup(requests.get(request_url).content, "html.parser")
    list_tags = soup.find_all("a")
    links = {}
    for tag in list_tags:
        link = tag.get("href")
        if ".mp4" in link:
            video_id = link.replace(".mp4", "")[::-1][0:11][::-1]
            video_title = link.split("/")[-1].replace("-" + video_id + ".mp4", "")
            links[video_id] = {"video_title": video_title, "url": "https://github.com" + link + "?raw=true"}
    return links


def scrapper_notebooks(request_url):
    soup = BeautifulSoup(requests.get(request_url).content, "html.parser")
    list_tags = soup.find_all("a")
    data = {}
    i = 1
    for tag in list_tags:
        info = tag.get("href")
        if ".ipynb" in info:
            file_info = {"name": info.split("/")[-1], "url": "https://github.com" + info + "?raw=true"}
            data["id=" + str(i)] = file_info
            i += 1
    return data


def music_database(branch):
    sections = ["part_" + str(j) for j in range(1, 11)]
    url = "https://github.com/alanmatzumiya/containers/tree/"
    data = {}
    for section in sections:
        data.update(scrapper_music(url + branch + "/" + section + "/"))
    save_data(data=data, name=branch)


def img_database(branch):
    sections = ["2003", "2011_1", "2011_2"]
    sections.extend(["20" + str(j) for j in range(15, 21)])
    parts = ["part_" + str(j) for j in range(1, 4)]
    url = "https://github.com/alanmatzumiya/img_containers/tree/"

    data = {branch: {}}
    for section in sections:
        img = scrapper(url + branch + "/" + section + "/")
        if img != {}:
            if img["id=1"]["name"] in parts:
                img = {}
                for part in parts: img.update(scrapper(url + branch + "/" + section + "/" + part))
                data[branch][section] = img
            else:
                data[branch][section] = img
    save_data(data=data, name=branch)


def notebooks_database(topic, modules):
    url = "https://github.com/alanmatzumiya/" + topic + "/tree/main/"
    app = "https://jupyternbs.herokuapp.com/notebooks/"
    data = {topic: {}}
    for module in modules:
        notebooks = scrapper_notebooks(url + module)
        for n in list(notebooks.keys()):
            notebooks[n]["app"] = app + topic + "/" + module + "/" + notebooks[n]["name"]
        data[topic][module] = notebooks
    save_data(data=data, name=topic)


def git_scrapper(url, next=False):
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    elements = soup.find_all(class_="wb-break-all")
    data = {}
    target_branch = ["main", "gh-pages", "master", "localhost"]

    for s in elements:
        repo = s.find("a").get("href")
        get_branches = BeautifulSoup(requests.get("https://github.com" + repo + "/branches/all").content,
                                     "html.parser").find_all(class_="branch-name")
        branches = []
        for get_branch in get_branches:
            if get_branch.text in target_branch: branches.append(get_branch.text)
        data[repo.split("/")[-1]] = {"url": "https://github.com" + repo, "branches": branches}
    if next:
        return data, soup.find_all(class_="btn btn-outline BtnGroup-item")[1].get("href")
    else:
        return data


def get_repos():
    organization = "CircuitalMinds"
    user = "alanmatzumiya"
    data = {organization: {}, user: {}}

    url_organization = "https://github.com/" + organization + "?tab=repositories"
    url_user = "https://github.com/" + user + "?tab=repositories"

    data[organization].update(git_scrapper(url=url_organization))

    while url_user is not None:
        repos_data, url_user = git_scrapper(url=url_user, next=True)
        data[user].update(repos_data)

    save_data(data=data, name="repos")


def update(data, branch=None):
    # notebooks
    if data == "notebooks" or data == "all":
        notebooks_database(topic="data_analysis", modules=["module_" + str(j) for j in range(1, 8)])
        notebooks_database(topic="engineering-basic", modules=["module_" + str(j) for j in range(0, 8)])
    # music
    if data == "music" or data == "all":
        if branch is None:
            for j in range(1, 11):
                music_database(branch="music_" + str(j))
        else:
            music_database(branch=branch)
    # repos
    if data == "repos" or data == "all":
        get_repos()
    # img
    if data == "img" or data == "all":
        for j in range(1, 7):
            img_database(branch="img_" + str(j))
