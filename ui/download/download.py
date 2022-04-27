import os
from pathlib import Path

from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QFile, Qt, Signal
from PySide6.QtUiTools import QUiLoader

from ui.common.downloadprogressbar import DownloadProgressBar
from ui.common.draggablewindow import DraggableWindow
import ui.download.resources


class LostArkMarketLauncherDownload(QMainWindow):
    launch = Signal()
    finished_download = Signal()

    def __init__(self, data):
        super(LostArkMarketLauncherDownload, self).__init__()
        self.data = data
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        loader.registerCustomWidget(DownloadProgressBar)
        loader.registerCustomWidget(DraggableWindow)                         
        ui_file = QFile(os.path.join(os.path.dirname(
            __file__), "../../assets/ui/download.ui"))
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        self.ui.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.ui.lblTitle.setText(
            f'New version of the Lost Ark Market Watcher Found: v{self.data["version"]}')
        self.ui.btnClose.clicked.connect(self.close)
        self.ui.btnSkip.clicked.connect(self.close)
        self.ui.btnDownload.clicked.connect(self.download)
        self.ui.pbDownload.finished.connect(self.download_done)

        self.ui.show()
        ui_file.close()

    def close(self):
        os._exit(1)

    def download(self):
        self.ui.btnDownload.setEnabled(False)
        self.ui.btnSkip.setEnabled(False)
        self.ui.pbDownload.download_file(
            self.data['url'], 'LostArkMarketWatcher.exe')

    def download_done(self):
        self.ui.btnDownload.clicked.disconnect(self.download)
        self.ui.btnDownload.setText('Launch')
        self.ui.btnDownload.setEnabled(True)
        self.ui.btnDownload.clicked.connect(self.launch_app)
        self.finished_download.emit()

    def launch_app(self):
        self.ui.close()
        self.launch.emit()
