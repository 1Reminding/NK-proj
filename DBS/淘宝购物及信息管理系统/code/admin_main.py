from PyQt5 import QtWidgets
from admin_personal_info import AdminPersonalInfoWindow
from admin_user_management import AdminUserManagementWindow

class AdminMainWindow(QtWidgets.QWidget):
    def __init__(self, main_window, admin_id):
        super().__init__()
        self.main_window = main_window
        self.admin_id = admin_id
        self.init_ui()

    def init_ui(self):
        self.main_window.setWindowTitle('管理员界面')

        # 设置全局样式表，统一字体大小为14
        self.setStyleSheet("""
                            QLabel, QLineEdit, QPushButton, QTableWidget {
                                font-size: 10pt;
                            }
                            QTableWidget {
                                font-size: 8pt;  # 表格内容字体大小
                            }
                        """)

        self.personal_info_button = QtWidgets.QPushButton('个人信息管理', self)
        self.user_info_button = QtWidgets.QPushButton('用户信息管理', self)
        self.order_management_button = QtWidgets.QPushButton('订单信息管理', self)
        self.product_management_button = QtWidgets.QPushButton('产品信息管理', self)
        self.back_button = QtWidgets.QPushButton('Back', self)

        self.personal_info_button.clicked.connect(self.show_personal_info)
        self.user_info_button.clicked.connect(self.show_user_info)
        self.order_management_button.clicked.connect(self.show_order_management)
        self.product_management_button.clicked.connect(self.show_product_management)
        self.back_button.clicked.connect(self.go_back)
        #
        # self.personal_info_button.clicked.connect(self.show_personal_info)
        # self.user_management_button.clicked.connect(self.show_user_management)
        # self.order_management_button.clicked.connect(self.show_order_management)
        # self.product_management_button.clicked.connect(self.show_product_management)
        # self.back_button.clicked.connect(self.go_back)
        #别改错名字user_info别改，否则登录时直接报错退出


        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.personal_info_button)
        layout.addWidget(self.user_info_button)
        layout.addWidget(self.order_management_button)
        layout.addWidget(self.product_management_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def show_personal_info(self):
        self.main_window.setCentralWidget(AdminPersonalInfoWindow(self.main_window, self.admin_id))

    def show_user_info(self):
        self.main_window.setCentralWidget(AdminUserManagementWindow(self.main_window,self.admin_id))
        # 这里可以添加跳转到用户信息修改的逻辑

    def show_order_management(self):
        from admin_order_management import AdminOrderManagementWindow
        self.main_window.setCentralWidget(AdminOrderManagementWindow(self.main_window))

    def show_product_management(self):
        from admin_product_management import AdminProductManagementWindow
        self.main_window.setCentralWidget(AdminProductManagementWindow(self.main_window))

    def go_back(self):
        from admin_login import AdminLoginWindow
        self.main_window.setCentralWidget(AdminLoginWindow(self.main_window))