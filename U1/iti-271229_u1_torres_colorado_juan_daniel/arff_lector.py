import pandas as pd
from scipy.io import arff

# Clase para leer archivos ARFF
class ArffLector():
    path = None
    # Constructor
    def __init__(self, path = None):
        self.path = path

    # Definir direccion
    def setPath(self, path):
        self.path = path

    # Validación del archivo
    def isValid(self):
        return not (self.path == '' or self.path == None or len(self.path) == 0)
    
    # Cargar archivo y obtener DataFrame
    def getDataFrame(self):
        arff_file = arff.loadarff(self.path)
        return pd.DataFrame(arff_file[0])
    
    # Obtener contenido
    def getContent(self):
        if (self.isValid()):
            return self.getDataFrame().head()
        return ("El directorio '" + self.path + "' es inválido.")