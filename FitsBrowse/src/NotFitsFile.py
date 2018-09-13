'''
Created on Jul 30, 2018

@author: dlytle
'''

import os

class NotFitsFile(object):
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_name = os.path.basename(self.file_path)
