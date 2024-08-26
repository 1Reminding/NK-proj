# main.py
from PyQt5 import QtWidgets
from main_window import MainWindow
from role_selection import RoleSelectionWindow

if __name__ == "__main__":
    # import sys
    # app = QtWidgets.QApplication(sys.argv)
    # main_window = MainWindow()
    # main_window.show()
    # sys.exit(app.exec_())
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())