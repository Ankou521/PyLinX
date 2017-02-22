'''
Some PySide stuff - disorganized
'''
#import sys
# from PySide import QtCore, QtGui, QtUiTools
# 
# 
# 
# # def loadUiWidget(uifilename, parent=None):
# #     loader = QtUiTools.QUiLoader()
# #     uifile = QtCore.QFile(uifilename)
# #     uifile.open(QtCore.QFile.ReadOnly)
# #     ui = loader.load(uifile, parent)
# #     uifile.close()
# #     return ui
# # 
# # 
# # if __name__ == "__main__":
# #     import sys
# #     app = QtGui.QApplication(sys.argv)
# #     MainWindow = loadUiWidget("PyLinX_v0.ui")
# #     MainWindow.show()
# #     sys.exit(app.exec_())
#  
# class BQUiLoader(QtUiTools.QUiLoader):
#     def __init__(self, baseinstance):
#         #QtUiTools.QUiLoader.__init__(self)
#         super(BQUiLoader, self).__init__(baseinstance)
#         self.baseinstance = baseinstance
#   
# #     def createWidget(self, className, parent=None, name=""):
# #         widget = QtUiTools.QUiLoader.createWidget(self, className, parent, name)
# #         if parent is None:
# #             return self.baseinstance
# #         else:
# #             setattr(self.baseinstance, name, widget)
# #             return widget
# 
# 
# 
#     def createWidget(self, className, parent = None, name = ""):
#         if className in QtUiTools.QUiLoader.availableWidgets(self):
#             widget = QtUiTools.QUiLoader.createWidget(self, className, parent, name)
#         else:
#             if hasattr(self.baseinstance, "customWidgets"):
#                 if className in self.baseinstance.customWidgets.keys():
#                     widget = self.baseinstance.customWidgets[className](parent)
#                 else:
#                     raise KeyError("Unknown widget '%s'" % className)
#             else:
#                 raise AttributeError("Trying to load custom widget '%s', but base\
#                     instance '%s' does not specify custom widgets." % (className,\
#                     repr(self.baseinstance)))
#         
#         if self.baseinstance is not None:
#             setattr(self.baseinstance, name, widget)
#         
#         return widget
# 
# 
#  
# class MyWidget(QtGui.QWidget, QtCore.QObject):
#     def __init__(self, parent = None):
#         super(QtGui.QWidget, self).__init__(parent)
#         loader = BQUiLoader(None)
#         file = QtCore.QFile("PyLinX_v0.ui")
#         file.open(QtCore.QFile.ReadOnly)
#         myWidget = loader.load(file, self)
#         file.close()
#  
#         layout = QtGui.QVBoxLayout()
#         layout.addWidget(myWidget)
#         self.setLayout(layout)
#         self.show()
#          
# if __name__ == "__main__":
#     import sys
#     app = QtGui.QApplication(sys.argv)
#     myWindow = MyWidget()
#     sys.exit(app.exec_())
#      
#      
#  
# # 
# # def loadUi(uifile, baseinstance=None):
# #     loader = MyQUiLoader(baseinstance)
# #     ui = loader.load(uifile)
# #     QtCore.QMetaObject.connectSlotsByName(ui)
# #     return ui
# 
# # import sys
# # from PySide import QtGui
# #  
# # app = QtGui.QApplication(sys.argv)
# #  
# # win = QtGui.QWidget()
# #  
# # win.resize(320, 240)  
# # win.setWindowTitle("Hello, World!") 
# # win.show()
# #  
# # sys.exit(app.exec_())

'''
Interactive svg
'''

# 
# import sys
# from PyQt4 import QtCore, QtGui, QtSvg
# from PyQt4.QtWebKit import QGraphicsWebView
# if __name__ == "__main__":
#     app = QtGui.QApplication(sys.argv)
# 
#     scene = QtGui.QGraphicsScene()
#     view = QtGui.QGraphicsView(scene)
# 
#     br = QtSvg.QGraphicsSvgItem("your_interactive_svg.svg").boundingRect()
# 
#     webview = QGraphicsWebView()
#     webview.load(QtCore.QUrl("C:\your_interactive_svg.svg"))
#     webview.setFlags(QtGui.QGraphicsItem.ItemClipsToShape)
#     webview.setCacheMode(QtGui.QGraphicsItem.NoCache)
#     webview.resize(br.width(), br.height())
# 
#     scene.addItem(webview)
#     view.resize(br.width()+10, br.height()+10)
#     view.show()
#     sys.exit(app.exec_())
#     
'''
drag and drop
'''
    
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial

This is a simple drag and drop example. 

