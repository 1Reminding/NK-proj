from PyQt5 import QtWidgets,QtGui
import os
class UserSelectionWindow(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        # 设置背景图片
        self.background_label = QtWidgets.QLabel(self)
        self.set_background_image()
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label.setScaledContents(True)
        self.background_label.lower()  # 将背景图片置于最底层

        self.main_window.setWindowTitle('身份选择')
        self.buyer_button = QtWidgets.QPushButton('Buyer', self)
        self.seller_button = QtWidgets.QPushButton('Seller', self)
        self.back_button = QtWidgets.QPushButton('Back', self)

        self.buyer_button.clicked.connect(self.go_to_buyer_choice)
        self.seller_button.clicked.connect(self.go_to_seller_choice)
        self.back_button.clicked.connect(self.go_back)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.buyer_button)
        layout.addWidget(self.seller_button)
        layout.addWidget(self.back_button)
        self.setLayout(layout)

    def go_to_buyer_choice(self):
        from user_choice import UserChoiceWindow
        self.main_window.setCentralWidget(UserChoiceWindow(self.main_window, 'buyer'))

    def go_to_seller_choice(self):
        from user_choice import UserChoiceWindow
        self.main_window.setCentralWidget(UserChoiceWindow(self.main_window, 'seller'))

    def set_background_image(self):
        background_image = QtGui.QPixmap(os.path.join(os.path.dirname(__file__), '3.png'))
        self.background_label.setPixmap(background_image)

    def resizeEvent(self, event):
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def go_back(self):
        from role_selection import RoleSelectionWindow
        self.main_window.setCentralWidget(RoleSelectionWindow(self.main_window))
