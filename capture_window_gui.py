from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout,\
        QMessageBox, QPushButton, QListWidget, QFrame, QSplitter, QLabel, QTableWidget,\
        QTableWidgetItem, QHeaderView, QFileDialog, QErrorMessage, QRubberBand 
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSignal, Qt, QRect, QSize
from PyQt5.QtGui import QBrush, QPainter, QColor, QFont, QPixmap, QPen, QImage, QPalette, QIcon
import sip
import win32gui
import win32ui
import win32con
from ctypes import windll
from PIL import Image
from tablemap import Tablemap
from resizable_rubber_band import ResizableRubberBand
import time
import random

IMAGE_NAME = 'capture.bmp'

class CaptureWindowGui(QWidget):
    def __init__(self, tablemap=None):
        super().__init__()
        self.window_width = -1 
        self.window_height = -1 
        self.selected_label = ''
        self.selected_tablemap_area = None
        self.rubber_band = None
        self.pixel_map = None
        self.tablemap = tablemap
        self.init_layouts()
        self.windows = self.get_windows()
        self.init_windows_list()
        self.show()

    def get_windows(self):
        hwnds = []
        windows = []
        win32gui.EnumWindows(CaptureWindowGui.enum_windows_proc, hwnds)
        for hwnd in hwnds:
            text = win32gui.GetWindowText(hwnd)
            if len(text) > 2:
                windows.append((hwnd, text))
        return windows
    
    def init_layouts(self):
        self.main_layout = QVBoxLayout(self)

    def init_windows_list(self):
        self.windows_list = QListWidget()
        for window in self.windows:
            self.windows_list.addItem(f'{window[1]} ({window[0]})')
        self.windows_list.itemClicked.connect(self.window_selected_event)
        self.main_layout.addWidget(self.windows_list)

    def paintEvent(self, event):
        if self.pixel_map is None:
            return 
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(self.pixel_map))
        self.setPalette(palette)
        painter = QPainter(self)
        painter.eraseRect(event.rect())
        painter.setPen(QPen(Qt.red, 1, Qt.SolidLine))
        if self.tablemap is not None:
            for tablemap_area in self.tablemap.tablemap_areas:
                if self.selected_label != tablemap_area.label:
                    painter.drawRect(tablemap_area.x, tablemap_area.y, tablemap_area.w, tablemap_area.h)

    def window_selected_event(self, item):
        hwnd = int(item.text().split(' ')[-1][1:-1])
        print(hwnd)
        self.setWindowTitle(item.text())
        self.windows_list.setParent(None)
        self.grab_image(hwnd)
        self.pixel_map = QPixmap(IMAGE_NAME)
        self.resize(self.pixel_map.width(), self.pixel_map.height())
        self.window_width = self.pixel_map.width()
        self.window_height = self.pixel_map.height()
        self.setMaximumWidth(self.pixel_map.width())
        self.setMaximumHeight(self.pixel_map.height())

    def save_tablemap_area_selected(self):
        if self.selected_tablemap_area is not None:
            geo = self.rubber_band.geometry()
            x, y, w, h = geo.x(), geo.y(), geo.width(), geo.height()
            self.selected_tablemap_area.x = x
            self.selected_tablemap_area.y = y
            self.selected_tablemap_area.w = w
            self.selected_tablemap_area.h = h

    def tablemap_area_selected(self, tablemap_area):
        self.save_tablemap_area_selected()
        self.selected_tablemap_area = tablemap_area
        self.selected_label = tablemap_area.label
        if self.rubber_band is None:
            self.rubber_band = ResizableRubberBand(self)
            self.rubber_band.show()
        self.rubber_band.setGeometry(tablemap_area.x, tablemap_area.y, tablemap_area.w, tablemap_area.h)

    def grab_image(self, hwnd):
        left, top, right, bot = win32gui.GetClientRect(hwnd)
        w = right - left
        h = bot - top
        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        saveDC.SelectObject(saveBitMap)
        result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)
        if result == 1:
            im.save(IMAGE_NAME)

    @staticmethod
    def enum_windows_proc(hwnd, top_windows):
        if win32gui.IsWindowVisible(hwnd):
            top_windows.append(hwnd)
        return True 
