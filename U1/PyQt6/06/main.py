#!/usr/bin/python

"""
ZetCode PyQt6 tutorial

In this example, we position two push
buttons in the bottom-right corner
of the window.

Author: Jan Bodnar
Website: zetcode.com
"""

import sys
from PyQt6.QtWidgets import (QWidget, QPushButton,
        QHBoxLayout, QVBoxLayout, QApplication)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")
        TB = QPushButton("TB")

        hbox = QHBoxLayout()
        #hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)
        hbox.addWidget(TB)

        vbox = QVBoxLayout()
        vbox.addStretch(4)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Buttons')
        self.show()


def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
