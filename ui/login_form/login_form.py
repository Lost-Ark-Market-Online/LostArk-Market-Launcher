import os
import traceback
from pathlib import Path
from PySide6.QtWidgets import QMainWindow, QLineEdit
from PySide6.QtCore import QFile, Qt, Signal
from modules.logging import AppLogger
from ui.common.draggablewindow import DraggableWindow
from ui.common.uiloader import UiLoader
import ui.login_form.resources

from modules.auth import login


class LostArkMarketLoginForm(QMainWindow):
    ui = None
    login_success = Signal()
    login_error = Signal()

    def __init__(self):
        super(LostArkMarketLoginForm, self).__init__()
        self.load_ui()
        self.setWindowTitle("Login - Lost Ark Market Online")
        self.show()

    def load_ui(self):
        loader = UiLoader(self)
        ui_file = QFile(os.path.join(os.path.dirname(
            __file__), "../../assets/ui/login_form.ui"))
        ui_file.open(QFile.ReadOnly)
        loader.registerCustomWidget(DraggableWindow)
        widget = loader.load(ui_file)
        widget.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        widget.btnLogin.clicked.connect(self.login)
        widget.btnClose.clicked.connect(self.close)
        widget.txtPassword.setEchoMode(QLineEdit.Password)
        ui_file.close()

    def login(self):
        self.btnLogin.setEnabled(False)
        try:
            login(self.txtEmail.text(), self.txtPassword.text())
            self.login_success.emit()
        except Exception as ex:
            AppLogger().exception(ex)
            self.btnLogin.setEnabled(True)
            self.login_error.emit()
