import pandas as pd
from scipy.io import arff

# Clase para leer archivos ARFF
class ArffLector():
    # Constructor
    def __init__(self, path = None):
        pass

    # Validación del archivo
    def isValid(self, path = None):
        return not (path == '' or path == None or len(path) == 0)
            
    
    # Obtener la información
    def getData(self, path):
        data = arff.loadarff(path)
        df = pd.DataFrame(data[0])
        return df

    # Abrir archivo
    def openFile(self, path):
        if (self.isValid(path)):
            print ((self.getData(path)).head())
        else:
            print ("No es valido el directorio")

lector = ArffLector()
lector.openFile('example.arff')