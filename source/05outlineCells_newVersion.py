

# """
# PyQt seam cells analysis GUI

# NB: the python package tifffile (Gohlke) needs to be installed.

# author: Nicola Gritti
# last edited: June 2015
# """

# import sys
# from tifffile import *
# from generalFunctions import *
# import pickle
# import os
# from PyQt4 import QtGui, QtCore
# import numpy as np
# from matplotlib.figure import Figure
# import matplotlib.pyplot as plt
# from matplotlib.backend_bases import key_press_handler
# from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends import qt_compat
# import glob
# import pandas as pd
# use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE

# class GUI(QtGui.QWidget):
    
#     def __init__(self):

#         super(GUI, self).__init__()
        
#         self.setWindowTitle( 'Outline Cells' )
#         self.cellNames = ['1.p','4.a','1.pp','4.aa','1.ppa','1.ppp','4.aaa','4.aap','b_1','b_4']
#         self.initUI()
        
#     #-----------------------------------------------------------------------------------------------
#     # INITIALIZATION OF THE WINDOW - DEFINE AND PLACE ALL THE WIDGETS
#     #-----------------------------------------------------------------------------------------------

#     def initUI(self):
        
#         # SET THE GEOMETRY
        
#         mainWindow = QtGui.QVBoxLayout()
#         mainWindow.setSpacing(15)
        
#         fileBox = QtGui.QHBoxLayout()
#         spaceBox1 = QtGui.QHBoxLayout()
#         rawDataBox = QtGui.QHBoxLayout()
        
#         mainWindow.addLayout(fileBox)
#         mainWindow.addLayout(spaceBox1)
#         mainWindow.addLayout(rawDataBox)
        
#         Col1 = QtGui.QGridLayout()
#         Col2 = QtGui.QHBoxLayout()
#         Col3 = QtGui.QVBoxLayout()
        
#         rawDataBox.addLayout(Col1)
#         rawDataBox.addLayout(Col2)
#         rawDataBox.addLayout(Col3)
        
#         self.setLayout(mainWindow)

#         # DEFINE ALL WIDGETS AND BUTTONS
        
#         loadBtn = QtGui.QPushButton('Load DataSet')
#         saveBtn = QtGui.QPushButton('Save data (F12)')
        
#         tpLbl = QtGui.QLabel('Timepoint:')
#         slLbl = QtGui.QLabel('Slice:')
        
#         self.tp = QtGui.QSpinBox(self)
#         self.tp.setValue(0)
#         self.tp.setMaximum(100000)

#         self.sl = QtGui.QSpinBox(self)
#         self.sl.setValue(0)
#         self.sl.setMaximum(100000)
        
#         self._488nmBtn = QtGui.QRadioButton('488nm')
#         self._561nmBtn = QtGui.QRadioButton('561nm')
#         self.CoolLEDBtn = QtGui.QRadioButton('CoolLED')
        
#         self.sld1 = QtGui.QSlider(QtCore.Qt.Vertical, self)
#         self.sld1.setMaximum(2**16-1)
#         self.sld1.setValue(0)
#         self.sld2 = QtGui.QSlider(QtCore.Qt.Vertical, self)
#         self.sld2.setMaximum(2**16)
#         self.sld2.setValue(2**16-1)

#         self.fig1 = Figure((8.0, 8.0), dpi=100)
#         self.fig1.subplots_adjust(left=0., right=1., top=1., bottom=0.)
#         self.ax1 = self.fig1.add_subplot(111)
#         self.canvas1 = FigureCanvas(self.fig1)
#         self.canvas1.setFocusPolicy( QtCore.Qt.ClickFocus )
#         self.canvas1.setFocus()
#         self.canvas1.setFixedSize(QtCore.QSize(600,600))
#         self.canvas1.setSizePolicy( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding )

#         self.cellTbl = QtGui.QTableWidget()

