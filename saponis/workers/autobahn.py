from __future__ import unicode_literals
import youtube_dl


def youtube_downloader(self, name, url=None):
    if url is None:
        data = self.youtube_search(name)
        url = data["url"]
        name = data["name"]
import geckodriver_autoinstaller
from selenium.webdriver import Firefox, FirefoxOptions
import yaml
import os
from time import sleep
import random

geckodriver_autoinstaller.install()
options = FirefoxOptions()
options.headless = True


class BotDriver:
    playlist = {
        "Top2020": "https://youtube.com/playlist?list=PLU1cYDntAmw3w3vtqMjVgQED_FzzlSFCh",
        "myHub": "https://youtube.com/playlist?list=PLU1cYDntAmw0aYr8KIS1doIaI46BUCMsB"
    }

    def youtube_downloader(self, name, url=None):
        if url is None:
            data = self.youtube_search(name)
            url = data["url"]
            name = data["name"]

        name = name.replace("(", "")
        name = name.replace(")", "")
        name = name.replace(" ", "-")
        cont = "music_" + str(random.randint(1, 10))
        part = "/part_" + str(random.randint(1, 10))
        path = "../root_server/home/music/" + cont
        downloader = "youtube-dl -f mp4 -o "
        output = path + part + "/" + name + ".mp4 "
        print(downloader + output + url)
        os.system(downloader + output + url)
        sentence = "cd " + path + " && git init && git add . && git commit -m 'auto' && git push origin " + cont
        print(sentence)
        os.system(sentence)

    @staticmethod
    def youtube_search(name):
        driver = Firefox(options=options)
        driver.get('https://www.youtube.com/results?search_query=' + name)
        titles = driver.find_elements_by_id('video-title')[0:10]
        songs = {}
        for song in titles:
            songs.update({song.get_attribute("title"): song.get_attribute("href")})
        driver.close()
        return songs

    def get_playlist(self, url_playlist, name, path):
        driver = Firefox(options=options)
        driver.get(url_playlist)
        sleep(1)
        playlist = {}
        titles = driver.find_elements_by_id('video-title')
        # for a in driver.find_elements_by_xpath('.//a'):
        for song in titles:
            name = song.get_attribute("title")
            url = song.get_attribute('href')
            playlist[name] = url
            self.youtube_downloader(url)
        driver.close()
        with open(path + name + ".yml", "w") as outfile:
            yaml.dump(playlist, outfile, default_flow_style=False)