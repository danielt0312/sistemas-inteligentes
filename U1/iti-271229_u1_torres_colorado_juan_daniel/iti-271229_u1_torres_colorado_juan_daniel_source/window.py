import os
from PyQt6.QtWidgets import (QWidget, QPushButton, QFileDialog, QGridLayout, 
                             QMessageBox, QComboBox)
from arff_lector import *

# Clase para la interfaz visual y sus funciones
class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Variables que se usarán durante la ejecución
        self.figure = None
        self.lector = ArffLector()
        self.cbxColumns = QComboBox()
        self.cbxColumns.addItem('Seleccione un archivo primero.')
        self.cbxColumns.setEnabled(False)
        self.cbxColumns.currentTextChanged.connect(self.selectedColumn)

        # Crear ventana con elementos de la interfaz
        self.customUI()

    # Creacion de la ventana
    def customUI(self):
        # Contenido principal
        content = QGridLayout()
        self.setLayout(content)

        # Boton para seleccionar archivo
        btnSelectFile = QPushButton('Cargar Archivo')
        btnSelectFile.clicked.connect(self.loadFile)

        # GridLayout para las acciones
        gridTools = QGridLayout()
        gridTools.addWidget(btnSelectFile, 0, 0)
        gridTools.addWidget(self.cbxColumns, 0, 1)

        # GridLayout para la figura
        self.gridFigure = QGridLayout()

        # Agregar seccion de botones y figura al contenido principal
        content.addLayout(gridTools, 0, 0, 1, 4)
        content.addLayout(self.gridFigure, 1, 0, 3, 4)

        # Estilo de la ventana
        self.resize(1920,1080)
        self.setWindowTitle('Visualize the PDF and CDF')

    # Cambio de item en cbxColumns
    def selectedColumn(self, column_name):
        if (self.lector.isValid() and column_name != ''):
            self.loadFigure(column_name)

    # Cargar figura
    def loadFigure(self, column):
        figureCanvas = self.lector.getFigure(self.lector.getDataFrame()[column])

        # Validar figura
        if figureCanvas:
            if self.figure:
                self.figure.deleteLater()
            self.figure = figureCanvas
            self.gridFigure.addWidget(self.figure)

    # Leer archivo ARFF
    def loadFile(self):
        path = self.getPath()
        self.lector = ArffLector(path[0])

        # Validar el archivo proporcionado
        if (self.lector.isValid()):
            self.lector.showEDA()
            # Mostrar figura
            self.loadItems()
            return
        elif (self.figure):
            self.figure.deleteLater()
            self.figure = None
        
        self.cbxColumns.clear()
        self.cbxColumns.addItem('Seleccione un archivo válido.')
        self.cbxColumns.setEnabled(False)
        print('*** Archivo invalido ***')

        return self.messageWarning(self.lector.getCause())
        
    # Cargar columnas al cbxColumns
    def loadItems(self):
        # Eliminamos items previos cargados
        self.cbxColumns.clear()

        # Ingresamos las columnas
        self.cbxColumns.setEnabled(True)
        for column_name in self.lector.getColumns():
            self.cbxColumns.addItem(column_name)
        
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
    def messageWarning(self, causa):
        return QMessageBox.warning(
            self,
            "Advertencia",
            causa,
            buttons = QMessageBox.StandardButton.Discard,
            defaultButton = QMessageBox.StandardButton.Discard,
        )