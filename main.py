import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow


if __name__ == '__main__':
    print('Starting Tablemap Builder')
    app = QApplication(sys.argv)
    gui = MainWindow()
    sys.exit(app.exec_())
