from PyQt5 import QtWidgets
from db_connection import get_db_connection


class AdminPersonalInfoWindow(QtWidgets.QWidget):
    def __init__(self, main_window, admin_id):
        super().__init__()
        self.main_window = main_window
        self.admin_id = admin_id
        self.init_ui()
        self.load_admin_info()

    def init_ui(self):
        self.main_window.setWindowTitle('个人信息修改')

        # 设置全局样式表，统一字体大小为
        self.setStyleSheet("""
                                    QLabel, QLineEdit, QPushButton, QTableWidget {
                                        font-size: 10pt;
                                    }
                                    QTableWidget {
                                        font-size: 8pt;  # 表格内容字体大小
                                    }
                                """)

        self.name_label = QtWidgets.QLabel('Name:')
        self.password_label = QtWidgets.QLabel('Password:')
        self.email_label = QtWidgets.QLabel('Email:')
        self.phone_label = QtWidgets.QLabel('Phone:')
        self.address_label = QtWidgets.QLabel('Address:')

        self.name_input = QtWidgets.QLineEdit(self)
        self.password_input = QtWidgets.QLineEdit(self)
        self.email_input = QtWidgets.QLineEdit(self)
        self.phone_input = QtWidgets.QLineEdit(self)
        self.address_input = QtWidgets.QLineEdit(self)

        self.save_button = QtWidgets.QPushButton('保存修改', self)
        self.back_button = QtWidgets.QPushButton('Back', self)

        self.save_button.clicked.connect(self.save_changes)
        self.back_button.clicked.connect(self.go_back)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.name_label, 0, 0)
        layout.addWidget(self.name_input, 0, 1)
        layout.addWidget(self.password_label, 1, 0)
        layout.addWidget(self.password_input, 1, 1)
        layout.addWidget(self.email_label, 2, 0)
        layout.addWidget(self.email_input, 2, 1)
        layout.addWidget(self.phone_label, 3, 0)
        layout.addWidget(self.phone_input, 3, 1)
        layout.addWidget(self.address_label, 4, 0)
        layout.addWidget(self.address_input, 4, 1)
        layout.addWidget(self.save_button, 5, 1)
        layout.addWidget(self.back_button, 6, 1)

        self.setLayout(layout)

    def load_admin_info(self):
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = "SELECT username, password, email, phone, address FROM administrators WHERE admin_id=%s"
                cursor.execute(sql, (self.admin_id,))
                result = cursor.fetchone()
                if result:
                    self.name_input.setText(result['username'])
                    self.password_input.setText(result['password'])
                    self.email_input.setText(result['email'])
                    self.phone_input.setText(result['phone'])
                    self.address_input.setText(result['address'])
        except Exception as e:
            print(f"Error loading admin info: {e}")
        finally:
            connection.close()  # 确保连接关闭

    def save_changes(self):
        username = self.name_input.text() or 'default_name'
        password = self.password_input.text() or 'default_password'
        email = self.email_input.text() or 'default_email'
        phone = self.phone_input.text() or 'default_phone'
        address = self.address_input.text() or 'default_address'

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = """
                UPDATE administrators
                SET username=%s, password=%s, email=%s, phone=%s, address=%s
                WHERE admin_id=%s
                """
                cursor.execute(sql, (username, password, email, phone, address, self.admin_id))
            connection.commit()
            QtWidgets.QMessageBox.information(self, 'Success', 'Information updated successfully')
        except Exception as e:
            print(f"Error saving admin info: {e}")
            QtWidgets.QMessageBox.warning(self, 'Error', 'Failed to update information')
        finally:
            connection.close()  # 确保连接关闭

    def go_back(self):
        from admin_main import AdminMainWindow
        self.main_window.setCentralWidget(AdminMainWindow(self.main_window, self.admin_id))
        self.main_window.resize(800,600)  # 返回时调整窗口大小