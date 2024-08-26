from PyQt5 import QtWidgets
import os
from role_selection import RoleSelectionWindow
from buyer_main import BuyerMainWindow  # 确保引入正确的 BuyerMainWindow
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Shopping Platform')
        self.setGeometry(400,200, 1800,1100)
        self.setCentralWidget(RoleSelectionWindow(self))

