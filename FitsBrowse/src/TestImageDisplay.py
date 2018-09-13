'''
Created on Aug 6, 2018

@author: dlytle
'''

from PyQt5.QtWidgets import (QWidget, QMainWindow)


class TestImageDisplay(QMainWindow):

    def __init__(self, parent=None, width=5, height=5, dpi=100):
    
        super(TestImageDisplay, self).__init__(parent)
        self.main_widget = QWidget(self)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        self.show()