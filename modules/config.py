import configparser
import os
import pefile
import requests
from packaging import version
from modules.common.singleton import Singleton


class Config(metaclass=Singleton):
    version = "1.2.1.1"
    debug = False
    id_token: str = None
    refresh_token: str = None
    uid: str = None
    play_audio: bool = True
    save_log: bool = True
    run_after_download: bool = True
    needs_update = False
    watcher_version: str = None
    watcher_file: str = None

    def __init__(self) -> None:
        self._config = configparser.ConfigParser()
        self._config.read("config.ini")
        self.load_config()

    def load_config(self):
        if self._config.has_section("Token"):
            self.id_token = self._config.get("Token", "id_token")
            self.refresh_token = self._config.get("Token", "refresh_token")
            self.uid = self._config.get("Token", "uid")

        if self._config.has_section("Launcher"):
            self.run_after_download = self._config.get(
                "Launcher", "run_after_download") == 'True'
            self.debug = self._config.get(
                "Launcher", "debug") == 'True'

    def update_config_file(self):
        if self._config.has_section("Token") == False:
            self._config.add_section("Token")

        self._config.set("Token", "refresh_token", self.refresh_token)
        self._config.set("Token", "id_token", self.id_token)
        self._config.set("Token", "uid", self.uid)

        if self._config.has_section("Launcher") == False:
            self._config.add_section("Launcher")

        self.set_or_remove_config_option(
            "Launcher", "run_after_download", self.run_after_download
        )
        self.set_or_remove_config_option(
            "Launcher", "debug", self.debug
        )
        with open("config.ini", "w") as configfile:
            self._config.write(configfile)

    def update_token(self, token):
        self.id_token = token["id_token"]
        self.refresh_token = token["refresh_token"]
        self.uid = token["uid"]
        self.update_config_file()

    def set_or_remove_config_option(self, section, option, value):
        if value is None:
            self._config.remove_option(section, option)
        else:
            self._config.set(section, option, str(value))

    def check_watcher_version(self):
        res = requests.get(
            f'https://firestore.googleapis.com/v1/projects/lostarkmarket-79ddf/databases/(default)/documents/app-info/market-watcher')
        res = res.json()
        self.watcher_file = res["fields"]["file"]["stringValue"]
        self.watcher_version = res["fields"]["version"]["stringValue"]

        if os.path.isfile(f"{self.watcher_file}.exe") == False:
            self.needs_update = True
        else:
            pe = pefile.PE(f"{self.watcher_file}.exe")

            def LOWORD(dword):
                return dword & 0x0000ffff

            def HIWORD(dword):
                return dword >> 16
            
            ms = pe.VS_FIXEDFILEINFO[0].ProductVersionMS
            ls = pe.VS_FIXEDFILEINFO[0].ProductVersionLS

            curr_version = version.parse(
                f"{HIWORD(ms)}.{LOWORD(ms)}.{HIWORD(ls)}.{LOWORD(ls)}")
            latest_version = version.parse(self.watcher_version)

            if latest_version > curr_version:
                self.needs_update = True