#         self.fig2 = Figure((4.0, 4.0), dpi=100)
#         self.fig2.subplots_adjust(left=0., right=1., top=1., bottom=0.)
#         self.ax2 = self.fig2.add_subplot(111)
#         self.canvas2 = FigureCanvas(self.fig2)
#         self.canvas2.setFixedSize(QtCore.QSize(300,300))
#         self.canvas2.setSizePolicy( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding )

#         # PLACE ALL THE WIDGET ACCORDING TO THE GRIDS

#         fileBox.addWidget(loadBtn)
#         fileBox.addWidget(saveBtn)

#         spaceBox1.addWidget(self.HLine())

#         Col1.addWidget(tpLbl, 0, 0)#, 1, 1, Qt.AlignTop)
#         Col1.addWidget(self.tp, 0, 1)#, 1, 1, Qt.AlignTop)
#         Col1.addWidget(slLbl, 1, 0)#, 1, 1, Qt.AlignTop)
#         Col1.addWidget(self.sl, 1, 1)#, 1, 1, Qt.AlignTop)
#         Col1.addWidget(self._488nmBtn, 3, 0 )
#         Col1.addWidget(self._561nmBtn, 4, 0 )
#         Col1.addWidget(self.CoolLEDBtn, 5, 0 )
        
#         Col2.addWidget(self.sld1)
#         Col2.addWidget(self.sld2)
#         Col2.addWidget(self.canvas1)

#         Col3.addWidget(self.cellTbl)
#         Col3.addWidget(self.canvas2)
        
#         self.setFocus()
#         self.show()
        
#         # BIND BUTTONS TO FUNCTIONS
        
#         loadBtn.clicked.connect(self.selectWorm)
#         saveBtn.clicked.connect(self.saveData)

#         self.tp.valueChanged.connect(self.loadNewStack)
#         self.sl.valueChanged.connect(self.updateAllCanvas)
#         self.sld1.valueChanged.connect(self.updateAllCanvas)
#         self.sld2.valueChanged.connect(self.updateAllCanvas)

#         self._488nmBtn.toggled.connect(self.radioClicked)
#         self._561nmBtn.toggled.connect(self.radioClicked)
#         self.CoolLEDBtn.toggled.connect(self.radioClicked)

#         self.fig1.canvas.mpl_connect('button_press_event',self.onMouseClickOnCanvas1)        
#         self.fig1.canvas.mpl_connect('scroll_event',self.wheelEvent)        
#         # self.connect(mainWindow, SIGNAL("tabPressed"),self.keyPressEvent)        
#     #-----------------------------------------------------------------------------------------------
#     # FORMATTING THE WINDOW
#     #-----------------------------------------------------------------------------------------------

#     def center(self):
        
#         qr = self.frameGeometry()
#         cp = QtGui.QDesktopWidget().availableGeometry().center()
#         qr.moveCenter(cp)
#         self.move(qr.topLeft())
        
#     def HLine(self):
        
#         toto = QtGui.QFrame()
#         toto.setFrameShape(QtGui.QFrame.HLine)
#         toto.setFrameShadow(QtGui.QFrame.Sunken)
#         return toto

#     def VLine(self):
        
#         toto = QtGui.QFrame()
#         toto.setFrameShape(QtGui.QFrame.VLine)
#         toto.setFrameShadow(QtGui.QFrame.Sunken)
#         return toto

#     def heightForWidth(self, width):
        
#         return width
    
#     #-----------------------------------------------------------------------------------------------
#     # BUTTON FUNCTIONS
#     #-----------------------------------------------------------------------------------------------

#     def selectWorm(self):

#         self.pathDial = QtGui.QFileDialog.getExistingDirectory(self, 'Select a folder', 'Y:\\Images')
#         self.worm = self.pathDial.split("\\")[-1]
#         self.path = self.pathDial[:-len(self.worm)]
        
#         if not os.path.isfile(self.path+self.worm+'\\LEDmovie.tif'):
#             QtGui.QMessageBox.about(self,'Warning!','There is no movie in this folder! Create a movie first!')
#             return