author: Jan Bodnar
website: zetcode.com
last edited: October 2013
"""

# import sys
# from PyQt4 import QtGui
# 
# 
# class Button(QtGui.QPushButton):
#   
#     def __init__(self, title, parent):
#         super(Button, self).__init__(title, parent)
#         
#         self.setAcceptDrops(True)
# 
#     def dragEnterEvent(self, e):
#       
#         if e.mimeData().hasFormat('text/plain'):
#             e.accept()
#             
#         else:
#             e.ignore() 
# 
#     def dropEvent(self, e):
#         
#         self.setText(e.mimeData().text()) 
# 
# 
# class Example(QtGui.QWidget):
#   
#     def __init__(self):
#         super(Example, self).__init__()
#         
#         self.initUI()
#         
#     def initUI(self):
# 
#         edit = QtGui.QLineEdit('', self)
#         edit.setDragEnabled(True)
#         edit.move(30, 65)
# 
#         button = Button("Button", self)
#         button.move(190, 65)
#         
#         self.setWindowTitle('Simple Drag & Drop')
#         self.setGeometry(300, 300, 300, 150)
#         self.show()
# 
# 
# def main():
#   
#     app = QtGui.QApplication([])
#     ex = Example()
#     app.exec_()  
#   
# 
# if __name__ == '__main__':
#     main()  

#!/usr/bin/env python

############################################################################
##
## Copyright (C) 2006-2006 Trolltech ASA. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## Licensees holding a valid Qt License Agreement may use this file in
## accordance with the rights, responsibilities and obligations
## contained therein.  Please consult your licensing agreement or
## contact sales@trolltech.com if any conditions of this licensing
## agreement are not clear to you.
##
## Further information about Qt licensing is available at:
## http://www.trolltech.com/products/qt/licensing.html or by
## contacting info@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
############################################################################

'''
Qt Graphics-View Example
'''

# from PyQt4 import QtCore, QtGui
# 
# #import dragdroprobot_rc
# 
# 
# class ColorItem(QtGui.QGraphicsItem):
#     n = 0
# 
#     def __init__(self):
#         super(ColorItem, self).__init__()
# 
#         self.color = QtGui.QColor(QtCore.qrand() % 256, QtCore.qrand() % 256,
#                 QtCore.qrand() % 256)
# 
#         self.setToolTip(
#             "QColor(%d, %d, %d)\nClick and drag this color onto the robot!" % 
#               (self.color.red(), self.color.green(), self.color.blue())
#         )
#         self.setCursor(QtCore.Qt.OpenHandCursor)
#     
#     def boundingRect(self):
#         return QtCore.QRectF(-15.5, -15.5, 34, 34)
# 
#     def paint(self, painter, option, widget):
#         painter.setPen(QtCore.Qt.NoPen)
#         painter.setBrush(QtCore.Qt.darkGray)
#         painter.drawEllipse(-12, -12, 30, 30)
#         painter.setPen(QtGui.QPen(QtCore.Qt.black, 1))
#         painter.setBrush(QtGui.QBrush(self.color))
#         painter.drawEllipse(-15, -15, 30, 30)
# 
#     def mousePressEvent(self, event):
#         if event.button() != QtCore.Qt.LeftButton:
#             event.ignore()
#             return
# 
#         self.setCursor(QtCore.Qt.ClosedHandCursor)
# 
#     def mouseMoveEvent(self, event):
#         if QtCore.QLineF(QtCore.QPointF(event.screenPos()), QtCore.QPointF(event.buttonDownScreenPos(QtCore.Qt.LeftButton))).length() < QtGui.QApplication.startDragDistance():
#             return
# 
#         drag = QtGui.QDrag(event.widget())
#         mime = QtCore.QMimeData()
#         drag.setMimeData(mime)
# 
#         ColorItem.n += 1
#         if ColorItem.n > 2 and QtCore.qrand() % 3 == 0:
#             image = QtGui.QImage(':/images/head.png')
#             mime.setImageData(image)
#             drag.setPixmap(QtGui.QPixmap.fromImage(image).scaled(30,40))
#             drag.setHotSpot(QtCore.QPoint(15, 30))
#         else:
#             mime.setColorData(self.color)
#             mime.setText("#%02x%02x%02x" % (self.color.red(), self.color.green(), self.color.blue()))
# 
#             pixmap = QtGui.QPixmap(34, 34)
#             pixmap.fill(QtCore.Qt.white)
# 
#             painter = QtGui.QPainter(pixmap)
#             painter.translate(15, 15)
#             painter.setRenderHint(QtGui.QPainter.Antialiasing)
#             self.paint(painter, None, None)
#             painter.end()
# 
#             pixmap.setMask(pixmap.createHeuristicMask())
# 
#             drag.setPixmap(pixmap)
#             drag.setHotSpot(QtCore.QPoint(15, 20))
# 
#         drag.exec_()
#         self.setCursor(QtCore.Qt.OpenHandCursor)
# 
#     def mouseReleaseEvent(self, event):
#         self.setCursor(QtCore.Qt.OpenHandCursor)
# 
# 
# class RobotPart(QtGui.QGraphicsItem):
#     def __init__(self, parent=None):
#         super(RobotPart, self).__init__(parent)
# 
#         self.color = QtGui.QColor(QtCore.Qt.lightGray)
#         self.pixmap = None
#         self.dragOver = False
# 
#         self.setAcceptDrops(True)
# 
#     def dragEnterEvent(self, event):
#         if event.mimeData().hasColor() or \
#           (isinstance(self, RobotHead) and event.mimeData().hasImage()):
#             event.setAccepted(True)
#             self.dragOver = True
#             self.update()
#         else:
#             event.setAccepted(False)
# 
#     def dragLeaveEvent(self, event):
#         self.dragOver = False
#         self.update()
#  
#     def dropEvent(self, event):
#         self.dragOver = False
#         if event.mimeData().hasColor():
#             self.color = QtGui.QColor(event.mimeData().colorData())
#         elif event.mimeData().hasImage():
#             self.pixmap = QtGui.QPixmap(event.mimeData().imageData())
# 
#         self.update()
# 
# 
# class RobotHead(RobotPart):
#     def boundingRect(self):
#         return QtCore.QRectF(-15, -50, 30, 50)
# 
#     def paint(self, painter, option, widget=None):
#         if not self.pixmap:
#             painter.setBrush(self.dragOver and self.color.light(130) 
#                                             or self.color)
#             painter.drawRoundedRect(-10, -30, 20, 30, 25, 25,
#                     QtCore.Qt.RelativeSize)
#             painter.setBrush(QtCore.Qt.white)
#             painter.drawEllipse(-7, -3 - 20, 7, 7)
#             painter.drawEllipse(0, -3 - 20, 7, 7)
#             painter.setBrush(QtCore.Qt.black)
#             painter.drawEllipse(-5, -1 - 20, 2, 2)
#             painter.drawEllipse(2, -1 - 20, 2, 2)
#             painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
#             painter.setBrush(QtCore.Qt.NoBrush)
#             painter.drawArc(-6, -2 - 20, 12, 15, 190 * 16, 160 * 16)
#         else:
#             painter.scale(.2272, .2824)
#             painter.drawPixmap(QtCore.QPointF(-15*4.4, -50*3.54), self.pixmap)
# 
# 
# class RobotTorso(RobotPart):
#     def boundingRect(self):
#         return QtCore.QRectF(-30, -20, 60, 60)
# 
#     def paint(self, painter, option, widget=None):
#         painter.setBrush(self.dragOver and self.color.light(130) 
#                                         or self.color)
#         painter.drawRoundedRect(-20, -20, 40, 60, 25, 25,
#                 QtCore.Qt.RelativeSize)
#         painter.drawEllipse(-25, -20, 20, 20)
#         painter.drawEllipse(5, -20, 20, 20)
#         painter.drawEllipse(-20, 22, 20, 20)
#         painter.drawEllipse(0, 22, 20, 20)
# 
# 
# class RobotLimb(RobotPart):
#     def boundingRect(self):
#         return QtCore.QRectF(-5, -5, 40, 10)
# 
#     def paint(self, painter, option, widget=None):
#         painter.setBrush(self.dragOver and self.color.light(130) or self.color)
#         painter.drawRoundedRect(self.boundingRect(), 50, 50,
#                 QtCore.Qt.RelativeSize)
#         painter.drawEllipse(-5, -5, 10, 10)
# 
# 
# class Robot(RobotPart):
#     def __init__(self):
#         super(Robot, self).__init__()
# 
#         self.torsoItem         = RobotTorso(self)
#         self.headItem          = RobotHead(self.torsoItem)
#         self.upperLeftArmItem  = RobotLimb(self.torsoItem)
#         self.lowerLeftArmItem  = RobotLimb(self.upperLeftArmItem)
#         self.upperRightArmItem = RobotLimb(self.torsoItem)
#         self.lowerRightArmItem = RobotLimb(self.upperRightArmItem)
#         self.upperRightLegItem = RobotLimb(self.torsoItem)
#         self.lowerRightLegItem = RobotLimb(self.upperRightLegItem)
#         self.upperLeftLegItem  = RobotLimb(self.torsoItem)
#         self.lowerLeftLegItem  = RobotLimb(self.upperLeftLegItem)
# 
#         self.timeline = QtCore.QTimeLine()
#         settings = [
#         #             item               position    rotation at
#         #                                 x    y    time 0  /  1
#             ( self.headItem,              0,  -18,      20,   -20 ),
#             ( self.upperLeftArmItem,    -15,  -10,     190,   180 ),
#             ( self.lowerLeftArmItem,     30,    0,      50,    10 ),
#             ( self.upperRightArmItem,    15,  -10,     300,   310 ),
#             ( self.lowerRightArmItem,    30,    0,       0,   -70 ),
#             ( self.upperRightLegItem,    10,   32,      40,   120 ),
#             ( self.lowerRightLegItem,    30,    0,      10,    50 ),
#             ( self.upperLeftLegItem,    -10,   32,     150,    80 ),
#             ( self.lowerLeftLegItem,     30,    0,      70,    10 ),
#             ( self.torsoItem,             0,    0,       5,   -20 )
#         ]
#         self.animations = []
#         for item, pos_x, pos_y, rotation1, rotation2 in settings: 
#             item.setPos(pos_x,pos_y)
#             animation = QtGui.QGraphicsItemAnimation()
#             animation.setItem(item)
#             animation.setTimeLine(self.timeline)
#             animation.setRotationAt(0, rotation1)
#             animation.setRotationAt(1, rotation2)
#             self.animations.append(animation)
#         self.animations[0].setScaleAt(1, 1.1, 1.1)
#     
#         self.timeline.setUpdateInterval(1000 / 25)
#         self.timeline.setCurveShape(QtCore.QTimeLine.SineCurve)
#         self.timeline.setLoopCount(0)
#         self.timeline.setDuration(2000)
#         self.timeline.start()
# 
#     def boundingRect(self):
#         return QtCore.QRectF()
# 
#     def paint(self, painter, option, widget=None):
#         pass
# 
# 
# if __name__== '__main__':
# 
#     import sys
#     import math
# 
#     app = QtGui.QApplication(sys.argv)
# 
#     QtCore.qsrand(QtCore.QTime(0, 0, 0).secsTo(QtCore.QTime.currentTime()))
# 
#     scene = QtGui.QGraphicsScene(-200, -200, 400, 400)
# 
#     for i in range(10):
#         item = ColorItem()
#         angle = i*6.28 / 10.0
#         item.setPos(math.sin(angle)*150, math.cos(angle)*150)
#         scene.addItem(item)
# 
#     robot = Robot()
#     robot.scale(1.4, 1.4)
#     robot.setPos(0, -20)
#     scene.addItem(robot)
# 
#     view = QtGui.QGraphicsView(scene)
#     view.setRenderHint(QtGui.QPainter.Antialiasing)
#     view.setViewportUpdateMode(QtGui.QGraphicsView.BoundingRectViewportUpdate)
#     view.setBackgroundBrush(QtGui.QColor(230, 200, 167))
#     view.setWindowTitle("Drag and Drop Robot")
#     view.show()
# 
#     sys.exit(app.exec_())

#!/usr/bin/env python

# -*- coding: utf-8 -*-
#!/usr/bin/env python

'''
Simple GUI
'''
# from PyQt4 import QtGui, QtCore
# 
# class Images(QtGui.QScrollArea):
#     def __init__(self, images):
#         super(Images, self).__init__()
# 
#         self.content = QtGui.QWidget()
#         self.layout = QtGui.QGridLayout(self.content)
#         self.layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
#         col = 0
#         for image in images:
#             thumb = QtGui.QLabel()
#             thumb.setPixmap(QtGui.QPixmap(image))
#             self.layout.addWidget(thumb, 0, col)
#             col += 1
# 
#         self.setWidget(self.content)
#         self.setMinimumWidth(self.content.sizeHint().width())
#         self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
# 
# app = QtGui.QApplication([])
# 
# window = QtGui.QWidget()
# layout = QtGui.QVBoxLayout(window)
# scroll_area = Images(['hallo.png','hallo.png','hallo.png','hallo.png'])
# layout.addWidget(scroll_area)
# window.show()
# 
# app.exec_()

#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2005-2005 Trolltech AS. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## This file may be used under the terms of the GNU General Public
## License version 2.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http://www.trolltech.com/products/qt/opensource.html
##
## If you are unsure which license is appropriate for your use, please
## review the following information:
## http://www.trolltech.com/products/qt/licensing.html or contact the
## sales department at sales@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
#############################################################################
'''
Bildbetrachter
'''
# from PyQt4 import QtCore, QtGui
# 
# 
# class ImageViewer(QtGui.QMainWindow):
#     def __init__(self):
#         super(ImageViewer, self).__init__()
# 
#         self.printer = QtGui.QPrinter()
#         self.scaleFactor = 0.0
# 
#         self.imageLabel = QtGui.QLabel()
#         self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
#         self.imageLabel.setSizePolicy(QtGui.QSizePolicy.Ignored,
#                 QtGui.QSizePolicy.Ignored)
#         self.imageLabel.setScaledContents(True)
# 
#         self.scrollArea = QtGui.QScrollArea()
#         self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
#         self.scrollArea.setWidget(self.imageLabel)
#         self.setCentralWidget(self.scrollArea)
# 
#         self.createActions()
#         self.createMenus()
# 
#         self.setWindowTitle("Image Viewer")
#         self.resize(500, 400)
# 
#     def open(self):
#         fileName = QtGui.QFileDialog.getOpenFileName(self, "Open File",
#                 QtCore.QDir.currentPath())
#         if fileName:
#             image = QtGui.QImage(fileName)
#             if image.isNull():
#                 QtGui.QMessageBox.information(self, "Image Viewer",
#                         "Cannot load %s." % fileName)
#                 return
# 
#             self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))
#             self.scaleFactor = 1.0
# 
#             self.printAct.setEnabled(True)
#             self.fitToWindowAct.setEnabled(True)
#             self.updateActions()
# 
#             if not self.fitToWindowAct.isChecked():
#                 self.imageLabel.adjustSize()
# 
#     def print_(self):
#         dialog = QtGui.QPrintDialog(self.printer, self)
#         if dialog.exec_():
#             painter = QtGui.QPainter(self.printer)
#             rect = painter.viewport()
#             size = self.imageLabel.pixmap().size()
#             size.scale(rect.size(), QtCore.Qt.KeepAspectRatio)
#             painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
#             painter.setWindow(self.imageLabel.pixmap().rect())
#             painter.drawPixmap(0, 0, self.imageLabel.pixmap())
# 
#     def zoomIn(self):
#         self.scaleImage(1.25)
# 
#     def zoomOut(self):
#         self.scaleImage(0.8)
# 
#     def normalSize(self):
#         self.imageLabel.adjustSize()
#         self.scaleFactor = 1.0
# 
#     def fitToWindow(self):
#         fitToWindow = self.fitToWindowAct.isChecked()
#         self.scrollArea.setWidgetResizable(fitToWindow)
#         if not fitToWindow:
#             self.normalSize()
# 
#         self.updateActions()
# 
#     def about(self):
#         QtGui.QMessageBox.about(self, "About Image Viewer",
#                 "<p>The <b>Image Viewer</b> example shows how to combine "
#                 "QLabel and QScrollArea to display an image. QLabel is "
#                 "typically used for displaying text, but it can also display "
#                 "an image. QScrollArea provides a scrolling view around "
#                 "another widget. If the child widget exceeds the size of the "
#                 "frame, QScrollArea automatically provides scroll bars.</p>"
#                 "<p>The example demonstrates how QLabel's ability to scale "
#                 "its contents (QLabel.scaledContents), and QScrollArea's "
#                 "ability to automatically resize its contents "
#                 "(QScrollArea.widgetResizable), can be used to implement "
#                 "zooming and scaling features.</p>"
#                 "<p>In addition the example shows how to use QPainter to "
#                 "print an image.</p>")
# 
#     def createActions(self):
#         self.openAct = QtGui.QAction("&Open...", self, shortcut="Ctrl+O",
#                 triggered=self.open)
# 
#         self.printAct = QtGui.QAction("&Print...", self, shortcut="Ctrl+P",
#                 enabled=False, triggered=self.print_)
# 
#         self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",
#                 triggered=self.close)
# 
#         self.zoomInAct = QtGui.QAction("Zoom &In (25%)", self,
#                 shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)
# 
#         self.zoomOutAct = QtGui.QAction("Zoom &Out (25%)", self,
#                 shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)
# 
#         self.normalSizeAct = QtGui.QAction("&Normal Size", self,
#                 shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)
# 
#         self.fitToWindowAct = QtGui.QAction("&Fit to Window", self,
#                 enabled=False, checkable=True, shortcut="Ctrl+F",
#                 triggered=self.fitToWindow)
# 
#         self.aboutAct = QtGui.QAction("&About", self, triggered=self.about)
# 
#         self.aboutQtAct = QtGui.QAction("About &Qt", self,
#                 triggered=QtGui.qApp.aboutQt)
# 
#     def createMenus(self):
#         self.fileMenu = QtGui.QMenu("&File", self)
#         self.fileMenu.addAction(self.openAct)
#         self.fileMenu.addAction(self.printAct)
#         self.fileMenu.addSeparator()
#         self.fileMenu.addAction(self.exitAct)
# 
#         self.viewMenu = QtGui.QMenu("&View", self)
#         self.viewMenu.addAction(self.zoomInAct)
#         self.viewMenu.addAction(self.zoomOutAct)
#         self.viewMenu.addAction(self.normalSizeAct)
#         self.viewMenu.addSeparator()
#         self.viewMenu.addAction(self.fitToWindowAct)
# 
#         self.helpMenu = QtGui.QMenu("&Help", self)
#         self.helpMenu.addAction(self.aboutAct)
#         self.helpMenu.addAction(self.aboutQtAct)
# 
#         self.menuBar().addMenu(self.fileMenu)
#         self.menuBar().addMenu(self.viewMenu)
#         self.menuBar().addMenu(self.helpMenu)
# 
#     def updateActions(self):
#         self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
#         self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
#         self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())
# 
#     def scaleImage(self, factor):
#         self.scaleFactor *= factor
#         self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())
# 
#         self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
#         self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)
# 
#         self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
#         self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)
# 
#     def adjustScrollBar(self, scrollBar, factor):
#         scrollBar.setValue(int(factor * scrollBar.value()
#                                 + ((factor - 1) * scrollBar.pageStep()/2)))
# 
# 
# if __name__ == '__main__':
# 
#     import sys
# 
#     app = QtGui.QApplication(sys.argv)
#     imageViewer = ImageViewer()
#     imageViewer.show()
#     sys.exit(app.exec_())

'''
Diamond example
'''

# class First(object):
#     def __init__(self):
#         print "first"
#         self.test = "test"
# 
# class Second(First):
#     def __init__(self):
#         super(Second, self).__init__()
#         print "second"
# 
# class Third(First):
#     def __init__(self):
#         super(Third,self).__init__()
#         print "third"
# 
# class Fourth(Second, Third):
#     def __init__(self):
#         super(Fourth, self).__init__()
#         print "that's it"
#         
# fourth = Fourth()
# print "Ende!"

'''
Font size
'''

# from PyQt4 import QtGui, QtCore
# 
# class Window(QtGui.QWidget):
#     def __init__(self):
#         QtGui.QWidget.__init__(self)
#         self.setAutoFillBackground(True)
#         self.setBackgroundRole(QtGui.QPalette.Mid)
#         self.setLayout(QtGui.QFormLayout(self))
#         self.fonts = QtGui.QFontComboBox(self)
#         self.fonts.currentFontChanged.connect(self.handleFontChanged)
#         self.layout().addRow('font:', self.fonts)
#         for text in (
#             u'H\u2082SO\u2084 + Be',
#             u'jib leaf jib leaf',
#             ):
#             for label in ('boundingRect', 'width', 'size'):
#                 field = QtGui.QLabel(text, self)
#                 field.setStyleSheet('background-color: yellow')
#                 field.setAlignment(QtCore.Qt.AlignCenter)
#                 self.layout().addRow(label, field)
#         self.handleFontChanged(self.font())
# 
#     def handleFontChanged(self, font):
#         layout = self.layout()
#         font.setPointSize(20)
#         metrics = QtGui.QFontMetrics(font)
#         for index in range(1, layout.rowCount()):
#             field = layout.itemAt(index, QtGui.QFormLayout.FieldRole).widget()
#             label = layout.itemAt(index, QtGui.QFormLayout.LabelRole).widget()
#             method = label.text().split(' ')[0]
#             text = field.text()
#             if method == 'width':
#                 width = metrics.width(text)
#             elif method == 'size':
#                 width = metrics.size(field.alignment(), text).width()
#             else:
#                 width = metrics.boundingRect(text).width()
#             field.setFixedWidth(width)
#             field.setFont(font)
#             label.setText('%s (%d):' % (method, width))
# 
# if __name__ == '__main__':
# 
#     import sys
#     app = QtGui.QApplication(sys.argv)
#     window = Window()
#     window.show()
#     sys.exit(app.exec_())

'''Example Code'''

# def calcMain():
#     
#     global DataDictionary
#     
#     Variable_3 = DataDictionary["Variable_3"]
#     Variable_1 = DataDictionary["Variable_1"]
#     Variable_2 = DataDictionary["Variable_2"]
#     
#     Variable_3 = Variable_1 + Variable_2
#     
#     DataDictionary["Variable_3"] = Variable_3
#     DataDictionary["Variable_1"] = Variable_1
#     DataDictionary["Variable_2"] = Variable_2
#     
'''
Context menu
'''
# import sys
# from PyQt4 import QtGui, QtCore
# 
# class MainForm(QtGui.QMainWindow):
#     def __init__(self, parent=None):
#         super(MainForm, self).__init__(parent)
# 
#         # create button
#         self.button = QtGui.QPushButton("test button", self)       
#         self.button.resize(100, 30)
# 
#         # set button context menu policy
#         self.button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
#         self.connect(self.button, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), self.on_context_menu)
# 
#         # create context menu
#         self.popMenu = QtGui.QMenu(self)
#         self.popMenu.addAction(QtGui.QAction('test0', self))
#         self.popMenu.addAction(QtGui.QAction('test1', self))
#         self.popMenu.addSeparator()
#         self.popMenu.addAction(QtGui.QAction('test2', self))        
# 
#     def on_context_menu(self, point):
#         # show context menu
#         self.popMenu.exec_(self.button.mapToGlobal(point))        
# 
# def main():
#     app = QtGui.QApplication(sys.argv)
#     form = MainForm()
#     form.show()
#     app.exec_()
# 
# if __name__ == '__main__':
#     main()

#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2004-2005 Trolltech AS. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## This file may be used under the terms of the GNU General Public
## License version 2.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http://www.trolltech.com/products/qt/opensource.html
##
## If you are unsure which license is appropriate for your use, please
## review the following information:
## http://www.trolltech.com/products/qt/licensing.html or contact the
## sales department at sales@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
#############################################################################

'''
Example Qt-GUI
'''

# from PyQt4 import QtCore, QtGui
#  
#  
# class Window(QtGui.QWidget):
#     def __init__(self, parent=None):
#         super(Window, self).__init__(parent)
#  
#         grid = QtGui.QGridLayout()
#         grid.addWidget(self.createFirstExclusiveGroup(), 0, 0)
#         grid.addWidget(self.createSecondExclusiveGroup(), 1, 0)
#         grid.addWidget(self.createNonExclusiveGroup(), 0, 1)
#         grid.addWidget(self.createPushButtonGroup(), 1, 1)
#         self.setLayout(grid)
#  
#         self.setWindowTitle("Group Box")
#         self.resize(480, 320)
#  
#     def createFirstExclusiveGroup(self):
#         groupBox = QtGui.QGroupBox("Exclusive Radio Buttons")
#  
#         radio1 = QtGui.QRadioButton("&Radio button 1")
#         radio2 = QtGui.QRadioButton("R&adio button 2")
#         radio3 = QtGui.QRadioButton("Ra&dio button 3")
#  
#         radio1.setChecked(True)
#  
#         vbox = QtGui.QVBoxLayout()
#         vbox.addWidget(radio1)
#         vbox.addWidget(radio2)
#         vbox.addWidget(radio3)
#         vbox.addStretch(1)
#         groupBox.setLayout(vbox)
#  
#         return groupBox
#  
#     def createSecondExclusiveGroup(self):
#         groupBox = QtGui.QGroupBox("E&xclusive Radio Buttons")
#         groupBox.setCheckable(True)
#         groupBox.setChecked(False)
#  
#         radio1 = QtGui.QRadioButton("Rad&io button 1")
#         radio2 = QtGui.QRadioButton("Radi&o button 2")
#         radio3 = QtGui.QRadioButton("Radio &button 3")
#         radio1.setChecked(True)
#         checkBox = QtGui.QCheckBox("Ind&ependent checkbox")
#         checkBox.setChecked(True)
#  
#         vbox = QtGui.QVBoxLayout()
#         vbox.addWidget(radio1)
#         vbox.addWidget(radio2)
#         vbox.addWidget(radio3)
#         vbox.addWidget(checkBox)
#         vbox.addStretch(1)
#         groupBox.setLayout(vbox)
#  
#         return groupBox
#  
#     def createNonExclusiveGroup(self):
#         groupBox = QtGui.QGroupBox("Non-Exclusive Checkboxes")
#         groupBox.setFlat(True)
#  
#         checkBox1 = QtGui.QCheckBox("&Checkbox 1")
#         checkBox2 = QtGui.QCheckBox("C&heckbox 2")
#         checkBox2.setChecked(True)
#         tristateBox = QtGui.QCheckBox("Tri-&state button")
#         tristateBox.setTristate(True)
#         tristateBox.setCheckState(QtCore.Qt.PartiallyChecked)
#  
#         vbox = QtGui.QVBoxLayout()
#         vbox.addWidget(checkBox1)
#         vbox.addWidget(checkBox2)
#         vbox.addWidget(tristateBox)
#         vbox.addStretch(1)
#         groupBox.setLayout(vbox)
#  
#         return groupBox
#  
#     def createPushButtonGroup(self):
#         groupBox = QtGui.QGroupBox("&Push Buttons")
#         groupBox.setCheckable(True)
#         groupBox.setChecked(True)
#  
#         pushButton = QtGui.QPushButton("&Normal Button")
#         toggleButton = QtGui.QPushButton("&Toggle Button")
#         toggleButton.setCheckable(True)
#         toggleButton.setChecked(True)
#         flatButton = QtGui.QPushButton("&Flat Button")
#         flatButton.setFlat(True)
#  
#         popupButton = QtGui.QPushButton("Pop&up Button")
#         menu = QtGui.QMenu(self)
#         menu.addAction("&First Item")
#         menu.addAction("&Second Item")
#         menu.addAction("&Third Item")
#         menu.addAction("F&ourth Item")
#         popupButton.setMenu(menu)
#  
#         newAction = menu.addAction("Submenu")
#         subMenu = QtGui.QMenu("Popup Submenu", self)
#         subMenu.addAction("Item 1")
#         subMenu.addAction("Item 2")
#         subMenu.addAction("Item 3")
#         newAction.setMenu(subMenu)
#  
#         vbox = QtGui.QVBoxLayout()
#         vbox.addWidget(pushButton)
#         vbox.addWidget(toggleButton)
#         vbox.addWidget(flatButton)
#         vbox.addWidget(popupButton)
#         vbox.addStretch(1)
#         groupBox.setLayout(vbox)
#  
#         return groupBox
#  
#  
# if __name__ == '__main__':
#  
#     import sys
#  
#     app = QtGui.QApplication(sys.argv)
#     clock = Window()
#     clock.show()
#     sys.exit(app.exec_())

'''
Example QDialog
'''
    
# from PyQt4.QtGui import *
# from PyQt4.QtCore import *
# #from PyQt4 import Qt
#      
# class DateDialog(QDialog):
#     def __init__(self, parent = None):
#         super(DateDialog, self).__init__(parent)
#  
#         layout = QVBoxLayout(self)
#  
#         # nice widget for editing the date
#         self.datetime = QDateTimeEdit(self)
#         self.datetime.setCalendarPopup(True)
#         self.datetime.setDateTime(QDateTime.currentDateTime())
#         layout.addWidget(self.datetime)
#  
#         # OK and Cancel buttons
#         self.buttons = QDialogButtonBox(
#             QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
#             Qt.Horizontal, self)
#         self.layout().addWidget(self.buttons)
#  
#     # get current date and time from the dialog
#     def dateTime(self):
#         return self.datetime.dateTime()
#  
#     # static method to create the dialog and return (date, time, accepted)
#     @staticmethod
#     def getDateTime(parent = None):
#         dialog = DateDialog(parent)
#         result = dialog.exec_()
#         date = dialog.dateTime()
#         return (date.date(), date.time(), result == QDialog.Accepted)
#  
# if __name__ == '__main__':
#  
#     import sys
#  
#     app = QApplication(sys.argv)
#     date, time, ok = DateDialog.getDateTime()
#     print "date: ", date
#     print "time: ", time
#     print "ok: ", ok
#     sys.exit(app.exec_())


#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial 

This example shows
how to use QtGui.QComboBox widget.
 
author: Jan Bodnar
website: zetcode.com 
last edited: September 2011
"""

