import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import arff

# Clase para leer archivos ARFF
class ArffLector():
    dir = None
    # Constructor
    def __init__(self, dir = None):
        self.dir = dir

    # Definir direccion
    def setPath(self, dir):
        self.dir = dir

    # Validación del archivo
    def isValid(self):
        return not (self.dir == '' or self.dir == None or len(self.dir) == 0)
    
    # Cargar archivo y obtener DataFrame
    def getDataFrame(self):
        arff_file = arff.loadarff(self.dir)
        return pd.DataFrame(arff_file[0])
    
    # Obtener contenido
    def getContent(self):
        if (self.isValid()):
            self.showEDA(self.getDataFrame())
            return ("El directorio '" + self.dir + "' es válido.")
        return ("El directorio '" + self.dir + "' es inválido.")
    
    # Mostrar el Análisis Exploratorio de Datos
    def showEDA(self, df):
        print("First five rows")
        print(df.head())
        print("*********")
        print("columns",df.columns)
        print("*********")
        print("shape:",df.shape)
        print("*********")
        print("Size:",df.size)
        #print("*********")
        #print("no. of samples available for each type") 
        #print(df["type"].value_counts())
        print("*********")
        print(df.describe())
        self.showFigure(df)

    # Mostrar figura del archivo cargado
    def showFigure(self, df):
        counts,bin_edges = np.histogram(df["edad"],bins=10,density=True)
        pdf = counts / (sum(counts))
        print(pdf)
        print(bin_edges)
        
        cdf=np.cumsum(pdf)
        plt.plot(bin_edges[1:],pdf)
        plt.plot(bin_edges[1:],cdf)
        plt.show()