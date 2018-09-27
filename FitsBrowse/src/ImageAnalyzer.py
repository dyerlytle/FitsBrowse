import sys

from PyQt5.QtWidgets import (QApplication, QPushButton, QVBoxLayout,
                             QMainWindow, QWidget)

from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg
                                                as FigureCanvas,
                                                NavigationToolbar2QT
                                                as NavigationToolbar)
from matplotlib.figure import Figure
from astropy.io import fits
from astropy.visualization import (MinMaxInterval, SqrtStretch, SquaredStretch,
                                   ImageNormalize, ZScaleInterval)


class ImageAnalyzer(QMainWindow):
    def __init__(self,
                 disp_file="/data/lemi-archive-2016-04/20160427/lmi.0229.fits",
                 parent=None, width=5, height=5, dpi=100):
        self.disp_file = disp_file
        self.width = width
        self.height = height
        self.dpi = dpi
        
        super(ImageAnalyzer, self).__init__(parent)

        # A widget for the image display, we will put in the main window.
        self.main_frame = QWidget()

        # A figure instance to plot on
        self.figure = Figure()

        # Canvas Widget that displays the `figure`. It takes the `figure`
        # instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # Navigation widget takes the Canvas widget and a parent.
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Set the layout, add widgets.
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.main_frame.setLayout(layout)

        self.setCentralWidget(self.main_frame)
        
        # Plot the data.
        self.plot()
        self.show()

    def plot(self):
        
        # Get the data from the FITS file.
        self.image_data = fits.getdata(self.disp_file, ext=0)
        # Crop 10% of image all the way around the edge.
        sz = self.image_data.shape
#         self.image_data = self.crop_center(self.image_data, int(sz[0]*0.8),
#                                               int(sz[1]*0.8))
        
        # Normalize the image as well as setting min/max and taking squareroot.
        self.norm = ImageNormalize(self.image_data,
                      interval=ZScaleInterval(), stretch=SqrtStretch())
#        interval=ZScaleInterval(), stretch=SqrtStretch())
        # Add a subplot and clear it.
        ax = self.figure.add_subplot(111)
        ax.clear()

        # Plot data.
        ax.imshow(self.image_data, cmap='gray', norm=self.norm)

        # Refresh canvas.
        self.canvas.draw()
        
    def crop_center(self, img, cropy, cropx):
        """ Crop the input 2D array (img) to the size indicated by
            (cropx,cropy).  The center of the image stays at the center."""
            
        y,x = img.shape
        
        startx = x//2-(cropx//2)
        starty = y//2-(cropy//2)    
        
        return img[starty:starty+cropy,startx:startx+cropx]

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # The main window.
    main = ImageAnalyzer()
    main.show()

    sys.exit(app.exec_())

