import sys
from pathlib import Path
import cv2
import numpy as np
import pytesseract
from PyQt6.QtWidgets import (QMainWindow, QFileDialog, QApplication, QDialog,
                             QLabel, QVBoxLayout, QWidget)
from PyQt6.QtGui import QAction, QPixmap, QImage
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtMultimedia import QMediaPlayer
from tensorflow.keras.models import load_model

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

        # Cargar el modelo preentrenado
        self.brand_model = load_model('modeloGasolineras.h5')

    def initUI(self):
        self.statusBar()

        openFile = QAction('Selecc. Archivo', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Seleccionar archivo')
        openFile.triggered.connect(self.showDialog)

        showAuthors = QAction('Acerca de', self)
        showAuthors.setShortcut('Ctrl+A')
        showAuthors.setStatusTip('Mostrar autores')
        showAuthors.triggered.connect(self.showAuthorsDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Abrir')
        fileMenu.addAction(openFile)
        fileMenu.addAction(showAuthors)

        self.mainLayout = QVBoxLayout()

        self.displayLabel = QLabel(self)
        self.mainLayout.addWidget(self.displayLabel)

        self.videoWidget = QVideoWidget(self)
        self.player = QMediaPlayer(self)
        self.player.setVideoOutput(self.videoWidget)
        self.mainLayout.addWidget(self.videoWidget)

        centralWidget = QWidget(self)
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)

        self.setGeometry(300, 300, 550, 450)
        self.setWindowTitle('Detección de Gasolineras')
        self.show()

    def loadPicture(self, path: str):
        img = cv2.imread(path)
        detected_brand = self.detect_brand(img)
        detected_prices = self.detect_prices(img)

        print(f"Marca detectada: {detected_brand}")
        print(f"Precios detectados: {detected_prices}")

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = img_rgb.shape
        bytes_per_line = ch * w
        qimg = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        self.displayLabel.setPixmap(QPixmap.fromImage(qimg))
        self.displayLabel.show()
        self.videoWidget.hide()

    def loadVideo(self, path: str):
        cap = cv2.VideoCapture(path)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            detected_brand = self.detect_brand(frame)
            detected_prices = self.detect_prices(frame)

            print(f"Marca detectada: {detected_brand}")
            print(f"Precios detectados: {detected_prices}")

        cap.release()
        self.player.setSource(QUrl.fromLocalFile(path))
        self.player.play()
        self.displayLabel.hide()
        self.videoWidget.show()

    def customDialog(self, dialogTitle: str, dialogText: str):
        dialog = QDialog(self)
        dialog.setWindowTitle(dialogTitle)

        label = QLabel(dialogText)

        dialog_layout = QVBoxLayout()
        dialog_layout.addWidget(label)
        dialog.setLayout(dialog_layout)
        dialog.show()

    def showAuthorsDialog(self):
        authors = "Autores: Tu nombre"
        self.customDialog('Autores', authors)

    def isMedia(self, filename: str):
        IMAGE_EXTS = ['png', 'jpg', 'jpeg', 'avif']
        VIDEO_EXTS = ['mp4', 'avi', 'mov', 'mkv']
        ext = self.splitString(filename, '.')
        return ext in IMAGE_EXTS or ext in VIDEO_EXTS

    def splitString(self, _str: str, char: str):
        return _str[_str.rfind(char) + 1:len(_str) + 1]

    def showDialog(self):
        home_dir = str(Path.home())
        file_filter = "Media Files (*.png *.jpg *.jpeg *.avif *.mp4 *.avi *.mov *.mkv)"
        file_name, _ = QFileDialog.getOpenFileName(self, 'Seleccionar Archivo', home_dir, file_filter)
        if file_name:
            if self.splitString(file_name, '.') in ['png', 'jpg', 'jpeg', 'avif']:
                self.loadPicture(file_name)
            elif self.splitString(file_name, '.') in ['mp4', 'avi', 'mov', 'mkv']:
                self.loadVideo(file_name)
        else:
            self.customDialog('Error', 'Archivo no válido')

    def detect_brand(self, img):
        resized_img = cv2.resize(img, (224, 224))  # Ajusta según el tamaño que espere tu modelo
        img_array = np.array(resized_img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        predictions = self.brand_model.predict(img_array)
        predicted_brand = np.argmax(predictions)

        brands = {0: 'Pemex', 1: 'Mobil'}
        return brands[predicted_brand]

    def detect_prices(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY_INV, 11, 2)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = [c for c in contours if 500 < cv2.contourArea(c) < 10000]

        detected_prices = ""
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)
            if 2 < aspect_ratio < 6:
                roi = thresh[y:y + h, x:x + w]
                text = pytesseract.image_to_string(roi, config='--psm 6')
                detected_prices += text.strip() + " "

                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return detected_prices.strip()

def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()