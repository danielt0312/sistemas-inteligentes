#!/usr/bin/python

"""
ZetCode PyQt6 tutorial

This program creates a quit
button. When we press the button,
the application terminates.

Author: Jan Bodnar
Website: zetcode.com
"""

import sys
# from PyQt6.QtWidgets import QWidget, QPushButton, QApplication
# from PyQt6.QtWidgets import QWidget, QMessageBox, QApplication
from PyQt6.QtWigets import *

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        qbtn = QPushButton('Quit', self)
        # qbtn.clicked.connect(QApplication.instance().quit)
        qbtn.clicked.connect(self.FuncionParaHacerAlgo)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 50)
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Quit button')
        self.show()
        
    def FuncionParaHacerAlgo(self):
    	print ("Se termino la clase")
    	
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                    "Are you sure to quit?", QMessageBox.StandardButton.Yes |
                    QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
