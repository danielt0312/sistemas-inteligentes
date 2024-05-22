import os
from PyQt6.QtWidgets import (QWidget, QPushButton, QFileDialog, QGridLayout)
from arff_lector import *

# Clase para la interfaz visual
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.customUI()

    # Creacion de la ventana
    def customUI(self):
        # Layout para la ventana principal
        layout = QGridLayout()
        self.setLayout(layout)

        # Boton para seleccionar archivo
        btnSelectFile = QPushButton('Cargar Archivo')
        btnSelectFile.clicked.connect(self.loadFile)
        layout.addWidget(btnSelectFile, 0, 0, 1, 4)

        # Widget de gráfico
        #self.graphicsView = QGraphicsView()
        #layout.addWidget(self.graphicsView, 1, 0, 1, 4)

        # Boton para deseleccionar archivo
        btnSelectFile = QPushButton('Deseleccionar Archivo')
        #btnSelectFile.clicked.connect(self.loadFile)
        layout.addWidget(btnSelectFile, 1, 0, 1, 4)

        # Estilo de la ventana
        self.resize(600, 600)
        self.setWindowTitle('Interfaz')
    
    # Cargar archivo ARFF
    def loadFile(self):
        path = self.getFileName()
        print(path)
        lector = ArffLector(path[0])
        print (lector.getContent())

        
    # Seleccionar archivo
    def getFileName(self):
        return QFileDialog.getOpenFileName(
            parent = self,
            caption = 'Select a file',
            directory = os.getcwd(),
            filter = 'ARFF File (*.arff);;',
            initialFilter = 'ARFF File (*.arff)'
        )