#         # load the dataframe file
#         self.df = pickle.load( open(self.path + '\\worm' + self.worm.split('_')[0] + '.pickle','rb') )
#         if not( 'cXoutline' in self.df.keys().values ):
#             self.df['cXoutline'] = np.nan
#             self.df['cYoutline'] = np.nan
#             self.df.cXoutline = self.df.cXoutline.astype(object)
#             self.df.cYoutline = self.df.cYoutline.astype(object)
#             for i in np.arange(1,len(self.df.cXoutline.values)):    
#                 self.df.cXoutline.values[i] = np.array([np.nan])
#                 self.df.cYoutline.values[i] = np.array([np.nan])
#         else:
#             for i in np.arange(1,len(self.df.cXoutline.values)):
#                 if isinstance(self.df.cXoutline.values[i],float):
#                     self.df.cXoutline.values[i] = np.array([np.nan])
#                     self.df.cYoutline.values[i] = np.array([np.nan])

#         self.compression = self.df.ix[ self.df.rowtype == 'param', 'compression' ].values[0]
#         self.hatchingtidx = int( np.abs( np.min( self.df.ix[ self.df.rowtype== 'body', 'tidx' ].values ) ) )

#         self.tp.setValue( 0 )
#         self.setWindowTitle('Mark Cells - ' + self.pathDial)

#         # detect available channels
#         self.channels = []
#         chns = ['488nm','561nm','CoolLED']
#         for c in chns:
#             flist = glob.glob(self.path + self.worm + '\\z*'+c+'.tif')
#             if len(flist)>0:
#                 self.channels.append(c)
#         self.currentChannel = '488nm'

#         self.currentCell = ''

#         # read in all the metadata files
#         self.fMetaList = glob.glob(self.path + self.worm + '\\z*.txt')

#         self.tp.setMaximum(1000)
        
#         self.loadNewStack()

#         # self.pathDial.show()
#         self.updateAllCanvas()
#         self.setFocus()

#     def loadNewStack(self):
        
#         # print(self.fList['gfp'][self.tp.value()])
        
#         self.stacks = {}
#         for ch in self.channels:
#             filename = self.path+self.worm+'\\z%.3d_%s.tif'%(self.tp.value()+self.hatchingtidx+1,ch)
#             if os.path.isfile(filename):
#                 self.stacks[ch] = loadstack(filename)

#         if len( self.stacks.keys() ) > 0:
#             # print(self.stacks.keys(), self.stacksStraight)
#             self.sl.setMaximum(self.stacks[self.currentChannel].shape[0]-1)

#             self.setBCslidersMinMax()
        
#         tpmask = self.df.tidx == self.tp.value()
#         cellmask = self.df.rowtype == 'cell'

#         cnames = list( self.df.ix[tpmask&cellmask,'cname'].values )
#         cZpos = list( self.df.ix[tpmask&cellmask,'cZpos'].values )

#         print('labeled cells: ' + str(cnames) ) 
#         if len( cnames ) > 0:
#             self.currentCell = cnames[0]
#             self.sl.setValue(cZpos[0])
#         else:
#             self.currentCell = ''

#         # self.updateTable()
#         self.updateAllCanvas()

#     def saveData(self):
        
#         pickle.dump( self.df, open(self.path+'\\worm'+self.worm.split('_')[0]+'.pickle','wb'), protocol=2 )        
#         self.setFocus()
        
#     def updateAllCanvas(self):
#         self.updateRadioBtn()
#         self.updateCanvas1()
#         self.updateCanvas2()
        
