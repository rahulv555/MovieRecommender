from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class scrollLabel(QScrollArea):
    def __init__(self):
        QScrollArea.__init__(self)


        content = QWidget(self) 
        self.setWidget(content)

        # creating vertical box layout
        layout = QVBoxLayout(content)

        # label
        self.label = QLabel(content)

        # text allignment
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.label.setWordWrap(True)

        layout.addWidget(self.label)


    def setText(self, text):
        self.label.setText(text)
