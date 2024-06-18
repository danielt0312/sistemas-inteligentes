import os
import subprocess
from classifier import Classifier

"""
Clase para procesar los archivos PDF 
"""
class PDFLector():
    # Constructor
    def __init__(self, dir_path = '.'):
        self.setDirPath(dir_path)
        self.causes = []
        self.pdf_files = []

    # Actualizar Directorio
    def setDirPath(self, dir_path = '.'):
        self.directories = [
            dir_path,   # raiz
            dir_path + '/documentos',
            dir_path + '/documentos/txt',
            dir_path + '/documentos/Inglés',
            dir_path + '/documentos/Español',
            './train'   # carpeta para entrenar el clasificador
        ]

    # Validación de los directorios
    def isValid(self):
        return self.findCause()

    # Buscar causa en caso de haber un problema
    def findCause(self):
        self.causes.clear()     # limpiar  si hay causas antiguas
        
        return self.validTrain() and self.validFiles() and self.validDirectories()
    
    # Validar directorio para poder entrenar el clasificador
    def validTrain(self):
        if not self.pathExists(self.directories[5]):
            self.causes.append("No existe el directorio 'train' en el programa")
            return False
        return True

    # Validar cantidad mínima de PDFs en el directorio raíz
    def validFiles(self):
        if (self.validDir(self.directories[0])):
            files = self.listFiles(self.directories[0])
            self.pdf_files = self.getPDFFiles(files)

            if len(self.pdf_files) == 0:
                self.causes.append(f"No se encontraron archivos PDFs en el directorio '{self.directories[0]}'.")

            return len(self.pdf_files) > 0    # valido si hay archivo(s)
        return False

    # Validar todos los directorios
    def validDirectories(self):
        for directory in self.directories[1:]:
            if not (self.validDir(directory) and self.dirExists(directory)):
                print (self.causes[-1])
                return False
        return True
    
    # Validar directorio proporcionado 
    def validDir(self, directory):
        if (directory == '' or directory == None or len(directory) == 0):
            self.causes.append(f"El directorio '{directory}' no fue correctamente proporcionado.")
            return False
        return True
    
    # Validar si el directorio existe, sino, intentar crearlo y validar si se creó
    def dirExists(self, directory):
        return (self.pathExists(directory) or self.createDir(directory))

    # Validar si una dirección existe
    def pathExists(self, directory):
        return os.path.exists(directory)

    # Clasificar los documentos
    def classify(self):
        if (self.isValid()):
            dir_train = self.directories[5] + '/'

            print('Iniciando clasificacion')
            cf = Classifier(dir_train, self.listFiles(dir_train))
            for f in self.listFiles(self.directories[2]):
                cf.classify(self.directories[2]+'/'+f)
            print('Clasificación terminada')
            
        else:
            print(self.causes[0])

    # Crear directorio
    def createDir(self, directory):
        try:
            os.mkdir(directory)
            print(f"Directorio creado: '{directory}'")
        except OSError as ex:
            self.causes.append(f"El directorio '{directory}' no se pudo crear. \nERROR: {ex}")
            return False
        return True
    
    # Convertir archivos
    def convertFiles(self):
        if (self.isValid()):
            for name in self.pdf_files:
                if (not self.pdfToTxt(self.directories[0] + '/' + name + '.pdf', self.directories[2] + '/' + name + '.txt')):
                    print(self.causes[-1])
            print('Conversión terminada.')
        else:
            print(self.causes[-1])
    
    # Conversión de PDF a TXT
    def pdfToTxt(self, pdf_path, txt_path):
        try:
            subprocess.run(["pdftotext", pdf_path, txt_path])
            print(f"Archivo PDF convertido a TXT: {txt_path}")
        except Exception as ex:
            self.causes.append(f"No se pudo convertir PDF a TXT: \nERROR:{ex}")
            return False
        return True
    
    # Devolver archivos PDFs y sus nombres
    def getPDFFiles(self, files):
        return self.getNameFiles(self.filtFiles(files, '.pdf'))
    
    # Listar los archivos de un directorio 
    def listFiles(self, directory):
        return os.listdir(directory)
    
    # Filtrar los archivos deacuerdo a una extension (default: pdf)
    def filtFiles(self, files, extension = '.pdf'):
        return [fname for fname in files if fname.endswith(extension)]
    
    # Devolver los nombres de los archivos
    def getNameFiles(self, files):
        return [os.path.splitext(fname)[0] for fname in files]

    # Devolver causas
    def getCauses(self):
        return self.causes
    