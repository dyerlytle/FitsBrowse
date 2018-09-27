'''
Created on Aug 6, 2018

@author: dlytle
'''

from PyQt5.QtWidgets import (QWidget, QApplication, QMessageBox, QVBoxLayout,
                             QMainWindow, QTableWidget, QHBoxLayout,
                             QSizePolicy, QLabel, QPushButton, QFrame,
                             QSizePolicy)
from PyQt5 import QtCore
from PyQt5.Qt import QTableView, QListView
from PyQt5.QtCore import Qt
import sys

from matplotlib.backends.backend_qt5agg import\
    FigureCanvasQTAgg as FigureCanvas

import matplotlib.image as mpimg
import numpy as np
from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector
import matplotlib.pyplot as plt
import os
from astropy.io import fits
from astropy.visualization import (MinMaxInterval, SqrtStretch, SquaredStretch,
                                   ImageNormalize, ZScaleInterval)

class ImageDisplay(QMainWindow):
    '''
    Image display widget for FitsBrowse.
    '''
    
    xoffset = 0
    yoffset = 0
    rs = None

    def __init__(self,
                 disp_file="/data/lemi-archive-2016-04/20160427/lmi.0229.fits",
                 parent=None, width=5, height=5, dpi=100):
    
        super(ImageDisplay, self).__init__(parent)
        
        self.disp_file = disp_file
        self.width = width
        self.height = height
        self.dpi = dpi
        self.parent = parent
        self.create_main_frame()
        #self.on_draw()
        
    def create_main_frame(self):
        self.main_frame = QWidget()

        # Set up the matplotlib figure.
        self.fig = Figure(figsize=(self.width, self.height), dpi=self.dpi)
        self.fig_canvas = FigureCanvas(self.fig)
        self.fig_canvas.setParent(self.main_frame)
        self.fig_canvas.setFocusPolicy(Qt.ClickFocus)
        self.fig_canvas.setFocus()
        self.axs = self.fig.gca()   # Get Current Axes
        
        self.fig_canvas.mpl_connect('key_press_event', self.on_key)
        self.fig_canvas.mpl_connect('key_press_event', self.on_key)
        
        # Put an image in the figure at startup.
        self.compute_initial_figure(self.disp_file)
        
        # Allow for the widget to expand/contract with the main widget.
        self.fig_canvas.setSizePolicy(QSizePolicy.Expanding,
                                      QSizePolicy.Expanding)
        self.fig_canvas.updateGeometry()
        
        # Set up another figure for plotting (can be used for focus plot).
        self.plotfigure = plt.figure()
        self.plotdisp = FigureCanvas(self.plotfigure)
        self.plotdisp.setMaximumHeight(150)
        
        layout = QVBoxLayout(self.main_frame)
        layout.addWidget(self.fig_canvas)
        layout.addWidget(self.plotdisp)
        self.main_frame.setLayout(layout)
        self.setCentralWidget(self.main_frame)
        self.setWindowTitle(self.disp_file)
        
        self.rs = RectangleSelector(self.axs,
                                    self.line_select_callback,
                                    drawtype='box', useblit=True,
                                    button=[1, 3],  # don't use middle button
                                    minspanx=5, minspany=5,
                                    spancoords='pixels',
                                    interactive=False)
        print(type(self.rs))
        

        self.show()
        
        
        # Offset each new ImageDisplay window by 20,20 pixels until
        # we get to 200,200, then reset back to 0,0.
        geo = self.geometry()
        self.move(geo.x() + ImageDisplay.xoffset,
                  geo.y() + ImageDisplay.yoffset)
        ImageDisplay.xoffset = ImageDisplay.xoffset + 20
        ImageDisplay.yoffset = ImageDisplay.yoffset + 20
        if (ImageDisplay.xoffset > 200):
            ImageDisplay.xoffset = 0
        if (ImageDisplay.yoffset > 200):
            ImageDisplay.yoffset = 0
            
    
    def line_select_callback(self, eclick, erelease):
        print("line_select_callback")
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata

        if (x1 > x2): x1, x2 = x2, x1
        if (y1 > y2): y1, y2 = y2, y1
        print(int(x1), int(x2))
        self.cropped_data = self.image_data[int(y1):int(y2), int(x1):int(x2)]
        print("doing imshow")
        self.axs.imshow(self.cropped_data, cmap='prism', norm=self.norm)
        #self.compute_initial_figure(self.disp_file)
        
    
    def reset_zoom(self):
            self.compute_initial_figure(self.disp_file)
            
            
    def on_key(self, event):
        print('you pressed', event.key, event.xdata, event.ydata)
        if(event.key == 'u'):
            self.reset_zoom()
        if event.key in ['Q', 'q'] and self.rs.active:
            print(' RectangleSelector deactivated.')
            self.rs.set_active(False)
        if event.key in ['A', 'a'] and not self.rs.active:
            print(' RectangleSelector activated.')
            self.rs.set_active(True)
            
                
    def compute_initial_figure(self, disp_file):
        try:
            # Read the image data from the FITS file.
            self.image_data = fits.getdata(disp_file, ext=0)
        
            # Normalise the data, stretch to Min/Max, and take the squareroot.
#             self.norm = ImageNormalize(self.image_data,
#                                        interval=MinMaxInterval(),
#                                        stretch=SqrtStretch())
            

            self.norm = ImageNormalize(self.image_data,
                      interval=ZScaleInterval(), stretch=SquaredStretch())
         
            # Plot image with "prism" color map and norm defined above.
            self.axs.imshow(self.image_data, cmap='gray', norm=self.norm)
         
        except Exception as e:
            print(e)
            print("Error reading and displaying FITS file")

#     def on_draw(self):
#         self.fig.clear()
#         self.axes = self.fig.add_subplot(111)
#         #self.axes.plot(self.x, self.y, 'ro')
#         self.norm = ImageNormalize(self.image_data,
#                                        interval=MinMaxInterval(),
#                                        stretch=SqrtStretch())
#         self.axes.imshow(self.image_data, cmap='prism', norm=self.norm)
#         self.fig_canvas.draw()

if (__name__ == "__main__"):
    app = QApplication(sys.argv)
    id = ImageDisplay()
    id.show()
    sys.exit(app.exec_())