from time import sleep
from modules.logging import AppLogger
from modules.messagebox import MessageBoxHandler
import modules.single_instance
import os
import sys
import traceback
import subprocess

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal
from modules.app_version import get_app_version
from modules.config import Config
from modules.sound import VolumeController, playDownloadComplete, playError, playSuccess, playUpdateDetected
from ui.download.download import LostArkMarketLauncherDownload
from ui.login_form.login_form import LostArkMarketLoginForm


class LostArkMarketOnlineLauncher(QApplication):
    message_box_handler: MessageBoxHandler
    volume_controller: VolumeController
    message_box = Signal(dict)

    def __init__(self, *args, **kwargs):
        QApplication.__init__(self, *args, **kwargs)

        self.volume_controller = VolumeController()
        self.message_box_handler = MessageBoxHandler(self.message_box)

        self.launcher_check_config()

    # Launcher Version Check
    def launcher_check_config(self):
        Config().check_launcher_version()
        AppLogger().info(
            f"Launcher remote version {Config().launcher_version}")
        if Config().launcher_needs_update == True:
            AppLogger().info(f"Launcher needs update")
            playUpdateDetected()
            self.download = LostArkMarketLauncherDownload({
                "url": f'https://github.com/Lost-Ark-Market-Online/LostArk-Market-Launcher/releases/download/{Config().launcher_version}/{Config().launcher_file}.exe',
                "title": f'New version of the Lost Ark Market Launcher Found: v{Config().launcher_version}',
                "file":  f'{Config().launcher_file}.exe.new'
            })
            self.download.launch.connect(self.launch_launcher)
            self.download.finished_download.connect(self.launcher_downloaded)
        else:
            self.session_check()

    def launch_launcher(self):
        f = open("update-launcher.bat", "w")
        f.write("""@echo off
taskkill /f /im lamo-launcher.exe >nul
timeout /t 1 /nobreak >nul
del lamo-launcher.exe
timeout /t 1 /nobreak >nul
ren lamo-launcher.exe.new lamo-launcher.exe
timeout /t 1 /nobreak >nul
start /b lamo-launcher.exe
(goto) 2>nul & del "%~f0""")
        f.close()
        os.system("update-launcher.bat")

    def launcher_downloaded(self):
        playDownloadComplete()
        if(Config().run_after_download):
            self.download.close()
            self.launch_launcher()

    # Session Check
    def session_check(self):
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

    # Watcher Version Check
    def check_config(self):
        Config().check_watcher_version()
        print(f"Needs watcher update: {Config().watcher_needs_update}")
        if Config().watcher_needs_update == True:
            playUpdateDetected()
            self.download = LostArkMarketLauncherDownload({
                "url": f'https://github.com/Lost-Ark-Market-Online/LostArk-Market-Watcher/releases/download/{Config().watcher_version}/{Config().watcher_file}.exe',
                "title": f'New version of the Lost Ark Market Watcher Found: v{Config().watcher_version}',
                "file":  f'{Config().watcher_file}.exe.new'
            })
            self.download.launch.connect(self.launch_watcher)
            self.download.finished_download.connect(self.watcher_downloaded)
        else:
            self.launch_watcher()

    def watcher_downloaded(self):
        playDownloadComplete()
        if(Config().run_after_download):
            self.download.close()
            self.launch_watcher()

    def launch_watcher(self):
        sleep(2)
        if os.path.exists(f"{Config().watcher_file}.exe.new") == True:
            if os.path.exists(f"{Config().watcher_file}.exe") == True:
                os.system(f"del /f {Config().watcher_file}.exe")
            os.system(f"rename {Config().watcher_file}.exe.new {Config().watcher_file}.exe")
        sleep(2)
        playSuccess()
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.call(f"{Config().watcher_file}.exe")
        sys.exit()

if __name__ == "__main__":
    try:
        Config()
        AppLogger()
        AppLogger().info("Start Launcher")
        app = LostArkMarketOnlineLauncher([])
        icon = QIcon(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                  "assets/icons/favicon.png")))
        app.setWindowIcon(icon)
        sys.exit(app.exec())
    except Exception as ex:
        print(ex)
        AppLogger().exception(ex)
