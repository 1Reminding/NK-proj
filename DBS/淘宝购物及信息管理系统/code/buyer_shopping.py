from PyQt5 import QtWidgets, QtCore
from db_connection import get_db_connection
import datetime


class BuyerShoppingWindow(QtWidgets.QWidget):
    def __init__(self, main_window, user_id):
        super().__init__()
        self.main_window = main_window
        self.user_id = user_id
        self.init_ui()
        self.load_all_products()  # 加载所有产品信息

    def init_ui(self):
        self.main_window.setWindowTitle('Go Shopping')
        # 调整窗口大小
        self.setFixedSize(1200, 1200)
        self.setStyleSheet("""
                                            QLabel, QLineEdit, QPushButton, QTableWidget {
                                                font-size: 10pt;
                                            }
                                            QTableWidget {
                                                font-size: 8pt;  # 表格内容字体大小
                                            }
                                        """)
        self.product_name_label = QtWidgets.QLabel('产品名称:')
        self.description_label = QtWidgets.QLabel('描述:')
        self.shop_name_label = QtWidgets.QLabel('店铺名称:')
        self.subcategory_name_label = QtWidgets.QLabel('细致分类名称:')

        self.product_name_input = QtWidgets.QLineEdit(self)
        self.description_input = QtWidgets.QLineEdit(self)
        self.shop_name_input = QtWidgets.QLineEdit(self)
        self.subcategory_name_input = QtWidgets.QLineEdit(self)

        self.search_button = QtWidgets.QPushButton('查找', self)
        self.search_button.clicked.connect(self.search_products)

        self.table = QtWidgets.QTableWidget(self)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ['产品ID', '产品名称', '描述', '单品价格', '库存数量', '店铺名称', '细致分类名称'])

        # 增大表格显示区域`
        self.table.setFixedHeight(650)

        self.recipient_name_label = QtWidgets.QLabel('收货姓名:')
        self.phone_label = QtWidgets.QLabel('电话号码:')
        self.address_label = QtWidgets.QLabel('地址:')
        self.product_id_label = QtWidgets.QLabel('商品ID:')
        self.quantity_label = QtWidgets.QLabel('数目:')
        self.notes_label = QtWidgets.QLabel('备注:')

        self.recipient_name_input = QtWidgets.QLineEdit(self)
        self.phone_input = QtWidgets.QLineEdit(self)
        self.address_input = QtWidgets.QLineEdit(self)
        self.product_id_input = QtWidgets.QLineEdit(self)
        self.quantity_input = QtWidgets.QLineEdit(self)
        self.notes_input = QtWidgets.QLineEdit(self)

        self.submit_order_button = QtWidgets.QPushButton('确认并提交订单', self)
        self.submit_order_button.clicked.connect(self.submit_order)

        self.back_button = QtWidgets.QPushButton('返回', self)
        self.back_button.clicked.connect(self.go_back)

        # 设置布局
        layout = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(self.product_name_label, self.product_name_input)
        form_layout.addRow(self.description_label, self.description_input)
        form_layout.addRow(self.shop_name_label, self.shop_name_input)
        form_layout.addRow(self.subcategory_name_label, self.subcategory_name_input)
        layout.addLayout(form_layout)
        layout.addWidget(self.search_button)
        layout.addWidget(self.table)

        order_layout = QtWidgets.QFormLayout()
        order_layout.addRow(self.recipient_name_label, self.recipient_name_input)
        order_layout.addRow(self.phone_label, self.phone_input)
        order_layout.addRow(self.address_label, self.address_input)
        order_layout.addRow(self.product_id_label, self.product_id_input)
        order_layout.addRow(self.quantity_label, self.quantity_input)
        order_layout.addRow(self.notes_label, self.notes_input)
        layout.addLayout(order_layout)
        layout.addWidget(self.submit_order_button)

        # 创建一个水平布局来放置返回按钮，并将其右对齐
        bottom_layout = QtWidgets.QHBoxLayout()
        bottom_layout.addStretch()  # 添加弹性空间
        bottom_layout.addWidget(self.back_button)

        layout.addLayout(bottom_layout)
        self.setLayout(layout)

    def load_all_products(self):
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT p.product_id, p.product_name, p.description, p.price, p.stock, s.shop_name, sc.subcategory_name
                    FROM products p
                    JOIN shops s ON p.shop_id = s.shop_id
                    JOIN subcategories sc ON p.subcategory_id = sc.subcategory_id
                """)
                results = cursor.fetchall()
                self.table.setRowCount(len(results))
                for row_num, row_data in enumerate(results):
                    self.table.setItem(row_num, 0, QtWidgets.QTableWidgetItem(row_data['product_id']))
                    self.table.setItem(row_num, 1, QtWidgets.QTableWidgetItem(row_data['product_name']))
                    self.table.setItem(row_num, 2, QtWidgets.QTableWidgetItem(row_data['description']))
                    self.table.setItem(row_num, 3, QtWidgets.QTableWidgetItem(str(row_data['price'])))
                    self.table.setItem(row_num, 4, QtWidgets.QTableWidgetItem(str(row_data['stock'])))
                    self.table.setItem(row_num, 5, QtWidgets.QTableWidgetItem(row_data['shop_name']))
                    self.table.setItem(row_num, 6, QtWidgets.QTableWidgetItem(row_data['subcategory_name']))
        except Exception as e:
            print(f"Error loading products: {e}")
        finally:
            connection.close()

    def search_products(self):
        product_name = self.product_name_input.text()
        description = self.description_input.text()
        shop_name = self.shop_name_input.text()
        subcategory_name = self.subcategory_name_input.text()

        query = """
                SELECT p.product_id, p.product_name, p.description, p.price, p.stock, s.shop_name, sc.subcategory_name
                FROM products p
                JOIN shops s ON p.shop_id = s.shop_id
                JOIN subcategories sc ON p.subcategory_id = sc.subcategory_id
                WHERE 1=1
                """
        params = []

        if product_name:
            query += " AND p.product_name LIKE %s"
            params.append(f'%{product_name}%')
        if description:
            query += " AND p.description LIKE %s"
            params.append(f'%{description}%')
        if shop_name:
            query += " AND s.shop_name LIKE %s"
            params.append(f'%{shop_name}%')
        if subcategory_name:
            query += " AND sc.subcategory_name LIKE %s"
            params.append(f'%{subcategory_name}%')

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute(query, tuple(params))
                results = cursor.fetchall()
                self.table.setRowCount(len(results))
                for row_num, row_data in enumerate(results):
                    self.table.setItem(row_num, 0, QtWidgets.QTableWidgetItem(row_data['product_id']))
                    self.table.setItem(row_num, 1, QtWidgets.QTableWidgetItem(row_data['product_name']))
                    self.table.setItem(row_num, 2, QtWidgets.QTableWidgetItem(row_data['description']))
                    self.table.setItem(row_num, 3, QtWidgets.QTableWidgetItem(str(row_data['price'])))
                    self.table.setItem(row_num, 4, QtWidgets.QTableWidgetItem(str(row_data['stock'])))
                    self.table.setItem(row_num, 5, QtWidgets.QTableWidgetItem(row_data['shop_name']))
                    self.table.setItem(row_num, 6, QtWidgets.QTableWidgetItem(row_data['subcategory_name']))
                if not results:
                    QtWidgets.QMessageBox.warning(self, 'Error', '未找到符合条件的产品')
        except Exception as e:
            print(f"Error searching products: {e}")
        finally:
            connection.close()

    def submit_order(self):
        recipient_name = self.recipient_name_input.text()
        phone = self.phone_input.text()
        address = self.address_input.text()
        product_id = self.product_id_input.text()
        quantity = self.quantity_input.text()
        notes = self.notes_input.text()

        if not recipient_name or not phone or not address:
            QtWidgets.QMessageBox.warning(self, 'Error', '请填写收货姓名、电话号码和地址')
            return

        if not product_id or not quantity:
            QtWidgets.QMessageBox.warning(self, 'Error', '请填写商品ID和数量')
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
                    "INSERT INTO orders (order_id, buyer_id, order_date, total_amount, status, recipient_name, address, phone, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (new_order_id, self.user_id, order_date, subtotal, '待处理', recipient_name, address, phone, notes))

                cursor.execute(
                    "INSERT INTO order_items (order_item_id, order_id, product_id, quantity, subtotal, product_name) VALUES (%s, %s, %s, %s, %s, %s)",
                    (new_order_item_id, new_order_id, product_id, quantity, subtotal, product_name))

                cursor.execute("UPDATE products SET stock = stock - %s WHERE product_id = %s", (quantity, product_id))

            connection.commit()
            QtWidgets.QMessageBox.information(self, 'Success', '订单提交成功')
        except Exception as e:
            print(f"Error submitting order: {e}")
            QtWidgets.QMessageBox.warning(self, 'Error', '提交订单失败')
        finally:
            connection.close()

    def go_back(self):
        from buyer_main import BuyerMainWindow
        self.main_window.setCentralWidget(BuyerMainWindow(self.main_window, self.user_id))