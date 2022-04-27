import os
import sys
import traceback
import subprocess

from PySide6.QtWidgets import QApplication
from modules.app_version import get_app_version
from modules.config import update_latest_app_version, get_tokens, needs_update, update_current_app_version
from modules.errors import NoTokenError
from modules.sound import playDownloadComplete, playError, playSuccess, playUpdateDetected
from ui.download.download import LostArkMarketLauncherDownload
from ui.login_form.login_form import LostArkMarketLoginForm
from modules.auth import refresh_token



class LostArkMarketOnlineLauncher(QApplication):
    refresh_token = None
    id_token = None
    uid = None

    def __init__(self, *args, **kwargs):
        QApplication.__init__(self, *args, **kwargs)
        try:
            self.id_token, self.refresh_token, self.uid = get_tokens()
            self.id_token, self.refresh_token, self.uid = refresh_token(
                self.refresh_token)
            self.check_config()
        except NoTokenError:
            traceback.print_exc()
            playUpdateDetected()
            self.login_form = LostArkMarketLoginForm()
            self.login_form.login_success.connect(self.login_success)
            self.login_form.login_error.connect(self.login_error)

    def login_error(self):
        playError()

    def login_success(self):
        playSuccess()
        self.login_form.ui.hide()
        self.check_config()

    def check_config(self):
        self.latest_app_version = get_app_version()
        update_latest_app_version(self.latest_app_version)
        if needs_update() == True:
            playUpdateDetected()
            self.download = LostArkMarketLauncherDownload({
                "url": f'https://github.com/gogodr/LostArk-Market-Watcher/releases/download/{self.latest_app_version}/LostArkMarketWatcher.exe',
                "version": self.latest_app_version
            })
            self.download.launch.connect(self.launch_watcher)
            self.download.finished_download.connect(self.finished_download)
        else:
            self.launch_watcher()

    def finished_download(self):
        playDownloadComplete()
        update_current_app_version(self.latest_app_version)

    def launch_watcher(self):
        playSuccess()
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.call("LostArkMarketWatcher.exe")
        sys.exit()


if __name__ == "__main__":
    app = LostArkMarketOnlineLauncher([])
    sys.exit(app.exec())
