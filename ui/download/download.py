import os
from pathlib import Path

from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QFile, Qt, Signal
from modules.config import Config

from ui.common.downloadprogressbar import DownloadProgressBar
from ui.common.draggablewindow import DraggableWindow
from ui.common.uiloader import UiLoader
import ui.download.resources


class LostArkMarketLauncherDownload(QMainWindow):
    launch = Signal()
    finished_download = Signal()

    def __init__(self, data):
        super(LostArkMarketLauncherDownload, self).__init__()
        self.data = data
        self.load_ui()
        self.setWindowTitle("Download - Lost Ark Market Online")
        self.show()

    def load_ui(self):
        loader = UiLoader(self)
        loader.registerCustomWidget(DownloadProgressBar)
        loader.registerCustomWidget(DraggableWindow)                         
        ui_file = QFile(os.path.join(os.path.dirname(
            __file__), "../../assets/ui/download.ui"))
        ui_file.open(QFile.ReadOnly)
        widget = loader.load(ui_file)
        widget.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        widget.lblTitle.setText(self.data['title'])
        widget.btnClose.clicked.connect(self.close)
        widget.btnSkip.clicked.connect(self.close)
        widget.btnDownload.clicked.connect(self.download)
        widget.pbDownload.finished.connect(self.download_done)
        ui_file.close()
        return widget

    def download(self):
        self.btnDownload.setEnabled(False)
        self.btnSkip.setEnabled(False)
        self.pbDownload.download_file(
            self.data['url'], self.data['file'])

    def download_done(self):
        self.btnDownload.clicked.disconnect(self.download)
        self.btnDownload.setText('Launch')
        self.btnDownload.setEnabled(True)
        self.btnDownload.clicked.connect(self.launch_app)
        self.finished_download.emit()

    def launch_app(self):
        self.launch.emit()
        self.close()
