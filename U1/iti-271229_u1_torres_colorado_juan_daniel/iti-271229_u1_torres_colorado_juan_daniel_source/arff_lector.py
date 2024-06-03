import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
from scipy.io import arff

# Generar figura
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Clase para leer archivos ARFF
class ArffLector():
    # Constructor
    def __init__(self, dir = None):
        self.dir = dir
        self.cause = 'No se ha encontrado algún problema'
        self.df = None

    # Definir direccion del archivo
    def setPath(self, dir):
        self.dir = dir

    # Validación del archivo
    def isValid(self):
        self.findCause()
        return not (self.dir == '' or self.dir == None or len(self.dir) == 0 or self.columns > 10)

    # Buscar causa en caso de haber un problema
    def findCause(self):
        self.rows, self.columns = self.getColumns().shape
        if (self.dir == '' or self.dir == None or len(self.dir) == 0):
            self.cause = 'El archivo no fue proporcionado.'
        elif (self.columns > 10):
            self.cause = 'El limite máximo de columnas es de 10.\nPorfavor, modifique o cambie de archivo.'
        elif (self.columns == 0):
            self.cause = 'No se encuentra una longitud válida de filas o columnas.\nPorfavor, modifique o cambie de archivo.'
        else:
            self.cause = 'No se ha encontrado algún problema'

    # Devolver causa
    def getCause(self):
        return self.cause
    
    # Cargar archivo y obtener DataFrame
    def getDataFrame(self):
        arff_file = arff.loadarff(self.dir)
        return pd.DataFrame(arff_file[0])
    
    # Obtener solo columnas numericas
    def getColumns(self):
        if self.df is None:
            self.df = self.getDataFrame()
        return self.df.select_dtypes(include=[np.number])

    # Mostrar el Análisis Exploratorio de todos los Datos proporcionados en el archivo
    def showEDA(self):
        self.df = self.getDataFrame()
        print("\nRows")
        print(self.df.head())
        print("*********")
        print("columns", self.df.columns)
        print("*********")
        print("length columns", len(self.df.columns.names))
        print("*********")
        print("shape:",self.df.shape)
        print("*********")
        print("Size:",self.df.size)
        print("*********")
        print(self.df.describe())
        print()

    # Mostrar figura del archivo cargado
    def getFigure(self, data):
        counts,bin_edges = np.histogram(data, bins = 10, density = True)
        pdf = counts / (sum(counts))

        print('\npdf: ', pdf)
        print('bin_edges: ', bin_edges)

        # Figura de Matplotlib (grafica)
        figura = Figure()
        ejes = figura.add_subplot(111)

        cdf = np.cumsum(pdf)
        print('cdf: ', cdf)

        # Agregar puntos y leyenda
        ejes.plot(bin_edges[1:], pdf, label='PDF', color='royalblue')
        ejes.plot(bin_edges[1:], cdf, label='CDF', color='darkorange')
        ejes.legend()

        # plt.plot(bin_edges[1:],pdf)
        # plt.plot(bin_edges[1:],cdf)
        # plt.show() # mostrar en la clase window, mas especificamente en el QGridLayout "grid"

        # Regresamos el lienzo
        return FigureCanvas(figura)