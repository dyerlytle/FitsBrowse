'''
Created on Jul 30, 2018

@author: dlytle
'''

from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt5.QtGui import QColor

NAME, NAXIS1, NAXIS2, OBJNAME, OBSERVER, EXPTIME, FILTERS = range(7)

class FitsFileTableModel(QAbstractTableModel):
    
    def __init__(self, current_directory):
        super(FitsFileTableModel, self).__init__()
        self.current_directory = current_directory
        self.fits_files = current_directory.fits_files


    def sortByFileName(self):
        self.fits_files.file_name = sorted(self.fits_files.file_name)
        self.reset()


    def data(self, index, role=Qt.DisplayRole):
        if (not index.isValid() or
            not (0 <= index.row() < len(self.fits_files))):
            return None
        fits_file = self.fits_files[index.row()]
        column = index.column()
        
        if role == Qt.DisplayRole:
            return {
                NAME: fits_file.file_name,
                NAXIS1: str(fits_file.header_info["NAXIS1"]),
                NAXIS2: str(fits_file.header_info["NAXIS2"]),
                OBJNAME: fits_file.header_info["OBJNAME"],
                OBSERVER: fits_file.header_info["OBSERVER"],
                EXPTIME: str(fits_file.header_info["EXPTIME"]),
                FILTERS: fits_file.header_info["FILTERS"]
            }[column]
#             if column == NAME:
#                 return str(fits_file.file_name)
#             elif column == NAXIS1:
#                 return str(fits_file.header_info["NAXIS1"])
#             elif column == NAXIS2:
#                 return str(fits_file.header_info["NAXIS2"])
#             elif column == OBJNAME:
#                 return fits_file.header_info["OBJNAME"]
#             elif column == OBSERVER:
#                 return fits_file.header_info["OBSERVER"]
#             elif column == EXPTIME:
#                 return str(fits_file.header_info["EXPTIME"])
#             elif column == FILTERS:
#                 return fits_file.header_info["FILTERS"]
        elif role == Qt.TextAlignmentRole:
            if column == EXPTIME or column == NAXIS1 or column == NAXIS2:
                return int(Qt.AlignRight|Qt.AlignVCenter)
            return int(Qt.AlignLeft|Qt.AlignVCenter)
        elif role == Qt.TextColorRole:
            return QColor(Qt.black)
        elif role == Qt.BackgroundColorRole:
            if column == EXPTIME and fits_file.header_info["EXPTIME"] > 10.0:
                return QColor(250, 200, 200)
            if column == OBJNAME and 'flat' in fits_file.header_info["OBJNAME"]:
                return QColor(200, 200, 250)
            return QColor(230, 250, 230)
        return None


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return int(Qt.AlignLeft|Qt.AlignVCenter)
            return int(Qt.AlignRight|Qt.AlignVCenter)
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if section == NAME:
                return "File Name"
            elif section == NAXIS1:
                return "X Dim"
            elif section == NAXIS2:
                return "Y Dim"
            elif section == OBJNAME:
                return "Object Name"
            elif section == OBSERVER:
                return "Observer"
            elif section == EXPTIME:
                return "Exp Time"
            elif section == FILTERS:
                return "Filters"
        return int(section + 1)


    def rowCount(self, index=QModelIndex()):
        return len(self.fits_files)


    def columnCount(self, index=QModelIndex()):
        return 7