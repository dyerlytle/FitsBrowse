'''
Created on Jul 30, 2018

@author: dlytle
'''

import os
from astropy.io import fits

class FitsFile(object):
    '''
    This Class represents a FITS File.
    '''

    def __init__(self, file_path):
        ''' Constructor '''
        self.file_path = file_path
        self.file_name = os.path.basename(self.file_path)
        self.file_size = 0
        self.header_info = {}
        self.pixel_data = None
        self.init_header_info()
        

    def __hash__(self):
        return super(FitsFile, self).__hash__()


    def __lt__(self, other):
        return self.file_name.lower() < other.file_name.lower()
    
    
    def init_header_info(self):
        with fits.open(self.file_path) as hdul:
            head_dict = hdul[0].header
            
            self.header_info['NAXIS1'] = head_dict['NAXIS1']
            self.header_info['NAXIS2'] = head_dict['NAXIS2']
            
            if 'OBJNAME' in head_dict:
                self.header_info['OBJNAME'] = head_dict['OBJNAME']
            else:
                self.header_info['OBJNAME'] = 'unknown'
                
            if 'OBSERVER' in head_dict:
                self.header_info['OBSERVER'] = head_dict['OBSERVER']
            else:
                self.header_info['OBSERVER'] = 'unknown'
                
            if 'EXPTIME' in head_dict:
                self.header_info['EXPTIME'] = head_dict['EXPTIME']
            else:
                self.header_info['EXPTIME'] = 'unknown'
                
            if 'FILTERS' in head_dict:
                self.header_info['FILTERS'] = head_dict['FILTERS']
            else:
                self.header_info['FILTERS'] = 'unknown'
                