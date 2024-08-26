from PyQt5 import QtWidgets
from db_connection import get_db_connection
import datetime


class SellerOrderManagementWindow(QtWidgets.QWidget):
    def __init__(self, main_window, seller_id):
        super().__init__()
        self.main_window = main_window
        self.seller_id = seller_id
        self.init_ui()
        self.load_order_info()

    def init_ui(self):
        self.setFixedSize(1400, 800)  # 设置窗口大小
        self.main_window.setWindowTitle('订单处理')
        self.setStyleSheet("""
                                            QLabel, QLineEdit, QPushButton, QTableWidget {
                                                font-size: 10pt;
                                            }
                                            QTableWidget {
                                                font-size: 8pt;  # 表格内容字体大小
                                            }
                                        """)
        self.order_id_label = QtWidgets.QLabel('订单ID:')
        self.product_id_label = QtWidgets.QLabel('商品ID:')
        self.buyer_id_label = QtWidgets.QLabel('买家ID:')
        self.quantity_label = QtWidgets.QLabel('数目:')
        self.recipient_name_label = QtWidgets.QLabel('收货姓名:')
        self.phone_label = QtWidgets.QLabel('电话:')
        self.address_label = QtWidgets.QLabel('地址:')
        self.notes_label = QtWidgets.QLabel('备注:')
        self.status_label = QtWidgets.QLabel('状态:')

        self.order_id_input = QtWidgets.QLineEdit(self)
        self.product_id_input = QtWidgets.QLineEdit(self)
        self.buyer_id_input = QtWidgets.QLineEdit(self)
        self.quantity_input = QtWidgets.QLineEdit(self)
        self.recipient_name_input = QtWidgets.QLineEdit(self)
        self.phone_input = QtWidgets.QLineEdit(self)
        self.address_input = QtWidgets.QLineEdit(self)
        self.notes_input = QtWidgets.QLineEdit(self)
        self.status_input = QtWidgets.QLineEdit(self)

        self.search_button = QtWidgets.QPushButton('查找', self)
        self.search_button.clicked.connect(self.search_orders)
        self.add_button = QtWidgets.QPushButton('增加', self)
        self.add_button.clicked.connect(self.add_order)
        self.update_button = QtWidgets.QPushButton('修改', self)
        self.update_button.clicked.connect(self.update_order)
        self.delete_button = QtWidgets.QPushButton('删除', self)
        self.delete_button.clicked.connect(self.delete_order)
        self.back_button = QtWidgets.QPushButton('返回', self)
        self.back_button.clicked.connect(self.go_back)

        self.table = QtWidgets.QTableWidget(self)
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(
            ['订单ID', '商品ID', '买家ID', '数目', '收货姓名', '电话', '地址', '备注', '状态'])

        layout = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(self.order_id_label, self.order_id_input)
        form_layout.addRow(self.product_id_label, self.product_id_input)
        form_layout.addRow(self.buyer_id_label, self.buyer_id_input)
        form_layout.addRow(self.quantity_label, self.quantity_input)
        form_layout.addRow(self.recipient_name_label, self.recipient_name_input)
        form_layout.addRow(self.phone_label, self.phone_input)
        form_layout.addRow(self.address_label, self.address_input)
        form_layout.addRow(self.notes_label, self.notes_input)
        form_layout.addRow(self.status_label, self.status_input)
        layout.addLayout(form_layout)

        # 设置增删改查按钮在一行
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        layout.addLayout(button_layout)

        layout.addWidget(self.table)

        # 设置返回按钮在右下角
        back_button_layout = QtWidgets.QHBoxLayout()
        back_button_layout.addStretch()
        back_button_layout.addWidget(self.back_button)
        layout.addLayout(back_button_layout)

        self.setLayout(layout)

    def load_order_info(self):
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT o.order_id, oi.product_id, o.buyer_id, oi.quantity, o.recipient_name, o.phone, o.address, o.notes, o.status
                    FROM orders o
                    JOIN order_items oi ON o.order_id = oi.order_id
                    JOIN products p ON oi.product_id = p.product_id
                    JOIN shops s ON p.shop_id = s.shop_id
                    WHERE s.seller_id=%s
                """, (self.seller_id,))
                orders = cursor.fetchall()
                self.table.setRowCount(len(orders))
                for row_num, row_data in enumerate(orders):
                    self.table.setItem(row_num, 0, QtWidgets.QTableWidgetItem(row_data['order_id']))
                    self.table.setItem(row_num, 1, QtWidgets.QTableWidgetItem(row_data['product_id']))
                    self.table.setItem(row_num, 2, QtWidgets.QTableWidgetItem(row_data['buyer_id']))
                    self.table.setItem(row_num, 3, QtWidgets.QTableWidgetItem(str(row_data['quantity'])))
                    self.table.setItem(row_num, 4, QtWidgets.QTableWidgetItem(row_data['recipient_name']))
                    self.table.setItem(row_num, 5, QtWidgets.QTableWidgetItem(row_data['phone']))
                    self.table.setItem(row_num, 6, QtWidgets.QTableWidgetItem(row_data['address']))
                    self.table.setItem(row_num, 7, QtWidgets.QTableWidgetItem(row_data['notes']))
                    self.table.setItem(row_num, 8, QtWidgets.QTableWidgetItem(row_data['status']))
        except Exception as e:
            print(f"Error loading orders: {e}")
        finally:
            connection.close()

    def search_orders(self):
        order_id = self.order_id_input.text()
        product_id = self.product_id_input.text()
        buyer_id = self.buyer_id_input.text()

        query = """
        SELECT o.order_id, oi.product_id, o.buyer_id, oi.quantity, o.recipient_name, o.phone, o.address, o.notes, o.status
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        JOIN shops s ON p.shop_id = s.shop_id
        WHERE s.seller_id=%s
        """
        params = [self.seller_id]

        if order_id:
            query += " AND o.order_id LIKE %s"
            params.append(f'%{order_id}%')
        if product_id:
            query += " AND oi.product_id LIKE %s"
            params.append(f'%{product_id}%')
        if buyer_id:
            query += " AND o.buyer_id LIKE %s"
            params.append(f'%{buyer_id}%')

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute(query, tuple(params))
                results = cursor.fetchall()
                self.table.setRowCount(len(results))
                for row_num, row_data in enumerate(results):
                    self.table.setItem(row_num, 0, QtWidgets.QTableWidgetItem(row_data['order_id']))
                    self.table.setItem(row_num, 1, QtWidgets.QTableWidgetItem(row_data['product_id']))
                    self.table.setItem(row_num, 2, QtWidgets.QTableWidgetItem(row_data['buyer_id']))
                    self.table.setItem(row_num, 3, QtWidgets.QTableWidgetItem(str(row_data['quantity'])))
                    self.table.setItem(row_num, 4, QtWidgets.QTableWidgetItem(row_data['recipient_name']))
                    self.table.setItem(row_num, 5, QtWidgets.QTableWidgetItem(row_data['phone']))
                    self.table.setItem(row_num, 6, QtWidgets.QTableWidgetItem(row_data['address']))
                    self.table.setItem(row_num, 7, QtWidgets.QTableWidgetItem(row_data['notes']))
                    self.table.setItem(row_num, 8, QtWidgets.QTableWidgetItem(row_data['status']))
                if not results:
                    QtWidgets.QMessageBox.warning(self, 'Error', '未找到符合条件的订单')
        except Exception as e:
            print(f"Error searching orders: {e}")
        finally:
            connection.close()

    def add_order(self):
        recipient_name = self.recipient_name_input.text()
        phone = self.phone_input.text()
        address = self.address_input.text()
        product_id = self.product_id_input.text()
        quantity = self.quantity_input.text()
        buyer_id = self.buyer_id_input.text()
        notes = self.notes_input.text()

        if not recipient_name or not phone or not address or not product_id or not quantity or not buyer_id:
            QtWidgets.QMessageBox.warning(self, 'Error', '请填写所有必填信息')
            return

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            QtWidgets.QMessageBox.warning(self, 'Error', '数量必须为正整数')
            return

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT price, stock, product_name FROM products WHERE product_id=%s", (product_id,))
                product = cursor.fetchone()
                if not product:
                    QtWidgets.QMessageBox.warning(self, 'Error', '商品ID不存在')
                    return

                price = product['price']
                stock = product['stock']
                product_name = product['product_name']

                if quantity > stock:
                    QtWidgets.QMessageBox.warning(self, 'Error', '库存不足')
                    return

                subtotal = price * quantity
                order_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                cursor.execute("SELECT MAX(order_id) AS max_order_id FROM orders")
                max_order_id = cursor.fetchone()['max_order_id']
                new_order_id = f'O{int(max_order_id[1:]) + 1:04d}'

                cursor.execute("SELECT MAX(order_item_id) AS max_order_item_id FROM order_items")
                max_order_item_id = cursor.fetchone()['max_order_item_id']
                new_order_item_id = f'OI{int(max_order_item_id[2:]) + 1:04d}'

                cursor.execute(
                    "INSERT INTO orders (order_id, buyer_id, order_date, total_amount, status, recipient_name, phone, address, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (new_order_id, buyer_id, order_date, subtotal, '待处理', recipient_name, phone, address, notes))

                cursor.execute(
                    "INSERT INTO order_items (order_item_id, order_id, product_id, quantity, subtotal, product_name) VALUES (%s, %s, %s, %s, %s, %s)",
                    (new_order_item_id, new_order_id, product_id, quantity, subtotal, product_name))

                cursor.execute("UPDATE products SET stock = stock - %s WHERE product_id = %s", (quantity, product_id))

            connection.commit()
            QtWidgets.QMessageBox.information(self, 'Success', '订单提交成功')
            self.load_order_info()
        except Exception as e:
            print(f"Error adding order: {e}")
            QtWidgets.QMessageBox.warning(self, 'Error', '提交订单失败')
        finally:
            connection.close()

    def update_order(self):
        order_id = self.order_id_input.text()
        recipient_name = self.recipient_name_input.text()
        phone = self.phone_input.text()
        address = self.address_input.text()
        notes = self.notes_input.text()
        status = self.status_input.text()

        if not order_id:
            QtWidgets.QMessageBox.warning(self, 'Error', '请填写订单ID')
            return

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                # 获取当前订单信息
                cursor.execute("SELECT recipient_name, phone, address, notes, status FROM orders WHERE order_id=%s", (order_id,))
                current_order = cursor.fetchone()

                # 使用输入的值覆盖当前的值
                recipient_name = recipient_name if recipient_name else current_order['recipient_name']
                phone = phone if phone else current_order['phone']
                address = address if address else current_order['address']
                notes = notes if notes else current_order['notes']
                status = status if status else current_order['status']

                cursor.execute(
                    "UPDATE orders SET recipient_name=%s, phone=%s, address=%s, notes=%s, status=%s WHERE order_id=%s",
                    (recipient_name, phone, address, notes, status, order_id))
            connection.commit()
            QtWidgets.QMessageBox.information(self, 'Success', '订单信息更新成功')
            self.load_order_info()
        except Exception as e:
            print(f"Error updating order: {e}")
            QtWidgets.QMessageBox.warning(self, 'Error', '更新订单信息失败')
        finally:
            connection.close()

    def delete_order(self):
        order_id = self.order_id_input.text()

        if not order_id:
            QtWidgets.QMessageBox.warning(self, 'Error', '请填写订单ID')
            return

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT product_id, quantity FROM order_items WHERE order_id=%s", (order_id,))
                order_items = cursor.fetchall()

                cursor.execute("DELETE FROM orders WHERE order_id=%s", (order_id,))
                cursor.execute("DELETE FROM order_items WHERE order_id=%s", (order_id,))

                for item in order_items:
                    cursor.execute("UPDATE products SET stock = stock + %s WHERE product_id = %s",
                                   (item['quantity'], item['product_id']))

            connection.commit()
            QtWidgets.QMessageBox.information(self, 'Success', '订单删除成功')
            self.load_order_info()
        except Exception as e:
            print(f"Error deleting order: {e}")
            QtWidgets.QMessageBox.warning(self, 'Error', '删除订单失败')
        finally:
            connection.close()

    def go_back(self):
        from seller_main import SellerMainWindow
        self.main_window.setCentralWidget(SellerMainWindow(self.main_window, self.seller_id))
        self.main_window.resize(800, 600)  # 返回时调整窗口大小