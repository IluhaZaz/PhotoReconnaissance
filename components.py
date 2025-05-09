import os

from PyQt5.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QAction,
    QToolBar,
    QMenu,
    QWidget,
    QLabel, 
    QVBoxLayout, 
    QWidget, 
    QLineEdit, 
    QPushButton, 
    QColorDialog
    )
from PyQt5.QtGui import QTransform
from PyQt5.QtCore import Qt

from utils import count_P


class InputPanel(QWidget):
    def __init__(self, main_window: QMainWindow):
        super().__init__()

        self.main_window = main_window

        layout = QVBoxLayout(self)
        
        self.Rвпис_label = QLabel("Радиус вписанной окружности, м")
        layout.addWidget(self.Rвпис_label)
        self.Rвпис = QLineEdit()
        layout.addWidget(self.Rвпис)

        self.Rопис_label = QLabel("Радиус описанной окружности, м")
        layout.addWidget(self.Rопис_label)
        self.Rопис = QLineEdit()
        layout.addWidget(self.Rопис)

        self.G_label = QLabel("Периметр объекта, м")
        layout.addWidget(self.G_label)
        self.G = QLineEdit()
        layout.addWidget(self.G)

        self.S_label = QLabel("Площадь объекта, м^2")
        layout.addWidget(self.S_label)
        self.S = QLineEdit()
        layout.addWidget(self.S)

        self.Lф_label = QLabel("Яркость фона")
        layout.addWidget(self.Lф_label)
        self.Lф = QLineEdit()
        layout.addWidget(self.Lф)

        self.Lо_label = QLabel("Яркость объекта")
        layout.addWidget(self.Lо_label)
        self.Lо = QLineEdit()
        layout.addWidget(self.Lо)

        self.lm_label = QLabel("Максимальный линейный размер, м")
        layout.addWidget(self.lm_label)
        self.lm = QLineEdit()
        layout.addWidget(self.lm)

        self.R_label = QLabel("Расстояние до объекта, м")
        layout.addWidget(self.R_label)
        self.R = QLineEdit()
        layout.addWidget(self.R)

        self.O_label = QLabel("Угол захвата по горизонтали, град")
        layout.addWidget(self.O_label)
        self.O = QLineEdit()
        layout.addWidget(self.O)

        self.Kпр_label = QLabel("Коэффициент прогноза")
        layout.addWidget(self.Kпр_label)
        self.Kпр = QLineEdit()
        layout.addWidget(self.Kпр)

        self.pick_color_btn = QPushButton("Посмотреть цвет")
        self.pick_color_btn.clicked.connect(self.pickColor)
        layout.addWidget(self.pick_color_btn)

        self.count_btn = QPushButton("Рассчитать коэффициенты", self)
        self.count_btn.clicked.connect(self.count_results)
        layout.addWidget(self.count_btn)

        self.Pобн_label = QLabel("Коэффициент обнаружения")
        layout.addWidget(self.Pобн_label)

        self.Pрасп_label = QLabel("Коэффициент распознавания")
        layout.addWidget(self.Pрасп_label)

        self.exif_label = QLabel()
        layout.addWidget(self.exif_label)

    def pickColor(self):
        dialog = QColorDialog()
        dialog.getColor(options=QColorDialog.ShowAlphaChannel)

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

        Pобн, Pрасп = count_P(Rвпис, Rопис, S, G, self.main_window.L, Lоб, Lф, lm, R, self.main_window.N, O, kпр)

        self.Pобн_label.setText("Коэффициент обнаружения: " + str(round(Pобн, 4)))
        self.Pрасп_label.setText("Коэффициент расспознавания: " + str(round(Pрасп, 4)))


class MenuBar(QMenu):
    def __init__(self, main_window: QMainWindow):
        super().__init__(title="Меню", parent=main_window)

        self.main_window = main_window
        
        open_action = QAction('Открыть папку', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.openFolder)
        self.addAction(open_action)
        
        exit_action = QAction('Выход', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        self.addAction(exit_action)

    def openFolder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Выберите папку с фотками')
        
        if folder_path:
            self.main_window.image_files = []
            valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
            
            for file in os.listdir(folder_path):
                if file.lower().endswith(valid_extensions):
                    self.main_window.image_files.append(os.path.join(folder_path, file))
            
            if self.main_window.image_files:
                self.main_window.current_image_index = 0
                self.main_window.rotation_angle = 0
                self.main_window.loadCurrentImage()
                self.main_window.toolbar.updateButtons()

class ToolBar(QToolBar):
    def __init__(self, parent: QMainWindow):
        super().__init__(parent)

        self.main_window = parent
        
        self.prev_button = QAction('◄ Назад', self)
        self.prev_button.setShortcut('Left')
        self.prev_button.triggered.connect(self.prevImage)
        self.prev_button.setEnabled(False)
        self.addAction(self.prev_button)
        
        self.next_button = QAction('Вперед ►', self)
        self.next_button.setShortcut('Right')
        self.next_button.triggered.connect(self.nextImage)
        self.next_button.setEnabled(False)
        self.addAction(self.next_button)
        
        self.rotate_left_button = QAction('↶ Повернуть влево', self)
        self.rotate_left_button.setShortcut('Ctrl+L')
        self.rotate_left_button.triggered.connect(self.rotateLeft)
        self.rotate_left_button.setEnabled(False)
        self.addAction(self.rotate_left_button)
        
        self.rotate_right_button = QAction('↷ Повернуть вправо', self)
        self.rotate_right_button.setShortcut('Ctrl+R')
        self.rotate_right_button.triggered.connect(self.rotateRight)
        self.rotate_right_button.setEnabled(False)
        self.addAction(self.rotate_right_button)

    def rotateLeft(self):
        self.main_window.rotation_angle -= 90
        if self.main_window.rotation_angle < 0:
            self.main_window.rotation_angle = 270
        self.applyRotation()
    
    def rotateRight(self):
        self.main_window.rotation_angle += 90
        if self.main_window.rotation_angle >= 360:
            self.main_window.rotation_angle = 0
        self.applyRotation()
    
    def prevImage(self):
        if self.main_window.current_image_index > 0:
            self.main_window.current_image_index -= 1
            self.main_window.rotation_angle = 0
            self.main_window.loadCurrentImage()
            self.updateButtons()
    
    def nextImage(self):
        if self.main_window.current_image_index < len(self.main_window.image_files) - 1:
            self.main_window.current_image_index += 1
            self.main_window.acceptDropsrotation_angle = 0
            self.main_window.loadCurrentImage()
            self.updateButtons()

    def applyRotation(self):
        transform = QTransform().rotate(self.main_window.rotation_angle)
        rotated_pixmap = self.main_window.original_pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)
        
        scaled_pixmap = rotated_pixmap.scaled(
            self.main_window.image_label.width(), 
            self.main_window.image_label.height(), 
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.main_window.image_label.setPixmap(scaled_pixmap)
    
    def updateButtons(self):
        has_images = len(self.main_window.image_files) > 0
        self.prev_button.setEnabled(has_images and self.main_window.current_image_index > 0)
        self.next_button.setEnabled(has_images and self.main_window.current_image_index < len(self.main_window.image_files) - 1)
        self.rotate_left_button.setEnabled(has_images)
        self.rotate_right_button.setEnabled(has_images)
