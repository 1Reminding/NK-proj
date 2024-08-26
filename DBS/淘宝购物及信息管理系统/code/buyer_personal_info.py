from PyQt5 import QtWidgets, QtCore
from db_connection import get_db_connection
import re


class BuyerPersonalInfoWindow(QtWidgets.QWidget):
    def __init__(self, main_window, user_id):
        super().__init__()
        self.main_window = main_window
        self.user_id = user_id
        self.init_ui()

    def init_ui(self):
        self.main_window.setWindowTitle('个人信息修改')
        self.setStyleSheet("""
                                            QLabel, QLineEdit, QPushButton, QTableWidget {
                                                font-size: 10pt;
                                            }
                                            QTableWidget {
                                                font-size: 8pt;  # 表格内容字体大小
                                            }
                                        """)
        self.username_label = QtWidgets.QLabel('用户名:')
        self.password_label = QtWidgets.QLabel('密码:')
        self.email_label = QtWidgets.QLabel('邮箱:')
        self.phone_label = QtWidgets.QLabel('联系方式:')
        self.address_label = QtWidgets.QLabel('地址:')

        self.username_input = QtWidgets.QLineEdit(self)
        self.password_input = QtWidgets.QLineEdit(self)
        self.email_input = QtWidgets.QLineEdit(self)
        self.phone_input = QtWidgets.QLineEdit(self)
        self.address_input = QtWidgets.QLineEdit(self)

        self.update_button = QtWidgets.QPushButton('更新', self)
        self.back_button = QtWidgets.QPushButton('返回', self)

        self.update_button.clicked.connect(self.update_info)
        self.back_button.clicked.connect(self.go_back)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.username_label, 0, 0)
        layout.addWidget(self.username_input, 0, 1)
        layout.addWidget(self.password_label, 1, 0)
        layout.addWidget(self.password_input, 1, 1)
        layout.addWidget(self.email_label, 2, 0)
        layout.addWidget(self.email_input, 2, 1)
        layout.addWidget(self.phone_label, 3, 0)
        layout.addWidget(self.phone_input, 3, 1)
        layout.addWidget(self.address_label, 4, 0)
        layout.addWidget(self.address_input, 4, 1)
        layout.addWidget(self.update_button, 5, 1)
        layout.addWidget(self.back_button, 6, 1)

        self.setLayout(layout)
        self.load_info()

    def load_info(self):
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = "SELECT username, password, email, phone, address FROM users WHERE user_id=%s"
                cursor.execute(sql, (self.user_id,))
                result = cursor.fetchone()
                if result:
                    self.username_input.setText(result['username'])
                    self.password_input.setText(result['password'])
                    self.email_input.setText(result['email'])
                    self.phone_input.setText(result['phone'])
                    self.address_input.setText(result['address'])
        except Exception as e:
            print(f"Error loading user info: {e}")
        finally:
            connection.close()

    def update_info(self):
        username = self.username_input.text()
        password = self.password_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()
        address = self.address_input.text()

        if not username or not re.match(r'^U\d{6}$', self.user_id):
            QtWidgets.QMessageBox.warning(self, 'Error', '用户名或用户ID格式不正确')
            return

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = "UPDATE users SET username=%s, password=%s, email=%s, phone=%s, address=%s WHERE user_id=%s"
                cursor.execute(sql, (username, password, email, phone, address, self.user_id))
            connection.commit()
            QtWidgets.QMessageBox.information(self, 'Success', '信息更新成功')
        except Exception as e:
            print(f"Error updating user info: {e}")
            QtWidgets.QMessageBox.warning(self, 'Error', '信息更新失败')
        finally:
            connection.close()

    def go_back(self):
        from buyer_main import BuyerMainWindow
        self.main_window.setCentralWidget(BuyerMainWindow(self.main_window, self.user_id))