#     def radioClicked(self):
#         if self._488nmBtn.isChecked():
#             if '488nm' in self.channels:
#                 self.currentChannel = '488nm'
#             else:
#                 QtGui.QMessageBox.about(self, 'Warning', 'No 488nm channel!')
#         elif self._561nmBtn.isChecked():
#             if '561nm' in self.channels:
#                 self.currentChannel = '561nm'
#             else:
#                 QtGui.QMessageBox.about(self, 'Warning', 'No 561nm channel!')
#         elif self.CoolLEDBtn.isChecked():
#             if 'CoolLED' in self.channels:
#                 self.currentChannel = 'CoolLED'
#             else:
#                 QtGui.QMessageBox.about(self, 'Warning', 'No CoolLED channel!')
#         self.setBCslidersMinMax()
#         self.resetBC()
#         self.setFocus()
#         self.updateAllCanvas()

#     #-----------------------------------------------------------------------------------------------
#     # DEFAULT FUNCTION FOR KEY AND MOUSE PRESS ON WINDOW
#     #-----------------------------------------------------------------------------------------------

#     def keyPressEvent(self, event):
        
#         # print(event.key())

#         # change timepoint
#         if event.key() == QtCore.Qt.Key_Right:
#             self.changeSpaceTime( self.tp, +1 )

#         elif event.key() == QtCore.Qt.Key_Left:
#             self.changeSpaceTime( self.tp, -1 )

#         # change slice
#         elif event.key() == QtCore.Qt.Key_Up:
#             self.changeSpaceTime( self.sl, +1 )
            
#         elif event.key() == QtCore.Qt.Key_Down:
#             self.changeSpaceTime( self.sl, -1 )

#         elif event.key() == QtCore.Qt.Key_Space:
#             tpmask = self.df.tidx == self.tp.value()
#             cellmask = self.df.rowtype == 'cell'

#             cnames = list(self.df.ix[tpmask&cellmask,'cname'].values)
#             cZpos = list(self.df.ix[tpmask&cellmask,'cZpos'].values)

#             idx = np.mod( cnames.index(self.currentCell)+1, len(cnames) )
#             if len( cnames ) > 0:
#                 self.currentCell = cnames[idx]
#                 self.sl.setValue(cZpos[idx])
#             else:
#                 self.currentCell = ''
#             self.updateAllCanvas()

#         self.setFocus()

#     def wheelEvent(self,event):
#         if self.canvas1.underMouse():
#             step = event.step
#         else:          
#             step = event.delta()/abs(event.delta())
#         self.sl.setValue( self.sl.value() + step) 

#     #-----------------------------------------------------------------------------------------------
#     # ADDITIONAL FUNCTIONS FOR KEY AND MOUSE PRESS ON CANVASES
#     #-----------------------------------------------------------------------------------------------

#     def onMouseClickOnCanvas1(self, event):

#         pos = np.array( [ int(event.xdata), int(event.ydata), int(self.sl.value()) ] )  

#         cellmask = self.df['cname'] == self.currentCell
#         tpmask = self.df['tidx'] == self.tp.value()
#         Xoutline = self.df.ix[ tpmask & cellmask, 'cXoutline'].values[0]
#         Youtline = self.df.ix[ tpmask & cellmask, 'cYoutline'].values[0]

#         if event.button == 1:

#             # create an empty cell: the only entries are tidx, times, xyzpos, side
#             Xoutline = np.append(Xoutline,pos[0])
#             Youtline = np.append(Youtline,pos[1])

#             # if the first line is still full of nan, remove it
#             if np.isnan(Xoutline[0]):
#                 Xoutline = Xoutline[1:]
#             if np.isnan(Youtline[0]):
#                 Youtline = Youtline[1:]

#         elif event.button == 3:
#             Xoutline = Xoutline[:-1]
#             Youtline = Youtline[:-1]

#         index = self.df.ix[tpmask&cellmask].index[0]
#         self.df.cXoutline.values[index] = Xoutline
#         self.df.cYoutline.values[index] = Youtline
#         self.df = self.df.sort(['tidx','rowtype','cZpos']).reset_index(drop=True)

#         self.updateCanvas1()
#         self.setFocus()
#         # print(event.button,event.xdata,event.ydata)