# import sys
# from PyQt4 import QtGui, QtCore
# 
# class Example(QtGui.QWidget):
#     
#     def __init__(self):
#         super(Example, self).__init__()
#         
#         self.initUI()
#         
#     def initUI(self):      
# 
#         self.lbl = QtGui.QLabel("Ubuntu", self)
# 
#         combo = QtGui.QComboBox(self)
#         combo.addItem("Ubuntu")
#         combo.addItem("Mandriva")
#         combo.addItem("Fedora")
#         combo.addItem("Red Hat")
#         combo.addItem("Gentoo")
# 
#         combo.move(50, 50)
#         self.lbl.move(50, 150)
# 
#         combo.activated[str].connect(self.onActivated)        
#          
#         self.setGeometry(300, 300, 300, 200)
#         self.setWindowTitle('QtGui.QComboBox')
#         self.show()
#         
#     def onActivated(self, text):
#       
#         self.lbl.setText(text)
#         self.lbl.adjustSize()  
#                 
# def main():
#     
#     app = QtGui.QApplication(sys.argv)
#     ex = Example()
#     sys.exit(app.exec_())
# 
# 
# if __name__ == '__main__':
#     main()

#! /usr/bin/python

'''
Exammple for Texteditor
'''

# import sys
# import os
# from PyQt4 import QtGui
# 
# class Notepad(QtGui.QMainWindow):
# 
#     def __init__(self):
#         super(Notepad, self).__init__()
#         self.initUI()
#         
#     def initUI(self):
#         newAction = QtGui.QAction('New', self)
#         newAction.setShortcut('Ctrl+N')
#         newAction.setStatusTip('Create new file')
#         newAction.triggered.connect(self.newFile)
#         
#         saveAction = QtGui.QAction('Save', self)
#         saveAction.setShortcut('Ctrl+S')
#         saveAction.setStatusTip('Save current file')
#         saveAction.triggered.connect(self.saveFile)
#         
#         openAction = QtGui.QAction('Open', self)
#         openAction.setShortcut('Ctrl+O')
#         openAction.setStatusTip('Open a file')
#         openAction.triggered.connect(self.openFile)
#         
#         closeAction = QtGui.QAction('Close', self)
#         closeAction.setShortcut('Ctrl+Q')
#         closeAction.setStatusTip('Close Notepad')
#         closeAction.triggered.connect(self.close)
#         
#         menubar = self.menuBar()
#         fileMenu = menubar.addMenu('&File')
#         fileMenu.addAction(newAction)
#         fileMenu.addAction(saveAction)
#         fileMenu.addAction(openAction)
#         fileMenu.addAction(closeAction)
#         
#         self.text = QtGui.QTextEdit(self)
#         
#         self.setCentralWidget(self.text)
#         self.setGeometry(300,300,300,300)
#         self.setWindowTitle('Notepad')
#         self.show()
#         
#     def newFile(self):
#         self.text.clear()
#         
#     def saveFile(self):
#         filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File', os.getenv('HOME'))
#         f = open(filename, 'w')
#         filedata = self.text.toPlainText()
#         f.write(filedata)
#         f.close()
#         
#         
#     def openFile(self):
#         filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
#         f = open(filename, 'r')
#         filedata = f.read()
#         self.text.setText(filedata)
#         f.close()
#         
# def main():
#     app = QtGui.QApplication(sys.argv)
#     notepad = Notepad()
#     sys.exit(app.exec_())
#     
# if __name__ == '__main__':
#     main()

