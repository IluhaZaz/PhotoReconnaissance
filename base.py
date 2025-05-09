import os

from PyQt5.QtWidgets import (
    QMainWindow, 
    QLabel,
    QHBoxLayout, 
    QWidget
    )
from PyQt5.QtGui import QPixmap

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

        self.L = None
        self.N = None
    
    def loadCurrentImage(self):
        image_path = self.image_files[self.current_image_index]
        self.original_pixmap = QPixmap(image_path)
        
        if not self.original_pixmap.isNull():
            self.toolbar.applyRotation()
            self.setWindowTitle(f'Фото: {os.path.basename(image_path)}')

            exif_data = get_exif_data(image_path)
            resolution = (exif_data['ExifImageWidth'], exif_data['ExifImageHeight'])
            self.input_panel.exif_label.setText(str(resolution))
            self.L = max(resolution)
            self.N = resolution[0]
    
    def resizeEvent(self, event):
        if hasattr(self, 'original_pixmap') and self.original_pixmap:
            self.toolbar.applyRotation()
        super().resizeEvent(event)


class DPCinitUI:

    @staticmethod
    def initUI(main_window: DetectionProbabilityCounter):
        main_window.setCentralWidget(main_window.central_widget)

        main_window.input_panel.setFixedSize(400, 900)
        main_window.image_label.setFixedHeight(900)
        
        layout = QHBoxLayout(main_window.central_widget)
        layout.addWidget(main_window.image_label)
        layout.addWidget(main_window.input_panel)
        
        menubar = main_window.menuBar()
        menubar.addMenu(MenuBar(main_window))

        main_window.addToolBar(main_window.toolbar)
                
        main_window.setWindowTitle('Просмотр фоток')
        main_window.setGeometry(0, 0, 1920, 1080)
