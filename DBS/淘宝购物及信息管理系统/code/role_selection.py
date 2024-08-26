# role_selection.py
from PyQt5 import QtWidgets, QtGui, QtCore
from admin_login import AdminLoginWindow
from user_choice import UserChoiceWindow
import os
class RoleSelectionWindow(QtWidgets.QWidget):
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

        self.admin_button = QtWidgets.QPushButton('管理员', self)
        self.user_button = QtWidgets.QPushButton('用户', self)

        # 设置按钮图标
        admin_icon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), 'admin.png'))
        user_icon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), 'user.png'))
        self.admin_button.setIcon(admin_icon)
        self.user_button.setIcon(user_icon)

        # 设置图标大小
        self.admin_button.setIconSize(QtCore.QSize(50, 50))
        self.user_button.setIconSize(QtCore.QSize(50, 50))

        self.admin_button.clicked.connect(self.show_admin_login)
        self.user_button.clicked.connect(self.show_user_choice)
        # 设置按钮样式
        self.admin_button.setStyleSheet("""
                   QPushButton {
                       background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #4CAF50, stop:1 #45a049);
                       color: white;
                       font-size: 32px;
                       border-radius: 30px;
                       padding: 15px 30px;
                       font-family: 'Segoe UI', sans-serif;
                       font-weight: bold;
                       box-shadow: 4px 4px 12px rgba(0, 0, 0, 0.4);
                       border: none;
                   }
                   QPushButton:hover {
                       background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #45a049, stop:1 #4CAF50);
                   }
                   QPushButton:pressed {
                       background-color: #388E3C;
                   }
               """)

        self.user_button.setStyleSheet("""
                   QPushButton {
                       background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #2196F3, stop:1 #1e87e5);
                       color: white;
                       font-size: 32px;
                       border-radius: 30px;
                       padding: 15px 30px;
                       font-family: 'Segoe UI', sans-serif;
                       font-weight: bold;
                       box-shadow: 4px 4px 12px rgba(0, 0, 0, 0.4);
                       border: none;
                   }
                   QPushButton:hover {
                       background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #1e87e5, stop:1 #2196F3);
                   }
                   QPushButton:pressed {
                       background-color: #1976D2;
                   }
               """)
        # 设置按钮大小
        self.admin_button.setFixedSize(300, 100)
        self.user_button.setFixedSize(300, 100)

        # 使用QHBoxLayout使按钮并列排放在屏幕下方
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch(1)  # 左侧留空白
        button_layout.addWidget(self.admin_button)
        button_layout.addSpacerItem(QtWidgets.QSpacerItem(80, 60, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))  # 控制间距
        button_layout.addWidget(self.user_button)
        button_layout.addStretch(1)  # 右侧留空白

        # 使用QVBoxLayout使按钮布局在垂直方向居中
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addStretch(2)  # 上侧留空白
        main_layout.addLayout(button_layout)
        main_layout.addStretch(1)  # 下侧留空白

        self.setLayout(main_layout)

    def set_background_image(self):
        background_image = QtGui.QPixmap(os.path.join(os.path.dirname(__file__), '6.png'))
        self.background_label.setPixmap(background_image)

    def resizeEvent(self, event):
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def show_admin_login(self):
        self.main_window.setCentralWidget(AdminLoginWindow(self.main_window))
        self.main_window.resize(800,600)  # 跳转到管理员登录页面时调整窗口大小

    def show_user_choice(self):
        self.main_window.setCentralWidget(UserChoiceWindow(self.main_window))
        self.main_window.resize(800,600)