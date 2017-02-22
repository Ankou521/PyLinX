'''
Created on 30.10.2014

@author: Waetzold Plaum
'''
# General Libraries - alphabedic order
import copy
import cProfile
import ctypes
import inspect
import os
from PyQt4 import QtGui, QtCore, uic, Qt
import sys
import threading
import Queue
import codecs
from PyQt4.QtCore import pyqtSignal

import PyLinXData
import PyLinXData.PyLinXHelper as PyLinXHelper
import PyLinXData.PX_Signals as PX_Signals
import PyLinXData.PX_DataDictionary as PX_DataDictionary 
from PyLinXGui import *
from PyLinXCompiler import *
import PyLinXGui.PX_Templates as PX_Templ
import PyLinXGui.PX_TabWidget_main as PX_TabWidget_main
import PyLinXGui.PX_Tab_SignalSelect as PX_Tab_SignalSelect
import PyLinXGui.PX_CommandConsole as PX_CommandConsole 
import PyLinXGui.PX_Tab_Recorder as PX_Tab_Recorder
import PyLinXData.PyLinXHelper as helper
from PyLinXCtl import PyLinXProjectController

# NEW
import PyLinXGui.PX_Tab_ObjectHandlerList as PX_Tab_ObjectHandlerList


class PyLinXMain(QtGui.QMainWindow):
    
    def __init__(self):
 
        super(PyLinXMain, self).__init__()

        # Loading ui-file
        uiString = u".//Recources//Ui//PyLinX_v0_5.ui"
        self.ui = uic.loadUi(uiString)
        
        reload(sys) 
        sys.setdefaultencoding('utf8')


        self.runThreadMessageQueue = Queue.Queue()
        #QtGui.QApplication.setStyle( QtGui.QStyleFactory.create('cleanlooks') )
        #QtGui.QApplication.setStyle( QtGui.QStyleFactory.create('plastique') )
        #QtGui.QApplication.setStyle( QtGui.QStyleFactory.create('motif') )
        #QtGui.QApplication.setStyle( QtGui.QStyleFactory.create('cde') )
        
        
        ######################
        # Main Data Structures
        ######################
        
        self.mainController = PyLinXProjectController.PyLinXProjectController(mainWindow = self )
        _rootGraphics = self.mainController.getb(u"rootGraphics")

        # run Engine
        self.runEngine = None

        # Events
        self.stopRunEvent = threading.Event()
        self.repaintEvent = threading.Event()
        
        
        ##########################
        # Building the main Window
        ##########################
        
        # Decoration
        self.ui.setWindowIcon(QtGui.QIcon(r"icons/pylinx_16.png"))
        self.ui.setWindowTitle('PyLinX')        
        
        # ScrollArea
        self.ui.scrollingArea = QtGui.QScrollArea()
        self.ui.scrollingArea.setAutoFillBackground(False)
        
        # DrawWidget
        self.ui.drawWidget = PX_Widget_MainDrawArea.DrawWidget(self.mainController, self, self.repaintEvent )        
        
        ############
        # TabWidgets
        ############
        
        # TabWidget left
        ################

        self.ui.TabWidgetLeft = PX_TabWidget_main.PX_TabWidget_main(mainController = self.mainController)
        
        self.ui.TabWidgetLeft.setMinimumWidth(260)
        
        # Info
        self.ui.TabInfo = QtGui.QWidget() 
        self.ui.TabWidgetLeft.adjoinTab(self.ui.TabInfo, u"Info", PX_TabWidget_main.PX_TabWidget_main.DisplayRole.inEditAndSimulationMode,1)
        # Signals
        self.ui.TabSignals = PX_Tab_SignalSelect.PX_Tab_SignalSelect(self.mainController, drawWidget = self.ui.drawWidget  )
        self.ui.TabWidgetLeft.adjoinTab(self.ui.TabSignals, u"Signals", PX_TabWidget_main.PX_TabWidget_main.DisplayRole.onlyInSimulationMode,2)
        # Elements
        self.ui.TabElements = PX_Tab_ObjectHandlerList.PX_Tab_ObjectHandlerList(self.mainController)
        self.ui.TabWidgetLeft.adjoinTab(self.ui.TabElements, u"Elements", PX_TabWidget_main.PX_TabWidget_main.DisplayRole.onlyInEditMode,3)
        # Recorder
        self.ui.Tabrecorder = PX_Tab_Recorder.PX_Tab_Recorder(self.mainController)
        self.ui.TabWidgetLeft.adjoinTab(self.ui.Tabrecorder, u"Recorder", PX_TabWidget_main.PX_TabWidget_main.DisplayRole.onlyInSimulationMode,4)
        
        #Connect Signal
        self.connect(self, QtCore.SIGNAL("ctlChanged__simMode"), self.ui.TabWidgetLeft.updateTabs)
        
        # TabWidget Bottom
        ##################

        # Console
        self.ui.Console = PX_CommandConsole.PX_CommandConsole(parent = self, mainController = self.mainController)    

        self.ui.TabWidgetBottom = PX_TabWidget_main.PX_TabWidget_main(mainController = self.mainController, TabPosition = QtGui.QTabWidget.North)
        self.ui.TabWidgetBottom.adjoinTab(self.ui.Console, u"Console", PX_TabWidget_main.PX_TabWidget_main.DisplayRole.inEditAndSimulationMode,1)

        #_widget = QtGui.QWidget()
        #self.ui.TabWidgetBottom.adjoinTab(_widget, u"Info", PX_TabWidget_main.PX_TabWidget_main.DisplayRole.inEditAndSimulationMode,2)
        
        self.ui.TabWidgetBottom.setMinimumHeight(120)
        
        #self.ui.TabWidgetBottom.updateTabs()
        
        #Connect Signal
        self.connect(self, QtCore.SIGNAL("ctlChanged__simMode"), self.ui.TabWidgetBottom.updateTabs)
        
        # Building drawWidget and Console
        self.ui.mainWidget = QtGui.QWidget(self)

        # Splitter 2
        self.ui.splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.ui.splitter2.addWidget(self.ui.scrollingArea)
        self.ui.splitter2.addWidget(self.ui.TabWidgetBottom)        
        self.ui.splitter2.setStretchFactor(1,1)
        self.ui.splitter2.setStretchFactor(0,3)
        self.ui.splitter2.setStyleSheet("""
         .QSplitter {
             padding-left: 0px;
             padding-top: 0px;
             padding-right: 0px;
             }
         """)

        
        
        # Splitter 1
        self.ui.splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.ui.splitter1.addWidget(self.ui.TabWidgetLeft)
        self.ui.splitter1.addWidget(self.ui.splitter2)
        self.ui.splitter1.setStretchFactor(1,4)
        self.ui.splitter1.setStretchFactor(0,1)
        self.ui.splitter1.setStyleSheet("""
        .QSplitter {
            padding-left: 8px;
            padding-top: 8px;
            padding-right: 8px;
            }
        """)



        

        # Connecting ScrollingArea and DrawingArea
        self.ui.scrollingArea.setWidget(self.ui.drawWidget)        

        # Set central Widget
        self.ui.setCentralWidget(self.ui.splitter1)


        ####################
        # Connecting Signals
        ####################
        
        self.connect(self.ui.drawWidget, QtCore.SIGNAL(u"guiAction__drawWidget_dropped"),self.ui.TabSignals.repaint)
        self.connect(self, QtCore.SIGNAL(u"dataChanged__coreDataObjects"),self.ui.TabElements.repaint)
        self.connect(self, QtCore.SIGNAL(u"ctlChanged__commandInit"), self.ui.Console.commandInit)
        self.connect(self, QtCore.SIGNAL(u"ctlChanged__commandExit"), self.ui.Console.commandExit)
        

        # Menu-Bar
            
        # Programm
        
        self.ui.actionClose.triggered.connect(self.closeApplication)
        
        # Project
        
        self.ui.actionNewProject.triggered.connect(self.on_actionNewProject)
        self.ui.actionLoadProject.triggered.connect(self.on_actionLoadProject)
        self.ui.actionSave.triggered.connect(self.on_actionSave)
        self.ui.actionSave_As.triggered.connect(self.on_actionSave_As)
        
        # Tool-Bar
        
        self.ui.actionNewElement.triggered.connect(self.on_actionNewElement)
        self.ui.actionNewElement.setCheckable(True)
        self.ui.actionNewPlus.triggered.connect(self.on_actionNewPlus)
        self.ui.actionNewMinus.triggered.connect(self.on_actionNewMinus)
        self.ui.actionNewMultiplication.triggered.connect(self.on_actionNewMultiplication)
        self.ui.actionNewDivision.triggered.connect(self.on_actionNewDivision)
        
        self.ui.actionNewPlus.setCheckable(True)
        self.ui.actionNewMinus.setCheckable(True)
        self.ui.actionNewMultiplication.setCheckable(True)
        self.ui.actionNewDivision.setCheckable(True)
        self.ui.actionRun.setEnabled(False)
        self.ui.actionActivate_Simulation_Mode.triggered.connect(self.on_Activate_Simulation_Mode)
        # The order of cennoction will determine the order of calls
        self.ui.actionRun.triggered.connect(self.ui.Tabrecorder.runInit)
        self.ui.actionRun.triggered.connect(self.on_run)
        self.ui.actionStop.triggered.connect(self.on_stop)

        # Configurations that require the GUI to exist
        self.mainController.bSimulationMode = False

        ################
        # ExampleData
        ################

        #_file = open(r"D:\Projekte\PyLinX\Aptana-Projekte\PyLinX2\Recources\Testfiles\testBugOszi.pyp")
        _file = open(r"D:\Projekte\PyLinX\Aptana-Projekte\PyLinX2\Recources\Testdata\testProjekt_setUeberarbeitung.pyp")
        self.__loadFile(_file)

        script = u"new varElement TestVar_0 150 90 15 refName=\"TestVar_0\"\n\
new varElement Variable_id4 150 140 15 refName=\"Variable_id4_1\" \n\
new varElement Variable_id4 400.0 100.0 15 refName=\"Variable_id4_2\"\n\
new basicOperator + 300.0 100.0 name=u\"Operator_1\"\n\
new connector TestVar_0 Operator_1 idxInPin=-1\n\
new connector Variable_id4_1 Operator_1 idxInPin=-2\n\
new connector Operator_1 Variable_id4_2 idxInPin=-1"

        ############
        # Finish
        ############
        
        # Show GUI
        self.ui.resize(1200,800)
        self.ui.show()
        
