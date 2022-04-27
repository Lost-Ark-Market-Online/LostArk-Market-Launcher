import os
import traceback
from pathlib import Path
from PySide6.QtWidgets import QMainWindow, QLineEdit
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt, Signal
from ui.common.draggablewindow import DraggableWindow
import ui.login_form.resources

from modules.auth import login


class LostArkMarketLoginForm(QMainWindow):
    ui = None
    login_success = Signal()
    login_error = Signal()

    def __init__(self):
        print('Init Login Form')
        super(LostArkMarketLoginForm, self).__init__()
        self.load_ui()

    def load_ui(self):
        print('Login Form: Load UI')
        loader = QUiLoader()
        ui_file = QFile(os.path.join(os.path.dirname(
            __file__), "../../assets/ui/login_form.ui"))
        ui_file.open(QFile.ReadOnly)
        loader.registerCustomWidget(DraggableWindow)
        self.ui = loader.load(ui_file, self)
        self.ui.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.ui.btnLogin.clicked.connect(self.login)
        self.ui.btnClose.clicked.connect(self.close)
        self.ui.txtPassword.setEchoMode(QLineEdit.Password)
        self.ui.show()
        ui_file.close()

    def login(self):
        self.ui.btnLogin.setEnabled(False)
        try:
            login(self.ui.txtEmail.text(), self.ui.txtPassword.text())
            self.login_success.emit()
        except:
            traceback.print_exc()
            self.ui.btnLogin.setEnabled(True)
            self.login_error.emit()

    def close(self):
        os._exit(1)
