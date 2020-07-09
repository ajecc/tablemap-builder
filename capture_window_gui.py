from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout,\
        QMessageBox, QPushButton, QListWidget, QFrame, QSplitter, QLabel, QTableWidget,\
        QTableWidgetItem, QHeaderView, QFileDialog, QErrorMessage
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from win32gui import EnumWindows

class CaptureWindowGui(QWidget):
    def __init__(self):
        super().__init__()
        self.windows = self.get_all_windows()
        print(self.windows)

    def get_all_windows(self):
        windows_temp = []
        EnumWindows(CaptureWindowGui.enum_windows_proc, windows_temp)
        return windows_temp

    @staticmethod
    def enum_windows_proc(hwnd, top_windows):
        return True