######################
# Methods
#####################
    
    def get_DrawWidgetSize(self):
        return (self.ui.scrollingArea.width(), self.ui.scrollingArea.height())

# Callbacks
####################

    def closeApplication(self):
        
        if QtGui.QMessageBox.question(None, u"", u"Soll PyLinX wirklich beendet werden?", \
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,QtGui.QMessageBox.No)\
                 == QtGui.QMessageBox.Yes:
            QtGui.QApplication.quit()
            
    def on_actionNewElement(self):
        
        if self.mainController.get(u"idxToolSelected") == PyLinXHelper.ToolSelected.none:
            self.mainController.set(u"idxToolSelected", PyLinXHelper.ToolSelected.newVarElement) 
        else:
            self.mainController.set(u"idxToolSelected", PyLinXHelper.ToolSelected.none)
            
    def on_actionNewPlus(self):
        
        if self.mainController.get(u"idxToolSelected") == PyLinXHelper.ToolSelected.none:
            self.mainController.set(u"idxToolSelected", PyLinXHelper.ToolSelected.newPlus) 
        else:
            self.mainController.set(u"idxToolSelected", PyLinXHelper.ToolSelected.none)

    def on_actionNewMinus(self):
        
        if self.mainController.get(u"idxToolSelected") == PyLinXHelper.ToolSelected.none:
            self.mainController.set(u"idxToolSelected", PyLinXHelper.ToolSelected.newMinus) 
        else:
            self.mainController.set(u"idxToolSelected", PyLinXHelper.ToolSelected.none)
            
    def on_actionNewMultiplication(self):
        
        if self.mainController.get(u"idxToolSelected") == PyLinXHelper.ToolSelected.none:
            self.mainController.set(u"idxToolSelected", PyLinXHelper.ToolSelected.newMultiplication) 
        else:
            self.mainController.set(u"idxToolSelected", PyLinXHelper.ToolSelected.none)
            
    def on_actionNewDivision(self):
        
        if self.mainController.get(u"idxToolSelected") == PyLinXHelper.ToolSelected.none:
            self.mainController.set(u"idxToolSelected", PyLinXHelper.ToolSelected.newDivision) 
        else:
            self.mainController.set(u"idxToolSelected", PyLinXHelper.ToolSelected.none)

            
    def on_actionSave(self):
        rootGraphics = self.mainController.getb(u"rootGraphics")
        if rootGraphics.isAttr(u"strSavePath"):
            strSavePath = rootGraphics.get(u"strSavePath")
            self.__saveProject(strSavePath)
        else:
            self.on_actionSave_As()

    
    def on_actionSave_As(self):
        if self.mainController.isAttr(u"strSavePath"):
            strSavePath_old = self.mainController.get(u"strSavePath")
            (strPath, strSavePath_old_file) = os.path.split(strSavePath_old)
        else:
            strPath = os.getcwd()
        strSavePath= PyLinXHelper.showFileSelectionDialog(self.ui,strPath, bDir = False, strExt = u"*.pyp", \
                                                    strHeader =u"Select File to save Project...",\
                                                    dialogType = u"save",\
                                                    bFileObject = False)
        (strSavePath_base,strSavePath_ext) = os.path.splitext(strSavePath)
        if not  strSavePath_ext == u"pyp":
            strSavePath = strSavePath_base + u".pyp"
        self.__saveProject(strSavePath)

     
    def __saveProject(self, strSavePath):    
        
        _file = codecs.open(strSavePath, encoding='utf-8', mode='w')
        
        listCommands = self.mainController.listCommands
        strCommands = u""
        for command in listCommands:
            strCommands += command
            strCommands += u"\n"
        _file.write(strCommands)
        _file.close()
        rootGraphics = self.mainController.getb(u"rootGraphics")
        rootGraphics.set(u"strSavePath", strSavePath)

  
    def on_actionLoadProject(self):
         
        strPath = os.getcwd()
        _file, strSavePath = PyLinXHelper.showFileSelectionDialog(self.ui,strPath, bDir = False,strHeader ="Select File to load Project...",\
                                                     strExt = u"*.pyp",\
                                                     dialogType = u"load")  
 
        self.__loadFile(_file)

        rootGraphics = self.mainController.getb(u"rootGraphics")
        rootGraphics.set(u"strSavePath", strSavePath)           
    
    def __loadFile(self, _file):
                
        if _file == None:
            return
        old_Controller = self.mainController
        self.mainController = PyLinXProjectController.PyLinXProjectController(mainWindow = self )
        # TODO: should be removed in the long term
        self.ui.drawWidget.newProject(self.mainController)
        self.ui.TabWidgetLeft.newProject(self.mainController)
        self.ui.TabWidgetBottom.newProject(self.mainController)
        
        _file_read = _file.read()
        self.mainController.execScript(_file_read)
        old_Controller.delete()
        self.ui.repaint()

    
    def on_actionNewProject(self):
        rootGraphicsNew = PyLinXData.PyLinXCoreDataObjects.PX_PlottableObject(None, u"rootGraphics")
        self.mainController.delete(u"rootGraphics")
        self.mainController.paste(rootGraphicsNew)
        self.mainController.bSimulationMode = False
        self.ui.drawWidget.activeGraphics = rootGraphicsNew
        self.ui.drawWidget.repaint()
        

        
    def on_Activate_Simulation_Mode(self):
        
        bSimulationMode = self.mainController.bSimulationMode
        if bSimulationMode:
            self.mainController.execCommand(u"@mainController set bSimulationMode False")
        else:
            self.mainController.execCommand(u"@mainController set bSimulationMode True")
        self.ui.repaint() 
                
    def on_run(self):
        
        self.runEngine = self.mainController.getb(u"PX_CodeGeerator")
        self.runEngine.startRun(self.ui.drawWidget, self.stopRunEvent, self.repaintEvent)

            
    def on_stop(self):
        self.runThreadMessageQueue.put(u"stopRun")
        

def _run():
    app = QtGui.QApplication(sys.argv)
    PyLinXMain()   
    app.exec_()
    
    
if __name__ == '__main__':
    
    PROFILE = False
    
    if PROFILE:
        cProfile.run('_run()')
    else:
        #exec('_run()')
        _run()