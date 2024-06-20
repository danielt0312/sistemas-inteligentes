import os
import subprocess  # para usar pdftotext y pdfinfo de poppler, sudo apt-get install poppler-utils
import shutil
from PyQt6.QtCore import QObject, pyqtSignal
from classifier import Classifier
from cluster import Cluster

"""
Clase para procesar los archivos PDF 
"""
class PDFFilter(QObject):
    errorSignal = pyqtSignal(str)  # Señal que emite una cadena (mensaje de error)

    # Constructor
    def __init__(self, dir_path='.'):
        super().__init__()
        self.causes = []
        self.pdf_files = []
        self.setDirPath(dir_path)

    # Actualizar Directorio
    def setDirPath(self, dir_path='.'):
        self.directories = [
            dir_path,   # raiz
            dir_path + '/documentos',
            dir_path + '/documentos/analysis',
            dir_path + '/documentos/Inglés',
            dir_path + '/documentos/Español',
            './train'   # carpeta para entrenar el clasificador
        ]
        self.isValid()

    # Buscar causa en caso de haber un problema
    def isValid(self):
        self.causes.clear()  # limpiar si hay causas antiguas

        if not (self.validFiles() and self.validDirectories()):
            self.emitErrorSignal()
            return False
        return True

    # Validar directorio para poder entrenar el clasificador
    def validTrain(self):
        if len(self.filtFiles(self.listFiles(self.directories[2] + '/'), '.txt')) == 0:
            self.causes.append(f"No se encontraron archivos de texto en el directorio '{self.directories[2]}'")
            self.emitErrorSignal()
            return False
        return True

    # Validar cantidad mínima de PDFs en el directorio raíz
    def validFiles(self):
        if (self.validDir(self.directories[0])):
            files = self.listFiles(self.directories[0] + '/')
            self.pdf_files = self.getNameFiles(self.filtFiles(files, '.pdf'))

            if len(self.pdf_files) == 0:
                self.causes.append(f"No se encontraron archivos PDFs en el directorio '{self.directories[0]}'.")

            return len(self.pdf_files) > 0  # valido si hay archivo(s)
        return False

    # Validar todos los directorios
    def validDirectories(self):
        for directory in self.directories[1:]:
            if not (self.validDir(directory) and self.dirExists(directory)):
                return False
        return True

    # Validar directorio proporcionado 
    def validDir(self, directory):
        if (directory == '' or directory is None or len(directory) == 0):
            self.causes.append(f"El directorio '{directory}' no fue correctamente proporcionado.")
            return False
        return True

    # Clasificar todos los archivos PDFs de la carpeta proporcionada
    def classifyFiles(self):
        if self.isValid() and self.validTrain():
            dir_train = self.directories[5] + '/'

            self.files_en = []
            self.files_es = []

            print('Iniciando clasificación, esto puede llevar tiempo...')
            self.cf = Classifier(dir_train, self.listFiles(dir_train))
            for f in self.listFiles(self.directories[2]):
                self.classifyFile(self.directories[2], f)
            print('Clasificación terminada')

            # self.moveFiles(self.directories[0], self.directories[3], self.getNameFiles(self.files_en))
            # self.moveFiles(self.directories[0], self.directories[4], self.getNameFiles(self.files_es))
            # self.renameFiles()
            self.clustering()

    # Implementar las tecnicas de clustering
    def clustering(self):
        titles = self.getNameFiles(self.files_en)
        content = []
        
        for f in self.files_en:
            content.append((" ".join(self.cf.text2paragraphs(self.directories[2] + '/' + f)).replace('\n', ' ')))
        
        cl = Cluster(titles, content, 3)
        cl.showFigures()

    # Clasificar un archivo si está en inglés o español
    def classifyFile(self, dir_path, f):
        language = self.cf.classify(dir_path + '/' + f, f)
        if language == 'es':
            self.files_es.append(f)
        elif language == 'en':
            self.files_en.append(f)

    # Mover una lista de archivos a otro directorio
    def moveFiles(self, dir_orig, dir_dest, files):
        for f in files:
            shutil.move(dir_orig + '/' + f + '.pdf', dir_dest + '/' + f + '.pdf')

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
        if self.isValid():
            print('Iniciando conversión de archivos PDF a TXT, esto puede llevar tiempo...')
            for name in self.pdf_files:
                if not self.pdfToTxt(self.directories[0] + '/' + name + '.pdf', self.directories[2] + '/' + name + '.txt', name):
                    print(self.causes[-1])
            print('Conversión terminada.')

    # Conversión de PDF a TXT
    def pdfToTxt(self, pdf_path, txt_path, fname):
        try:
            subprocess.run(["pdftotext", pdf_path, txt_path])
            print(f"Archivo PDF convertido a TXT: {fname}")
        except Exception as ex:
            self.causes.append(f"No se pudo convertir PDF a TXT: \nERROR:{ex}")
            return False
        return True

    # Renombrar archivos según los metadatos
    def renameFiles(self):
        for name in self.getNameFiles(self.files_en):
            pdf_path = self.directories[3] + '/' + name + '.pdf'
            new_name = self.getNewName(pdf_path, name)
            if new_name:
                new_path = self.directories[3] + '/' + new_name + '.pdf'
                os.rename(pdf_path, new_path)
                print(f"Archivo renombrado: {name} -> {new_name}")

    # Obtener nuevo nombre del archivo basado en los metadatos
    def getNewName(self, pdf_path, name):
        try:
            result = subprocess.run(['pdfinfo', pdf_path], capture_output=True, text=True)
            metadata = result.stdout
            journal = self.extractMetadata(metadata, 'Title').replace(' ', '_')

            if journal:
                title = self.extractMetadata(metadata, 'Subject')
                if not title:
                    title = name
                return f"{journal}_{title.replace(' ', '_')}"
        except Exception as ex:
            self.causes.append(f"No se pudo extraer metadatos del PDF: {pdf_path}\nERROR: {ex}")
        return None

    # Extraer un campo específico de los metadatos
    def extractMetadata(self, metadata, field):
        for line in metadata.split('\n'):
            if line.startswith(field):
                return line.split(':', 1)[1].strip()
        return ''
    
    # Mostrar mensajes de advertencias y/o errores
    def emitErrorSignal(self):
        error_message = "\n".join(self.causes)  # Unir todas las causas en un mensaje de error
        self.errorSignal.emit(error_message)  # Emitir la señal con el mensaje de error

    # Listar los archivos de un directorio 
    def listFiles(self, directory):
        return os.listdir(directory)

    # Filtrar los archivos de acuerdo a una extensión (default: pdf)
    def filtFiles(self, files, extension='.pdf'):
        return [fname for fname in files if fname.endswith(extension)]

    # Devolver los nombres de los archivos
    def getNameFiles(self, files):
        return [os.path.splitext(fname)[0] for fname in files]

    # Devolver causas
    def getCauses(self):
        return self.causes

    # Validar si el directorio existe, sino, intentar crearlo y validar si se creó
    def dirExists(self, directory):
        return self.pathExists(directory) or self.createDir(directory)

    # Validar si una dirección existe
    def pathExists(self, directory):
        return os.path.exists(directory)
