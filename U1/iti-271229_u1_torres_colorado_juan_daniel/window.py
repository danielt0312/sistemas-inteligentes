import sys
from PyQt6.QtWidgets import QApplication, QWidget

# Clase para la interfaz visual
class Window():
    def main():
        app = QApplication(sys.argv)

        w = QWidget()
        w.resize(500, 500)
        #w.move(300, 300)

        w.setWindowTitle('Interfaz')
        w.show()

        sys.exit(app.exec())
