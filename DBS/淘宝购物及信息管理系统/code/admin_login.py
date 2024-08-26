# admin_login.py
from PyQt5 import QtWidgets
from db_connection import get_db_connection
from admin_main import AdminMainWindow
import os
class AdminLoginWindow(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(800, 600)
        self.main_window.setWindowTitle('Admin Login')

        # 设置背景图
        script_dir = os.path.dirname(os.path.abspath(__file__))
        background_image_path = os.path.join(script_dir, 'main.png')
        self.setStyleSheet(f"""
                    QWidget {{
                        background-image: url({background_image_path});
                        background-repeat: no-repeat;
                        background-position: center;
                        background-attachment: fixed;
                        background-size: cover;
                    }}
                """)

        self.admin_id_label = QtWidgets.QLabel('管理员 ID:')
        self.password_label = QtWidgets.QLabel('密码:')
        self.admin_id_input = QtWidgets.QLineEdit(self)
        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_button = QtWidgets.QPushButton('登录', self)
        self.back_button = QtWidgets.QPushButton('Back', self)


        # 设置控件样式
        label_style = "color: black; font-size: 22px;"
        input_style = "background-color: white; font-size: 20px;"
        button_style = """
                   QPushButton {
                       background-color: #4CAF50; 
                       color: black; 
                       font-size: 20px; 
                       border-radius: 10px; 
                       padding: 10px;
                   }
                   QPushButton:hover {
                       background-color: #45a049;
                   }
               """
        self.admin_id_label.setStyleSheet(label_style)
        self.password_label.setStyleSheet(label_style)
        self.admin_id_input.setStyleSheet(input_style)
        self.password_input.setStyleSheet(input_style)
        self.login_button.setStyleSheet(button_style)
        self.back_button.setStyleSheet(button_style)


        # 连接按钮点击事件
        self.login_button.clicked.connect(self.login)
        self.back_button.clicked.connect(self.go_back)
        #设置布局
        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(100, 100, 100, 100)
        layout.setVerticalSpacing(20)
        layout.setHorizontalSpacing(10)
        layout.addWidget(self.admin_id_label, 0, 0)
        layout.addWidget(self.admin_id_input, 0, 1)
        layout.addWidget(self.password_label, 1, 0)
        layout.addWidget(self.password_input, 1, 1)
        layout.addWidget(self.login_button, 2, 1, 1, 2)
        layout.addWidget(self.back_button, 3, 1, 1, 2)
        # # 设置布局
        # form_layout = QtWidgets.QFormLayout()
        # form_layout.addRow(self.admin_id_label, self.admin_id_input)
        # form_layout.addRow(self.password_label, self.password_input)
        #
        # button_layout = QtWidgets.QHBoxLayout()
        # button_layout.addStretch(1)
        # button_layout.addWidget(self.login_button)
        # button_layout.addWidget(self.back_button)
        # button_layout.addStretch(1)
        #
        # main_layout = QtWidgets.QVBoxLayout()
        # main_layout.addStretch(1)
        # main_layout.addLayout(form_layout)
        # main_layout.addLayout(button_layout)
        # main_layout.addStretch(1)
        #
        # container = QtWidgets.QWidget()
        # container.setLayout(main_layout)
        # container.setMaximumWidth(400)
        #
        # outer_layout = QtWidgets.QHBoxLayout()
        # outer_layout.addStretch(1)
        # outer_layout.addWidget(container)
        # outer_layout.addStretch(1)
        self.setLayout(layout)

    def login(self):
        admin_id = self.admin_id_input.text()
        password = self.password_input.text()
        if self.check_login(admin_id, password):
            QtWidgets.QMessageBox.information(self, 'Success', '登录成功！')
            self.main_window.setCentralWidget(AdminMainWindow(self.main_window, admin_id))
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', '管理员ID或密码错误！')

    def go_back(self):
        from role_selection import RoleSelectionWindow
        self.main_window.setCentralWidget(RoleSelectionWindow(self.main_window))

        self.main_window.resize(1800, 1100)  # 返回时调整窗口大小
    def check_login(self, admin_id, password):
        try:
            print(f"Trying to login with admin ID: {admin_id}")
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = "SELECT password FROM administrators WHERE admin_id=%s"
                cursor.execute(sql, (admin_id,))
                result = cursor.fetchone()
                print(f"Admin login query result: {result}")
                if result and result['password'] == password:
                    return True
        except Exception as e:
            print(f"Error checking admin login: {e}")
        # finally:  admin用户信息管理界面返回报错
            # connection.close()  # 确保连接关闭
        return False
