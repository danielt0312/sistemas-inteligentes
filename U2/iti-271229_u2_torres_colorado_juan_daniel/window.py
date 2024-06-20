import os
from PyQt6.QtWidgets import (QWidget, QPushButton, QFileDialog, QGridLayout, 
                             QMessageBox)
from PyQt6.QtCore import pyqtSlot
from pdf_filter import PDFFilter

"""
Clase para la interfaz visual y sus funciones
"""
class Window(QWidget):
    # Constructor
    def __init__(self):
        super().__init__()

        # Seguimiento de los archivos PDF
        self.lector = PDFFilter()

        # Conectar señales provinientes del filtro
        self.lector.errorSignal.connect(self.messageError)
        self.lector.infoSignal.connect(self.messageInfo)

        # Crear ventana con elementos de la interfaz
        self.customUI()

    # Creacion de la ventana
    def customUI(self):
        # Contenido principal
        content = QGridLayout()
        self.setLayout(content)

        # Boton para seleccionar directorio
        btnSelectDir = QPushButton('Seleccionar carpeta')
        btnSelectDir.clicked.connect(self.loadFile)

        # Botón para convertir archivos
        btnConvertFiles = QPushButton('Convertir archivos')
        btnConvertFiles.clicked.connect(self.lector.convertFiles)

        # Botón para clasificar
        btnClassifier = QPushButton('Clasificar documentos')
        btnClassifier.clicked.connect(self.lector.classifyFiles)
        
        # Botón para mostrar clustering
        btnClustering = QPushButton('Realizar clustering')
        btnClustering.clicked.connect(self.lector.clustering)

        # GridLayout para las acciones
        gridTools = QGridLayout()
        gridTools.addWidget(btnSelectDir, 0, 0)
        gridTools.addWidget(btnConvertFiles, 1, 0)
        gridTools.addWidget(btnClassifier, 2, 0)
        gridTools.addWidget(btnClustering, 3, 0)

        # GridLayout para la figura
        self.gridFigure = QGridLayout()

        # Agregar seccion de botones y figura al contenido principal
        content.addLayout(gridTools, 0, 0, 1, 4)

        # Estilo de la ventana
        self.resize(720,540)
        self.setWindowTitle('Filtrar documentos en Inglés y Español')

    # Leer archivo ARFF
    def loadFile(self):
        path = self.getDirPath()
        self.lector.setDirPath(path)

    # Proporcionar la direccion de la carpeta
    def getDirPath(self):
        return QFileDialog.getExistingDirectory(
            parent = self,
            caption = 'Selecciona el directorio',
            directory = os.getcwd(),    # abrir en el directorio del programa
            options = QFileDialog.Option.ShowDirsOnly
        )
    
    @pyqtSlot(str)
    # Mostrar advertencias o errores que se generan en el programa
    def messageError(self, causa):
        return QMessageBox.warning(
            self,
            "Advertencia",
            causa,
            buttons = QMessageBox.StandardButton.Close,
            defaultButton = QMessageBox.StandardButton.Close,
        )
    
    @pyqtSlot(str)
    # Mostrar procesos terminados/completados que se generan en el programa
    def messageInfo(self, causa):
        return QMessageBox.information(
            self,
            "Información",
            causa,
            buttons = QMessageBox.StandardButton.Ok,
            defaultButton = QMessageBox.StandardButton.Ok,
        )