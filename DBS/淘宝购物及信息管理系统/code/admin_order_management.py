from PyQt5 import QtWidgets
from db_connection import get_db_connection
import datetime

class AdminOrderManagementWindow(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
        self.load_all_orders()  # 加载所有订单信息

    def init_ui(self):
        self.main_window.setWindowTitle('订单信息管理')
        self.setFixedSize(1200, 800)  # 设置窗口大小

        # 设置全局样式表，统一字体大小为
        self.setStyleSheet("""
                                    QLabel, QLineEdit, QPushButton, QTableWidget {
                                        font-size: 10pt;
                                    }
                                    QTableWidget {
                                        font-size: 8pt;  # 表格内容字体大小
                                    }
                                """)

        self.order_id_label = QtWidgets.QLabel('订单ID:')
        self.buyer_id_label = QtWidgets.QLabel('买家ID:')
        self.product_id_label = QtWidgets.QLabel('产品ID:')
        self.quantity_label = QtWidgets.QLabel('数量:')
        self.product_name_label = QtWidgets.QLabel('产品名称:')
        self.subtotal_label = QtWidgets.QLabel('小计:')
        self.shop_id_label = QtWidgets.QLabel('店铺ID:')
        self.status_label = QtWidgets.QLabel('状态:')

        self.order_id_input = QtWidgets.QLineEdit(self)
        self.buyer_id_input = QtWidgets.QLineEdit(self)
        self.product_id_input = QtWidgets.QLineEdit(self)
        self.quantity_input = QtWidgets.QLineEdit(self)
        self.product_name_input = QtWidgets.QLineEdit(self)
        self.product_name_input.setReadOnly(True)
        self.subtotal_input = QtWidgets.QLineEdit(self)
        self.subtotal_input.setReadOnly(True)
        self.shop_id_input = QtWidgets.QLineEdit(self)
        self.shop_id_input.setReadOnly(True)
        self.status_input = QtWidgets.QLineEdit(self)

        self.search_button = QtWidgets.QPushButton('查找', self)
        self.add_button = QtWidgets.QPushButton('增加', self)
        self.delete_button = QtWidgets.QPushButton('删除', self)
        self.update_button = QtWidgets.QPushButton('修改', self)
        self.confirm_button = QtWidgets.QPushButton('确认', self)
        self.back_button = QtWidgets.QPushButton('返回', self)

        self.search_button.clicked.connect(self.search_order)
        self.add_button.clicked.connect(self.add_order)
        self.delete_button.clicked.connect(self.delete_order)
        self.update_button.clicked.connect(self.update_order)
        self.confirm_button.clicked.connect(self.confirm_changes)
        self.back_button.clicked.connect(self.go_back)

        self.table = QtWidgets.QTableWidget(self)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['订单ID', '买家ID', '产品ID', '数量', '小计', '店铺ID', '状态'])

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.order_id_label, 0, 0)
        layout.addWidget(self.order_id_input, 0, 1)
        layout.addWidget(self.buyer_id_label, 1, 0)
        layout.addWidget(self.buyer_id_input, 1, 1)
        layout.addWidget(self.product_id_label, 2, 0)
        layout.addWidget(self.product_id_input, 2, 1)
        layout.addWidget(self.quantity_label, 3, 0)
        layout.addWidget(self.quantity_input, 3, 1)
        layout.addWidget(self.product_name_label, 4, 0)
        layout.addWidget(self.product_name_input, 4, 1)
        layout.addWidget(self.subtotal_label, 5, 0)
        layout.addWidget(self.subtotal_input, 5, 1)
        layout.addWidget(self.shop_id_label, 6, 0)
        layout.addWidget(self.shop_id_input, 6, 1)
        layout.addWidget(self.status_label, 7, 0)
        layout.addWidget(self.status_input, 7, 1)

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

    def load_all_orders(self):
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT orders.order_id, orders.buyer_id, order_items.product_id, order_items.quantity, 
                           order_items.subtotal, products.shop_id, orders.status 
                    FROM orders 
                    JOIN order_items ON orders.order_id = order_items.order_id 
                    JOIN products ON order_items.product_id = products.product_id
                """)
                results = cursor.fetchall()
                self.table.setRowCount(len(results))
                for row_num, row_data in enumerate(results):
                    self.table.setItem(row_num, 0, QtWidgets.QTableWidgetItem(row_data['order_id']))
                    self.table.setItem(row_num, 1, QtWidgets.QTableWidgetItem(row_data['buyer_id']))
                    self.table.setItem(row_num, 2, QtWidgets.QTableWidgetItem(row_data['product_id']))
                    self.table.setItem(row_num, 3, QtWidgets.QTableWidgetItem(str(row_data['quantity'])))
                    self.table.setItem(row_num, 4, QtWidgets.QTableWidgetItem(str(row_data['subtotal'])))
                    self.table.setItem(row_num, 5, QtWidgets.QTableWidgetItem(row_data['shop_id']))
                    self.table.setItem(row_num, 6, QtWidgets.QTableWidgetItem(row_data['status']))
        except Exception as e:
            print(f"Error loading orders: {e}")
        finally:
            connection.close()

    def search_order(self):
        order_id = self.order_id_input.text()
        buyer_id = self.buyer_id_input.text()
        product_id = self.product_id_input.text()
        quantity = self.quantity_input.text()
        product_name = self.product_name_input.text()
        subtotal = self.subtotal_input.text()
        shop_id = self.shop_id_input.text()
        status = self.status_input.text()

        query = """
        SELECT orders.order_id, orders.buyer_id, order_items.product_id, order_items.quantity, order_items.subtotal, products.shop_id, orders.status 
        FROM orders 
        JOIN order_items ON orders.order_id = order_items.order_id 
        JOIN products ON order_items.product_id = products.product_id 
        WHERE 1=1
        """
        params = []

        if order_id:
            query += " AND orders.order_id=%s"
            params.append(order_id)
        if buyer_id:
            query += " AND orders.buyer_id=%s"
            params.append(buyer_id)
        if product_id:
            query += " AND order_items.product_id=%s"
            params.append(product_id)
        if quantity:
            query += " AND order_items.quantity=%s"
            params.append(quantity)
        if product_name:
            query += " AND products.product_name=%s"
            params.append(product_name)
        if subtotal:
            query += " AND order_items.subtotal=%s"
            params.append(subtotal)
        if shop_id:
            query += " AND products.shop_id=%s"
            params.append(shop_id)
        if status:
            query += " AND orders.status=%s"
            params.append(status)

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute(query, tuple(params))
                results = cursor.fetchall()
                self.table.setRowCount(len(results))
                for row_num, row_data in enumerate(results):
                    self.table.setItem(row_num, 0, QtWidgets.QTableWidgetItem(row_data['order_id']))
                    self.table.setItem(row_num, 1, QtWidgets.QTableWidgetItem(row_data['buyer_id']))
                    self.table.setItem(row_num, 2, QtWidgets.QTableWidgetItem(row_data['product_id']))
                    self.table.setItem(row_num, 3, QtWidgets.QTableWidgetItem(str(row_data['quantity'])))
                    self.table.setItem(row_num, 4, QtWidgets.QTableWidgetItem(str(row_data['subtotal'])))
                    self.table.setItem(row_num, 5, QtWidgets.QTableWidgetItem(row_data['shop_id']))
                    self.table.setItem(row_num, 6, QtWidgets.QTableWidgetItem(row_data['status']))
                if not results:
                    QtWidgets.QMessageBox.warning(self, 'Error', 'Order not found')
        except Exception as e:
            print(f"Error searching order: {e}")
        finally:
            connection.close()

    def add_order(self):
        buyer_id = self.buyer_id_input.text()
        product_id = self.product_id_input.text()
        quantity = self.quantity_input.text()

        if not product_id:
            QtWidgets.QMessageBox.warning(self, 'Error', '缺失产品ID！')
            return

        if not quantity:
            QtWidgets.QMessageBox.warning(self, 'Error', '缺失数量！')
            return

        if int(quantity) <= 0:
            QtWidgets.QMessageBox.warning(self, 'Error', '数量必须大于0！')
            return

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                # 生成订单ID
                cursor.execute("SELECT MAX(order_id) FROM orders")
                max_order_id = cursor.fetchone()['MAX(order_id)']
                new_order_id = f"O{int(max_order_id[1:]) + 1:04d}"

                # 生成订单明细ID
                cursor.execute("SELECT MAX(order_item_id) FROM order_items")
                max_order_item_id = cursor.fetchone()['MAX(order_item_id)']
                new_order_item_id = f"OI{int(max_order_item_id[2:]) + 1:04d}"

                # 获取产品信息
                cursor.execute("SELECT product_name, price, stock, shop_id FROM products WHERE product_id=%s", (product_id,))
                product_info = cursor.fetchone()
                if not product_info:
                    QtWidgets.QMessageBox.warning(self, 'Error', '产品不存在！')
                    return

                product_name = product_info['product_name']
                price = product_info['price']
                stock = product_info['stock']
                shop_id = product_info['shop_id']

                if int(quantity) > stock:
                    QtWidgets.QMessageBox.warning(self, 'Error', '库存不足！')
                    return

                subtotal = float(price) * int(quantity)
                order_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # 插入订单数据
                cursor.execute(
                    "INSERT INTO orders (order_id, buyer_id, order_date, total_amount, status) VALUES (%s, %s, %s, %s, %s)",
                    (new_order_id, buyer_id, order_date, subtotal, '待处理')
                )

                # 插入订单明细数据
                cursor.execute(
                    "INSERT INTO order_items (order_item_id, order_id, product_id, quantity, subtotal, product_name) VALUES (%s, %s, %s, %s, %s, %s)",
                    (new_order_item_id, new_order_id, product_id, quantity, subtotal, product_name)
                )

                # 更新产品库存
                cursor.execute(
                    "UPDATE products SET stock=stock-%s WHERE product_id=%s",
                    (quantity, product_id)
                )

            connection.commit()
            QtWidgets.QMessageBox.information(self, 'Success', 'Order added successfully')
        except Exception as e:
            print(f"Error adding order: {e}")
            QtWidgets.QMessageBox.warning(self, 'Error', 'Failed to add order')
        finally:
            connection.close()

    def delete_order(self):
        order_id = self.order_id_input.text()
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                # 开启事务
                connection.begin()
                # 获取订单明细中的产品信息
                cursor.execute("SELECT product_id, quantity FROM order_items WHERE order_id=%s", (order_id,))
                order_items = cursor.fetchall()

                # 删除与订单相关的所有信息
                cursor.execute("DELETE FROM order_items WHERE order_id=%s", (order_id,))
                cursor.execute("DELETE FROM orders WHERE order_id=%s", (order_id,))

                # 恢复产品库存
                for item in order_items:
                    cursor.execute(
                        "UPDATE products SET stock=stock+%s WHERE product_id=%s",
                        (item['quantity'], item['product_id'])
                    )

                # 提交事务
                connection.commit()
                QtWidgets.QMessageBox.information(self, 'Success', 'Order deleted successfully')
        except Exception as e:
            connection.rollback()
            print(f"Error deleting order: {e}")
            QtWidgets.QMessageBox.warning(self, 'Error', 'Failed to delete order')
        finally:
            connection.close()

    def update_order(self):
        order_id = self.order_id_input.text()
        buyer_id = self.buyer_id_input.text()
        product_id = self.product_id_input.text()
        quantity = self.quantity_input.text()
        status = self.status_input.text()

        if quantity and int(quantity) <= 0:
            QtWidgets.QMessageBox.warning(self, 'Error', '数量必须大于0！')
            return

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                # 获取原始订单明细信息
                cursor.execute("SELECT product_id, quantity, subtotal FROM order_items WHERE order_id=%s", (order_id,))
                original_order_item = cursor.fetchone()
                original_quantity = original_order_item['quantity']

                # 更新订单数据
                sql = "UPDATE orders SET "
                updates = []
                params = []
                if buyer_id:
                    updates.append("buyer_id=%s")
                    params.append(buyer_id)
                if status:
                    updates.append("status=%s")
                    params.append(status)
                sql += ", ".join(updates) + " WHERE order_id=%s"
                params.append(order_id)
                cursor.execute(sql, params)

                # 更新订单明细数据
                if product_id or quantity:
                    sql = "UPDATE order_items SET "
                    updates = []
                    params = []
                    if product_id:
                        updates.append("product_id=%s")
                        params.append(product_id)
                    if quantity:
                        updates.append("quantity=%s")
                        params.append(quantity)
                    sql += ", ".join(updates) + " WHERE order_id=%s"
                    params.append(order_id)
                    cursor.execute(sql, params)

                    # 更新小计和库存
                    if quantity:
                        new_subtotal = original_order_item['subtotal'] / original_quantity * int(quantity)
                        cursor.execute(
                            "UPDATE order_items SET subtotal=%s WHERE order_id=%s AND product_id=%s",
                            (new_subtotal, order_id, product_id if product_id else original_order_item['product_id'])
                        )
                        cursor.execute(
                            "UPDATE products SET stock=stock+(%s-%s) WHERE product_id=%s",
                            (original_quantity, int(quantity),
                             product_id if product_id else original_order_item['product_id'])
                        )

                # 更新总金额
                cursor.execute("SELECT SUM(subtotal) AS total_amount FROM order_items WHERE order_id=%s", (order_id,))
                new_total_amount = cursor.fetchone()['total_amount']
                cursor.execute("UPDATE orders SET total_amount=%s WHERE order_id=%s", (new_total_amount, order_id))

            connection.commit()
            QtWidgets.QMessageBox.information(self, 'Success', 'Order updated successfully')
        except Exception as e:
            connection.rollback()
            print(f"Error updating order: {e}")
            QtWidgets.QMessageBox.warning(self, 'Error', 'Failed to update order')
        finally:
            connection.close()

    def confirm_changes(self):
        QtWidgets.QMessageBox.information(self, 'Info', 'Changes confirmed')

    def go_back(self):
        from admin_main import AdminMainWindow
        self.main_window.setCentralWidget(AdminMainWindow(self.main_window))
