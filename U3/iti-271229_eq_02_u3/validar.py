import os
from PIL import Image

def verify_images(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            try:
                img_path = os.path.join(root, file)
                img = Image.open(img_path)
                img.verify()  # Verifica que la imagen es válida
            except (IOError, SyntaxError) as e:
                print(f"Archivo inválido detectado y eliminado: {img_path}")
                os.remove(img_path)

# Verificar imágenes en las carpetas de entrenamiento
verify_images('data/train/Pemex')
verify_images('data/train/Mobil')
