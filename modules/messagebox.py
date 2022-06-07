
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMessageBox, QApplication, QMainWindow
from PySide6.QtCore import Qt

from modules.config import Config


class MessageBoxHandler(QObject):
    app: QApplication
    msgBox: QMessageBox

    def __init__(self, message_box):
        self.app = QApplication.instance()
        self.msgBox = QMessageBox()
        self.msgBox.hide()
        message_box.connect(self.spawn_message_box)
        pass

    def spawn_message_box(self, data):
        match data["type"]:
            case "VERSION":
                self.new_version(data)
                return

    def new_version(self, data):
        self.msgBox.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.msgBox.setWindowTitle("Lost Ark Market Online")
        self.msgBox.setText(f"New version v{data['new_version']} available.")
        self.msgBox.setInformativeText(
            "Please close the app and run the launcher to download the new version.")
        self.msgBox.setIcon(QMessageBox.Information)
        self.msgBox.exec()
