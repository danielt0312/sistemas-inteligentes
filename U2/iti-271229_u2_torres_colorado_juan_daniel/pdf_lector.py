
"""
Clase para procesar archivos PDF 
"""
class PDFLector():
    # Constructor
    def __init__(self, path = None):
        self.path = path
        self.cause = 'No se ha encontrado algún problema'
        self.df = None

    # Validación del archivo
    def isValid(self):
        self.findCause()
        return not (self.path == '' or self.path == None or len(self.path) == 0)

    # Buscar causa en caso de haber un problema
    def findCause(self):
        if (self.path == '' or self.path == None or len(self.path) == 0):
            self.cause = 'El archivo no fue proporcionado.'
        else:
            self.cause = 'No se ha encontrado algún problema'

    # Devolver causa
    def getCause(self):
        return self.cause