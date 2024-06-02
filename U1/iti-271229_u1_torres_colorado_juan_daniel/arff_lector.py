import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

    # Definir direccion
    def setPath(self, dir):
        self.dir = dir

    # Validación del archivo
    def isValid(self):
        self.findCause()
        return not (self.dir == '' or self.dir == None or len(self.dir) == 0)
    
    # Buscar causa en caso de haber un problema
    def findCause(self):
        if (self.dir == '' or self.dir == None or len(self.dir) == 0):
            self.cause = 'El directorio no fue proporcionado.'
        else:
            self.cause = 'No se ha encontrado algún problema'

    # Devolver causa
    def getCause(self):
        return self.cause
    
    # Cargar archivo y obtener DataFrame
    def getDataFrame(self):
        arff_file = arff.loadarff(self.dir)
        return pd.DataFrame(arff_file[0])
    
    # Mostrar el Análisis Exploratorio de Datos
    def showEDA(self):
        self.df = self.getDataFrame()
        print("Rows")
        print(self.df.head())
        print("*********")
        print("columns",self.df.columns)
        print("*********")
        print("shape:",self.df.shape)
        print("*********")
        print("Size:",self.df.size)
        # print("*********")
        # print("no. of samples available for each type") 
        # print(self.df["type"].value_counts())
        print("*********")
        print(self.df.describe())

    # Mostrar figura del archivo cargado
    def getFigure(self, df):
        counts,bin_edges = np.histogram(df["edad"], bins = 10, density = True)
        pdf = counts / (sum(counts))
        cdf = np.cumsum(pdf)

        print(pdf)
        print(bin_edges)

        # Figura de Matplotlib (grafica)
        figura = Figure()
        ejes = figura.add_subplot(111)
        ejes.plot(bin_edges[1:], pdf)
        ejes.plot(bin_edges[1:],cdf)

        plt.plot(bin_edges[1:],pdf)
        plt.plot(bin_edges[1:],cdf)
        # plt.show() # mostrar en la clase window, mas especificamente en el QGridLayout "grid"

        # Regresamos el lienzo
        return FigureCanvas(figura)