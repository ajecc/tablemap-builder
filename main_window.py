from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout,\
        QMessageBox, QPushButton, QListWidget, QFrame, QSplitter, QLabel, QTableWidget,\
        QTableWidgetItem, QHeaderView, QFileDialog, QErrorMessage
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from tablemap_file_manager import TablemapFileManager
import os


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.tablemap_file_manager = TablemapFileManager()
        self.init_window()
        self.init_layouts()
        self.init_tablemap_file_manager_buttons()
        self.show()

    def init_window(self):
        self.setWindowTitle('No tablemap loaded')

    def init_layouts(self):
        self.main_layout = QVBoxLayout(self)
        self.tablemap_file_manager_buttons_layout = QHBoxLayout()
        self.main_layout.addLayout(self.tablemap_file_manager_buttons_layout)

    def init_tablemap_file_manager_buttons(self):
        self.new_tablemap_file_button = QPushButton('New') 
        self.load_tablemap_file_button = QPushButton('Load') 
        self.save_tablemap_file_button = QPushButton('Save') 
        self.capture_window_button = QPushButton('Capture')

        self.save_tablemap_file_button.setEnabled(False)

        self.new_tablemap_file_button.clicked.connect(self.new_tablemap_file)
        self.load_tablemap_file_button.clicked.connect(self.load_tablemap_file)
        self.save_tablemap_file_button.clicked.connect(self.save_tablemap_file)
        self.capture_window_button.clicked.connect(self.capture_window)

        self.tablemap_file_manager_buttons_layout.addWidget(self.new_tablemap_file_button)
        self.tablemap_file_manager_buttons_layout.addWidget(self.load_tablemap_file_button)
        self.tablemap_file_manager_buttons_layout.addWidget(self.save_tablemap_file_button)

    def new_tablemap_file(self):
        q_file_dialog = QFileDialog()
        q_file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        dir = q_file_dialog.getSaveFileName(self, 'Select Directory', 'tablemap_dir_name', 'Directory')[0] 
        if os.path.isdir(dir) or os.path.isfile(dir):
            self.display_error('A directory/file with that name already exists! Can\'t store a tablemap in it')
        os.mkdir(dir)
        if self.tablemap_file_manager.can_save_tablemap():
            self.tablemap_file_manager.save_tablemap()
        self.tablemap_file_manager.new_tablemap(dir, dir.split('/')[-1])
        self.save_tablemap_file_button.setEnabled(True)
        print(dir.split('/')[-1])

    def load_tablemap_file(self):
        dir = QFileDialog.getExistingDirectory() 
        if self.tablemap_file_manager.can_save_tablemap():
            self.tablemap_file_manager.save_tablemap()
        try:
            self.tablemap_file_manager.load_tablemap(dir, dir.split('/')[-1])
        except Exception as e:
            print(e)
            self.display_error('Could not load the tablemap. Make sure the directory is valid.')
        self.save_tablemap_file_button.setEnabled(True)

    def save_tablemap_file(self):
        pass
    
    def capture_window(self):
        pass
    
    def display_error(self, text):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(text)
        error_dialog.exec_()