#     #-----------------------------------------------------------------------------------------------
#     # UTILS
#     #-----------------------------------------------------------------------------------------------

#     def updateRadioBtn(self):
#         if self.currentChannel == '488nm':
#             self._488nmBtn.setChecked(True)
#         elif self.currentChannel == '561nm':
#             self._561nmBtn.setChecked(True)
#         elif self.currentChannel == 'CoolLED':
#             self.CoolLEDBtn.setChecked(True)
#         self.setFocus()

#     def setBCslidersMinMax(self):
#         self.sld1.setMaximum(np.max(self.stacks[self.currentChannel]))
#         self.sld1.setMinimum(np.min(self.stacks[self.currentChannel]))
#         self.sld2.setMaximum(np.max(self.stacks[self.currentChannel]))
#         self.sld2.setMinimum(np.min(self.stacks[self.currentChannel]))

#     def resetBC(self):
#         self.sld1.setValue(np.min(self.stacks[self.currentChannel]))
#         self.sld2.setValue(np.max(self.stacks[self.currentChannel]))
        
#     def updateCanvas1(self):

#         if ( len( self.stacks.keys() ) == 0 ) or ( self.currentCell == '' ):
#             self.fig1.clf()
#             self.fig1.subplots_adjust(left=0., right=1., top=1., bottom=0.)
#             self.ax1 = self.fig1.add_subplot(111)
#             self.canvas1.draw()
#             return

#         # extract current cell data
#         tpmask = self.df.tidx == self.tp.value()
#         currentcellmask = self.df.cname == self.currentCell
#         cData = self.df.ix[tpmask&currentcellmask]

#         # plot the image
#         imgpxl = 51
#         self.ax1.cla()
#         imgplot = self.ax1.imshow(self.stacks[self.currentChannel][self.sl.value(),cData.cYpos-(imgpxl-1)/2:cData.cYpos+imgpxl-(imgpxl-1)/2,cData.cXpos-(imgpxl-1)/2:cData.cXpos+imgpxl-(imgpxl-1)/2], cmap = 'gray', interpolation = 'nearest')
        
#         # remove the white borders and plot outline and spline
#         self.ax1.autoscale(False)
#         self.ax1.axis('Off')
#         self.fig1.subplots_adjust(left=0., right=1., top=1., bottom=0.)

#         # print cell name
#         if cData.cZpos.values[0] == self.sl.value():
#             self.ax1.text( (imgpxl-1)/2, (imgpxl-1)/2+5, self.currentCell, color='yellow', size='small', alpha=.8,
#                     rotation=90, fontsize = 20)
#             self.ax1.plot( (imgpxl-1)/2, (imgpxl-1)/2, 'x', color='yellow', alpha = .8, ms = 10 )

#         # # draw outline
#         Xoutline = self.df.ix[tpmask&currentcellmask,'cXoutline'].values[0]
#         if len(Xoutline) > 1:
#             Xoutline = np.append(Xoutline, Xoutline[0])
#         Youtline = self.df.ix[tpmask&currentcellmask,'cYoutline'].values[0]
#         if len(Youtline) > 1:
#             Youtline = np.append(Youtline, Youtline[0])
#         self.ax1.plot( Xoutline, Youtline, '-x', color='yellow', ms=5, alpha=1., lw = .5 )      

#         # change brightness and contrast
#         self.sld1.setValue(np.min([self.sld1.value(),self.sld2.value()]))
#         self.sld2.setValue(np.max([self.sld1.value(),self.sld2.value()]))
#         imgplot.set_clim(self.sld1.value(), self.sld2.value())  

#         # redraw the canvas
#         self.canvas1.draw()
#         self.setFocus()

#     def updateCanvas2(self):
        
#         # plot the image
#         self.ax2.cla()
#         imgplot = self.ax2.imshow(self.stacks[self.currentChannel][self.sl.value()], cmap = 'gray')
        
