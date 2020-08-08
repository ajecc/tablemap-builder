from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout,\
        QMessageBox, QPushButton, QListWidget, QFrame, QSplitter, QLabel, QTableWidget,\
        QTableWidgetItem, QHeaderView, QFileDialog, QErrorMessage
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from tablemap_file_manager import TablemapFileManager
from tablemap import Tablemap
from capture_window_gui import CaptureWindowGui
import os


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.capture_window_gui = None
        self.tablemap_file_manager = TablemapFileManager()
        self.init_window()
        self.init_layouts()
        self.init_tablemap_file_manager_buttons()
        self.selected_tablemap_area = None
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
        self.tablemap_file_manager_buttons_layout.addWidget(self.capture_window_button)

    def init_tablemap_builder_buttons(self):
        self.tablemap_builder_layout = QVBoxLayout()
        self.tablemap_area_labels = QListWidget()
        for tablemap_area in self.tablemap_file_manager.tablemap.tablemap_areas:
            self.tablemap_area_labels.addItem(tablemap_area.label)
        self.tablemap_area_labels.itemClicked.connect(self.tablemap_area_selected_event)
        self.tablemap_builder_layout.addWidget(self.tablemap_area_labels)

        self.label_line_edit_label = QLabel()
        self.label_line_edit_label.setText('label')
        self.label_line_edit = QLineEdit()
        self.label_line_edit_layout = QHBoxLayout()
        self.label_line_edit_layout.addWidget(self.label_line_edit_label)
        self.label_line_edit_layout.addWidget(self.label_line_edit)
        self.tablemap_builder_layout.addLayout(self.label_line_edit_layout)

        self.bool_sym_line_edit_label = QLabel()
        self.bool_sym_line_edit_label.setText('bool_sym?')
        self.bool_sym_line_edit = QLineEdit()
        self.bool_sym_line_edit_layout = QHBoxLayout()
        self.bool_sym_line_edit_layout.addWidget(self.bool_sym_line_edit_label)
        self.bool_sym_line_edit_layout.addWidget(self.bool_sym_line_edit)
        self.tablemap_builder_layout.addLayout(self.bool_sym_line_edit_layout)

        self.add_button = QPushButton('Add') 
        self.remove_button = QPushButton('Remove')
        self.remove_button.setEnabled(False)
        self.add_button.clicked.connect(self.add_tablemap_area)
        self.remove_button.clicked.connect(self.remove_tablemap_area)
        self.tablemap_builder_layout.addWidget(self.add_button)
        self.tablemap_builder_layout.addWidget(self.remove_button)

        self.main_layout.addLayout(self.tablemap_builder_layout)

    def tablemap_exists_event(self, dir):
        self.save_tablemap_file_button.setEnabled(True)
        self.load_tablemap_file_button.setEnabled(False)
        self.new_tablemap_file_button.setEnabled(False)
        self.init_tablemap_builder_buttons()
        self.setWindowTitle(dir.split('/')[-1])
        if self.capture_window_gui is not None:
            self.capture_window_gui.tablemap = self.tablemap_file_manager.tablemap
            self.capture_window_gui.activateWindow()

    def new_tablemap_file(self):
        q_file_dialog = QFileDialog()
        q_file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        dir = q_file_dialog.getSaveFileName(self, 'Select Directory', 'tablemap_dir_name', 'Directory')[0] 
        if os.path.isdir(dir) or os.path.isfile(dir):
            self.display_error('A directory/file with that name already exists! Can\'t store a tablemap in it')
            return
        try:
            os.mkdir(dir)
        except Exception as e:
            print(e)
            self.display_error('Could not load the tablemap. Make sure the directory is valid.')
            return
        if self.tablemap_file_manager.can_save_tablemap():
            self.tablemap_file_manager.save_tablemap()
        self.tablemap_file_manager.new_tablemap(dir, dir.split('/')[-1])
        self.tablemap_exists_event(dir)

    def load_tablemap_file(self):
        dir = QFileDialog.getExistingDirectory() 
        if self.tablemap_file_manager.can_save_tablemap():
            self.tablemap_file_manager.save_tablemap()
        try:
            self.tablemap_file_manager.load_tablemap(dir, dir.split('/')[-1])
        except Exception as e:
            print(e)
            self.display_error('Could not load the tablemap. Make sure the directory is valid.')
            return
        self.tablemap_exists_event(dir)

    def tablemap_area_selected_event(self, item):
        label = item.text()
        for tablemap_area in self.tablemap_file_manager.tablemap.tablemap_areas:
            if tablemap_area.label == label:
                self.selected_tablemap_area = tablemap_area
                break
        self.remove_button.setEnabled(True)
        if self.capture_window_gui is not None:
            self.capture_window_gui.tablemap_area_selected(self.selected_tablemap_area)
            self.capture_window_gui.activateWindow()

    def add_tablemap_area(self):
        label = self.label_line_edit.text()
        is_bool_symbol = self.bool_sym_line_edit.text()
        if len(label) == 0 or (is_bool_symbol != '0' and is_bool_symbol != '1'):
            self.display_error('Error: label can\'t be empty and bool_sym can only be 0 or 1')
            return
        if is_bool_symbol == '0':
            is_bool_symbol = False
        else:
            is_bool_symbol = True
        for tablemap_area in self.tablemap_file_manager.tablemap.tablemap_areas:
            if tablemap_area.label == label:
                self.display_error('Such a label already exists')
                return
        self.tablemap_file_manager.tablemap.add(20, 20, 100, 50, label, is_bool_symbol)
        self.tablemap_area_labels.addItem(label)
        self.tablemap_area_labels.sortItems()
        idx = 0
        for tablemap_area in self.tablemap_file_manager.tablemap.tablemap_areas:
            if tablemap_area.label == label:
                break
            idx += 1
        self.tablemap_area_labels.setCurrentRow(idx)
        self.tablemap_area_selected_event(self.tablemap_area_labels.currentItem())
        if self.capture_window_gui is not None:
            self.capture_window_gui.activateWindow()
    
    def remove_tablemap_area(self):
        items = self.tablemap_area_labels.selectedItems()
        for item in items:
            self.tablemap_area_labels.takeItem(self.tablemap_area_labels.row(item))
            self.tablemap_file_manager.tablemap.remove(item.text())
        self.selected_tablemap_area = None
        if self.capture_window_gui is not None:
            self.capture_window_gui.activateWindow()

    def save_tablemap_file(self):
        if self.capture_window_gui is not None:
            self.capture_window_gui.save_tablemap_area_selected()
            self.capture_window_gui.activateWindow()
        self.tablemap_file_manager.save_tablemap()
    
    def capture_window(self):
        self.capture_window_gui = CaptureWindowGui(self.tablemap_file_manager.tablemap)
        if self.selected_tablemap_area is not None:
            self.capture_window_gui.tablemap_area_selected(self.selected_tablemap_area)

    def closeEvent(self, event):
        qm = QMessageBox()
        if self.tablemap_file_manager.can_save_tablemap():
            ans = qm.question(self, '', 'Do you want to save the tablemap?', qm.Yes | qm.No)
            if ans == qm.Yes:
                self.save_tablemap_file()
        if self.capture_window_gui is not None:
            self.capture_window_gui.close()
        exit(0)

    def display_error(self, text):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(text)
        error_dialog.exec_()
