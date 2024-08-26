# user_login_register.py
from PyQt5 import QtWidgets
from db_connection import get_db_connection
import re
from seller_main import SellerMainWindow
from buyer_main import BuyerMainWindow
class UserLoginRegisterWindow(QtWidgets.QWidget):
    def __init__(self, main_window, user_type, action):
        super().__init__()
        self.main_window = main_window
        self.user_type = user_type
        self.action = action
        self.init_ui()

    def init_ui(self):
        self.main_window.setWindowTitle('User Login')
        # 设置全局样式表，统一字体大小为
        self.setStyleSheet("""
                                    QLabel, QLineEdit, QPushButton, QTableWidget {
                                        font-size: 10pt;
                                    }
                                    QTableWidget {
                                        font-size: 8pt;  # 表格内容字体大小
                                    }
                                """)
        if self.action == 'register':
            self.userid_label = QtWidgets.QLabel('用户 ID:')
            self.userid_input = QtWidgets.QLineEdit(self)

        self.username_label = QtWidgets.QLabel('用户名:')
        self.password_label = QtWidgets.QLabel('密码:')
        self.username_input = QtWidgets.QLineEdit(self)
        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.action_button = QtWidgets.QPushButton(self.action.capitalize(), self)
        self.back_button = QtWidgets.QPushButton('Back', self)

        self.action_button.clicked.connect(self.perform_action)
        self.back_button.clicked.connect(self.go_back)

        layout = QtWidgets.QGridLayout()

        if self.action == 'register':
            layout.addWidget(self.userid_label, 0, 0)
            layout.addWidget(self.userid_input, 0, 1)
            layout.addWidget(self.username_label, 1, 0)
            layout.addWidget(self.username_input, 1, 1)
            layout.addWidget(self.password_label, 2, 0)
            layout.addWidget(self.password_input, 2, 1)
            layout.addWidget(self.action_button, 3, 1)
            layout.addWidget(self.back_button, 4, 1)
        else:
            self.username_label.setText('User ID:')
            layout.addWidget(self.username_label, 0, 0)
            layout.addWidget(self.username_input, 0, 1)
            layout.addWidget(self.password_label, 1, 0)
            layout.addWidget(self.password_input, 1, 1)
            layout.addWidget(self.action_button, 2, 1)
            layout.addWidget(self.back_button, 3, 1)

        self.setLayout(layout)

    def perform_action(self):
        if self.action == 'login':
            self.login(self.username_input.text(), self.password_input.text())
        elif self.action == 'register':
            self.register(self.userid_input.text(), self.username_input.text(), self.password_input.text())

    # def login(self, userid, password):
    #     if not self.validate_userid_format(userid):
    #         QtWidgets.QMessageBox.warning(self, 'Error', 'Invalid User ID format')
    #         return
    #
    #     if self.check_login(userid, password):
    #         QtWidgets.QMessageBox.information(self, 'Success', 'Login successful')
    #         # 跳转到用户主界面
    #         self.main_window.setCentralWidget(BuyerMainWindow(self.main_window, userid))
    #     else:
    #         QtWidgets.QMessageBox.warning(self, 'Error', 'Invalid user ID or password')

    def login(self, userid, password):
        if not self.validate_userid_format(userid):
            QtWidgets.QMessageBox.warning(self, 'Error', '用户ID格式错误！')
            return

        if self.check_login(userid, password):
            QtWidgets.QMessageBox.information(self, 'Success', '登录成功！')
            # 获取用户类型
            user_type = self.get_user_type(userid)
            if user_type == 'buyer':
                self.main_window.setCentralWidget(BuyerMainWindow(self.main_window, userid))
            elif user_type == 'seller':
                self.main_window.setCentralWidget(SellerMainWindow(self.main_window, userid))
            else:
                QtWidgets.QMessageBox.warning(self, 'Error', 'Unknown user type')
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', '用户ID或密码错误！')

    def get_user_type(self, userid):
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT user_type FROM users WHERE user_id = %s", (userid,))
                result = cursor.fetchone()
                if result:
                    return result['user_type']
                else:
                    return None
        except Exception as e:
            print(f"Error getting user type: {e}")
            return None
        finally:
            connection.close()

    def register(self, userid, username, password):
        if not self.validate_userid_format(userid):
            QtWidgets.QMessageBox.warning(self, 'Error', '用户ID格式错误！')
            return

        if self.check_user_exists(userid):
            QtWidgets.QMessageBox.warning(self, 'Error', '用户ID已存在！')
        else:
            self.add_user(userid, username, password)
            QtWidgets.QMessageBox.information(self, 'Success', '注册成功！')

    def go_back(self):
        from user_choice import UserLoginRegisterChoiceWindow
        self.main_window.setCentralWidget(UserLoginRegisterChoiceWindow(self.main_window, self.user_type))

    def validate_userid_format(self, userid):
        return re.match(r'^U\d{6}$', userid) is not None

    def check_login(self, userid, password):
        try:
            print(f"Trying to login with user ID: {userid}")
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = "SELECT password FROM users WHERE user_id=%s"
                cursor.execute(sql, (userid,))
                result = cursor.fetchone()
                print(f"Login query result: {result}")
                if result and result['password'] == password:
                    return True
        except Exception as e:
            print(f"Error checking login: {e}")
        finally:
            connection.close()  # 确保连接关闭
        return False

    def check_user_exists(self, userid):
        try:
            print(f"Checking if user ID exists: {userid}")
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = "SELECT user_id FROM users WHERE user_id=%s"
                cursor.execute(sql, (userid,))
                result = cursor.fetchone()
                print(f"User existence query result: {result}")
                return result is not None
        except Exception as e:
            print(f"Error checking user existence: {e}")
        return False

    def add_user(self, userid, username, password):
        try:
            print(f"Adding user: {userid}, {username}")
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO users (user_id, username, password, user_type)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (userid, username, password, self.user_type))
            connection.commit()
            print(f"User added successfully: {userid}")
        except Exception as e:
            print(f"Error adding user: {e}")
        finally:
            connection.close()  # 确保连接关闭
