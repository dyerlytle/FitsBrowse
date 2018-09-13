'''
Created on Jul 30, 2018

@author: dlytle
'''

import os

class OtherDirectory(object):
    
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.dir_name = os.path.basename(self.dir_path)