
import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QMessageBox, QVBoxLayout,
                             QMainWindow, QHBoxLayout,
                             QSplashScreen, QLabel, QPushButton,
                             QFrame)
from PyQt5 import QtCore
from PyQt5.Qt import QTableView, QListView

from PyQt5.QtGui import QPixmap
import os

from FitsTableModel import FitsFileTableModel
from CurrentDirectory import CurrentDirectory
from DirectoryListModel import DirectoryListModel
from ImageAnalyzer import ImageAnalyzer
from TestImageDisplay import TestImageDisplay

class FITSBrowse(QMainWindow):
    """ The main window of this GUI."""
    
    imdisp = None
    
    def __init__(self, parent=None):
        """ 
        """
        print("Skeet")
            
        super(FITSBrowse, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("FITSBrowse")

        self.current_directory = CurrentDirectory(
            "/data/lemi-archive-2016-04/20160427")
        self.model = FitsFileTableModel(self.current_directory)
        self.d_model = DirectoryListModel(self.current_directory)
        self.main_widget = QWidget(self)
        
        self.dir_text = "Current Directory: {0}".format(
            self.current_directory.cur_dir_path)
        self.cur_dir_label = QLabel(self.dir_text, self)
        
        self.listLabel = QLabel("&Directories")
        
        self.list_view = QListView()
        self.listLabel.setBuddy(self.list_view)
        self.list_view.setModel(self.d_model)
        self.list_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        self.list_view.setMinimumWidth(self.list_view.sizeHintForColumn(0))
        self.list_view.setMaximumWidth(self.list_view.sizeHintForColumn(0))
        
        self.list_view_sm = self.list_view.selectionModel()
        self.list_view.doubleClicked.connect(self.change_directory)
        
        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.table_view_sm = self.table_view.selectionModel()
        self.table_view.doubleClicked.connect(self.display_image)
        
        list_vbox = QVBoxLayout()
        list_vbox.addWidget(self.listLabel)
        list_vbox.addWidget(self.list_view)
        self.list_widget = QWidget()
        self.list_widget.setLayout(list_vbox)
        
        #self.list_view.size

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.list_widget)
        main_layout.addWidget(self.table_view)
        
        button_layout = QHBoxLayout()
        quit_button = QPushButton('Quit', self)
        quit_button.setToolTip('This button quits FITSBrowse')
        quit_button.clicked.connect(QApplication.instance().quit)
        button_layout.addStretch()
        button_layout.addWidget(quit_button)
        
        sep_line = QFrame()
        sep_line.setFrameShape(QFrame.HLine)
        
        super_layout = QVBoxLayout(self.main_widget)
        super_layout.addWidget(self.cur_dir_label)
        super_layout.addWidget(sep_line)
        super_layout.addLayout(main_layout)
        super_layout.addLayout(button_layout)
        
        self.setCentralWidget(self.main_widget)
        QtCore.QTimer.singleShot(0, self.initialLoad)
        x = self.table_view.frameSize()
        x = x.width()
        self.table_view.setMinimumWidth(x)
        self.main_widget.setMinimumHeight(500)
        
        
    def initialLoad(self):
        for column in (1,2,3,4,5,6,7):
            self.table_view.resizeColumnToContents(column)
        
            
    def display_image(self):
        indexes = self.table_view_sm.selectedIndexes()
        index = indexes[0]
        file_name = str(index.data())
        if (file_name.endswith("fits") or
            file_name.endswith("fit")): 
                file_with_path = os.path.join(
                    self.current_directory.cur_dir_path, file_name)
                self.im_disp = ImageAnalyzer(file_with_path, parent=self)
        
            
    def change_directory(self):
        indexes = self.list_view_sm.selectedRows()
        if (indexes != []):  
            index = indexes[0]
            new_directory = str(index.data())
            current_path = self.current_directory.cur_dir_path
            if (new_directory == ".."):
                # Go up one directory
                if (current_path == "/"):
                    # Do nothing.
                    pass
                else:
                    self.current_directory = CurrentDirectory(
                        os.path.dirname(current_path))
            else:
                # Go down into the selected directory.
                self.current_directory = CurrentDirectory(
                    os.path.join(current_path, new_directory))
            print("change directory, new directory is:", self.current_directory.
                  cur_dir_path)
            self.model = FitsFileTableModel(self.current_directory)
            self.d_model = DirectoryListModel(self.current_directory)
            
            self.dir_text = "Current Directory: {0}".format(
            self.current_directory.cur_dir_path)
            self.cur_dir_label.setText(self.dir_text)
            
            self.list_view.setModel(self.d_model)
            self.list_view_sm = self.list_view.selectionModel()
            self.list_view.update()
            self.list_view.setMinimumWidth(self.list_view.sizeHintForColumn(0))
            self.list_view.setMaximumWidth(self.list_view.sizeHintForColumn(0))
            
            self.table_view.setModel(self.model)
            self.table_view_sm = self.table_view.selectionModel()
            self.table_view.update()
            QtCore.QTimer.singleShot(0, self.initialLoad)
            x = self.table_view.frameSize()
            x = x.width()
            self.table_view.setMinimumWidth(x)
        else:
            print("no directory selected")
        
#         self.list_view.resizeColumnToContents(1)

if __name__ == '__main__':
    
    # Construct the QApplication.
    app = QApplication(sys.argv)
    
    rootDirectory = os.path.dirname(__file__)
    splash_pix = QPixmap(os.path.join(rootDirectory,
                    '../images/fitsbrowse-logo.png'))
    
    splash = QSplashScreen(splash_pix);
    splash.show();
    
    # Construct my main application window make it visible.
    ex = FITSBrowse()
    ex.show()
    ex.move(200,200)
    
    splash.finish(ex)
    # Run the application.  When the application exits, pass the return code
    # to the operating system.
    sys.exit(app.exec_())
    