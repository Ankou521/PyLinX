import sys
import math
import numpy as np
import copy

from PyQt4 import QtGui, QtCore
from PyLinXCompiler import PyLinXRunEngine
from PyLinXData import PyLinXCoreDataObjects
from PX_PlotterWidget import PlotterWidget
class DataViewerGui(QtGui.QMainWindow):
    def __init__(self, varDispObj, idx = 0, t_max = 1.,  mainGui = None, mainController = None):
        super (DataViewerGui, self).__init__()
        
        global DataDictionary
        
        self.setWindowIcon(QtGui.QIcon(r"pylinx_16.png"))
        
        self.varDispObj = varDispObj
        self.mainController = mainController
         
        self.idx = idx        
        
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.setGeometry(405,300,598,410)
        self.checkview = False
        ###########################
        ### Toolbar
        toolbar = QtGui.QToolBar()      
        toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.addToolBar(toolbar)
        self.plotterWidget = PlotterWidget.PlotterWidget(self.varDispObj, self, self.mainController)
        self.setCentralWidget(self.plotterWidget)

        self.items = QtGui.QDockWidget("Data List",self)
        self.labelview =  QtGui.QTableView()        
        self.tablemodel = self.plotterWidget.getTableModel()
        self.items.setWidget(self.labelview)
        self.items.setFloating(False)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.items)
        
        #######  Hiding number
        self.labelview.verticalHeader().setVisible(False)
   
        self.items.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures |
                                       QtGui.QDockWidget.DockWidgetMovable) 
        ### Actions
        self.adjustAction = QtGui.QAction('Adjust', self)
        self.adjustAction.setShortcut('Ctrl+A')
        self.adjustAction.triggered.connect(self.__onActionAdjust)
        toolbar.addAction(self.adjustAction)
        self.walkAxisAction = QtGui.QAction('Walking Axis', self)
        self.walkAxisAction.setShortcut('Ctrl+W')
        self.walkAxisAction.triggered.connect(self.__onActionWalkingAxis)
        self.walkAxisAction.setCheckable(True)
        toolbar.addAction(self.walkAxisAction)

        self.saveAction = QtGui.QAction('Save', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.triggered.connect(self.__onActionSave)
        toolbar.addAction(self.saveAction)

        self.osziAction = QtGui.QAction('Show Oszi', self)
        self.osziAction.setShortcut('Ctrl+O')
        self.osziAction.triggered.connect(self.__onActionLegendOszi)        
        self.osziAction.setCheckable(True) 
        self.osziAction.setChecked(True)
        
        toolbar.addAction(self.osziAction)


        self.legendAction = QtGui.QAction('Show Data List', self)
        self.legendAction.setShortcut('Ctrl+L')
        self.plotterWidget.show()
        self.items.hide()
        self.legendAction.triggered.connect(self.__onActionLegendOszi)
        self.legendAction.setCheckable(True)
        self.legendAction.setDisabled(False)
        toolbar.addAction(self.legendAction)
        
        self.sliderAction = QtGui.QAction('Slider', self)
        self.sliderAction.setShortcut('Ctrl+S')
        self.sliderAction.triggered.connect(self.__onActionSlider)
        self.sliderAction.setCheckable(True)
        toolbar.addAction(self.sliderAction)
        self.sliderAction.setEnabled(False)
        
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Data-Viewer " + str(self.idx))
        
        self.listVars = list(self.varDispObj.get(u"setVars"))
        
        self.oldDockWidgetArea = 0
        self.newDockWidgetArea = QtCore.Qt.RightDockWidgetArea
        self.items.dockLocationChanged.connect(self.__on_dockLocationChanged)
        
    def __onActionSlider(self):
        geometry = copy.copy(self.geometry())
        x = geometry.x()
        width = self.width()
        height = self.height()
        
        if self.sliderAction.isChecked():
            
            self.plotterWidget.checkTrue()
            self.checkview = True
            self.labelview.setColumnWidth(1,66)
            self.labelview.setColumnWidth(2,66)
            self.labelview.setColumnWidth(3,66)
       
            if self.legendAction.isChecked():
                self.items.hide()
            if self.newDockWidgetArea in (QtCore.Qt.LeftDockWidgetArea, \
                                              QtCore.Qt.RightDockWidgetArea)\
                        and not self.items.isVisible():
                width += self.items.width()
            if self.newDockWidgetArea in (QtCore.Qt.TopDockWidgetArea, \
                                               QtCore.Qt.BottomDockWidgetArea)\
                        and not self.items.isVisible():
                height += self.items.height()
                
            self.items.show()
            self.plotterWidget.setLine()
            self.plotterWidget.refreshPixmap()
        else:   
            self.plotterWidget.checkFalse()
            self.checkview = False
            width = 698
            self.labelview.setColumnWidth(1,100)
            self.labelview.setColumnWidth(2,100)
            self.items.hide()
            self.items.hide()
            if self.legendAction.isChecked():
                self.items.show()
        width = 698
        
        self.setGeometry(x, geometry.y(), width,  height)
    def __on_dockLocationChanged(self, newLocation):
        self.newDockWidgetArea = newLocation
        
    def __onActionAdjust(self):
        self.plotterWidget.adjust()  
        
    def __onActionSave(self):
        print "ActionSave"
        
    def  __onActionLegendOszi(self):
        geometry = copy.copy(self.geometry())
        x = geometry.x()
        
        width = self.width()
        height = self.height()
        if self.legendAction.isChecked():
            self.plotterWidget.setLine()
            self.plotterWidget.refreshPixmap()
            if self.newDockWidgetArea in (QtCore.Qt.LeftDockWidgetArea, \
                                              QtCore.Qt.RightDockWidgetArea)\
                        and not self.items.isVisible():
                width += self.items.width()
            if self.newDockWidgetArea in (QtCore.Qt.TopDockWidgetArea, \
                                               QtCore.Qt.BottomDockWidgetArea)\
                        and not self.items.isVisible():
                height += self.items.height()
            if self.osziAction.isChecked():
                self.labelview.setColumnWidth(0,40)
                self.labelview.setColumnWidth(1,100)
                self.labelview.setColumnWidth(2,100)
                if not self.plotterWidget.isVisible():
                    if self.newDockWidgetArea == QtCore.Qt.LeftDockWidgetArea:
                        x -= self.plotterWidget.width()
                    if self.newDockWidgetArea in ( QtCore.Qt.LeftDockWidgetArea, QtCore.Qt.RightDockWidgetArea):
                        width += self.plotterWidget.width()
                    if self.newDockWidgetArea in (QtCore.Qt.TopDockWidgetArea, \
                                               QtCore.Qt.BottomDockWidgetArea):
                        height += self.plotterWidget.height()
                
                self.plotterWidget.show()
                self.adjustAction.setVisible(True) 
                self.walkAxisAction.setVisible(True)                                
                self.legendAction.setEnabled(True)
                self.sliderAction.setEnabled(True)
                
                self.osziAction.setEnabled(True)
                self.items.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures |
                                       QtGui.QDockWidget.DockWidgetMovable)                  
            else:
                
                if self.plotterWidget.isVisible() and \
                        self.newDockWidgetArea == QtCore.Qt.LeftDockWidgetArea:
                    x += self.plotterWidget.width()
                if self.newDockWidgetArea in (QtCore.Qt.TopDockWidgetArea, QtCore.Qt.BottomDockWidgetArea)\
                            and self.plotterWidget.isVisible():
                    height -= self.plotterWidget.height()
                if self.newDockWidgetArea in ( QtCore.Qt.LeftDockWidgetArea, QtCore.Qt.RightDockWidgetArea):
                    width -= self.plotterWidget.width()
                self.labelview.setColumnWidth(0,1)
                self.labelview.setColumnWidth(1,125)
                self.labelview.setColumnWidth(2,125)
                
                self.plotterWidget.hide()
                self.adjustAction.setVisible(False) 
                self.walkAxisAction.setVisible(False)                
                self.legendAction.setEnabled(False)
                self.sliderAction.setEnabled(False)
                self.osziAction.setEnabled(True)
                self.items.setFloating(False)
                self.items.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures |
                                       QtGui.QDockWidget.DockWidgetMovable) 
            self.items.show()
        else:
            self.sliderAction.setEnabled(True)
            if self.osziAction.isChecked(): 
                    
                self.items.hide()
                if self.newDockWidgetArea in (QtCore.Qt.LeftDockWidgetArea, \
                                                  QtCore.Qt.RightDockWidgetArea):
                    width -= self.items.width()
                if self.newDockWidgetArea in (QtCore.Qt.TopDockWidgetArea, \
                                                   QtCore.Qt.BottomDockWidgetArea)\
                            and not self.items.isVisible():                
                    height -= self.items.height()
                self.plotterWidget.show()
                self.adjustAction.setVisible(True) 
                self.walkAxisAction.setVisible(True)                 
                self.legendAction.setEnabled(True)
                self.osziAction.setEnabled(False)
        
        self.setGeometry(x, geometry.y(), width,  height)
        
    def __onActionWalkingAxis(self):
        if self.walkAxisAction.isChecked():
            self.plotterWidget.setBWalkingAxis(True)
        else:
            self.plotterWidget.setBWalkingAxis(False)
            
    def updateValues(self):
            
        self.plotterWidget.updateValues()
        self.labelview.setModel(self.tablemodel)
        self.tablemodel.dataChanged.emit(self.tablemodel.index(0,0), self.tablemodel.index(3,3))
        
        self.labelview.setColumnWidth(0,40)
        if self.checkview == True:
            self.labelview.setColumnWidth(1,66)
            self.labelview.setColumnWidth(2,66)
            self.labelview.setColumnWidth(3,66)
        else:
            self.labelview.setColumnWidth(1,100)
            self.labelview.setColumnWidth(2,100)
            
        if self.osziAction.isChecked() == False and self.legendAction.isChecked():
            self.labelview.setColumnWidth(0,1)
            self.labelview.setColumnWidth(1,125)
            self.labelview.setColumnWidth(2,125)
            self.sliderAction.setEnabled(True)
        
        self.plotterWidget.checkFalse()
        self.checkview = False
        
        self.items.setMinimumWidth(243)
        self.items.setMaximumWidth(243)
        
        if self.mainController.get(u"bSimulationRuning") == True:
            self.sliderAction.setEnabled(False)
            
    def addVar(self, varName):
        print "addVar"
        self.plotterWidget.addVar(varName)
            
    def delVar(self, varName):
        print "delVar"
        self.plotterWidget.delVar(varName)
        
    def stop_run(self):
        if self.sliderAction.isChecked():
            self.plotterWidget.checkTrue()
            self.checkview = True
            self.plotterWidget.refreshPixmap()
        self.plotterWidget.setLine()
        if self.osziAction.isChecked() == False and self.legendAction.isChecked():
            self.sliderAction.setEnabled(False)
        else:    
            self.sliderAction.setEnabled(True)
        self.plotterWidget.stop_run()
