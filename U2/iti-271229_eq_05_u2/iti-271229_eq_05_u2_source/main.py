import sys
from window import *
from PyQt6.QtWidgets import QApplication

# Ejectuar como programa principal
if __name__ == '__main__':
    app = QApplication(sys.argv)
        
    window = Window()
    window.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Terminando programa...')