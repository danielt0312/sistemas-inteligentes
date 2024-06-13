import os
from PyQt6.QtWidgets import (QWidget, QPushButton, QFileDialog, QGridLayout, 
                             QMessageBox)
from pdf_lector import *

# Clase para la interfaz visual y sus funciones
class Window(QWidget):
    # Constructor
    def __init__(self):
        super().__init__()

        # Crear ventana con elementos de la interfaz
        self.customUI()

    # Creacion de la ventana
    def customUI(self):
        # Contenido principal
        content = QGridLayout()
        self.setLayout(content)

        # Boton para seleccionar archivo
        btnSelectFile = QPushButton('Seleccionar carpeta')
        btnSelectFile.clicked.connect(self.loadFile)

        # GridLayout para las acciones
        gridTools = QGridLayout()
        gridTools.addWidget(btnSelectFile, 0, 0)

        # GridLayout para la figura
        self.gridFigure = QGridLayout()

        # Agregar seccion de botones y figura al contenido principal
        content.addLayout(gridTools, 0, 0, 1, 4)

        # Estilo de la ventana
        self.resize(1920,1080)
        self.setWindowTitle('Filtrar documentos en Inglés y Español')

    # Leer archivo ARFF
    def loadFile(self):
        path = self.getDirPath()
        print('PATH:' + path)
        self.lector = PDFLector(path)

        # Validar el archivo proporcionado
        if (self.lector.isValid()):
            print ('valido')
            return
        
        print('*** Archivo invalido ***')
        self.messageError(self.lector.getCause())

    # Proporcionar la direccion de la carpeta
    def getDirPath(self):
        return QFileDialog.getExistingDirectory(
            parent = self,
            caption = 'Selecciona el directorio',
            directory = os.getcwd(),
            options = QFileDialog.Option.ShowDirsOnly
        )
    
    # Mostrar advertencia sobre el directorio invalido
    def messageError(self, causa):
        return QMessageBox.warning(
            self,
            "Advertencia",
            causa,
            buttons = QMessageBox.StandardButton.Close,
            defaultButton = QMessageBox.StandardButton.Close,
        )