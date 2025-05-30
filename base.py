import os

from pathlib import Path

from PyQt5.QtWidgets import (
    QMainWindow, 
    QLabel,
    QHBoxLayout, 
    QWidget
    )
from PyQt5.QtGui import QPixmap
from PIL import Image

from utils import get_exif_data
from components import InputPanel, MenuBar, ToolBar


class DetectionProbabilityCounter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.image_label = QLabel()
        self.input_panel = InputPanel(self)
        self.toolbar = ToolBar(self)

        self.image_files = []
        self.current_image_index = 0
        self.rotation_angle = 0

        
        if not os.path.exists("results"):
            os.makedirs("results")

    def load_results(self):
        img_path = Path(self.image_files[self.current_image_index])
        img_name = img_path.name

        res_path = os.path.join("results", img_name) + ".txt"

        if(Path(res_path).exists()):
            with open(res_path, mode='r', encoding='utf-8') as f:
                data = dict()
                lines = f.readlines()

                for line in lines:
                    key, val = line.split(": ")
                    data[key] = val.rstrip("\n")
                self.input_panel.set_data(data)
        else:
            self.input_panel.clear()
    
    def loadCurrentImage(self):
        image_path = self.image_files[self.current_image_index]
        self.original_pixmap = QPixmap(image_path)
        
        if not self.original_pixmap.isNull():
            self.toolbar.applyRotation()
            self.setWindowTitle(f'Фото: {os.path.basename(image_path)}')

            exif_data = get_exif_data(image_path)
            if exif_data:
                resolution = (
                    exif_data.get('ExifImageWidth', ''), 
                    exif_data.get('ExifImageHeight', '')
                )
            else:
                with Image.open(image_path) as img:
                    resolution = img.size
            self.input_panel.exif_label.setText(str(resolution))
            self.L = max(resolution)
            self.N = resolution[0]

            self.load_results()
    
    def resizeEvent(self, event):
        if hasattr(self, 'original_pixmap') and self.original_pixmap:
            self.toolbar.applyRotation()
        super().resizeEvent(event)


class DPCinitUI:

    @staticmethod
    def initUI(main_window: DetectionProbabilityCounter):
        main_window.setCentralWidget(main_window.central_widget)

        main_window.input_panel.setFixedSize(470, 900)
        main_window.image_label.setFixedHeight(900)
        
        layout = QHBoxLayout(main_window.central_widget)
        layout.addWidget(main_window.image_label)
        layout.addWidget(main_window.input_panel)
        
        menubar = main_window.menuBar()
        menubar.addMenu(MenuBar(main_window))

        main_window.addToolBar(main_window.toolbar)

        main_window.setWindowTitle('SpyInspector')
        main_window.setGeometry(0, 0, 1920, 1080)
