from PyQt5 import QtWidgets
from db_connection import get_db_connection

class SellerPersonalInfoWindow(QtWidgets.QWidget):
    def __init__(self, main_window, seller_id):
        super().__init__()
        self.main_window = main_window
        self.seller_id = seller_id
        self.init_ui()
        self.load_seller_info()

    def init_ui(self):
        self.main_window.setWindowTitle('卖家个人信息修改')
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
        self.phone_label = QtWidgets.QLabel('电话:')
        self.address_label = QtWidgets.QLabel('地址:')
        self.gender_label = QtWidgets.QLabel('性别:')

        self.username_input = QtWidgets.QLineEdit(self)
        self.password_input = QtWidgets.QLineEdit(self)
        self.email_input = QtWidgets.QLineEdit(self)
        self.phone_input = QtWidgets.QLineEdit(self)
        self.address_input = QtWidgets.QLineEdit(self)
        self.gender_input = QtWidgets.QLineEdit(self)

        self.update_button = QtWidgets.QPushButton('更新', self)
        self.update_button.clicked.connect(self.update_seller_info)

        self.back_button = QtWidgets.QPushButton('返回', self)
        self.back_button.clicked.connect(self.go_back)

        layout = QtWidgets.QFormLayout()
        layout.addRow(self.username_label, self.username_input)
        layout.addRow(self.password_label, self.password_input)
        layout.addRow(self.email_label, self.email_input)
        layout.addRow(self.phone_label, self.phone_input)
        layout.addRow(self.address_label, self.address_input)
        layout.addRow(self.gender_label, self.gender_input)
        layout.addWidget(self.update_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_seller_info(self):
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT username, password, email, phone, address FROM users WHERE user_id=%s", (self.seller_id,))
                user_info = cursor.fetchone()
                cursor.execute("SELECT seller_name, IFNULL(gender, '未知') AS gender FROM sellers WHERE seller_id=%s", (self.seller_id,))
                seller_info = cursor.fetchone()

                if user_info and seller_info:
                    self.username_input.setText(user_info['username'])
                    self.password_input.setText(user_info['password'])
                    self.email_input.setText(user_info['email'])
                    self.phone_input.setText(user_info['phone'])
                    self.address_input.setText(user_info['address'])
                    self.gender_input.setText(seller_info['gender'])
                else:
                    QtWidgets.QMessageBox.warning(self, 'Error', '未找到卖家信息')
        except Exception as e:
            print(f"Error loading seller info: {e}")
        finally:
            connection.close()

    def update_seller_info(self):
        username = self.username_input.text()
        password = self.password_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()
        address = self.address_input.text()
        gender = self.gender_input.text()

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET username=%s, password=%s, email=%s, phone=%s, address=%s WHERE user_id=%s",
                    (username, password, email, phone, address, self.seller_id))
                cursor.execute(
                    "UPDATE sellers SET seller_name=%s, gender=%s WHERE seller_id=%s",
                    (username, gender, self.seller_id))
            connection.commit()
            QtWidgets.QMessageBox.information(self, 'Success', '卖家信息更新成功')
        except Exception as e:
            print(f"Error updating seller info: {e}")
            QtWidgets.QMessageBox.warning(self, 'Error', '更新卖家信息失败')
        finally:
            connection.close()

    def go_back(self):
        from seller_main import SellerMainWindow
        self.main_window.setCentralWidget(SellerMainWindow(self.main_window, self.seller_id))
