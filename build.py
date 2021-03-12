import os


SERVER_SETTING = {
    "path_config": "./saponis_server/_config.yml",
    "local": {
        "HOST": "127.0.0.1", "PORT": 8000, "DEBUG": True},
    "deploy": {
        "HOST": "https://saponis.herokuapp.com/", "PORT": 80, "DEBUG": False}}


def builder(option):
    if option == "config":
        mode = input("Run server as (local) or (deploy) mode: ")
        settings = SERVER_SETTING[str(mode)]
        path = SERVER_SETTING["path_config"]
        with open(path, "w") as outfile:
            outfile.write("HOST: " + settings['HOST'] + "\n" +
                          "PORT: " + str(settings["PORT"]) + "\n" +
                          "DEBUG: " + str(settings["DEBUG"]))
            outfile.close()

    else:
        os.environ["environment"] = "environment"
        if not os.path.isdir(os.environ["environment"]):
            os.system("virtualenv " + os.environ["environment"])

        os.system("bash install")


OPTION = input("build '[config]' or '[server]' : ")
builder(OPTION)
