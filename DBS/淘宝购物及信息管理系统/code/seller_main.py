from PyQt5 import QtWidgets
from seller_personal_info import SellerPersonalInfoWindow
from seller_shop_management import SellerShopManagementWindow
from seller_order_management import SellerOrderManagementWindow

class SellerMainWindow(QtWidgets.QWidget):
    def __init__(self, main_window, user_id):
        super().__init__()
        self.main_window = main_window
        self.user_id = user_id
        self.init_ui()

    def init_ui(self):
        self.main_window.setWindowTitle('卖家主界面')

        self.setStyleSheet("""
                                    QLabel, QLineEdit, QPushButton, QTableWidget {
                                        font-size: 10pt;
                                    }
                                    QTableWidget {
                                        font-size: 8pt;  # 表格内容字体大小
                                    }
                                """)
        self.personal_info_button = QtWidgets.QPushButton('个人信息修改', self)
        self.shop_management_button = QtWidgets.QPushButton('管理店铺', self)
        self.order_management_button = QtWidgets.QPushButton('订单处理', self)

        self.personal_info_button.clicked.connect(self.show_personal_info)
        self.shop_management_button.clicked.connect(self.show_shop_management)
        self.order_management_button.clicked.connect(self.show_order_management)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.personal_info_button)
        layout.addWidget(self.shop_management_button)
        layout.addWidget(self.order_management_button)

        self.setLayout(layout)

    def show_personal_info(self):
        self.main_window.setCentralWidget(SellerPersonalInfoWindow(self.main_window, self.user_id))
        self.main_window.resize(800, 600)  # 返回时调整窗口大小
    def show_shop_management(self):
        self.main_window.setCentralWidget(SellerShopManagementWindow(self.main_window, self.user_id))
        self.main_window.resize(800, 600)  # 返回时调整窗口大小
    def show_order_management(self):
        self.main_window.setCentralWidget(SellerOrderManagementWindow(self.main_window, self.user_id))
        self.main_window.resize(800,600)  # 返回时调整窗口大小