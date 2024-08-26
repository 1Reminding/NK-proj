from PyQt5 import QtWidgets

class BuyerMainWindow(QtWidgets.QWidget):
    def __init__(self, main_window, user_id):
        super().__init__()
        self.main_window = main_window
        self.user_id = user_id
        self.init_ui()

    def init_ui(self):
        self.main_window.setWindowTitle('买家主页')
        self.setStyleSheet("""
                                            QLabel, QLineEdit, QPushButton, QTableWidget {
                                                font-size: 10pt;
                                            }
                                            QTableWidget {
                                                font-size: 8pt;  # 表格内容字体大小
                                            }
                                        """)
        self.personal_info_button = QtWidgets.QPushButton('个人信息修改', self)
        self.shopping_button = QtWidgets.QPushButton('Go Shopping!', self)

        self.personal_info_button.clicked.connect(self.show_personal_info)
        self.shopping_button.clicked.connect(self.show_shopping)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.personal_info_button)
        layout.addWidget(self.shopping_button)
        self.setLayout(layout)

    def show_personal_info(self):
        from buyer_personal_info import BuyerPersonalInfoWindow
        self.main_window.setCentralWidget(BuyerPersonalInfoWindow(self.main_window, self.user_id))

    def show_shopping(self):
        from buyer_shopping import BuyerShoppingWindow
        self.main_window.setCentralWidget(BuyerShoppingWindow(self.main_window, self.user_id))
