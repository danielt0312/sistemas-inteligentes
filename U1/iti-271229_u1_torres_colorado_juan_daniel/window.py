import os
from PyQt6.QtWidgets import (QWidget, QPushButton, QFileDialog, QGridLayout, QMessageBox)
from arff_lector import *

# Clase para la interfaz visual y sus funciones
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.customUI()

    # Creacion de la ventana
    def customUI(self):
        # Contenido de la ventana principal
        content = QGridLayout()
        self.setLayout(content)

        # Boton para seleccionar archivo
        btnSelectFile = QPushButton('Cargar Archivo')
        btnSelectFile.clicked.connect(self.loadFigure)

        # Boton para deseleccionar archivo
        btnDeselectFile = QPushButton('Deseleccionar Archivo')

        # GridLayout para los botones
        gridButtons = QGridLayout()
        gridButtons.addWidget(btnSelectFile, 0, 0)
        gridButtons.addWidget(btnDeselectFile, 1, 0)

        # GridLayout para la figura
        self.gridFigure = QGridLayout()

        # Variables que se usarán durante la ejecución
        self.figure = None
        self.lector = ArffLector()

        # Ageegar seccion de botones y figura al contenido principal
        content.addLayout(gridButtons, 0, 0, 1, 4)
        content.addLayout(self.gridFigure, 1, 0, 3, 4)

        # Estilo de la ventana
        self.resize(1920,1080)
        self.setWindowTitle('Visualize the PDF and CDF')

    # Cargamos la figura
    def loadFigure(self):
        self.loadFile()
        if not (self.lector.isValid()):
            return self.messageWarningPath(self.lector.getCause())
        
        figureCanvas = self.lector.getFigure(self.lector.getDataFrame())

        # Validar figura
        if figureCanvas:
            if self.figure:
                self.figure.deleteLater()  # Eliminar el lienzo anterior si existe
            self.figure = figureCanvas
            self.gridFigure.addWidget(self.figure)

    # Leer archivo ARFF
    def loadFile(self):
        path = self.getPath()      
        self.lector = ArffLector(path[0])
        
        print (path)
        if (self.lector.isValid()):
            self.lector.showEDA()
        
    # Seleccionar archivo ARFF
    def getPath(self):
        return QFileDialog.getOpenFileName(
            parent = self,
            caption = 'Selecciona un archivo ARFF',
            directory = os.getcwd(),
            filter = 'ARFF File (*.arff) ',
            initialFilter = 'ARFF File (*.arff)'
        )
    
    # Mostrar advertencia sobre el directorio invalido
    def messageWarningPath(self, causa):
        return QMessageBox.warning(
            self,
            "Advertencia",
            causa,
            buttons = QMessageBox.StandardButton.Discard,
            defaultButton = QMessageBox.StandardButton.Discard,
        )