import os

from pathlib import Path

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
    QColorDialog,
    QTextEdit
    )
from PyQt5.QtGui import QTransform, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp

from utils import count_P


reg_ex = QRegExp("^-?[0-9]+([.][0-9]+)?$")
float_validator = QRegExpValidator(reg_ex)

class InputPanel(QWidget):
    def __init__(self, main_window: QMainWindow):
        super().__init__()

        self.main_window = main_window
        self.data = {}

        layout = QVBoxLayout(self)
        
        self.Rвпис_label = QLabel("Радиус вписанной окружности, м")
        layout.addWidget(self.Rвпис_label)
        self.Rвпис = QLineEdit()
        self.Rвпис.setValidator(float_validator)
        layout.addWidget(self.Rвпис)

        self.Rопис_label = QLabel("Радиус описанной окружности, м")
        layout.addWidget(self.Rопис_label)
        self.Rопис = QLineEdit()
        self.Rопис.setValidator(float_validator)
        layout.addWidget(self.Rопис)

        self.G_label = QLabel("Периметр объекта, м")
        layout.addWidget(self.G_label)
        self.G = QLineEdit()
        self.G.setValidator(float_validator)
        layout.addWidget(self.G)

        self.S_label = QLabel("Площадь объекта, м^2")
        layout.addWidget(self.S_label)
        self.S = QLineEdit()
        self.S.setValidator(float_validator)
        layout.addWidget(self.S)

        self.Lф_label = QLabel("Цвет фона: ")
        layout.addWidget(self.Lф_label)
        self.Lф = QPushButton("Выбрать цвет фона")
        self.Lф.clicked.connect(self.pickColorF)
        layout.addWidget(self.Lф)

        self.Lо_label = QLabel("Цвет объекта: ")
        layout.addWidget(self.Lо_label)
        self.Lо = QPushButton("Выбрать цвет объекта")
        self.Lо.clicked.connect(self.pickColorO)
        layout.addWidget(self.Lо)

        self.lm_label = QLabel("Максимальный линейный размер, м")
        layout.addWidget(self.lm_label)
        self.lm = QLineEdit()
        self.lm.setValidator(float_validator)
        layout.addWidget(self.lm)

        self.R_label = QLabel("Расстояние до объекта, м")
        layout.addWidget(self.R_label)
        self.R = QLineEdit()
        self.R.setValidator(float_validator)
        layout.addWidget(self.R)

        self.delta_d_label = QLabel("Максимальный размер отличающейся детали, м")
        layout.addWidget(self.delta_d_label)
        self.delta_d = QLineEdit()
        self.delta_d.setValidator(float_validator)
        layout.addWidget(self.delta_d)

        self.beta_label = QLabel("коэффициент значимости отличий")
        layout.addWidget(self.beta_label)
        self.beta = QLineEdit()
        self.beta.setValidator(float_validator)
        layout.addWidget(self.beta)

        self.w_label = QLabel("Ширина матрицы, мм")
        layout.addWidget(self.w_label)
        self.w = QLineEdit()
        self.w.setValidator(float_validator)
        layout.addWidget(self.w)

        self.f_label = QLabel("Фокусное расстояние, мм")
        layout.addWidget(self.f_label)
        self.f = QLineEdit()
        self.f.setValidator(float_validator)
        layout.addWidget(self.f)

        self.Kпр_label = QLabel("Коэффициент прогноза")
        layout.addWidget(self.Kпр_label)
        self.Kпр = QLineEdit()
        self.Kпр.setValidator(float_validator)
        layout.addWidget(self.Kпр)

        self.count_btn = QPushButton("Рассчитать коэффициенты", self)
        self.count_btn.clicked.connect(self.count_results)
        layout.addWidget(self.count_btn)

        self.Pобн_label = QLabel("Вероятность обнаружения")
        layout.addWidget(self.Pобн_label)

        self.Pрасп_label = QLabel("Вероятность распознавания")
        layout.addWidget(self.Pрасп_label)

        self.Pрасп_кор_label = QLabel("Скорректированная вероятность распознавания")
        layout.addWidget(self.Pрасп_кор_label)

        self.exif_label = QTextEdit("", self.main_window)
        layout.addWidget(self.exif_label)

        self.save_res_btn = QPushButton("Сохранить результаты")
        self.save_res_btn.clicked.connect(self.save_result)
        layout.addWidget(self.save_res_btn)

    def pickColorO(self):
        dialog = QColorDialog()
        color = dialog.getColor()
        color = color.getRgb()
        color = [str(c) for c in color]
        self.Lо_label.setText("Цвет объекта: " + " ".join(color))

    def pickColorF(self):
        dialog = QColorDialog()
        color = dialog.getColor()
        color = color.getRgb()
        color = [str(c) for c in color]
        self.Lф_label.setText("Цвет фона: " + " ".join(color))

    def clear(self):
        self.Rвпис.clear()
        self.Rопис.clear()
        self.S.clear()
        self.G.clear()
        self.lm.clear()
        self.R.clear()
        self.delta_d.clear()
        self.beta.clear()
        self.w.clear()
        self.f.clear()
        self.Kпр.clear()

        self.Lо_label.setText("Цвет объекта: ")
        self.Lф_label.setText("Цвет фона: ")
        self.Pобн_label.setText("Вероятность обнаружения")
        self.Pрасп_label.setText("Вероятность распознавания")
        self.Pрасп_кор_label.setText("Скорректированная вероятность распознавания")

    def set_data(self, data: dict[str, str]):
        self.Rвпис.setText(data.get('Rвпис', None))
        self.Rопис.setText(data.get('Rопис', None))
        self.S.setText(data.get('S', None))
        self.G.setText(data.get('G', None))
        self.Lо_label.setText("Цвет объекта: " + data.get('Lоб', None))
        self.Lф_label.setText("Цвет фона: " + data.get('Lф', None))
        self.lm.setText(data.get('lm', None))
        self.R.setText(data.get('R', None))
        self.delta_d.setText(data.get('delta_d', None))
        self.beta.setText(data.get('beta', None))
        self.w.setText(data.get('w', None))
        self.f.setText(data.get('f', None))
        self.Kпр.setText(data.get('kпр', None))

        self.Pобн_label.setText(f"Вероятность обнаружения: {data.get('Pобн', None)}")
        self.Pрасп_label.setText(f"Вероятность распознавания: {data.get('Pрасп', None)}")
        self.Pрасп_кор_label.setText(f"Скорректированная вероятность распознавания: {data.get('Pрасп_кор', None)}")

    def count_results(self):
        data = dict()

        resolution = self.exif_label.toPlainText()
        resolution = resolution[1:-1]
        resolution = [int(r) for r in resolution.split(", ")]

        Lо = self.Lо_label.text().lstrip("Цвет объекта: ").split()
        Lо = [int(c)/255 for c in Lо]

        Lф = self.Lф_label.text().lstrip("Цвет фона: ").split()
        Lф = [int(c)/255 for c in Lф]

        data['Lоб'] = Lо
        data['Lф'] = Lф

        try:
            data['Rвпис'] = float(self.Rвпис.text())
            data['Rопис'] = float(self.Rопис.text())
            data['S'] = float(self.S.text())
            data['G'] = float(self.G.text())
            data['L'] = max(resolution)
            data['lm'] = float(self.lm.text())
            data['R'] = int(self.R.text())
            data['delta_d'] = float(self.delta_d.text())
            data['beta'] = float(self.beta.text())
            data['w'] = float(self.w.text())
            data['f'] = float(self.f.text())
            data['N'] = resolution[0]
            data['kпр'] = float(self.Kпр.text())
        except:
            print("Wrong input data")
            return

        print(data)

        Pобн, Pрасп, Pрасп_кор = count_P(**data)

        data['Pобн'] = Pобн
        data['Pрасп'] = Pрасп
        data['Pрасп_кор'] = Pрасп_кор

        self.Pобн_label.setText("Вероятность обнаружения: " + str(round(Pобн, 4)))
        self.Pрасп_label.setText("Вероятность расспознавания: " + str(round(Pрасп, 4)))
        self.Pрасп_кор_label.setText("Скорректированная вероятность распознавания: " + str(round(Pрасп_кор, 4)))

        self.data = data

        self.data["Lоб"] = self.Lо_label.text().lstrip("Цвет объекта: ")
        self.data["Lф"] = self.Lф_label.text().lstrip("Цвет фона: ")

    def save_result(self):
        img_path = Path(self.main_window.image_files[self.main_window.current_image_index])
        img_name = img_path.name
        with open(os.path.join("results", img_name) + ".txt", mode="w", encoding="utf-8") as f:
            res = '\n'.join(f"{str(key)}: {str(val)}" for key, val in self.data.items())
            print(res)
            f.write(res)


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
        exit_action.triggered.connect(self.main_window.close)
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
        else:
            self.main_window.current_image_index = len(self.main_window.image_files) - 1
        self.main_window.rotation_angle = 0
        self.main_window.loadCurrentImage()
    
    def nextImage(self):
        if self.main_window.current_image_index < len(self.main_window.image_files) - 1:
            self.main_window.current_image_index += 1
        else:
            self.main_window.current_image_index = 0
        self.main_window.rotation_angle = 0
        self.main_window.loadCurrentImage()

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
        self.prev_button.setEnabled(has_images)
        self.next_button.setEnabled(has_images)
        self.rotate_left_button.setEnabled(has_images)
        self.rotate_right_button.setEnabled(has_images)