#         # remove the white borders and plot outline and spline
#         self.ax2.autoscale(False)
#         self.ax2.axis('Off')
#         self.fig2.subplots_adjust(left=0., right=1., top=1., bottom=0.)

#         # cell text on the image
#         tpmask = self.df['tidx'] == self.tp.value()
#         cellmask = self.df['rowtype'] == 'cell'

#         for idx, cell in self.df[tpmask & cellmask].iterrows():

#             if cell.cZpos == self.sl.value():
#                 clabel = str(cell.cname)
#                 color = 'red'
#                 if clabel == self.currentCell:
#                     color = 'yellow'
#                 self.ax2.text( cell.cXpos, cell.cYpos + 10, clabel, color=color, size='small', alpha=.8,
#                         rotation=90)
#                 self.ax2.plot( cell.cXpos, cell.cYpos, 'x', color=color, alpha = .8 )


#         # redraw the canvas
#         self.canvas2.draw()
#         self.setFocus()

#     def changeSpaceTime(self, whatToChange, increment):

#         whatToChange.setValue( whatToChange.value() + increment )

# if __name__ == '__main__':
    
#     app = QtGui.QApplication.instance() # checks if QApplication already exists 
#     if not app: # create QApplication if it doesnt exist 
#         app = QtGui.QApplication(sys.argv)
    
#     gui = GUI()
#     app.setStyle("plastique")
#     # app.installEventFilter(gui)
#     sys.exit(app.exec_())
 



#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2010 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


# These are only needed for Python v2 but are harmless for Python v3.
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui


class ScribbleArea(QtGui.QWidget):
    """
      this scales the image but it's not good, too many refreshes really mess it up!!!
    """
    def __init__(self, parent=None):
        super(ScribbleArea, self).__init__(parent)

        self.setAttribute(QtCore.Qt.WA_StaticContents)
        self.modified = False
        self.scribbling = False
        self.myPenWidth = 1
        self.myPenColor = QtCore.Qt.blue
        imageSize = QtCore.QSize(500, 500)
#       self.image = QtGui.QImage()
        self.image = QtGui.QImage(imageSize, QtGui.QImage.Format_RGB32)
        self.lastPoint = QtCore.QPoint()

    def openImage(self, fileName):
        loadedImage = QtGui.QImage()
        if not loadedImage.load(fileName):
            return False

        w = loadedImage.width()
        h = loadedImage.height()    
        self.mainWindow.resize(w, h)

#       newSize = loadedImage.size().expandedTo(self.size())
#       self.resizeImage(loadedImage, newSize)
        self.image = loadedImage
        self.modified = False
        self.update()
        return True

    def saveImage(self, fileName, fileFormat):
        visibleImage = self.image
        self.resizeImage(visibleImage, self.size())

        if visibleImage.save(fileName, fileFormat):
            self.modified = False
            return True
        else:
            return False

    def setPenColor(self, newColor):
        self.myPenColor = newColor

    def setPenWidth(self, newWidth):
        self.myPenWidth = newWidth

    def clearImage(self):
        self.image.fill(QtGui.qRgb(255, 255, 255))
        self.modified = True
        self.update()

    def mousePressEvent(self, event):
#       print "self.image.width() = %d" % self.image.width()
#       print "self.image.height() = %d" % self.image.height()
#       print "self.image.size() = %s" % self.image.size()
#       print "self.size() = %s" % self.size()
#       print "event.pos() = %s" % event.pos()
        if event.button() == QtCore.Qt.LeftButton:
            self.lastPoint = event.pos()
            self.scribbling = True

    def mouseMoveEvent(self, event):
        if (event.buttons() & QtCore.Qt.LeftButton) and self.scribbling:
            self.drawLineTo(event.pos())

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.scribbling:
            self.drawLineTo(event.pos())
            self.scribbling = False

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(event.rect(), self.image)

    def resizeEvent(self, event):