#!/usr/bin/env python

"""PyQt4 port of the richtext/syntaxhighlighter example from Qt v4.x"""

# from PyQt4 import QtCore, QtGui
# 
# 
# class MainWindow(QtGui.QMainWindow):
#     def __init__(self, parent=None):
#         super(MainWindow, self).__init__(parent)
# 
#         self.setupFileMenu()
#         self.setupHelpMenu()
#         self.setupEditor()
# 
#         self.setCentralWidget(self.editor)
#         self.setWindowTitle("Syntax Highlighter")
# 
#     def about(self):
#         QtGui.QMessageBox.about(self, "About Syntax Highlighter",
#                 "<p>The <b>Syntax Highlighter</b> example shows how to " \
#                 "perform simple syntax highlighting by subclassing the " \
#                 "QSyntaxHighlighter class and describing highlighting " \
#                 "rules using regular expressions.</p>")
# 
#     def newFile(self):
#         self.editor.clear()
# 
#     def openFile(self, path=None):
#         if not path:
#             path = QtGui.QFileDialog.getOpenFileName(self, "Open File",
#                     '', "C++ Files (*.cpp *.h)")
# 
#         if path:
#             inFile = QtCore.QFile(path)
#             if inFile.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
#                 text = inFile.readAll()
# 
#                 try:
#                     # Python v3.
#                     text = str(text, encoding='ascii')
#                 except TypeError:
#                     # Python v2.
#                     text = str(text)
# 
#                 self.editor.setPlainText(text)
# 
#     def setupEditor(self):
#         font = QtGui.QFont()
#         font.setFamily('Courier')
#         font.setFixedPitch(True)
#         font.setPointSize(10)
# 
#         self.editor = QtGui.QTextEdit()
#         self.editor.setFont(font)
# 
#         self.highlighter = Highlighter(self.editor.document())
# 
#     def setupFileMenu(self):
#         fileMenu = QtGui.QMenu("&File", self)
#         self.menuBar().addMenu(fileMenu)
# 
#         fileMenu.addAction("&New...", self.newFile, "Ctrl+N")
#         fileMenu.addAction("&Open...", self.openFile, "Ctrl+O")
#         fileMenu.addAction("E&xit", QtGui.qApp.quit, "Ctrl+Q")
# 
#     def setupHelpMenu(self):
#         helpMenu = QtGui.QMenu("&Help", self)
#         self.menuBar().addMenu(helpMenu)
# 
#         helpMenu.addAction("&About", self.about)
#         helpMenu.addAction("About &Qt", QtGui.qApp.aboutQt)
# 
# 
# class Highlighter(QtGui.QSyntaxHighlighter):
#     def __init__(self, parent=None):
#         super(Highlighter, self).__init__(parent)
# 
#         keywordFormat = QtGui.QTextCharFormat()
#         keywordFormat.setForeground(QtCore.Qt.darkBlue)
#         keywordFormat.setFontWeight(QtGui.QFont.Bold)
# 
#         keywordPatterns = ["\\bchar\\b", "\\bclass\\b", "\\bconst\\b",
#                 "\\bdouble\\b", "\\benum\\b", "\\bexplicit\\b", "\\bfriend\\b",
#                 "\\binline\\b", "\\bint\\b", "\\blong\\b", "\\bnamespace\\b",
#                 "\\boperator\\b", "\\bprivate\\b", "\\bprotected\\b",
#                 "\\bpublic\\b", "\\bshort\\b", "\\bsignals\\b", "\\bsigned\\b",
#                 "\\bslots\\b", "\\bstatic\\b", "\\bstruct\\b",
#                 "\\btemplate\\b", "\\btypedef\\b", "\\btypename\\b",
#                 "\\bunion\\b", "\\bunsigned\\b", "\\bvirtual\\b", "\\bvoid\\b",
#                 "\\bvolatile\\b"]
# 
#         self.highlightingRules = [(QtCore.QRegExp(pattern), keywordFormat)
#                 for pattern in keywordPatterns]
# 
#         classFormat = QtGui.QTextCharFormat()
#         classFormat.setFontWeight(QtGui.QFont.Bold)
#         classFormat.setForeground(QtCore.Qt.darkMagenta)
#         self.highlightingRules.append((QtCore.QRegExp("\\bQ[A-Za-z]+\\b"),
#                 classFormat))
# 
#         singleLineCommentFormat = QtGui.QTextCharFormat()
#         singleLineCommentFormat.setForeground(QtCore.Qt.red)
#         self.highlightingRules.append((QtCore.QRegExp("//[^\n]*"),
#                 singleLineCommentFormat))
# 
#         self.multiLineCommentFormat = QtGui.QTextCharFormat()
#         self.multiLineCommentFormat.setForeground(QtCore.Qt.red)
# 
#         quotationFormat = QtGui.QTextCharFormat()
#         quotationFormat.setForeground(QtCore.Qt.darkGreen)
#         self.highlightingRules.append((QtCore.QRegExp("\".*\""),
#                 quotationFormat))
# 
#         functionFormat = QtGui.QTextCharFormat()
#         functionFormat.setFontItalic(True)
#         functionFormat.setForeground(QtCore.Qt.blue)
#         self.highlightingRules.append((QtCore.QRegExp("\\b[A-Za-z0-9_]+(?=\\()"),
#                 functionFormat))
# 
#         self.commentStartExpression = QtCore.QRegExp("/\\*")
#         self.commentEndExpression = QtCore.QRegExp("\\*/")
# 
#     def highlightBlock(self, text):
#         for pattern, format in self.highlightingRules:
#             expression = QtCore.QRegExp(pattern)
#             index = expression.indexIn(text)
#             while index >= 0:
#                 length = expression.matchedLength()
#                 self.setFormat(index, length, format)
#                 index = expression.indexIn(text, index + length)
# 
#         self.setCurrentBlockState(0)
# 
#         startIndex = 0
#         if self.previousBlockState() != 1:
#             startIndex = self.commentStartExpression.indexIn(text)
# 
#         while startIndex >= 0:
#             endIndex = self.commentEndExpression.indexIn(text, startIndex)
# 
#             if endIndex == -1:
#                 self.setCurrentBlockState(1)
#                 commentLength = len(text) - startIndex
#             else:
#                 commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()
# 
#             self.setFormat(startIndex, commentLength,self.multiLineCommentFormat)
#             startIndex = self.commentStartExpression.indexIn(text,startIndex + commentLength)
# 
# 
# if __name__ == '__main__':
# 
#     import sys 
# 
#     app = QtGui.QApplication(sys.argv)
#     window = MainWindow()
#     window.resize(640, 512)
#     window.show()
#     sys.exit(app.exec_())

'''
QThread example
'''

# import sys, time
# from PyQt4 import QtCore, QtGui 
# 
# class WorkThread(QtCore.QThread): 
#      
#     def __init__(self):  
#         QtCore.QThread.__init__(self)  
#      
#     def __del__(self):  
#         self.wait()  
#          
#     def run(self):  
#         for i in range(6):   
#             time.sleep(0.3) 
#             # artificial time delay   
#         self.emit( QtCore.SIGNAL('update(QString)'), "from work thread " + str(i) )  
#         return 
#      
# class GenericThread(QtCore.QThread): 
#      
#     def __init__(self, function, *args, **kwargs):  
#         QtCore.QThread.__init__(self)  
#         self.function = function  
#         self.args = args  
#         self.kwargs = kwargs  
#          
#     def __del__(self):  
#         self.wait()  
#         
#     def run(self):  
#         self.function(*self.args,**self.kwargs)  
#         return 
# 
# class MyApp(QtGui.QWidget): 
#     def __init__(self, parent=None):  
#         QtGui.QWidget.__init__(self, parent)   
#         self.setGeometry(300, 300, 280, 600)  
#         self.setWindowTitle('threads')   
#         self.layout = QtGui.QVBoxLayout(self)   
#         self.testButton = QtGui.QPushButton("test")  
#         self.connect(self.testButton, QtCore.SIGNAL("released()"), self.test)  
#         self.listwidget = QtGui.QListWidget(self)   
#         self.layout.addWidget(self.testButton)  
#         self.layout.addWidget(self.listwidget)   
#         self.threadPool = []  
#         
#     def add(self, text):  
#         
#         """ Add item to list widget """  
#         print "Add: " + text  
#         self.listwidget.addItem(text)  
#         self.listwidget.sortItems()  
#         
#     def addBatch(self,text="test",iters=6,delay=0.3): 
#         
#         """ Add several items to list widget """ 
#         for i in range(iters):   
#             time.sleep(delay) # artificial time delay   
#             self.add(text+" "+str(i))  
#              
#     def addBatch2(self,text="test",iters=6,delay=0.3):  
#         for i in range(iters):   time.sleep(delay) 
#         # artificial time delay   
#         self.emit( QtCore.SIGNAL('add(QString)'), text+" "+str(i) )  
#         
#     def test(self):  
#         self.listwidget.clear()  
#         # adding in main application: locks ui  
#         #self.addBatch("_non_thread",iters=6,delay=0.3)   
#         # adding by emitting signal in different thread  
#         self.threadPool.append( WorkThread() )  
#         self.connect( self.threadPool[len(self.threadPool)-1], QtCore.SIGNAL("update(QString)"), self.add )  
#         self.threadPool[len(self.threadPool)-1].start()   
#         # generic thread using signal  
#         self.threadPool.append( GenericThread(self.addBatch2,"from generic thread using signal ",delay=0.3) )  
#         self.disconnect( self, QtCore.SIGNAL("add(QString)"), self.add )  
#         self.connect( self, QtCore.SIGNAL("add(QString)"), self.add )  
#         self.threadPool[len(self.threadPool)-1].start() 
#         
#  
#         
# #run
# app = QtGui.QApplication(sys.argv)
# test = MyApp()
# test.show()
# app.exec_()

'''
Example signals, qthread, eventloops 
'''
# import sip
# 
# sip.setapi('QString',2)
# sip.setapi('QVariant',2) 
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
# import sys 
# 
# def waitForSignal(sender, senderSignal, timeoutMs, expectedSignalParams=None):    
#     timer=QTimer(singleShot=True)    
#     loop=QEventLoop()     
#     senderSignalArgsWrong=[]     
#     
#     @pyqtSlot()    
#     def senderSignalSlot(*args):
#         senderSignalArgsWrong.append((expectedSignalParams is not None) and   expectedSignalParams!=args)        
#         loop.quit()     
#         
#     senderSignal.connect(senderSignalSlot)    
#     timer.timeout.connect(loop.quit)     
#     QTimer.singleShot(0, sender)    
#     timer.start(timeoutMs)     
#     ex=[]    
#         
#     def exceptHook(type_, value, traceback):        
#         ex.append(value)        
#         oeh(type_, value, traceback)     
#     oeh=sys.excepthook    
#     sys.excepthook=exceptHook     
#     loop.exec_()    
#     if ex: 
#         raise ex[0]     
#     ret=timer.isActive()    
#     timer.stop()    
#     senderSignal.disconnect(senderSignalSlot)    
#     timer.timeout.disconnect(loop.quit)     
#     
#     sys.excepthook=oeh     
#     return ret and senderSignalArgsWrong and (not senderSignalArgsWrong[0]) 
#         
# if __name__=="__main__":    
#     from sys import argv, exit     
#     class Widget(QWidget):        
#     
#         def __init__(self, parent=None, **kwargs):            
#             QWidget.__init__(self, parent, **kwargs)             
#             l=QVBoxLayout(self)            
#             l.addWidget(QPushButton("Start", self, clicked=self.start))            
#             self._stopButton=QPushButton("Stop", self)            
#             l.addWidget(self._stopButton)         
#             
#         @pyqtSlot()        
#         def start(self):            
#             print "Start"           
#             ret=waitForSignal(self.work, self._stopButton.clicked, 5000)            
#             print "Finished:", ret         
#             
#         @pyqtSlot()            
#         def work(self): 
#             print "Work"     
# a=QApplication(argv)    
# w=Widget()    
# w.show()    
# w.raise_()    
# exit(a.exec_())

