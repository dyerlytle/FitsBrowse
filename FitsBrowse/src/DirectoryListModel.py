'''
Created on Aug 2, 2018

@author: dlytle
'''
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt5.QtGui import QColor

class DirectoryListModel(QAbstractTableModel):
    '''
    Given a current_directory this model backs up the other directory list.
    '''

    def __init__(self, current_directory):
        super(DirectoryListModel, self).__init__()
        self.current_directory = current_directory
        self.other_directories = current_directory.directories

    def data(self, index, role=Qt.DisplayRole):
        if (not index.isValid() or
            not (0 <= index.row() < len(self.other_directories))):
            return None
        a_directory = self.other_directories[index.row()]
        
        if role == Qt.DisplayRole:
            return a_directory.dir_name
        elif role == Qt.TextAlignmentRole:
            return int(Qt.AlignLeft|Qt.AlignVCenter)
        elif role == Qt.TextColorRole:
            return QColor(Qt.black)
        elif role == Qt.BackgroundColorRole:
            return QColor(230, 230, 230)
        return None
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            return int(Qt.AlignLeft|Qt.AlignVCenter)
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return "Directories"
        return int(section)
    
    def rowCount(self, index=QModelIndex()):
        return len(self.other_directories)
    
    def columnCount(self, index=QModelIndex()):
        return 1
