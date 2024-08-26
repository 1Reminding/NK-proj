# user_choice.py
from PyQt5 import QtWidgets,QtCore
from user_login_register import UserLoginRegisterWindow
import  os
class UserChoiceWindow(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        # 设置窗口大小
        self.setFixedSize(800,600)
        self.main_window.setWindowTitle('User Choice')

        # 设置背景图
        script_dir = os.path.dirname(os.path.abspath(__file__))
        background_image_path = os.path.join(script_dir, '图片.png')
        self.setStyleSheet(f"""
                   QWidget {{
                       background-image: url({background_image_path});
                       background-repeat: no-repeat;
                       background-position: center;
                       background-attachment: fixed;
                       background-size: cover;
                   }}
               """)

        self.buyer_button = QtWidgets.QPushButton('Buyer', self)
        self.seller_button = QtWidgets.QPushButton('Seller', self)
        self.back_button = QtWidgets.QPushButton('Back', self)

        # 设置控件样式
        button_style = """
                   QPushButton {
                       background-color: #4CAF50; 
                       color: white; 
                       font-size: 22px; 
                       border-radius: 10px; 
                       padding: 10px;
                   }
                   QPushButton:hover {
                       background-color: #45a049;
                   }
               """
        self.buyer_button.setStyleSheet(button_style)
        self.seller_button.setStyleSheet(button_style)
        self.back_button.setStyleSheet(button_style)

        # 设置按钮大小
        self.buyer_button.setFixedSize(200, 50)
        self.seller_button.setFixedSize(200, 50)
        self.back_button.setFixedSize(100, 40)

        self.buyer_button.clicked.connect(self.show_buyer_options)
        self.seller_button.clicked.connect(self.show_seller_options)
        self.back_button.clicked.connect(self.go_back)

        # 设置布局
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.buyer_button)
        button_layout.addWidget(self.seller_button)
        button_layout.addStretch(1)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addStretch(1)
        main_layout.addLayout(button_layout)
        main_layout.addStretch(1)

        outer_layout = QtWidgets.QVBoxLayout()
        outer_layout.addLayout(main_layout)
        outer_layout.addWidget(self.back_button, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)

        self.setLayout(outer_layout)

    def show_buyer_options(self):
        self.show_user_login_register_options('buyer')

    def show_seller_options(self):
        self.show_user_login_register_options('seller')

    def show_user_login_register_options(self, user_type):
        self.main_window.setCentralWidget(UserLoginRegisterChoiceWindow(self.main_window, user_type))

    def go_back(self):
        from role_selection import RoleSelectionWindow
        self.main_window.setCentralWidget(RoleSelectionWindow(self.main_window))
        self.main_window.resize(1800, 1100)  # 返回时调整窗口大小

    def center_window(self):
        frame_geometry = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        center_point = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())



class UserLoginRegisterChoiceWindow(QtWidgets.QWidget):
    def __init__(self, main_window, user_type):
        super().__init__()
        self.main_window = main_window
        self.user_type = user_type
        self.init_ui()

    def init_ui(self):
        # 设置窗口大小
        self.setFixedSize(800,600)
        self.main_window.setWindowTitle(f'{self.user_type.capitalize()} Login/Register')

        # 设置全局样式表，统一字体大小为
        self.setStyleSheet("""
                                    QLabel, QLineEdit, QPushButton, QTableWidget {
                                        font-size: 10pt;
                                    }
                                    QTableWidget {
                                        font-size: 8pt;  # 表格内容字体大小
                                    }
                                """)
        self.register_button = QtWidgets.QPushButton('注册', self)
        self.login_button = QtWidgets.QPushButton('登录', self)
        self.back_button = QtWidgets.QPushButton('Back', self)
        # 设置控件样式
        button_style = """
                    QPushButton {{
                        background-color: #4CAF50; 
                        color: white; 
                        font-size: 28px; 
                        border-radius: 18px; 
                        padding: 10px;
                    }}
                    QPushButton:hover {{
                        background-color: #45a049;
                    }}
                """
        self.register_button.setStyleSheet(button_style)
        self.login_button.setStyleSheet(button_style)
        self.back_button.setStyleSheet(button_style)

        # 设置按钮大小
        self.register_button.setFixedSize(200, 50)
        self.login_button.setFixedSize(200, 50)
        self.back_button.setFixedSize(100, 40)


        self.register_button.clicked.connect(self.show_register)
        self.login_button.clicked.connect(self.show_login)
        self.back_button.clicked.connect(self.go_back)

        # 设置布局
        button_layout = QtWidgets.QVBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.register_button, alignment=QtCore.Qt.AlignCenter)
        button_layout.addWidget(self.login_button, alignment=QtCore.Qt.AlignCenter)
        button_layout.addStretch(1)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.back_button, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)

        self.setLayout(main_layout)

    def show_register(self):
        self.main_window.setCentralWidget(UserLoginRegisterWindow(self.main_window, self.user_type, 'register'))

    def show_login(self):
        self.main_window.setCentralWidget(UserLoginRegisterWindow(self.main_window, self.user_type, 'login'))

    def go_back(self):
        from user_choice import UserChoiceWindow
        self.main_window.setCentralWidget(UserChoiceWindow(self.main_window))