# import sys, time, random
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
# from PyQt4.Qt import * 
# 
# rand = random.Random()
# class WorkerThread(QThread):
#     def __init__(self, name, receiver):
#         QThread.__init__(self)
#         self.name = name
#         self.receiver = receiver
#         self.stopped = 0
#     def run(self):
#         while not self.stopped:
#             time.sleep(rand.random() * 0.3)
#             msg = rand.random()
#             event = QEvent(10000)
#             event.setData("%s: %f" % (self.name, msg))
#             QThread.postEvent(self.receiver, event)
# 
#     def stop(self):
#         self.stopped = 1
# 
# class ThreadExample(QLineEdit):
#     def __init__(self, *args):
#         QLineEdit.__init__(self, *args)
#         #self.setCaption("Threading Example")
#         self.threads = []
#         for name in ["t1", "t2", "t3"]:
#             t = WorkerThread(name, self)
#             t.start()
#             self.threads.append(t)
#       
#     def customEvent(self,event):
#         if event.type() == 10000:
#             s = event.data()
#             self.append(s)
# 
#     def __del__(self):
#         for t in self.threads:
#             running = t.running()
#             t.stop()
#             if not t.finished():
#                 t.wait()
# 
# 
# app = QApplication(sys.argv)
# threadExample = ThreadExample()
# #app.setMainWidget(threadExample)
# threadExample.show()
# 
# sys.exit(app.exec_())

'''Queue'''

# import time
# import Queue
# import threading
# from  PyQt4 import QtCore
# 
# class SimulationThread( QtCore.QThread ):
#     
#     def __init__(self, queue):
#         QtCore.QThread.__init__(self)
#         self.__runThreadMessageQueue = queue
#         
#     def __del__(self):
#         self.exit(0)
#         
#     def run(self):
# 
#         i = 0
#         while 1:
#             
#             print "i: ", i
#             i += 1
#             
#             print "self.__runThreadMessageQueue: ", self.__runThreadMessageQueue
#             
#             if not self.__runThreadMessageQueue.empty():
#                 try:
#                     message = self.__runThreadMessageQueue.get()
#                 except:
#                     print "Except Queue!"
#                     message = None
#             else:
#                 print "Queue not full!"
#                 message = None
#             
#             print "message: ", message
#                 
#             if message != None:
#                 #self.stopRun() 
#                 self.__runThreadMessageQueue.task_done()
#                 print "Thread stoped"
#                 time.sleep(0.01)
#                 return
#                 
# queue  = Queue.Queue()
# print "queue: ", queue
# thread = SimulationThread(queue)
# thread.start()
# time.sleep(0.01)
# print "---------------------------------------------------------------------------> QUEUE FILLED!!!"
# queue.put(-1)
# queue.put(-2)
# 
# if not queue.empty():
#     try:
#         message = queue.get()
#     except:
#         print "Except Queue (2)!"
#         message = None
# else:
#     print "Queue not full! (2)"
#     message = None
# 
# print "message (2): ", message
# 
# time.sleep(0.02)



#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/env python

"""PyQt4 port of the painting/svgviewer example from Qt v4.x"""

# #This is only needed for Python v2 but is harmless for Python v3.
# import sys
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
#   
# class ImageView(QGraphicsView):
#     def __init__(self, parent=None, origPixmap=None):
#         """
#         QGraphicsView that will show an image scaled to the current widget size
#         using events
#         """
#         super(ImageView, self).__init__(parent)
#         self.origPixmap = origPixmap
#         QMetaObject.connectSlotsByName(self)
#         self.scale(1.2, 1.2)
#       
#     def resizeEvent(self, event):
#         """
#         Handle the resize event.
#         """
#         size = event.size()
#         item =  self.items()[0]
#           
#         # using current pixmap after n-resizes would get really blurry image
#         #pixmap = item.pixmap()
#         pixmap = self.origPixmap
#           
#         pixmap = pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
#         self.centerOn(1.0, 1.0)
#         item.setPixmap(pixmap)
#   
#   
# app = QApplication(sys.argv)
#   
# pic = QPixmap('zappa.png')
# grview = ImageView(origPixmap=pic)
#   
# scene = QGraphicsScene()
# scene.addPixmap(pic)
#   
# grview.setScene(scene)
# grview.show()
#   
# sys.exit(app.exec_())

'''Class functions'''

# class Testclass2 (object):
#     
#     bHashedById = False
#     listClasses = []
# 
#     def __init__(self):
#         print type(self)
#         
#     @staticmethod
#     def initialize():
#         Testclass2.listClasses = [Testclass2, Testclass]
# 
# class Testclass(Testclass2):
#     
#     def __init__(self):
#     
#         super(Testclass, self).__init__()
#         Testclass2.bHashedById = True
# 
# Testclass2.initialize()
# 
# obj1 = Testclass()
# obj2 = Testclass2() 
'''
overwrite existing output
'''
# import sys
# import time
# for count in range(10) :
#    sys.stdout.write("%s\r" % count)
#    sys.stdout.flush()
#    time.sleep(1)

''' 
Test programm for the mv function
'''

# from PyLinXData import *
# 
# objRoot = BContainer.BContainer("root")
# obj1 = BContainer.BContainer("obj1")
# objRoot.paste(obj1)
# obj2 = BContainer.BContainer("obj2")
# objRoot.paste(obj2)
# obj3 = BContainer.BContainer("objToMove")
# obj1.paste(obj3)
# 
# print "---objRoot---"
# objRoot.ls()
# print "---obj1---"
# obj1.ls()
# print "---obj2---"
# obj2.ls()
# 
# objRoot.mv("/obj1/objToMove", "/obj2")
# 
# print "---objRoot---"
# objRoot.ls()
# print "---obj1---"
# obj1.ls()
# print "---obj2---"
# obj2.ls()

# from PyLinXData.BContainer import BContainer
# 
# con1 = BContainer("con1")
# con11 = BContainer("con11")
# con12 = BContainer("con12")
# con111 = BContainer("con111")
# 
# con1.paste(con11)
# con11.paste(con111)
# con1.paste(con12)
# 
# dictSet = {"attr1": 1, "@con11": {"attr2": "str2", "@con111":{"attr3":[1,2]}}}
# con1.set(None, dictSet)
# 
# print "=============="
# con1.lsAttr()
# print "--------------"
# con11.lsAttr()
# print "--------------"
# con12.lsAttr()
# print "--------------"
# con111.lsAttr()
# print "=============="
# 
# dictGet = {"attr1": None, "@con11": {"attr2": None, "@con111":{"attr3":None}}}
# 
# print dictGet
# print con1.get(dictGet, bComplex=True)
# 
# con111.ls()

'''Mausrad in PyQt'''
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
# import sys
# 
# #############Define MyWindow Class Here ############
# class MyWindow(QMainWindow):
# ##-----------------------------------------
#   def __init__(self):
#     QMainWindow.__init__(self)
#     self.label = QLabel("No data")
#     self.label.setGeometry(100, 200, 100, 100)
#     self.setCentralWidget(self.label)
#     self.setWindowTitle("QMainWindow WheelEvent")
#     self.x = 0
# ##-----------------------------------------
#   def wheelEvent(self,event):
#     self.x =self.x + event.delta()/120
#     print self.x
#     self.label.setText("Total Steps: "+QString.number(self.x))
# ##-----------------------------------------
# ##########End of Class Definition ##################
# 
# 
# def main():
#   app = QApplication(sys.argv)
#   window = MyWindow()
#   window.show()
#   return app.exec_()
# 
# if __name__ == '__main__':
#  main()
#! /usr/bin/env python

# Create a Qt application
# from PyQt4 import QtCore, QtGui
# 
# 
# app = QtGui.QApplication(sys.argv)
#  
# # Our main window will be a QListView
# list = QtGui.QListView()
# list.setWindowTitle('Honey-Do List')
# list.setMinimumSize(600, 400)
#  
# # Create an empty model for the list's data
# model = QtGui.QStandardItemModel(list)
#  
# # Add some textual items
# foods = [
#     'Cookie dough', # Must be store-bought
#     'Hummus', # Must be homemade
#     'Spaghetti', # Must be saucy
#     'Dal makhani', # Must be spicy
#     'Chocolate whipped cream' # Must be plentiful
# ]
#  
# for food in foods:
#     # Create an item with a caption
#     item = QtGui.QStandardItem(food)
#  
#     # Add a checkbox to it
#     item.setCheckable(True)
#  
#     # Add the item to the model
#     model.appendRow(item)
#  
# def on_item_changed(item):
#     print "on_item_changed"
#     # If the changed item is not checked, don't bother checking others
#     if not item.checkState():
#         return
#  
#     # Loop through the items until you get None, which
#     # means you've passed the end of the list
#     i = 0
#     while model.item(i):
#         if not model.item(i).checkState():
#             return
#         i += 1
#  
#     app.quit()
#  
# model.itemChanged.connect(on_item_changed)
#  
# # Apply the model to the list view
# list.setModel(model)
#  
# # Show the window and run the app
# list.show()
# app.exec_()

#!/usr/bin/env python

#!/usr/bin/env python

############################################################################
##
## Copyright (C) 2005-2005 Trolltech AS. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## This file may be used under the terms of the GNU General Public
## License version 2.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http://www.trolltech.com/products/qt/opensource.html
##
## If you are unsure which license is appropriate for your use, please
## review the following information:
## http://www.trolltech.com/products/qt/licensing.html or contact the
## sales department at sales@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
############################################################################

'''Test Color Factory'''

# from PyQt4 import QtCore
# class ColorFactory(object):
#     
#     def __init__(self):
#         super(ColorFactory, self).__init__()
#         self.listColor = [QtCore.Qt.red, \
#                           QtCore.Qt.green, \
#                           QtCore.Qt.lightGray,\
#                           QtCore.Qt.cyan, \
#                           QtCore.Qt.magenta, \
#                           QtCore.Qt.yellow]
#         
#         #self.listColorCount = [0,0,0,0,0,0]
#         self.idxColor = 0
#         
#         
#     def getColor(self):
#         idx = self.idxColor
#         self.idxColor = (self.idxColor + 1) % len(self.listColor)
#         return self.listColor[idx] 
#     
# fac = ColorFactory()
# for i in range(24):
#     print fac.getColor()

'''
Test Diamond Problem
'''
  
# class BaseClass(object):
#     def __init__(self):
#         self.__testVariable = {"name": "TestName"}
# 
#     def set(self, attr, val):
#         self._BaseClass__testVariable[attr] = val
#         
#     def prt(self):
#         print self.__testVariable
#         
# class ChildClass1(BaseClass):
#     def __init__(self):
#         super(ChildClass1, self).__init__()
#         self._BaseClass__testVariable["name2"] =  "TestName2"
# 
#     def set(self, attr, val):
#         if attr == "attr":
#             print "attr ChildClass1"
#         super(ChildClass1, self).set(attr, val)
# 
#         
# class ChildClass2(BaseClass):
#     def __init__(self):
#         super(ChildClass2, self).__init__()
#         self._BaseClass__testVariable["name3"] =  "TestName3"
# 
#     def set(self, attr, val):
#         if attr == "attr":
#             print "attr ChildClass2"
#         super(ChildClass2, self).set(attr, val)
# 
#         
# class ChildClass3(ChildClass1, ChildClass2):
#     def __init__(self):
#         super(ChildClass3, self).__init__()
#     def set(self, attr, val):
#         super(ChildClass3, self).set("attr", val)
#         
# obj = ChildClass3()
# obj.set("attr", 15)
# obj.prt()

