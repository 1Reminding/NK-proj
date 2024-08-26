# admin_user_management.py
from PyQt5 import QtWidgets, QtCore,QtGui
from db_connection import get_db_connection


class AdminUserManagementWindow(QtWidgets.QWidget):
    # def __init__(self, main_window):
    #     super().__init__()
    #     self.main_window = main_window
    #     self.init_ui()
    def __init__(self, main_window, admin_id):
        super().__init__()
        self.main_window = main_window
        self.admin_id = admin_id
        self.init_ui()
        self.load_all_users()  # 加载所有用户信息

    def init_ui(self):
        self.setFixedSize(1200, 800)  # 设置窗口大小
        self.main_window.setWindowTitle('用户信息管理')

        # 设置全局样式表，统一字体大小为14
        self.setStyleSheet("""
                    QLabel, QLineEdit, QPushButton, QTableWidget {
                        font-size: 10pt;
                    }
                    QTableWidget {
                        font-size: 8pt;  # 表格内容字体大小
                    }
                """)

        self.user_id_label = QtWidgets.QLabel('用户ID:')
        self.username_label = QtWidgets.QLabel('用户名:')
        self.password_label = QtWidgets.QLabel('密码:')
        self.user_type_label = QtWidgets.QLabel('用户类型:')
        self.email_label = QtWidgets.QLabel('邮箱:')
        self.phone_label = QtWidgets.QLabel('联系方式:')
        self.address_label = QtWidgets.QLabel('地址:')

        self.user_id_input = QtWidgets.QLineEdit(self)
        self.username_input = QtWidgets.QLineEdit(self)
        self.password_input = QtWidgets.QLineEdit(self)
        self.user_type_input = QtWidgets.QLineEdit(self)
        self.email_input = QtWidgets.QLineEdit(self)
        self.phone_input = QtWidgets.QLineEdit(self)
        self.address_input = QtWidgets.QLineEdit(self)

        self.search_button = QtWidgets.QPushButton('查找', self)
        self.add_button = QtWidgets.QPushButton('增加', self)
        self.delete_button = QtWidgets.QPushButton('删除', self)
        self.update_button = QtWidgets.QPushButton('修改', self)
        self.confirm_button = QtWidgets.QPushButton('确认', self)
        self.back_button = QtWidgets.QPushButton('返回', self)

        self.search_button.clicked.connect(self.search_user)
        self.add_button.clicked.connect(self.add_user)
        self.delete_button.clicked.connect(self.delete_user)
        self.update_button.clicked.connect(self.update_user)
        self.confirm_button.clicked.connect(self.confirm_changes)
        self.back_button.clicked.connect(self.go_back)

        self.table = QtWidgets.QTableWidget(self)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['用户ID', '用户名', '密码', '用户类型', '邮箱', '联系方式', '地址'])

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.user_id_label, 0, 0)
        layout.addWidget(self.user_id_input, 0, 1)
        layout.addWidget(self.username_label, 1, 0)
        layout.addWidget(self.username_input, 1, 1)
        layout.addWidget(self.password_label, 2, 0)
        layout.addWidget(self.password_input, 2, 1)
        layout.addWidget(self.user_type_label, 3, 0)
        layout.addWidget(self.user_type_input, 3, 1)
        layout.addWidget(self.email_label, 4, 0)
        layout.addWidget(self.email_input, 4, 1)
        layout.addWidget(self.phone_label, 5, 0)
        layout.addWidget(self.phone_input, 5, 1)
        layout.addWidget(self.address_label, 6, 0)
        layout.addWidget(self.address_input, 6, 1)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.update_button)

        layout.addLayout(button_layout, 8, 0, 1, 2)

        confirm_back_layout = QtWidgets.QHBoxLayout()
        confirm_back_layout.addStretch()
        confirm_back_layout.addWidget(self.confirm_button)
        confirm_back_layout.addWidget(self.back_button)

        layout.addLayout(confirm_back_layout, 9, 0, 1, 2)
        layout.addWidget(self.table, 10, 0, 1, 2)

        self.setLayout(layout)
        self.resize(600, 500)

    def load_all_users(self):
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT user_id, username, password, user_type, email, phone, address FROM users")
                results = cursor.fetchall()
                self.table.setRowCount(len(results))
                for row_num, row_data in enumerate(results):
                    self.table.setItem(row_num, 0, QtWidgets.QTableWidgetItem(row_data['user_id']))
                    self.table.setItem(row_num, 1, QtWidgets.QTableWidgetItem(row_data['username']))
                    self.table.setItem(row_num, 2, QtWidgets.QTableWidgetItem(row_data['password']))
                    self.table.setItem(row_num, 3, QtWidgets.QTableWidgetItem(row_data['user_type']))
                    self.table.setItem(row_num, 4, QtWidgets.QTableWidgetItem(row_data['email']))
                    self.table.setItem(row_num, 5, QtWidgets.QTableWidgetItem(row_data['phone']))
                    self.table.setItem(row_num, 6, QtWidgets.QTableWidgetItem(row_data['address']))
        except Exception as e:
            print(f"Error loading users: {e}")
        finally:
            connection.close()

    def search_user(self):
        user_id = self.user_id_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        user_type = self.user_type_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()
        address = self.address_input.text()

        query = "SELECT user_id, username, password, user_type, email, phone, address FROM users WHERE 1=1"
        params = []

        if user_id:
            query += " AND user_id=%s"
            params.append(user_id)
        if username:
            query += " AND username=%s"
            params.append(username)
        if password:
            query += " AND password=%s"
            params.append(password)
        if user_type:
            query += " AND user_type=%s"
            params.append(user_type)
        if email:
            query += " AND email=%s"
            params.append(email)
        if phone:
            query += " AND phone=%s"
            params.append(phone)
        if address:
            query += " AND address=%s"
            params.append(address)

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute(query, tuple(params))
                results = cursor.fetchall()
                self.table.setRowCount(len(results))
                for row_num, row_data in enumerate(results):
                    self.table.setItem(row_num, 0, QtWidgets.QTableWidgetItem(row_data['user_id']))
                    self.table.setItem(row_num, 1, QtWidgets.QTableWidgetItem(row_data['username']))
                    self.table.setItem(row_num, 2, QtWidgets.QTableWidgetItem(row_data['password']))
                    self.table.setItem(row_num, 3, QtWidgets.QTableWidgetItem(row_data['user_type']))
                    self.table.setItem(row_num, 4, QtWidgets.QTableWidgetItem(row_data['email']))
                    self.table.setItem(row_num, 5, QtWidgets.QTableWidgetItem(row_data['phone']))
                    self.table.setItem(row_num, 6, QtWidgets.QTableWidgetItem(row_data['address']))
                if not results:
                    QtWidgets.QMessageBox.warning(self, 'Error', 'User not found')
        except Exception as e:
            print(f"Error searching user: {e}")
        finally:
            connection.close()

    def add_user(self):

        user_id = self.user_id_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        user_type = self.user_type_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()
        address = self.address_input.text()
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = "INSERT INTO users (user_id, username, password, user_type, email, phone, address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (user_id, username, password, user_type, email, phone, address))
            connection.commit()
            QtWidgets.QMessageBox.information(self, 'Success', 'User added successfully')
        except Exception as e:
            print(f"Error adding user: {e}")
            QtWidgets.QMessageBox.warning(self, 'Error', 'Failed to add user')
        finally:
            connection.close()

    def delete_user(self):
        user_id = self.user_id_input.text()
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                # 开启事务
                connection.begin()
                # 删除与用户相关的所有信息
                cursor.execute(
                    "DELETE FROM order_items WHERE order_id IN (SELECT order_id FROM orders WHERE buyer_id=%s)",
                    (user_id,))
                cursor.execute("DELETE FROM orders WHERE buyer_id=%s", (user_id,))
                cursor.execute("DELETE FROM sellers WHERE seller_id=%s", (user_id,))
                cursor.execute("DELETE FROM buyers WHERE buyer_id=%s", (user_id,))
                cursor.execute("DELETE FROM users WHERE user_id=%s", (user_id,))
                # 提交事务
                connection.commit()
                QtWidgets.QMessageBox.information(self, 'Success', 'User deleted successfully')
        except Exception as e:
            connection.rollback()
            print(f"Error deleting user: {e}")
            QtWidgets.QMessageBox.warning(self, 'Error', 'Failed to delete user')
        finally:
            connection.close()

    def update_user(self):
        user_id = self.user_id_input.text()
        username = self.username_input.text() or None
        password = self.password_input.text() or None
        user_type = self.user_type_input.text() or None
        email = self.email_input.text() or None
        phone = self.phone_input.text() or None
        address = self.address_input.text() or None
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = "UPDATE users SET "
                updates = []
                params = []
                if username:
                    updates.append("username=%s")
                    params.append(username)
                if password:
                    updates.append("password=%s")
                    params.append(password)
                if user_type:
                    updates.append("user_type=%s")
                    params.append(user_type)
                if email:
                    updates.append("email=%s")
                    params.append(email)
                if phone:
                    updates.append("phone=%s")
                    params.append(phone)
                if address:
                    updates.append("address=%s")
                    params.append(address)
                sql += ", ".join(updates) + " WHERE user_id=%s"
                params.append(user_id)
                cursor.execute(sql, params)
            connection.commit()
            QtWidgets.QMessageBox.information(self, 'Success', 'User updated successfully')
        except Exception as e:
            print(f"Error updating user: {e}")
            QtWidgets.QMessageBox.warning(self, 'Error', 'Failed to update user')
        finally:
            connection.close()

    def confirm_changes(self):
        # 可用于确认修改或保存用户信息
        QtWidgets.QMessageBox.information(self, 'Info', 'Changes confirmed')

    def go_back(self):
        from admin_main import AdminMainWindow
        self.main_window.setCentralWidget(AdminMainWindow(self.main_window))
    # def go_back(self):
    #     from admin_main import AdminMainWindow
    #     self.main_window.setCentralWidget(AdminMainWindow(self.main_window, self.admin_id))