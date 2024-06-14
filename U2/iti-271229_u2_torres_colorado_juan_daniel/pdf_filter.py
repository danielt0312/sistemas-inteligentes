import os
# import pdftotext

"""
Clase para procesar los archivos PDF 
"""
class PDFLector():
    # Constructor
    def __init__(self, dir_path = '.'):
        self.setDirPath(dir_path)
        self.causes = []
    
    # Actualizar Directorio
    def setDirPath(self, dir_path = '.'):
        self.directories = [
            dir_path,   # raiz
            dir_path + '/documentos',
            dir_path + '/documentos/filter',
            dir_path + '/documentos/Inglés',
            dir_path + '/documentos/Español',
        ]

    # Validación de los directorios
    def isValid(self):
        return self.findCause()

    # Buscar causa en caso de haber un problema
    def findCause(self):
        self.causes.clear()     # limpiar  si hay causas antiguas
        
        # Validar todos los directorios
        for directory in self.directories:
            if not (self.validDir(directory) and self.dirExists(directory)):
                print (self.causes[-1])
        
        return len(self.causes) == 0    # válido si no hay causas    
    
    # Validar directorio proporcionado 
    def validDir(self, directory):
        if (directory == '' or directory == None or len(directory) == 0):
            self.causes.append(f"El directorio '{directory}' no fue correctamente proporcionado.")
            return False
        return True
    
    # Validar si el directorio existe, sino, intentar crearlo y validar si se creó
    def dirExists(self, directory):
        return (os.path.exists(directory) or self.createDir(directory))

    # Crear directorios
    def createDir(self, directory):
        try:
            os.mkdir(directory)
            print(f"Directorio creado: '{directory}'")
        except OSError as ex:
            self.causes.append(f"El directorio '{directory}' no se pudo crear. ERROR: {ex}")
            return False
        return True

    # # Convertir el PDF a un archivo txt legible
    # def pdfToTxt(pdf_path, txt_path):
    #     try:
    #         with open(pdf_path, "rb") as f:
    #             pdf_file = pdftotext.PDF(f)
            
    #         with open(txt_path, "w", encoding='utf-8') as txt_file:
    #             txt_file.write("\n\n".join(pdf_file))
            
    #         print(f"Archivo PDF convertido a TXT: {txt_path}")
    #     except Exception as e:
    #         print(f"Error al convertir PDF a TXT: {e}")
    
    # Devolver causas
    def getCauses(self):
        return self.causes