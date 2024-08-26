# seller_shop_management.py
from PyQt5 import QtWidgets
from db_connection import get_db_connection


class SellerShopManagementWindow(QtWidgets.QWidget):
    def __init__(self, main_window, seller_id):
        super().__init__()
        self.main_window = main_window
        self.seller_id = seller_id
        self.init_ui()
        self.load_shop_info()

    def init_ui(self):
        self.main_window.setWindowTitle('管理店铺')
        self.setStyleSheet("""
                                            QLabel, QLineEdit, QPushButton, QTableWidget {
                                                font-size: 10pt;
                                            }
                                            QTableWidget {
                                                font-size: 8pt;  # 表格内容字体大小
                                            }
                                        """)
        self.open_shop_label = QtWidgets.QLabel('想要自己的店铺？')
        self.open_shop_button = QtWidgets.QPushButton('一键开店', self)
        self.open_shop_button.clicked.connect(self.open_shop)

        self.table = QtWidgets.QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['用户ID', '店铺ID', '店铺名称', '店铺描述'])

        self.shop_id_label = QtWidgets.QLabel('店铺ID:')
        self.shop_name_label = QtWidgets.QLabel('店铺名称:')
        self.shop_description_label = QtWidgets.QLabel('店铺描述:')

        self.shop_id_input = QtWidgets.QLineEdit(self)
        self.shop_name_input = QtWidgets.QLineEdit(self)
        self.shop_description_input = QtWidgets.QLineEdit(self)

        self.modify_button = QtWidgets.QPushButton('修改', self)
        self.modify_button.clicked.connect(self.modify_shop_info)

        self.refresh_button = QtWidgets.QPushButton('更新', self)
        self.refresh_button.clicked.connect(self.load_shop_info)

        self.back_button = QtWidgets.QPushButton('返回', self)
        self.back_button.clicked.connect(self.go_back)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.open_shop_label)
        layout.addWidget(self.open_shop_button)
        layout.addWidget(self.table)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(self.shop_id_label, self.shop_id_input)
        form_layout.addRow(self.shop_name_label, self.shop_name_input)
        form_layout.addRow(self.shop_description_label, self.shop_description_input)
        layout.addLayout(form_layout)
        layout.addWidget(self.modify_button)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_shop_info(self):
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT shop_id, shop_name, shop_description FROM shops WHERE seller_id=%s",
                               (self.seller_id,))
                results = cursor.fetchall()
                self.table.setRowCount(len(results))
                for row_num, row_data in enumerate(results):
                    self.table.setItem(row_num, 0, QtWidgets.QTableWidgetItem(self.seller_id))
                    self.table.setItem(row_num, 1, QtWidgets.QTableWidgetItem(row_data['shop_id']))
                    self.table.setItem(row_num, 2, QtWidgets.QTableWidgetItem(row_data['shop_name']))
                    self.table.setItem(row_num, 3, QtWidgets.QTableWidgetItem(row_data['shop_description']))
        except Exception as e:
            print(f"Error loading shop info: {e}")
        finally:
            connection.close()

    def open_shop(self):
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT MAX(shop_id) AS max_shop_id FROM shops")
                max_shop_id = cursor.fetchone()['max_shop_id']
                new_shop_id = f'SH{int(max_shop_id[2:]) + 1:04d}'

                cursor.execute(
                    "INSERT INTO shops (shop_id, shop_name, shop_description, seller_id) VALUES (%s, %s, %s, %s)",
                    (new_shop_id, '新店铺', '描述', self.seller_id))
                connection.commit()
                self.load_shop_info()
                QtWidgets.QMessageBox.information(self, 'Success', '店铺创建成功')
        except Exception as e:
            print(f"Error opening shop: {e}")
            QtWidgets.QMessageBox.warning(self, 'Error', '店铺创建失败')
        finally:
            connection.close()

    def modify_shop_info(self):
        shop_id = self.shop_id_input.text()
        shop_name = self.shop_name_input.text()
        shop_description = self.shop_description_input.text()

        if not shop_id:
            QtWidgets.QMessageBox.warning(self, 'Error', '请填写店铺ID')
            return

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE shops SET shop_name=%s, shop_description=%s WHERE shop_id=%s AND seller_id=%s",
                    (shop_name, shop_description, shop_id, self.seller_id))
                connection.commit()
                self.load_shop_info()
                QtWidgets.QMessageBox.information(self, 'Success', '店铺信息更新成功')
        except Exception as e:
            print(f"Error modifying shop info: {e}")
            QtWidgets.QMessageBox.warning(self, 'Error', '店铺信息更新失败')
        finally:
            connection.close()

    def go_back(self):
        from seller_main import SellerMainWindow
        self.main_window.setCentralWidget(SellerMainWindow(self.main_window, self.seller_id))

