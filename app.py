#!/usr/bin/python

"""
PyQt4 simple window with image viewer and tresholding slider
author: Giulio Ungaretti
"""


import sys
from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
from matplotlib.pyplot import imread
from skimage.morphology import label
import numpy as np
import os
from functions2 import load_bmp, get_scale, find_radius


class dot_fitter(QtGui.QWidget):

    def __init__(self):
        super(dot_fitter, self).__init__()
        self.initUI()

    def initUI(self):
        # base class is already a QtWidget
        self.setWindowTitle('tresholding')
        # layout
        l = QtGui.QGridLayout()
        # l.setRowStretch(0, 5)
        self.setLayout(l)
        # create number of plots
        self.dummy_plot_orig = pg.PlotItem(title='Tresholded image')
        self.dummy_plot_labl = pg.PlotItem(title='Labeled image')
        # enable auto range in the plots:
        self.dummy_plot_orig.enableAutoRange()
        self.dummy_plot_labl.enableAutoRange()
        # create the images using dummy as view
        self.image_orig = pg.ImageView(view=self.dummy_plot_orig)
        self.image_labl = pg.ImageView(view=self.dummy_plot_labl)
        # load image
        # self.image_array = imread('lowdose/10/IMAGE6039.bmp')

        self.image_array = imread(sys.argv[1])

        self.image_orig.setImage(self.image_array)
        # create slider
        self.sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.sld.setFocusPolicy(QtCore.Qt.NoFocus)
        # trun off tracking so that signal is emitted only at the end
        self.sld.setTracking(False)
        self.sld.setGeometry(30, 40, 105, 30)
        # connect slider change with fuction
        self.sld.valueChanged[int].connect(self.treshold)
        # text to see the value
        self.text = pg.TextItem('value: {}'.format(self.sld.value()))
        self.dummy_plot_orig.addItem(self.text)
        # add widgets
        # fromRow, int fromColumn, int rowSpan, int columnSpan
        # l.setRowStretch(2, 1)
        # add quit button
        bn = QtGui.QPushButton('continue', self)
        qtbn = QtGui.QPushButton('close', self)
        bn.clicked.connect(self.analyze)
        qtbn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        l.addWidget(self.image_orig, 0, 0, 1, 1)
        l.addWidget(self.image_labl, 0, 1, 1, 1)
        l.addWidget(self.sld, 1, 0, 1, 2)
        l.addWidget(bn, 2, 0, 1, 1)
        l.addWidget(qtbn, 2, 1, 1, 1)
        self.setWindowTitle('Dot Fitter')
        self.center()
        self.show()

    def treshold(self, value):
        value = 2 * value
        self.image_tresholded = (self.image_array > value)
        self.image_labeled = label(self.image_tresholded)
        self.image_labl.setImage(self.image_labeled)
        self.image_orig.setImage(np.ma.masked_array(self.image_tresholded,
                                 mask=(self.image_array > value)))
        self.text.setText('value {}'.format(value))
        self.tresh = value

    def center(self):
        '''
        centers  the window on the screen
        '''
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def analyze(self):
        self.folder = sys.argv[2]
        self.tresh = float(self.tresh)
        self.area = float(sys.argv[3])
        self.format = str(sys.argv[4])
        self.filenames = load_bmp(self.format, self.folder)
        try:
            sys.argv[5]
            screen = ':0.0'
            os.environ['DISPLAY'] = screen
            print 'remote plotting on screen{}'.format(screen)
        except Exception:
            print 'plotting locally'
        self.scale_factor = get_scale(self.folder, self.filenames)
        find_radius(self.folder,
                    scale_factor=self.scale_factor,
                    filenames=self.filenames,
                    area=self.area,
                    treshold=self.tresh)


def main():
    app = QtGui.QApplication(sys.argv)
    dotz = dot_fitter()
    sys.exit(app.exec_())
    return dotz

if __name__ == '__main__':
    dotz = main()
