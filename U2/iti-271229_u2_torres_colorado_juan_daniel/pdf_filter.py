import os
import pdftotext

"""
Clase para procesar los archivos PDF 
"""
class PDFLector():
    # Constructor
    def __init__(self, dir_path = '.'):
        self.setDirPath(dir_path)
        self.cause = 'No se ha encontrado algún problema'
    
    # Actualizar Directorio
    def setDirPath(self, dir_path = '.'):
        self.dir_path = dir_path
        self.dir_docs = self.dir_path + '/documentos'
        self.dir_train = self.dir_docs + '/train'
        self.dir_docs_i = self.dir_docs + '/Inglés'
        self.dir_docs_e = self.dir_docs + '/Español'

    # Validación del archivo
    def isValid(self):
        self.findCause()
        return not (self.dir_path == '' or self.dir_path == None or len(self.dir_path) == 0)

    # Buscar causa en caso de haber un problema
    def findCause(self):
        if (self.dir_path == '' or self.dir_path == None or len(self.dir_path) == 0):
            self.cause = 'El directorio no fue proporcionado.'
        elif (os.path.exists(self.dir_path)):
            self.cause = 'El directorio ' + self.dir_path + 'no existe'
        else:
            self.cause = 'No se ha encontrado algún problema'
            return True
        return False

    # Devolver causa
    def getCause(self):
        return self.cause
    
    # Crear directorios para filtrar el idioma
    def createDirs(self):
        directories = [self.dir_docs, self.dir_train, self.dir_docs_i, self.dir_docs_e]
        for directory in directories:
            try:
                os.mkdir(directory)
                print(f"Carpeta creada: {directory}")
            except FileExistsError:
                print(f"*** Omitido*** Carpeta en existencia: {directory}")

    # Convertir el PDF a un archivo txt legible
    def pdfToTxt(pdf_path, txt_path):
        try:
            with open(pdf_path, "rb") as f:
                pdf_file = pdftotext.PDF(f)
            
            with open(txt_path, "w", encoding='utf-8') as txt_file:
                txt_file.write("\n\n".join(pdf_file))
            
            print(f"Archivo PDF convertido a TXT: {txt_path}")
        except Exception as e:
            print(f"Error al convertir PDF a TXT: {e}")