# from PyQt5 import QtWidgets
# from db_connection import get_db_connection
#
# class SellerShopManagementWindow(QtWidgets.QWidget):
#     def __init__(self, main_window, user_id):
#         super().__init__()
#         self.main_window = main_window
#         self.user_id = user_id
#         self.init_ui()
#         self.load_shop_info()
#
#     def init_ui(self):
#         self.setWindowTitle('管理店铺')
#
#         self.open_shop_button = QtWidgets.QPushButton('一键开店', self)
#         self.open_shop_button.clicked.connect(self.open_shop)
#
#         self.table = QtWidgets.QTableWidget(self)
#         self.table.setColumnCount(4)
#         self.table.setHorizontalHeaderLabels(['用户ID', '店铺ID', '店铺名称', '店铺描述'])
#
#         self.shop_id_label = QtWidgets.QLabel('店铺ID:')
#         self.shop_name_label = QtWidgets.QLabel('店铺名称:')
#         self.shop_description_label = QtWidgets.QLabel('店铺描述:')
#
#         self.shop_id_input = QtWidgets.QLineEdit(self)
#         self.shop_name_input = QtWidgets.QLineEdit(self)
#         self.shop_description_input = QtWidgets.QLineEdit(self)
#
#         self.update_button = QtWidgets.QPushButton('修改', self)
#         self.update_button.clicked.connect(self.update_shop_info)
#         self.refresh_button = QtWidgets.QPushButton('更新', self)
#         self.refresh_button.clicked.connect(self.load_shops)
#
#         layout = QtWidgets.QVBoxLayout()
#         layout.addWidget(QtWidgets.QLabel('想要自己的店铺?'))
#         layout.addWidget(self.open_shop_button)
#         layout.addWidget(self.table)
#
#         form_layout = QtWidgets.QFormLayout()
#         form_layout.addRow(self.shop_id_label, self.shop_id_input)
#         form_layout.addRow(self.shop_name_label, self.shop_name_input)
#         form_layout.addRow(self.shop_description_label, self.shop_description_input)
#         layout.addLayout(form_layout)
#         layout.addWidget(self.update_button)
#         layout.addWidget(self.refresh_button)
#
#         self.setLayout(layout)
#         self.load_shops()
#
#     def open_shop(self):
#         try:
#             connection = get_db_connection()
#             with connection.cursor() as cursor:
#                 cursor.execute("SELECT MAX(shop_id) AS max_shop_id FROM shops")
#                 max_shop_id = cursor.fetchone()['max_shop_id']
#                 new_shop_id = f'SH{int(max_shop_id[2:]) + 1:04d}'
#
#                 cursor.execute(
#                     "INSERT INTO shops (shop_id, shop_name, shop_description, seller_id) VALUES (%s, %s, %s, %s)",
#                     (new_shop_id, '新店铺', '店铺描述', self.user_id))
#                 cursor.execute(
#                     "UPDATE sellers SET shop_id=%s WHERE seller_id=%s",
#                     (new_shop_id, self.user_id))
#
#             connection.commit()
#             QtWidgets.QMessageBox.information(self, 'Success', '店铺创建成功')
#             self.load_shops()
#         except Exception as e:
#             print(f"Error opening shop: {e}")
#             QtWidgets.QMessageBox.warning(self, 'Error', '店铺创建失败')
#         finally:
#             connection.close()
#
#     def load_shops(self):
#         try:
#             connection = get_db_connection()
#             with connection.cursor() as cursor:
#                 cursor.execute(
#                     "SELECT s.shop_id, s.shop_name, s.shop_description, s.seller_id "
#                     "FROM shops s "
#                     "JOIN sellers sl ON s.shop_id = sl.shop_id "
#                     "WHERE sl.seller_id = %s", (self.user_id,))
#                 shops = cursor.fetchall()
#
#                 self.table.setRowCount(len(shops))
#                 for row_num, shop in enumerate(shops):
#                     self.table.setItem(row_num, 0, QtWidgets.QTableWidgetItem(shop['seller_id']))
#                     self.table.setItem(row_num, 1, QtWidgets.QTableWidgetItem(shop['shop_id']))
#                     self.table.setItem(row_num, 2, QtWidgets.QTableWidgetItem(shop['shop_name']))
#                     self.table.setItem(row_num, 3, QtWidgets.QTableWidgetItem(shop['shop_description']))
#                 if not shops:
#                     QtWidgets.QMessageBox.warning(self, 'Error', '未找到店铺信息')
#         except Exception as e:
#             print(f"Error loading shops: {e}")
#         finally:
#             connection.close()
#
#     def update_shop_info(self):
#         shop_id = self.shop_id_input.text()
#         shop_name = self.shop_name_input.text()
#         shop_description = self.shop_description_input.text()
#
#         if not shop_id or not shop_name or not shop_description:
#             QtWidgets.QMessageBox.warning(self, 'Error', '请填写所有店铺信息')
#             return
#
#         try:
#             connection = get_db_connection()
#             with connection.cursor() as cursor:
#                 cursor.execute(
#                     "UPDATE shops SET shop_name=%s, shop_description=%s WHERE shop_id=%s AND seller_id=%s",
#                     (shop_name, shop_description, shop_id, self.user_id))
#
#             connection.commit()
#             QtWidgets.QMessageBox.information(self, 'Success', '店铺信息更新成功')
#             self.load_shops()
#         except Exception as e:
#             print(f"Error updating shop info: {e}")
#             QtWidgets.QMessageBox.warning(self, 'Error', '更新店铺信息失败')
#         finally:
#             connection.close()
