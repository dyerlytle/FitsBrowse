'''
Created on Jul 30, 2018

@author: dlytle
'''

import os
from FitsFile import FitsFile
from OtherDirectory import OtherDirectory
from NotFitsFile import NotFitsFile

class CurrentDirectory(object):

    def __init__(self, cur_dir_path=""):
        self.cur_dir_path = cur_dir_path
        if (self.cur_dir_path == ""):
            self.cur_dir_path = os.getcwd()
        self.fits_files = list()
        self.directories = list()
        self.not_fits_files = list()
        self.load()


    def fitsInOrder(self):
        return sorted(self.fits_files.file_name)


    def load(self):
        
        self.directories.append(OtherDirectory(".."))
        with os.scandir(self.cur_dir_path) as it:
            for entry in it:
                if not entry.name.startswith('.'):
                    if entry.is_file():
                        file_path = os.path.join(self.cur_dir_path, entry.name)
                        if (entry.name.endswith("fits") or
                            entry.name.endswith("fit")):
                            self.fits_files.append(FitsFile(file_path))
                        else:
                            self.not_fits_files.append(NotFitsFile(file_path))
                    if entry.is_dir():
                        dir_path = os.path.join(self.cur_dir_path, entry.name)
                        self.directories.append(OtherDirectory(dir_path))
