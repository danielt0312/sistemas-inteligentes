import os
from PyQt6.QtWidgets import (QWidget, QPushButton, QFileDialog, QGridLayout, 
                             QMessageBox)
from pdf_filter import PDFLector

"""
Clase para la interfaz visual y sus funciones
"""
class Window(QWidget):
    # Constructor
    def __init__(self):
        super().__init__()

        # Seguimiento de los archivos PDF
        self.lector = PDFLector()

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
        btnClassifier.clicked.connect(self.lector.classify)

        # GridLayout para las acciones
        gridTools = QGridLayout()
        gridTools.addWidget(btnSelectDir, 0, 0)
        gridTools.addWidget(btnConvertFiles, 1, 0)
        gridTools.addWidget(btnClassifier, 2, 0)

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
        self.lector.setDirPath(path)

        # Validar el archivo proporcionado
        if (self.lector.isValid()):
            print ('***VALIDO ***')
        else:
            print ('*** INVALIDO ***')
            # for cause in self.lector.getCauses():
            #     print (cause)
                # self.messageError(cause)
        

    # Proporcionar la direccion de la carpeta
    def getDirPath(self):
        return QFileDialog.getExistingDirectory(
            parent = self,
            caption = 'Selecciona el directorio',
            directory = os.getcwd(),    # abrir en el directorio del programa
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