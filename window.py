import sys
import os

from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, 
                            QFileDialog, QAction, QToolBar, 
                            QStatusBar, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QColorDialog)
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import Qt

from utils import count_P, get_exif_data


class DetectionProbabilityCounter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.image_files = []
        self.current_image_index = 0
        self.rotation_angle = 0

        self.L = None
        self.N = None

        self.initUI()
        
    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        layout = QHBoxLayout(self.central_widget)
        
        self.image_label = QLabel()
        layout.addWidget(self.image_label)

        self.input_panel = QWidget()
        self.input_panel.setFixedSize(400, 900)
        self.input_layout = QVBoxLayout(self.input_panel)
        
        self.Rвпис_label = QLabel("Радиус вписанной окружности, м")
        self.input_layout.addWidget(self.Rвпис_label)
        self.Rвпис = QLineEdit()
        self.input_layout.addWidget(self.Rвпис)

        self.Rопис_label = QLabel("Радиус описанной окружности, м")
        self.input_layout.addWidget(self.Rопис_label)
        self.Rопис = QLineEdit()
        self.input_layout.addWidget(self.Rопис)

        self.G_label = QLabel("Периметр объекта, м")
        self.input_layout.addWidget(self.G_label)
        self.G = QLineEdit()
        self.input_layout.addWidget(self.G)

        self.S_label = QLabel("Площадь объекта, м^2")
        self.input_layout.addWidget(self.S_label)
        self.S = QLineEdit()
        self.input_layout.addWidget(self.S)

        self.Lф_label = QLabel("Яркость фона")
        self.input_layout.addWidget(self.Lф_label)
        self.Lф = QLineEdit()
        self.input_layout.addWidget(self.Lф)

        self.Lо_label = QLabel("Яркость объекта")
        self.input_layout.addWidget(self.Lо_label)
        self.Lо = QLineEdit()
        self.input_layout.addWidget(self.Lо)

        self.lm_label = QLabel("Максимальный линейный размер, м")
        self.input_layout.addWidget(self.lm_label)
        self.lm = QLineEdit()
        self.input_layout.addWidget(self.lm)

        self.R_label = QLabel("Расстояние до объекта, м")
        self.input_layout.addWidget(self.R_label)
        self.R = QLineEdit()
        self.input_layout.addWidget(self.R)

        self.O_label = QLabel("Угол захвата по горизонтали, град")
        self.input_layout.addWidget(self.O_label)
        self.O = QLineEdit()
        self.input_layout.addWidget(self.O)

        self.Kпр_label = QLabel("Коэффициент прогноза")
        self.input_layout.addWidget(self.Kпр_label)
        self.Kпр = QLineEdit()
        self.input_layout.addWidget(self.Kпр)

        self.pick_color_btn = QPushButton("Посмотреть цвет")
        self.pick_color_btn.clicked.connect(self.pickColor)
        self.input_layout.addWidget(self.pick_color_btn)

        self.count_btn = QPushButton("Рассчитать коэффициенты", self)
        self.count_btn.clicked.connect(self.count_results)
        self.input_layout.addWidget(self.count_btn)

        self.Pобн_label = QLabel("Коэффициент обнаружения")
        self.input_layout.addWidget(self.Pобн_label)

        self.Pрасп_label = QLabel("Коэффициент распознавания")
        self.input_layout.addWidget(self.Pрасп_label)

        self.exif_label = QLabel()
        self.input_layout.addWidget(self.exif_label)
        
        layout.addWidget(self.input_panel)
        
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Файл')
        
        open_action = QAction('Открыть папку', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.openFolder)
        file_menu.addAction(open_action)
        
        exit_action = QAction('Выход', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)
        
        self.prev_button = QAction('◄ Назад', self)
        self.prev_button.setShortcut('Left')
        self.prev_button.triggered.connect(self.prevImage)
        self.prev_button.setEnabled(False)
        self.toolbar.addAction(self.prev_button)
        
        self.next_button = QAction('Вперед ►', self)
        self.next_button.setShortcut('Right')
        self.next_button.triggered.connect(self.nextImage)
        self.next_button.setEnabled(False)
        self.toolbar.addAction(self.next_button)
        
        self.rotate_left_button = QAction('↶ Повернуть влево', self)
        self.rotate_left_button.setShortcut('Ctrl+L')
        self.rotate_left_button.triggered.connect(self.rotateLeft)
        self.rotate_left_button.setEnabled(False)
        self.toolbar.addAction(self.rotate_left_button)
        
        self.rotate_right_button = QAction('↷ Повернуть вправо', self)
        self.rotate_right_button.setShortcut('Ctrl+R')
        self.rotate_right_button.triggered.connect(self.rotateRight)
        self.rotate_right_button.setEnabled(False)
        self.toolbar.addAction(self.rotate_right_button)
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.setWindowTitle('Просмотр фоток')
        self.setGeometry(0, 0, 1920, 1080)

    def count_results(self):
        Rвпис = float(self.Rвпис.text())
        Rопис = float(self.Rопис.text())
        S = float(self.S.text())
        G = float(self.G.text())
        Lоб = int(self.Lо.text())
        Lф = int(self.Lф.text())
        lm = float(self.lm.text())
        R = int(self.R.text())
        O = int(self.O.text())
        kпр = float(self.Kпр.text())

        Pобн, Pрасп = count_P(Rвпис, Rопис, S, G, self.L, Lоб, Lф, lm, R, self.N, O, kпр)

        self.Pобн_label.setText("Коэффициент обнаружения" + str(Pобн))
        self.Pрасп_label.setText("Коэффициент расспознавания" + str(Pрасп))

    def pickColor(self):
        dialog = QColorDialog()
        dialog.getColor(options=QColorDialog.ShowAlphaChannel)
        
    def openFolder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Выберите папку с фотками')
        
        if folder_path:
            self.image_files = []
            valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
            
            for file in os.listdir(folder_path):
                if file.lower().endswith(valid_extensions):
                    self.image_files.append(os.path.join(folder_path, file))
            
            if self.image_files:
                self.current_image_index = 0
                self.rotation_angle = 0
                self.loadCurrentImage()
                self.updateButtons()
            else:
                self.status_bar.showMessage('Нет фоток в папке', 3000)
    
    def loadCurrentImage(self):
        if 0 <= self.current_image_index < len(self.image_files):
            image_path = self.image_files[self.current_image_index]
            self.original_pixmap = QPixmap(image_path)
            
            if not self.original_pixmap.isNull():
                self.applyRotation()
                self.setWindowTitle(f'Фото: {os.path.basename(image_path)}')

                exif_data = get_exif_data(image_path)
                resolution = (exif_data['ExifImageWidth'], exif_data['ExifImageHeight'])
                self.exif_label.setText(str(resolution))
                self.L = max(resolution)
                self.N = resolution[0]

                self.status_bar.showMessage(
                    f'Фото {self.current_image_index + 1} из {len(self.image_files)}', 
                    3000
                )
    
    def applyRotation(self):
        transform = QTransform().rotate(self.rotation_angle)
        rotated_pixmap = self.original_pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)
        
        scaled_pixmap = rotated_pixmap.scaled(
            self.image_label.width(), 
            self.image_label.height(), 
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)
    
    def rotateLeft(self):
        self.rotation_angle -= 90
        if self.rotation_angle < 0:
            self.rotation_angle = 270
        self.applyRotation()
    
    def rotateRight(self):
        self.rotation_angle += 90
        if self.rotation_angle >= 360:
            self.rotation_angle = 0
        self.applyRotation()
    
    def prevImage(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.rotation_angle = 0
            self.loadCurrentImage()
            self.updateButtons()
    
    def nextImage(self):
        if self.current_image_index < len(self.image_files) - 1:
            self.current_image_index += 1
            self.rotation_angle = 0
            self.loadCurrentImage()
            self.updateButtons()
    
    def updateButtons(self):
        has_images = len(self.image_files) > 0
        self.prev_button.setEnabled(has_images and self.current_image_index > 0)
        self.next_button.setEnabled(has_images and self.current_image_index < len(self.image_files) - 1)
        self.rotate_left_button.setEnabled(has_images)
        self.rotate_right_button.setEnabled(has_images)
    
    def resizeEvent(self, event):
        if hasattr(self, 'original_pixmap') and self.original_pixmap:
            self.applyRotation()
        super().resizeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = DetectionProbabilityCounter()
    viewer.show()
    sys.exit(app.exec_())