#       print "resize event"
#       print "event = %s" % event
#       print "event.oldSize() = %s" % event.oldSize()
#       print "event.size() = %s" % event.size()

        self.resizeImage(self.image, event.size())

#       if self.width() > self.image.width() or self.height() > self.image.height():
#           newWidth = max(self.width() + 128, self.image.width())
#           newHeight = max(self.height() + 128, self.image.height())
#           print "newWidth = %d, newHeight = %d" % (newWidth, newHeight)
#           self.resizeImage(self.image, QtCore.QSize(newWidth, newHeight))
#           self.update()

        super(ScribbleArea, self).resizeEvent(event)

    def drawLineTo(self, endPoint):
        painter = QtGui.QPainter(self.image)
        painter.setPen(QtGui.QPen(self.myPenColor, self.myPenWidth,
            QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.drawLine(self.lastPoint, endPoint)
        self.modified = True

        # rad = self.myPenWidth / 2 + 2
        # self.update(QtCore.QRect(self.lastPoint, endPoint).normalized().adjusted(-rad, -rad, +rad, +rad))
        self.update()
        self.lastPoint = QtCore.QPoint(endPoint)

    def resizeImage(self, image, newSize):
        if image.size() == newSize:
            return

#       print "image.size() = %s" % repr(image.size())
#       print "newSize = %s" % newSize

# this resizes the canvas without resampling the image
        newImage = QtGui.QImage(newSize, QtGui.QImage.Format_RGB32)
        newImage.fill(QtGui.qRgb(255, 255, 255))
        painter = QtGui.QPainter(newImage)
        painter.drawImage(QtCore.QPoint(0, 0), image)


##  this resampled the image but it gets messed up with so many events...       
##      painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
##      painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
#       
#       newImage = QtGui.QImage(newSize, QtGui.QImage.Format_RGB32)
#       newImage.fill(QtGui.qRgb(255, 255, 255))
#       painter = QtGui.QPainter(newImage)
#       srcRect = QtCore.QRect(QtCore.QPoint(0,0), image.size())
#       dstRect = QtCore.QRect(QtCore.QPoint(0,0), newSize)
##      print "srcRect = %s" % srcRect
##      print "dstRect = %s" % dstRect
#       painter.drawImage(dstRect, image, srcRect)


        self.image = newImage

    def print_(self):
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)

        printDialog = QtGui.QPrintDialog(printer, self)
        if printDialog.exec_() == QtGui.QDialog.Accepted:
            painter = QtGui.QPainter(printer)
            rect = painter.viewport()
            size = self.image.size()
            size.scale(rect.size(), QtCore.Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.image.rect())
            painter.drawImage(0, 0, self.image)
            painter.end()

    def isModified(self):
        return self.modified

    def penColor(self):
        return self.myPenColor

    def penWidth(self):
        return self.myPenWidth


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.saveAsActs = []

        self.scribbleArea = ScribbleArea(self)
        self.scribbleArea.clearImage()
        self.scribbleArea.mainWindow = self  # maybe not using this?
        self.setCentralWidget(self.scribbleArea)

        self.createActions()
        self.createMenus()

        self.setWindowTitle("Scribble")
        self.resize(500, 500)

    def open(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, "Open File",
            QtCore.QDir.currentPath())
        if fileName:
            self.scribbleArea.openImage(fileName)


    def createActions(self):
        self.openAct = QtGui.QAction("&Open...", self, shortcut="Ctrl+O",
            triggered=self.open)

        for format in QtGui.QImageWriter.supportedImageFormats():
            format = str(format)

            text = format.upper() + "..."

        self.clearScreenAct = QtGui.QAction("&Clear Screen", self,
            shortcut="Ctrl+L", triggered=self.scribbleArea.clearImage)

    def createMenus(self):
        fileMenu = QtGui.QMenu("&File", self)
        fileMenu.addAction(self.openAct)
        fileMenu.addSeparator()

        self.menuBar().addMenu(fileMenu)



if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())