'''
Example Treeview'''
# import sys
# import PyQt4.QtGui as QtGui
# import PyQt4.QtCore as QtCore
# 
# 
# ################################################################################
# # Underlying data
# # ----------------
# # - RuntimeItems hold the data. They come from a database.
# # - ViewItems are the objects, that are given to the model indexes of 
# #Qt. They
# #   are constructed according to some rules like filters and configuration.
# # - DummieViewItemFactory processes the rules and configurations. The 
# #example
# #   here is simplfied. An instance of the factory is given to each ViewItem.
# #   The view item calls the DummieViewItemFactory.get_view_item_children 
# #method
# #   to request calculation of its children on demand.
# # - For this demo-version, the number of items is controlled by
# #   DummieViewItemFactory.max_items. It's passed in by the constructor.
# # - Nesting as high as possible: One child per parent.
# ################################################################################
# 
# 
# class RuntimeItem(object):
#     """Represent the real world business items. These objects have a 
# lot of
#      relations.
#      """
# 
#     def __init__(self, name, ident, item_type):
#         self.name = name
#         self.ident = ident
#         self.item_type = item_type
# 
# 
# class ViewItem(object):
#     """Represent items that are to be shown to the user in a QTreeView.
#      Those items do only occur one time in a view. They have a corresponding
#      runtime_item.
#      The children are calculated by the view_item_factory on demand.
#      """
# 
#     def __init__(self, view_item_factory, runtime_item=None, parent=None,
#                   hidden_runtime_items=None):
#         self.view_item_factory = view_item_factory
#         self.runtime_item = runtime_item
#         self.parent = parent
#         self.hidden_runtime_items = hidden_runtime_items
# 
#     @property
#     def children(self):
#         try:
#             return self._children
#         except AttributeError:
#             self._children = self.view_item_factory.get_view_item_children(self)
#             return self._children
# 
#     @children.setter
#     def children(self, children):
#         self._children = children
# 
# 
# class DummieViewItemFactory(object):
#     """Creates the view_items. This is a dumb dummie as a simple example.
#      Normally a lot of things happen here like filtering and configuration.
#      But once the view_item hierachy is build, this shouldn't be called 
# at all.
#      """
# 
#     def __init__(self, runtime_item, max_items):
#         self.runtime_item = runtime_item
#         self.max_items = max_items
#         self.item_counter = 0
#         self.aux_root_view_item = ViewItem(self)
# 
#     def get_view_item_children(self, view_item_parent):
#         if self.item_counter > self.max_items:
#             return []
#         self.item_counter += 1
#         view_item = ViewItem(self, self.runtime_item, view_item_parent)
#         return [view_item]
# 
# 
# ################################################################################
# # Qt classes
# # ----------------
# # - This should be standard stuff. I've got most of it from the Rapid GUI
# #   Programming book.
# # - The ActiveColums class tells the model which colums to use.
# # - The TreeView has a context menu with navigation actions.
# # - The expand_all calls the Qt slot. Here is the surprise for the 
# # performance.
# ################################################################################
# 
# 
# class ActiveColumns(object):
# 
#     def __init__(self, columns):
#         self.columns = columns
# 
# 
# class TreeView(QtGui.QTreeView):
# 
#     def __init__(self, aux_root_view_item, active_columns, parent=None,
#                   header_hidden=False):
#         super(TreeView, self).__init__(parent)
#         self.setIndentation(10)
#         self.active_columns = active_columns
#         self.setAlternatingRowColors(True)
#         self.setHeaderHidden(header_hidden)
#         self.setAllColumnsShowFocus(True)
#         self.setUniformRowHeights(True)
#         self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
# 
#         model = TreeModel(aux_root_view_item, self)
#         self.setModel(model)
# 
#         e_a_action = QtGui.QAction("Expand all", self)
#         e_a_action.setToolTip("Expands all items of the tree.")
#         e_a_action.triggered.connect(self.expand_all)
#         e_a_b_action = QtGui.QAction("Expand all below", self)
#         e_a_b_action.setToolTip("Expands all items under the selection.")
#         e_a_b_action.triggered.connect(self.expand_all_below)
# 
#         c_a_action = QtGui.QAction("Collapse all", self)
#         c_a_action.setToolTip("Collapses all items of the tree.")
#         c_a_action.triggered.connect(self.collapse_all)
#         c_a_b_action = QtGui.QAction("Collapse all below", self)
#         c_a_b_action.setToolTip("Collapses all items under the selection.")
#         c_a_b_action.triggered.connect(self.collapse_all_below)
# 
#         for action in (e_a_action, c_a_action, e_a_b_action, c_a_b_action):
#             self.addAction(action)
# 
#     def expand_all(self):
#         self.expandAll()
# 
#     def collapse_all(self):
#         self.collapseAll()
# 
#     def expand_all_below(self):
#         def expand_all_below_recursive(parent_index):
#             self.expand(parent_index)
#             children_indexes = self.tree_itemmodel.get_children_indexes(parent_index)
#             for child_index in children_indexes:
#                 expand_all_below_recursive(child_index)
# 
#         indexes = self.selectedIndexes()
#         if indexes:
#             index = indexes[0]
#             expand_all_below_recursive(index)
# 
#     def collapse_all_below(self):
#         def collapse_all_below_recursive(parent_index):
#             self.collapse(parent_index)
#             children_indexes = self.tree_itemmodel.get_children_indexes(parent_index)
#             for child_index in children_indexes:
#                 collapse_all_below_recursive(child_index)
# 
#         indexes = self.selectedIndexes()
#         if indexes:
#             index = indexes[0]
#             collapse_all_below_recursive(index)
# 
# class TreeModel(QtCore.QAbstractItemModel):
# 
#     def __init__(self, aux_root_view_item, parent):
#         super(TreeModel, self).__init__(parent)
#         self.aux_root_view_item = aux_root_view_item
#         self.active_columns = parent.active_columns
# 
#     def rowCount(self, parent_index):
#         parent_view_item = self.view_item_from_index(parent_index)
#         if parent_view_item is None:
#             return 0
#         return len(parent_view_item.children)
# 
#     def get_children_indexes(self, parent_index):
#         children_indexes = []
#         for row_no in range(self.rowCount(parent_index)):
#             children_indexes.append(self.index(row_no, 0, parent_index))
#         return children_indexes
# 
#     def columnCount(self, parent):
#         return len(self.active_columns.columns)
# 
#     def data(self, index, role):
#         if role == QtCore.Qt.TextAlignmentRole:
#             return int(QtCore.Qt.AlignTop|QtCore.Qt.AlignLeft)
#         if role != QtCore.Qt.DisplayRole:
#             return None
#         view_item = self.view_item_from_index(index)
#         try:
#             data = getattr(view_item.runtime_item,self.active_columns.columns[index.column()])
#         except AttributeError:
#             data = ""
#         return data
# 
#     def headerData(self, section, orientation, role):
#         if (orientation == QtCore.Qt.Horizontal and
#             role == QtCore.Qt.DisplayRole):
#             assert 0 <= section <= len(self.active_columns.columns)
#             return self.active_columns.columns[section]
#         return QtCore.QVariant()
# 
#     def index(self, row, column, parent_index):
#         View_item_parent = self.view_item_from_index(parent_index)
#         return self.createIndex(row, column, View_item_parent.children[row])
# 
#     def parent(self, child_index):
#         child_view_item = self.view_item_from_index(child_index)
#         if child_view_item is None:
#             return QtCore.QModelIndex()
#         parent_view_item = child_view_item.parent
#         if parent_view_item is None:
#             return QtCore.QModelIndex()
#         grandparent_view_item = parent_view_item.parent
#         if grandparent_view_item is None:
#             return QtCore.QModelIndex()
#         grandparent_view_item
#         row = grandparent_view_item.children.index(parent_view_item)
#         assert row != -1
#         return self.createIndex(row, 0, parent_view_item)
# 
#     def view_item_from_index(self, index):
#         return (index.internalPointer() if index.isValid() else self.aux_root_view_item)
# 
# 
# if __name__ == "__main__":
# 
#     run_time_item = RuntimeItem("Test", "test_12", "Test Item")
#     view_factory = DummieViewItemFactory(run_time_item, max_items=5000)
#     active_colums = ActiveColumns(["name", "id", "item_type"])
# 
#     app = QtGui.QApplication(sys.argv)
#     tree_view = TreeView(view_factory.aux_root_view_item, active_colums)
#     app.setApplicationName("IPDM")
#     tree_view.show()
#     app.exec_()


''' Combo-Box '''

# from PyQt4 import QtGui, QtCore
# 
# class Window(QtGui.QWidget):
#     def __init__(self):
#         QtGui.QWidget.__init__(self)
#         layout = QtGui.QVBoxLayout(self)
#         self.combo = QtGui.QComboBox()
#         self.combo.setEditable(True)
#         self.combo.addItems('One Two Three Four Five'.split())
#         self.buttonOne = QtGui.QPushButton('Change (Default)', self)
#         self.buttonOne.clicked.connect(self.handleButtonOne)
#         self.buttonTwo = QtGui.QPushButton('Change (Blocked)', self)
#         self.buttonTwo.clicked.connect(self.handleButtonTwo)
#         layout.addWidget(self.combo)
#         layout.addWidget(self.buttonOne)
#         layout.addWidget(self.buttonTwo)
#         self.changeIndex()
#         self.combo.activated['QString'].connect(self.handleActivated)
#         self.combo.currentIndexChanged['QString'].connect(self.handleChanged)
#         self.changeIndex()
# 
#     def handleButtonOne(self):
#         self.changeIndex()
# 
#     def handleButtonTwo(self):
#         self.combo.blockSignals(True)
#         self.changeIndex()
#         self.combo.blockSignals(False)
# 
#     def changeIndex(self):
#         index = self.combo.currentIndex()
#         if index < self.combo.count() - 1:
#             self.combo.setCurrentIndex(index + 1)
#         else:
#             self.combo.setCurrentIndex(0)
# 
#     def handleActivated(self, text):
#         print('handleActivated: %s' % text)
# 
#     def handleChanged(self, text):
#         print('handleChanged: %s' % text)
# 
# if __name__ == '__main__':
# 
#     import sys
#     app = QtGui.QApplication(sys.argv)
#     window = Window()
#     window.show()
#     sys.exit(app.exec_())

# -*- coding: utf-8 -*-

'''QGraphicsView'''

"""The user interface for our app"""

import os,sys,time
 
# Import Qt modules
from PyQt4 import QtCore,QtGui, QtOpenGL
 
# Import the compiled UI module
from ui_clock import Ui_Form
 
from random import randint, shuffle
 
