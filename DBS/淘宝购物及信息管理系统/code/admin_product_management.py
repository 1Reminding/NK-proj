# admin_product_management.py
from PyQt5 import QtWidgets, QtCore
from db_connection import get_db_connection

class AdminProductManagementWindow(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
        self.load_all_products()  # 在窗口初始化时加载所有产品数据

    def init_ui(self):
        self.setFixedSize(1300, 800)  # 设置窗口大小
        self.main_window.setWindowTitle('产品信息管理')

        # 设置全局样式表，统一字体大小为
        self.setStyleSheet("""
                            QLabel, QLineEdit, QPushButton, QTableWidget {
                                font-size: 10pt;
                            }
                            QTableWidget {
                                font-size: 8pt;  # 表格内容字体大小
                            }
                        """)

        self.product_id_label = QtWidgets.QLabel('产品ID:')
        self.product_name_label = QtWidgets.QLabel('产品名:')
        self.description_label = QtWidgets.QLabel('描述:')
        self.price_label = QtWidgets.QLabel('价格:')
        self.stock_label = QtWidgets.QLabel('库存:')
        self.category_id_label = QtWidgets.QLabel('分类ID:')
        self.shop_id_label = QtWidgets.QLabel('店铺ID:')
        self.subcategory_id_label = QtWidgets.QLabel('子分类ID:')

        self.product_id_input = QtWidgets.QLineEdit(self)
        self.product_name_input = QtWidgets.QLineEdit(self)
        self.description_input = QtWidgets.QLineEdit(self)
        self.price_input = QtWidgets.QLineEdit(self)
        self.stock_input = QtWidgets.QLineEdit(self)
        self.category_id_input = QtWidgets.QLineEdit(self)
        self.shop_id_input = QtWidgets.QLineEdit(self)
        self.subcategory_id_input = QtWidgets.QLineEdit(self)

        self.search_button = QtWidgets.QPushButton('查找', self)
        self.add_button = QtWidgets.QPushButton('增加', self)
        self.delete_button = QtWidgets.QPushButton('删除', self)
        self.update_button = QtWidgets.QPushButton('修改', self)
        self.confirm_button = QtWidgets.QPushButton('确认', self)
        self.back_button = QtWidgets.QPushButton('返回', self)

        self.search_button.clicked.connect(self.search_product)
        self.add_button.clicked.connect(self.add_product)
        self.delete_button.clicked.connect(self.delete_product)
        self.update_button.clicked.connect(self.update_product)
        self.confirm_button.clicked.connect(self.confirm_changes)
        self.back_button.clicked.connect(self.go_back)

        self.table = QtWidgets.QTableWidget(self)
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(['产品ID', '产品名', '描述', '价格', '库存', '分类ID', '店铺ID', '子分类ID'])

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.product_id_label, 0, 0)
        layout.addWidget(self.product_id_input, 0, 1)
        layout.addWidget(self.product_name_label, 1, 0)
        layout.addWidget(self.product_name_input, 1, 1)
        layout.addWidget(self.description_label, 2, 0)
        layout.addWidget(self.description_input, 2, 1)
        layout.addWidget(self.price_label, 3, 0)
        layout.addWidget(self.price_input, 3, 1)
        layout.addWidget(self.stock_label, 4, 0)
        layout.addWidget(self.stock_input, 4, 1)
        layout.addWidget(self.category_id_label, 5, 0)
        layout.addWidget(self.category_id_input, 5, 1)
        layout.addWidget(self.shop_id_label, 6, 0)
        layout.addWidget(self.shop_id_input, 6, 1)
        layout.addWidget(self.subcategory_id_label, 7, 0)
        layout.addWidget(self.subcategory_id_input, 7, 1)

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

    def load_all_products(self):
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT product_id, product_name, description, price, stock, category_id, shop_id, subcategory_id FROM products")
                results = cursor.fetchall()
                self.table.setRowCount(len(results))
                for row_num, row_data in enumerate(results):
                    self.table.setItem(row_num, 0, QtWidgets.QTableWidgetItem(row_data['product_id']))
                    self.table.setItem(row_num, 1, QtWidgets.QTableWidgetItem(row_data['product_name']))
                    self.table.setItem(row_num, 2, QtWidgets.QTableWidgetItem(row_data['description']))
                    self.table.setItem(row_num, 3, QtWidgets.QTableWidgetItem(str(row_data['price'])))
                    self.table.setItem(row_num, 4, QtWidgets.QTableWidgetItem(str(row_data['stock'])))
                    self.table.setItem(row_num, 5, QtWidgets.QTableWidgetItem(row_data['category_id']))
                    self.table.setItem(row_num, 6, QtWidgets.QTableWidgetItem(row_data['shop_id']))
                    self.table.setItem(row_num, 7, QtWidgets.QTableWidgetItem(row_data['subcategory_id']))
        except Exception as e:
            print(f"Error loading products: {e}")
        finally:
            connection.close()

    def search_product(self):
        product_id = self.product_id_input.text()
        product_name = self.product_name_input.text()
        description = self.description_input.text()
        price = self.price_input.text()
        stock = self.stock_input.text()
        category_id = self.category_id_input.text()
        shop_id = self.shop_id_input.text()
        subcategory_id = self.subcategory_id_input.text()

        query = "SELECT product_id, product_name, description, price, stock, category_id, shop_id, subcategory_id FROM products WHERE 1=1"
        params = []

        if product_id:
            query += " AND product_id=%s"
            params.append(product_id)
        if product_name:
            query += " AND product_name=%s"
            params.append(product_name)
        if description:
            query += " AND description=%s"
            params.append(description)
        if price:
            query += " AND price=%s"
            params.append(price)
        if stock:
            query += " AND stock=%s"
            params.append(stock)
        if category_id:
            query += " AND category_id=%s"
            params.append(category_id)
        if shop_id:
            query += " AND shop_id=%s"
            params.append(shop_id)
        if subcategory_id:
            query += " AND subcategory_id=%s"
            params.append(subcategory_id)

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
                    self.table.setItem(row_num, 5, QtWidgets.QTableWidgetItem(row_data['category_id']))
                    self.table.setItem(row_num, 6, QtWidgets.QTableWidgetItem(row_data['shop_id']))
                    self.table.setItem(row_num, 7, QtWidgets.QTableWidgetItem(row_data['subcategory_id']))
                if not results:
                    QtWidgets.QMessageBox.warning(self, 'Error', 'Product not found')
        except Exception as e:
            print(f"Error searching product: {e}")
        finally:
            connection.close()

    def validate_category(self, category_id, subcategory_id):
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT category_id FROM categories WHERE category_id=%s", (category_id,))
                if not cursor.fetchone():
                    return False

                cursor.execute("SELECT subcategory_id FROM subcategories WHERE subcategory_id=%s", (subcategory_id,))
                if not cursor.fetchone():
                    return False
            return True
        except Exception as e:
            print(f"Error validating category: {e}")
            return False
        finally:
            connection.close()

    def add_product(self):
        product_id = self.product_id_input.text()
        product_name = self.product_name_input.text()
        description = self.description_input.text() or None
        price = self.price_input.text() or None
        stock = self.stock_input.text() or None
        category_id = self.category_id_input.text() or None
        shop_id = self.shop_id_input.text() or None
        subcategory_id = self.subcategory_id_input.text() or None

        if not product_id:
            QtWidgets.QMessageBox.warning(self, 'Error', '缺失产品ID！')
            return

        if not product_name:
            QtWidgets.QMessageBox.warning(self, 'Error', '缺失产品名称！')
            return

        if price is not None and float(price) < 0:
            QtWidgets.QMessageBox.warning(self, 'Error', '请检查信息是否正确！')
            return

        if stock is not None and int(stock) < 0:
            QtWidgets.QMessageBox.warning(self, 'Error', '请检查信息是否正确！')
            return

        if not self.validate_category(category_id, subcategory_id):
            QtWidgets.QMessageBox.warning(self, 'Error', '分类不存在！')
            return
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT product_id FROM products WHERE product_id=%s", (product_id,))
                if cursor.fetchone():
                    QtWidgets.QMessageBox.warning(self, 'Error', '产品ID重复！请重新输入。')
                    return

                sql = ("INSERT INTO products (product_id, product_name, description, price, stock, category_id,"
                       " shop_id, subcategory_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
                cursor.execute(sql, (product_id, product_name, description, price, stock, category_id, shop_id,
                                     subcategory_id))
            connection.commit()
            QtWidgets.QMessageBox.information(self, 'Success', 'Product added successfully')
        except Exception as e:
            print(f"Error adding product: {e}")
            QtWidgets.QMessageBox.warning(self, 'Error', 'Failed to add product')
        finally:
            connection.close()

    def delete_product(self):
        product_id = self.product_id_input.text()
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = "DELETE FROM products WHERE product_id=%s"
                cursor.execute(sql, (product_id,))
            connection.commit()
            QtWidgets.QMessageBox.information(self, 'Success', 'Product deleted successfully')
        except Exception as e:
            print(f"Error deleting product: {e}")
            QtWidgets.QMessageBox.warning(self, 'Error', 'Failed to delete product')
        finally:
            connection.close()

    def update_product(self):
        product_id = self.product_id_input.text()
        product_name = self.product_name_input.text() or None
        description = self.description_input.text() or None
        price = self.price_input.text() or None
        stock = self.stock_input.text() or None
        category_id = self.category_id_input.text() or None
        shop_id = self.shop_id_input.text() or None
        subcategory_id = self.subcategory_id_input.text() or None

        if not product_id:
            QtWidgets.QMessageBox.warning(self, 'Error', '请输入产品ID')
            return

        if price is not None and float(price) < 0:
            QtWidgets.QMessageBox.warning(self, 'Error', '请检查信息是否正确！')
            return

        if stock is not None and int(stock) < 0:
            QtWidgets.QMessageBox.warning(self, 'Error', '请检查信息是否正确！')
            return

        if not self.validate_category(category_id, subcategory_id):
            QtWidgets.QMessageBox.warning(self, 'Error', '分类不存在！')
            return

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = "UPDATE products SET "
                updates = []
                params = []
                if product_name:
                    updates.append("product_name=%s")
                    params.append(product_name)
                if description:
                    updates.append("description=%s")
                    params.append(description)
                if price:
                    updates.append("price=%s")
                    params.append(price)
                if stock:
                    updates.append("stock=%s")
                    params.append(stock)
                if category_id:
                    updates.append("category_id=%s")
                    params.append(category_id)
                if shop_id:
                    updates.append("shop_id=%s")
                    params.append(shop_id)
                if subcategory_id:
                    updates.append("subcategory_id=%s")
                    params.append(subcategory_id)
                sql += ", ".join(updates) + " WHERE product_id=%s"
                params.append(product_id)
                cursor.execute(sql, params)
            connection.commit()
            QtWidgets.QMessageBox.information(self, 'Success', 'Product updated successfully')
        except Exception as e:
            print(f"Error updating product: {e}")
            QtWidgets.QMessageBox.warning(self, 'Error', 'Failed to update product')
        finally:
            connection.close()

    def confirm_changes(self):
        QtWidgets.QMessageBox.information(self, 'Info', 'Changes confirmed')

    def go_back(self):
        from admin_main import AdminMainWindow
        self.main_window.setCentralWidget(AdminMainWindow(self.main_window))
