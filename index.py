import os
import sys
import traceback
import subprocess

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from modules.app_version import get_app_version
from modules.config import Config
from modules.sound import playDownloadComplete, playError, playSuccess, playUpdateDetected
from ui.download.download import LostArkMarketLauncherDownload
from ui.login_form.login_form import LostArkMarketLoginForm

class LostArkMarketOnlineLauncher(QApplication):
    def __init__(self, *args, **kwargs):
        QApplication.__init__(self, *args, **kwargs)
        
        if(Config().refresh_token):            
            self.check_config()
        else:
            self.login_form = LostArkMarketLoginForm()
            self.login_form.login_success.connect(self.login_success)
            self.login_form.login_error.connect(self.login_error)

    def login_error(self):
        playError()

    def login_success(self):
        playSuccess()
        self.login_form.close()
        self.check_config()

    def check_config(self):
        Config().check_watcher_version()
        if Config().needs_update == True:
            playUpdateDetected()
            self.download = LostArkMarketLauncherDownload({
                "url": f'https://github.com/gogodr/LostArk-Market-Watcher/releases/download/{Config().watcher_version}/{Config().watcher_file}.exe'
            })
            self.download.launch.connect(self.launch_watcher)
            self.download.finished_download.connect(self.finished_download)
        else:
            self.launch_watcher()

    def finished_download(self):
        playDownloadComplete()
        if(Config().run_after_download):
            self.download.close()
            self.launch_watcher()

    def launch_watcher(self):
        playSuccess()
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.call(f"{Config().watcher_file}.exe")
        sys.exit()


if __name__ == "__main__":
    Config()
    app = LostArkMarketOnlineLauncher([])
    icon = QIcon(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                "assets/icons/favicon.png")))
    app.setWindowIcon(icon)
    sys.exit(app.exec())