# Create a class for our main window
class Main(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
 
        # This is always the same
        self.ui=Ui_Form()
        self.ui.setupUi(self)
 
        self.scene=QtGui.QGraphicsScene()
        self.scene.setSceneRect(0,0,600,400)
        self.ui.view.setScene(self.scene)
        #self.ui.view.setViewport(QtOpenGL.QGLWidget())
        self.populate()
        self.setWindowState(QtCore.Qt.WindowMaximized)
 
        self.animator=QtCore.QTimer()
        self.animator.timeout.connect(self.animate)
        self.animate()
 
    def populate(self):
        self.digits=[]
        self.animations=[]
        font=QtGui.QFont('White Rabbit')
        font.setPointSize(120)
 
        self.dot1=QtGui.QGraphicsTextItem(':')
        self.dot1.setFont(font)
        self.dot1.setPos(140,0)
        self.scene.addItem(self.dot1)
        self.dot2=QtGui.QGraphicsTextItem(':')
        self.dot2.setFont(font)
        self.dot2.setPos(410,0)
        self.scene.addItem(self.dot2)
 
        for i in range(60):
            l = QtGui.QGraphicsTextItem(str(i%10))
            l.setFont(font)
            l.setZValue(-100)
            l.setPos(randint(0,500),randint(150,300))
            l.setOpacity(.3)
            #l.setDefaultTextColor(QtGui.QColor('lightgray'))
            self.scene.addItem(l)
            self.digits.append(l)
 
    def animate(self):
        self.animations=range(0,60)
 
        def animate_to(t,item,x,y,angle):
            animation=QtGui.QGraphicsItemAnimation()
            timeline=QtCore.QTimeLine(1000)
            timeline.setFrameRange(0,100)
            animation.setPosAt(t,QtCore.QPointF(x,y))
            animation.setRotationAt(t,angle)
            animation.setItem(item)
            animation.setTimeLine(timeline)
            return animation
 
        offsets=range(6)
        shuffle(offsets)
 
        # Some, animate with purpose
        h1,h2=map(int,'%02d'%time.localtime().tm_hour)
        h1+=offsets[0]*10
        h2+=offsets[1]*10
        self.animations[h1]=animate_to(0.2,self.digits[h1],-40,0,0)
        self.animations[h2]=animate_to(0.2,self.digits[h2],50,0,0)
 
        m1,m2=map(int,'%02d'%time.localtime().tm_min)
        m1+=offsets[2]*10
        m2+=offsets[3]*10
        self.animations[m1]=animate_to(0.2,self.digits[m1],230,0,0)
        self.animations[m2]=animate_to(0.2,self.digits[m2],320,0,0)
 
        s1,s2=map(int,'%02d'%time.localtime().tm_sec)
        s1+=offsets[4]*10
        s2+=offsets[5]*10
        self.animations[s1]=animate_to(0.2,self.digits[s1],500,0,0)
        self.animations[s2]=animate_to(0.2,self.digits[s2],590,0,0)
 
        # Random animations
        for i in range(60):
            l = self.digits[i]
            if i in [h1,h2,m1,m2,s1,s2]:
                l.setOpacity(1)
                continue
            l.setOpacity(.3)
            self.animations[i]=animate_to(1,l,randint(0,500),randint(0,300),randint(0,0))
 
        [ animation.timeLine().start() for animation in self.animations ]
 
 
        self.animator.start(1000)
         
 
def main():
    # Again, this is boilerplate, it's going to be the same on
    # almost every app you write
    app = QtGui.QApplication(sys.argv)
    window=Main()
    window.show()
 
 
    # It's exec_ because exec is a reserved word in Python
    sys.exit(app.exec_())
 
 
if __name__ == "__main__":
    main()

'''QSplitter'''

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial 

This example shows
how to use QtGui.QSplitter widget.
 
author: Jan Bodnar
website: zetcode.com 
last edited: September 2011
"""

# import sys
# from PyQt4 import QtGui, QtCore
# 
# class Example(QtGui.QWidget):
#     
#     def __init__(self):
#         super(Example, self).__init__()
#         
#         self.initUI()
#         
#     def initUI(self):      
# 
#         hbox = QtGui.QHBoxLayout(self)
# 
#         topleft = QtGui.QFrame(self)
#         topleft.setFrameShape(QtGui.QFrame.StyledPanel)
#  
#         topright = QtGui.QFrame(self)
#         topright.setFrameShape(QtGui.QFrame.StyledPanel)
# 
#         bottom = QtGui.QFrame(self)
#         bottom.setFrameShape(QtGui.QFrame.StyledPanel)
# 
#         splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
#         splitter1.addWidget(topleft)
#         splitter1.addWidget(topright)
# 
#         splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
#         splitter2.addWidget(splitter1)
#         splitter2.addWidget(bottom)
# 
#         hbox.addWidget(splitter2)
#         self.setLayout(hbox)
#         QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
#         
#         self.setGeometry(300, 300, 300, 200)
#         self.setWindowTitle('QtGui.QSplitter')
#         self.show()
#         
# def main():
#     
#     app = QtGui.QApplication(sys.argv)
#     ex = Example()
#     sys.exit(app.exec_())
# 
# 
# if __name__ == '__main__':
#     main()

'''TreeView und TreeModel '''   
    

# from PyQt4 import QtGui, QtCore
# 
# HORIZONTAL_HEADERS = ("Surname", "Given Name")
#     
# class person_class(object):
#     '''
#     a trivial custom data object
#     '''
#     def __init__(self, sname, fname, isMale):
#         self.sname = sname
#         self.fname = fname
#         self.isMale = isMale
# 
#     def __repr__(self):
#         return "PERSON - %s %s"% (self.fname, self.sname)
#     
# class TreeItem(object):
#     '''
#     a python object used to return row/column data, and keep note of
#     it's parents and/or children
#     '''
#     def __init__(self, person, header, parentItem):
#         self.person = person
#         self.parentItem = parentItem
#         self.header = header
#         self.childItems = []
# 
#     def appendChild(self, item):
#         self.childItems.append(item)
# 
#     def child(self, row):
#         return self.childItems[row]
# 
#     def childCount(self):
#         return len(self.childItems)
# 
#     def columnCount(self):
#         return 2
#     
#     def data(self, column):
#         if self.person == None:
#             if column == 0:
#                 return QtCore.QVariant(self.header)
#             if column == 1:
#                 return QtCore.QVariant("")                
#         else:
#             if column == 0:
#                 return QtCore.QVariant(self.person.sname)
#             if column == 1:
#                 return QtCore.QVariant(self.person.fname)
#         return QtCore.QVariant()
# 
#     def parent(self):
#         return self.parentItem
#     
#     def row(self):
#         if self.parentItem:
#             return self.parentItem.childItems.index(self)
#         return 0
# 
# class treeModel(QtCore.QAbstractItemModel):
#     '''
#     a model to display a few names, ordered by sex
#     '''
#     def __init__(self, parent=None):
#         super(treeModel, self).__init__(parent)
#         self.people = []
#         for fname, sname, isMale in (("John","Brown", 1), 
#         ("Fred", "Bloggs", 1), ("Sue", "Smith", 0)):
#             person = person_class(sname, fname, isMale)
#             self.people.append(person)
#             
#         self.rootItem = TreeItem(None, "ALL", None)
#         self.parents = {0 : self.rootItem}
#         self.setupModelData()
# 
#     def columnCount(self, parent=None):
#         if parent and parent.isValid():
#             return parent.internalPointer().columnCount()
#         else:
#             return len(HORIZONTAL_HEADERS)
# 
#     def data(self, index, role):
#         if not index.isValid():
#             return QtCore.QVariant()
# 
#         item = index.internalPointer()
#         if role == QtCore.Qt.DisplayRole:
#             return item.data(index.column())
#         if role == QtCore.Qt.UserRole:
#             if item:
#                 return item.person
# 
#         return QtCore.QVariant()
# 
#     def headerData(self, column, orientation, role):
#         if (orientation == QtCore.Qt.Horizontal and
#         role == QtCore.Qt.DisplayRole):
#             try:
#                 return QtCore.QVariant(HORIZONTAL_HEADERS[column])
#             except IndexError:
#                 pass
# 
#         return QtCore.QVariant()
# 
#     def index(self, row, column, parent):
#         if not self.hasIndex(row, column, parent):
#             return QtCore.QModelIndex()
# 
#         if not parent.isValid():
#             parentItem = self.rootItem
#         else:
#             parentItem = parent.internalPointer()
# 
#         childItem = parentItem.child(row)
#         if childItem:
#             return self.createIndex(row, column, childItem)
#         else:
#             return QtCore.QModelIndex()
# 
#     def parent(self, index):
#         if not index.isValid():
#             return QtCore.QModelIndex()
# 
#         childItem = index.internalPointer()
#         if not childItem:
#             return QtCore.QModelIndex()
#         
#         parentItem = childItem.parent()
# 
#         if parentItem == self.rootItem:
#             return QtCore.QModelIndex()
# 
#         return self.createIndex(parentItem.row(), 0, parentItem)
# 
#     def rowCount(self, parent=QtCore.QModelIndex()):
#         if parent.column() > 0:
#             return 0
#         if not parent.isValid():
#             p_Item = self.rootItem
#         else:
#             p_Item = parent.internalPointer()
#         return p_Item.childCount()
#     
#     def setupModelData(self):
#         for person in self.people:
#             if person.isMale:
#                 sex = "MALES"
#             else:
#                 sex = "FEMALES"
#             
#             if not self.parents.has_key(sex):                
#                 newparent = TreeItem(None, sex, self.rootItem)
#                 self.rootItem.appendChild(newparent)
# 
#                 self.parents[sex] = newparent
# 
#             parentItem = self.parents[sex]
#             newItem = TreeItem(person, "", parentItem)
#             parentItem.appendChild(newItem)
#         
#     def searchModel(self, person):
#         '''
#         get the modelIndex for a given appointment
#         '''
#         def searchNode(node):
#             '''
#             a function called recursively, looking at all nodes beneath node
#             '''
#             for child in node.childItems:
#                 if person == child.person:
#                     index = self.createIndex(child.row(), 0, child)
#                     return index
#                     
#                 if child.childCount() > 0:
#                     result = searchNode(child)
#                     if result:
#                         return result
#         
#         retarg = searchNode(self.parents[0])
#         print retarg
#         return retarg
#             
#     def find_GivenName(self, fname):
#         app = None
#         for person in self.people:
#             if person.fname == fname:
#                 app = person
#                 break
#         if app != None:
#             index = self.searchModel(app)
#             return (True, index)            
#         return (False, None)
# 
# if __name__ == "__main__":    
# 
#     def row_clicked(index):
#         '''
#         when a row is clicked... show the name
#         '''
#         print tv.model().data(index, QtCore.Qt.UserRole)
#         
#     def but_clicked():
#         '''
#         when a name button is clicked, I iterate over the model, 
#         find the person with this name, and set the treeviews current item
#         '''
#         name = dialog.sender().text()
#         print "BUTTON CLICKED:", name
#         result, index = model.find_GivenName(name)
#         if result:
#             if index:
#                 tv.setCurrentIndex(index)
#                 return
#         tv.clearSelection()
#         
#     app = QtGui.QApplication([])
#     
#     model = treeModel()
#     dialog = QtGui.QDialog()
# 
#     dialog.setMinimumSize(300,150)
#     layout = QtGui.QVBoxLayout(dialog)
# 
#     tv = QtGui.QTreeView(dialog)
#     tv.setModel(model)
#     tv.setAlternatingRowColors(True)
#     layout.addWidget(tv)
#     
#     label = QtGui.QLabel("Search for the following person")
#     layout.addWidget(label)
#     
#     buts = []
#     frame = QtGui.QFrame(dialog)
#     layout2 = QtGui.QHBoxLayout(frame)
#     
#     for person in model.people:
#         but = QtGui.QPushButton(person.fname, frame)
#         buts.append(but)
#         layout2.addWidget(but)
#         QtCore.QObject.connect(but, QtCore.SIGNAL("clicked()"), but_clicked)
#         
#     layout.addWidget(frame)
# 
#     but = QtGui.QPushButton("Clear Selection")
#     layout.addWidget(but)
#     QtCore.QObject.connect(but, QtCore.SIGNAL("clicked()"), tv.clearSelection)
# 
#     QtCore.QObject.connect(tv, QtCore.SIGNAL("clicked (QModelIndex)"),
#         row_clicked)
# 
#     dialog.exec_()
# 
#     app.closeAllWindows()

'''TreeView 2'''
# from PyQt4 import QtGui, QtCore
# import sys
# 
# class SI(object):
# 
# 
#     def __init__(self, group=None, parent=None):
#         self.parent = parent
#         self.group = group
#         self.children = []
# 
#     def data(self, column):
#         return self.group[column]
# 
#     def appendChild(self, group):
#         self.children.append(SI(group, self))
# 
#     def child(self, row):
#         return self.children[row]
# 
#     def childrenCount(self):
#         return len(self.children)
# 
#     def hasChildren(self):
#         if len(self.children) > 0 :
#             return True
#         return False
# 
#     def row(self):
#         if self.parent:
#             return self.parent.children.index(self)
#         return 0
# 
#     def columnCount(self):
#         return len(self.group)
# 
# class SM(QtCore.QAbstractItemModel):
# 
#     root = SI(["First", "Second"])
# 
#     def __init__(self, parent=None):
#         super(SM, self).__init__(parent)
#         self.createData()
# 
#     def createData(self):
#         for x in [["a", "A"], ["b","B"], ["c", "C"]]:
#             self.root.appendChild(x)
#         for y in [["aa", "AA"], ["ab", "AB"], ["ac","AC"]]:
#             self.root.child(0).appendChild(y)
# 
#     def columnCount(self, index=QtCore.QModelIndex()):
#         if index.isValid():
#             return index.internalPointer().columnCount()
#         else:
#             return self.root.columnCount()
# 
#     def rowCount(self, index=QtCore.QModelIndex()):
#         if index.isValid():
#             item = index.internalPointer()
#         else:
#             item = self.root
#         return item.childrenCount()
# 
#     def index(self, row, column, index=QtCore.QModelIndex()):
#         if not self.hasIndex(row, column, index):
#             return QtCore.QModelIndex()
#         if not index.isValid():
#             item = self.root
#         else:
#             item = index.internalPointer()
# 
#         child = item.child(row)
#         if child:
#             return self.createIndex(row, column, child)
#         return QtCore.QModelIndex()
# 
#     def parent(self, index):
#         if not index.isValid():
#             return QtCore.QModelIndex()
#         item = index.internalPointer()
#         if not item:
#             return QtCore.QModelIndex()
# 
#         parent = item.parent
#         if parent == self.root:
#             return QtCore.QModelIndex()
#         else:
#             return self.createIndex(parent.row(), 0, parent)
# 
#     def hasChildren(self, index):
#         if not index.isValid():
#             item = self.root
#         else:
#             item = index.internalPointer()
#         return item.hasChildren()
# 
#     def data(self, index, role=QtCore.Qt.DisplayRole):
#         if index.isValid() and role == QtCore.Qt.DisplayRole:
#             return index.internalPointer().data(index.column())
#         elif not index.isValid():
#             return self.root.getData()
# 
#     def headerData(self, section, orientation, role):
#         if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
#             return self.root.data(section)
# 
# class MyTree(QtGui.QTreeView):
#     def __init__(self, parent=None, model=SM):
#         super(MyTree, self).__init__(parent)
#         self.setModel(model())
# 
# 
# class Window(QtGui.QWidget):
#     def __init__(self, parent=None):
#         super(Window, self).__init__(parent)
#         self.initGui()
# 
#     def initGui(self):
#         vlo = QtGui.QVBoxLayout()
#         tree = MyTree(self)
#         vlo.addWidget(tree)
#         self.setLayout(vlo)
#         self.show()
# 
# def main():
#     app = QtGui.QApplication(sys.argv)
#     win = Window()
#     exit(app.exec_())
# 
# if __name__ == '__main__':
#     main()

'''Drag and Drop Example'''


# import sys
# from PyQt4 import QtGui
# from PyQt4 import QtCore
# from PyQt4.QtCore import Qt
#  
#  
# class DragFromWidget(QtGui.QDockWidget):
#  
#     def __init__(self, parent=None):
#         super(DragFromWidget, self).__init__(parent=parent)
#         self.layout().addWidget(QtGui.QLabel("Label!"))
#  
#     def dragEnterEvent(self, event):
#         print("dragEnterEvent")
#  
#     def mousePressEvent(self, event):
#         label = self.childAt(event.pos())
#         if not label:
#             return # nothing was selected
#         hotSpot = event.pos() - label.pos()
#         mimeData = QtCore.QMimeData()
#         mimeData.setText(label.text())
#         mimeData.setData("application/x-hotspot", str(hotSpot.x()))
#         pixmap = QtGui.QPixmap(label.size())
#         label.render(pixmap)
#  
#         drag = QtGui.QDrag(self)
#         drag.setMimeData(mimeData)
#         drag.setPixmap(pixmap)
#         drag.setHotSpot(hotSpot)
#  
#         dropAction = drag.exec_(Qt.CopyAction|Qt.MoveAction, Qt.CopyAction)
#         if dropAction == Qt.MoveAction:
#             label.close()
#  
#  
# class DragToWidget(QtGui.QDockWidget):
#  
#     def __init__(self, parent=None):
#         super(DragToWidget, self).__init__(parent=parent)
#         self.setAcceptDrops(True)
#  
#     def dragEnterEvent(self, event):
#         event.accept()
#  
#     def dropEvent(self, event):
#         print("'%s' was dropped onto me." % event)
#  
#  
# class SandboxApp(QtGui.QApplication):
#  
#     def __init__(self, *args, **kwargs):
#         super(SandboxApp, self).__init__(*args)
#         self.mainwindow = MainWindow()
#         self.mainwindow.show()
#  
#  
# class MainWindow(QtGui.QMainWindow):
#  
#     def __init__(self, parent=None):
#         super(MainWindow, self).__init__(parent=parent)
#         self.setDockOptions(QtGui.QMainWindow.AllowNestedDocks|QtGui.QMainWindow.AnimatedDocks)
#         self.addDockWidget(Qt.LeftDockWidgetArea, DragFromWidget())
#         self.addDockWidget(Qt.RightDockWidgetArea, DragToWidget())
#  
#  
# def main():
#     app = SandboxApp(sys.argv)
#     sys.exit(app.exec_())
#      
#  
#  
# if __name__ == "__main__":
#     main()
# 
# 
'''mdfreader'''

# import mdfreader
# import math
# import numpy as np
# import array
# import copy
# 
# class mfdWriteData(mdfreader.mdf):
#     
#     def __init__(self):
#         
#         super(mfdWriteData, self).__init__()
#         
#         time = [0.02 * i for i in range(1000)]
#         val1 = [math.sin(time[i]) for i in range(1000)]
#         val2 = [2 * math.sin(0.3 * time[i]) for i in range(1000)]
#         
#         nd_time = np.array(time, np.float64)
#         nd_val1 = np.array(val1, np.float64)
#         nd_val2 = np.array(val2, np.float64)
#         
#         self["val1"] = {}
#         self["val2"] = {}
#         self["time"] = {}
#         self["time_1"] = {}
#         self["time_2"] = {}
#         self["$CalibrationLog"] = {}
#         self["$EVENT_COMMENTS"] = {}
#         
#         self["val1"]["data"] = nd_val1
#         self["val2"]["data"] = nd_val2
#         self["time"]["data"] = nd_time
#         self["time_1"]["data"] = np.array([   0., time[-1]],np.float64)
#         self["time_2"]["data"] = np.array([   0. ],np.float64)
#         self["$CalibrationLog"]["data"] = array.array('c', [" "])
#         self["$EVENT_COMMENTS"]["data"] = array.array('c', ["D", "a", "t", "u", "m", ":",  "2", "7", ".", "1", "1", ".", "2", "0", "1", "5", " ",\
#                                                             " ", " ", " ", " ", "Z", "e", "i", "t", ":", " ", "1", "0", ":", "2", "1", ":", \
#                                                             "1", "1", "\\", "n", "\\", "n", "S", "t", "a", "r", "t", " ", "e", "v", "e", \
#                                                             "n", "t", " ", "o", "c", "c", "u", "r", "r", "e", "d"])
#         
#         self["val1"]["description"] = "des nd_val1"
#         self["val2"]["description"] = "des nd_val2"
#         self["time"]["description"] = "des time"
#         self["time_1"]["description"] = ""
#         self["time_2"]["description"] = ""
#         self["$CalibrationLog"]["description"] = ""
#         self["$EVENT_COMMENTS"]["description"] = ""
#         
#         self["val1"]["master"] = "time"
#         self["val2"]["master"] = "time"
#         self["time"]["master"] = "time"
#         self["time_1"]["master"] = "time_1"
#         self["time_2"]["master"] = "time_2"
#         self["$CalibrationLog"]["master"] = "time_1"
#         self["$EVENT_COMMENTS"]["master"] = "time_2"
#         
#         self["val1"]["masterType"] = 1
#         self["val2"]["masterType"] = 1
#         self["time"]["masterType"] = 1
#         self["time_1"]["masterType"] = 1
#         self["time_2"]["masterType"] = 1
#         self["$CalibrationLog"]["masterType"] = 1
#         self["$EVENT_COMMENTS"]["masterType"] = 1
#         
#         self["val1"]["unit"] = "[hPa]"
#         self["val2"]["unit"] = "[kg/s]"
#         self["time"]["unit"] = "[s]"
#         self["time_1"]["unit"] = "s"
#         self["time_2"]["unit"] = "s"
#         self["$CalibrationLog"]["unit"] = ""
#         self["$EVENT_COMMENTS"]["unit"] = ""
#         
# 
# 
# #_file = mdfreader.mdfreader.mdf()
# #_file.write("Tesetoutput.mdf")
# 
#     
# 
#         
# data = mfdWriteData()       
# #_file = mdfreader.mdfreader.mdf(u"D:/Temp/PyLinX/KleineTestdatei.dat")
# _file = mdfreader.mdfreader.mdf()
# 
# print "------------------------"
# print "var", "time_3"
# print "data", self.__dataDict[var][u"data"]
# print "len(data)", len(self.__dataDict[var][u"data"])
# print "master_channel", u"time" 
# print "master_type", self.__dataDict[var][u"masterType"]
# print "unit", str(self.__dataDict[var][u"unit"])
# print "description", str(self.__dataDict[var][u"description"])
# print "conversion",  None    
# 
# _file.add_channel(0, "time_3",\
#                    data["time"]["data"],\
#                    master_channel="time_3", \
#                    master_type = data["time"]["masterType"],\
#                    unit = data["time"]["unit"],\
#                    description = data["time"]["description"],\
#                    conversion = None)
# 
# 
# _file.add_channel(0, "val1",\
#                    data["val1"]["data"],\
#                    master_channel= "time_3", \
#                    master_type = data["val1"]["masterType"],\
#                    unit = data["val1"]["unit"],\
#                    description = data["val1"]["description"],\
#                    conversion = None)
# 
# # _file.add_channel(0, "val2",\
# #                    data["val2"]["data"],\
# #                    master_channel= "time_3", \
# #                    master_type = data["val2"]["masterType"],\
# #                    unit = data["val2"]["unit"],\
# #                    description = data["val2"]["description"],\
# #                    conversion = None)
# 
# _file.write("Tesetoutput3.mdf")
# print "ENDE"
#
# from mpl_toolkits.mplot3d import axes3d
# import matplotlib.pyplot as plt
# from matplotlib import cm
# 
# fig = plt.figure()
# ax = fig.gca(projection='3d')
# X, Y, Z = axes3d.get_test_data(0.05)
# ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.3)
# #cset = ax.contour(X, Y, Z, zdir='z', offset=-100, cmap=cm.coolwarm)
# #cset = ax.contour(X, Y, Z, zdir='x', offset=-40, cmap=cm.coolwarm)
# #cset = ax.contour(X, Y, Z, zdir='y', offset=40, cmap=cm.coolwarm)
# 
# ax.set_xlabel('X')
# #ax.set_xlim(-40, 40)
# ax.set_ylabel('Y')
# #ax.set_ylim(-40, 40)
# ax.set_zlabel('Z')
# #ax.set_zlim(-100, 100)
# 
# plt.show()

'''
CSV-Example
'''

# import csv
# 
# with open('D:/Projekte/PyLinX/Measure_5.ascii', 'rb') as csvfile:
#     #Heuristic for determining the deliminiter
#     strCSVFile = csvfile.read()
#     Chars =[';', '\t']
#     numChars = []
#     maxNumChars = 0
#     idxMaxNumChars = 0
#     for i,char in enumerate(Chars):
#         count = strCSVFile.count(char)
#         if maxNumChars > count:
#             idxMaxNumChars = i
#             maxNumChars = count 
#     delimiter = Chars[idxMaxNumChars]
# 
# with open('D:/Projekte/PyLinX/Measure_5.ascii', 'rb') as csvfile:    
#     print "delimiter", delimiter 
#     spamreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
#     for row in spamreader:
#         print row #', '
#     

''' Prototype for new getter and setter mechanism'''

# class dictCallbacks(dict):
#     
#     def __init__(self, * args, **kwargs):
#         super(dictCallbacks, self).__init__(*args, **kwargs)
#         
#     def addCallback(self, attr, callback):
#         if attr not in self:
#             self[attr] = callback
#         else:
#             raise Exception(u"Error dictCallbacks.addCallback: Callback for attribute \"" + attr + "\" allready exists!")
# 
# class classA(object):
#     
#     dictSetCallbacks = dictCallbacks({})
#     
#     def __init__(self):
#         self.__Attributes = {}
#         
#     def set(self, attr, val, **kwargs):
#  
#         if attr in classA.dictSetCallbacks:
#             classA.dictSetCallbacks[attr](self,val, **kwargs)
#         else:
#             self.__Attributes[attr] = val
#             
#     def set_attr1(self, val):
#         print "attr1 is set!"
#         self.__Attributes["attr1"] = val
#         
#     dictSetCallbacks.addCallback( "attr1", set_attr1)
#         
# class classB(classA):
#     
#     def __init__(self):
#         super(classB, self).__init__()
#     
#     def set_attr2(self, val):
#         print "attr2 is set!"
#         self._classA__Attributes["attr2"] = val
#                
#     classA.dictSetCallbacks.addCallback("attr2", set_attr2)
#         
# obj1 = classA()
# obj2 = classB()
# obj3 = classB()
# 
# obj1.set("attr1", 1)
# obj2.set("attr2", 2)
# obj2.set("attr1", 1)
# obj3.set("attr2", 4)
# obj3.set("attr1", 3)
# obj3.set("testattr", 4)
# 
# print "Ende"
'''strip'''


# def _strip(command):
#     command.strip()
#     commandList = []
#     word = u""
#     bStringPhrase = False
#     letterOld = None
#     for letter in command:
#         if letter == "\"":
#             word += letter
#             if not bStringPhrase:
#                 if letterOld == u" " or letterOld == None:
#                     bStringPhrase = True
#             else:
#                 commandList.append(word)
#                 word = u""
#                 bStringPhrase = False
#                 continue
#         else:
#             if not bStringPhrase:
#                 if letter != u" ":
#                     word += letter
#             else:
#                 word += letter
#                 continue
#         if letter == u" " and word != u"":
#             commandList.append(word)
#             word = u""
#         letterOld = letter
#     if word != u"":
#         commandList.append(word)
#     return commandList
# 
# 
# command = u"Hallo \"String mit einem Pfad\""
# print command
# print _strip(command)

'''Beispiel pyreverse (Erstellung von Klassengraphen '''
# import shlex
# import subprocess
# import PyLinXData.BContainer as BContainer   
# 
# file_name = BContainer.__file__
# command = 'pyreverse -c Composite -mn -a1 -s1 -f ALL -o png {0}'.format(file_name)
# print command
# #subprocess.call(shlex.split(command))
# #subprocess.call(command)