import subprocess
import os


class VCSTools:

    def __init__(self, repos, path):
        self.path = path
        self.repos = repos

    def git_clone(self, repo=None):
        if repo is not None:
            sentence = "cd " + self.path + " && git clone " + self.repos[repo]
            print(sentence)
            # os.system(sentence)
        else:
            for url in list(self.repos.values()):
                sentence = "cd " + self.path + " && git clone " + url
                print(sentence)
                # os.system(sentence)

    def git_push(self, repo=None):
        if repo is not None:
            sentence_1 = "cd " + self.path + repo
            os.system(sentence_1 + " && git init")
            branch = subprocess.getoutput(sentence_1 + " && git branch").replace("* ", "")
            sentence_2 = " && git add . && git commit -m 'auto' && git push origin " + branch
            print(sentence_1 + sentence_2)
            # return os.system(
            #    sentence_1 + sentence_2
            # )

        else:
            for rep in list(self.repos.keys()):
                sentence_1 = "cd " + self.path + rep
                os.system(sentence_1 + " && git init")
                branch = subprocess.getoutput(sentence_1 + " && git branch").replace("* ", "")
                sentence_2 = " && git add . && git commit -m 'auto' && git push origin " + branch
                print(sentence_1 + sentence_2)
                # return os.system(sentence_1 + sentence_2)
