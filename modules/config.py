import configparser
from modules.errors import NoTokenError


def update_token(token):
    config = configparser.ConfigParser()
    config.read("config.ini")

    if config.has_section("Token") == False:
        config.add_section("Token")
        config.set("Token", "refresh_token", token["refresh_token"])
        config.set("Token", "id_token", token["id_token"])
        config.set("Token", "uid", token["uid"])
    else:
        if 'refresh_token' in token:
            config.set("Token", "refresh_token", token["refresh_token"])
        if 'id_token' in token:
            config.set("Token", "id_token", token["id_token"])
        if 'uid' in token:
            config.set("Token", "uid", token["uid"])

    with open("config.ini", "w") as configfile:
        config.write(configfile)


def get_tokens():
    config = configparser.ConfigParser()
    config.read("config.ini")
    if config.has_section("Token") == False:
        raise NoTokenError()
    else:
        return config.get("Token", "id_token"), config.get("Token", "refresh_token"), config.get("Token", "uid")


def update_latest_app_version(app_version):
    config = configparser.ConfigParser()
    config.read("config.ini")

    if config.has_section("Launcher") == False:
        config.add_section("Launcher")
        config.set("Launcher", "current_app_version", 'None')
        config.set("Launcher", "latest_app_version", app_version)
    else:
        config.set("Launcher", "latest_app_version", app_version)

    with open("config.ini", "w") as configfile:
        config.write(configfile)


def update_current_app_version(app_version):
    config = configparser.ConfigParser()
    config.read("config.ini")
    config.set("Launcher", "current_app_version", app_version)
    with open("config.ini", "w") as configfile:
        config.write(configfile)


def needs_update():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config.get("Launcher", "current_app_version") != config.get("Launcher", "latest_app_version")
