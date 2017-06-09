'''
Created on 19.08.2015

@author: Waetzold Plaum
'''
import sys
from PyQt4 import QtGui, QtCore
import copy

import PyLinXData.BContainer as BContainer 
import PyLinXData.PyLinXHelper as PyLinXHelper 
import PyLinXGui.PX_Templates as PX_Templ
import PyLinXData.PX_Signals 
from PyLinXCompiler import PyLinXRunEngine
import PyLinXData.PyLinXHelper as helper
import BController


class PyLinXProjectController(BController.BController):

    _dictSetCallbacks = copy.copy(BController.BController._dictSetCallbacks)    
    _dictGetCallbacks = copy.copy(BController.BController._dictGetCallbacks)    


    def __init__(self, rootGraphics = None, mainWindow = None, bListActions = True):
        
        super(PyLinXProjectController, self).__init__(None, mainWindow, bListActions, u"MainController")

        # Initializing some data structures
        ###################################
        self.activeFolder       = PyLinXData.PyLinXCoreDataObjects.PX_PlottableGraphicsContainer(self, u"rootGraphics")
        self._latentGraphics    = PyLinXData.PyLinXCoreDataObjects.PX_PlottableLatentGraphicsContainer(self, name="latentGraphics")
        self._signalFiles       = PyLinXData.PX_Signals.PX_SignalsFolder(self)
        self._objectHandler     = PyLinXData.PX_ObjectHandler.PX_ObjectHandler(self)
        PyLinXData.PX_DataDictionary.PX_DataDictionary(self)


        # Initializing the dictionary of avaiable constructors
        ######################################################
        dictConstructors = {    u"basicOperator"   : PyLinXData.PyLinXCoreDataObjects.PX_PlottableBasicOperator,\
                                u"connector"       : PyLinXData.PyLinXCoreDataObjects.PX_PlottableConnector,\
                                u"highlightRect"   : PyLinXData.PyLinXCoreDataObjects.PX_LatentPlottable_HighlightRect,\
                                u"varElement"      : PyLinXData.PyLinXCoreDataObjects.PX_PlottableVarElement,\
                                u"dataViewer"      : PyLinXData.PyLinXCoreDataObjects.PX_PlottableVarDispElement,\
                                u"signalFile"      : PyLinXData.PX_Signals.PX_Signals}
        self.paste(PyLinXData.BContainer.BDict(dictConstructors, name="dictConstructors"), bForceOverwrite = True)
        
        # Configuration of the dict of aliases
        ###################################### 
        dictAlias = self.getb("dictAlias")
        dictAlias[ u"@latent"]          = self._latentGraphics
        dictAlias[ u"@signals"]         = self._signalFiles
        dictAlias[ u"@objects"]         = self._objectHandler
        dictAlias[ u"@mainController"]  = self

  
        # The Controller could instantiated without a GUI. In this case no actions are avaiable
        #######################################################################################
        if bListActions:
            self.__listActions = [None, mainWindow.ui.actionNewElement, \
                                        mainWindow.ui.actionNewPlus,\
                                        mainWindow.ui.actionNewMinus, \
                                        mainWindow.ui.actionNewMultiplication, \
                                        mainWindow.ui.actionNewDivision] 


        # Seting sonme attributes
        #########################
        self._BContainer__Attributes[u"px_mousePressedAt_X"] = sys.maxint
        self._BContainer__Attributes[u"px_mousePressedAt_Y"] = sys.maxint
        self._BContainer__Attributes[u"px_mousePressedAt_x"] = sys.maxint
        self._BContainer__Attributes[u"px_mousePressedAt_y"] = sys.maxint
        self._BContainer__Attributes[u"bSimulationMode"]     = False
        self._BContainer__Attributes[u"bSimulationRuning"]   = False
        # These attributes are used to manage 
        # the selection mechanims
        self._BContainer__Attributes[u"Selection_bDeep"]     = False        
        self._BContainer__Attributes[u"bConnectorPloting"]   = False
        self._BContainer__Attributes[u"ConnectorToModify"]   = None
        self._BContainer__Attributes[u"idxPointModified"]    = None
        
        self.set(u"LogLevel",1)   
        # idx that indicates the selected tool
        self.set(u"idxToolSelected", helper.ToolSelected.none)
        # ID of the connector which is actually drawn
        self.set(u"ID_activeConnector", -1)
        # idx of the last selected Data-Viewer
        self.set(u"idxLastSelectedDataViewer", -1)
        self.set(u"idxOutPinConnectorPloting", None)
        self.set(u"listDataDispObj", [])
         
    
    ##############
    # PROPERTIES
    ##############    
   
    def get_objectHandler(self):
        return self.getb(u"ObjectHandler")
    
    objectHandler = property(get_objectHandler)        


    def get_latentGraphics(self):
        return self._latentGraphics
    
    def set_latentGraphics(self, latentGraphics, options = None):
        self._latentGraphics = latentGraphics
                
    latentGraphics = property(get_latentGraphics, set_latentGraphics)


    def get_signalFiles(self):
        return self._signalFiles
    
    def set_signalFiles(self, signalFiles, options = None):
        self._signalFiles = signalFiles
        
    signalFiles = property(get_signalFiles, set_signalFiles)

   
    # Execute specific commands
    ############################

    def execCommand_select(self, command):
        
        BController.BController.execCommand_select(self,command)
        
        self._BController__mainWindow.emit(QtCore.SIGNAL(u"dataChanged__latentObjects"))           
        
        # reset ConnectorToModify if necessary
        len_selection = len(self.selection)
        if len_selection  > 0:
            if len_selection  > 1:
                return  self.set(u"ConnectorToModify", None)
            else:
                ConnectorToModify = self.get(u"ConnectorToModify")
                if self.selection[0] != ConnectorToModify:
                    return  self.set(u"ConnectorToModify", None)
                                
        self.activeFolder.set(u"ConnectorToModify", None )
        self.activeFolder.set(u"idxPointModified" , None )
   
    
    ###################
    # GETTER and SETTER
    ###################

    # ConnectModInfo
    ################
    def get__ConnectModInfo(self):            
        return (super(PyLinXProjectController, self).get(u"ConnectorToModify"),\
                super(PyLinXProjectController, self).get(u"idxPointModified"))
    _dictGetCallbacks.addCallback(u"ConnectModInfo", get__ConnectModInfo)        

    def set__ConnectModInfo(self, value, options= None):  
        super(PyLinXProjectController, self).set(u"ConnectorToModify",self.mainController.activeFolder.getb(unicode(value[0])), options)
        super(PyLinXProjectController, self).set(u"idxPointModified",value[1], options)
    _dictSetCallbacks.addCallback(u"ConnectModInfo", set__ConnectModInfo)
    ConnectModInfo = property(get__ConnectModInfo, set__ConnectModInfo)

    # lenDataDictionary
    ###################
    def get__lenDataDictionary(self):
        if self.isInBody(u"DataDictionary"):
            return len(self.getb(u"DataDictionary"))
        else:
            return None
    _dictGetCallbacks.addCallback(u"lenDataDictionary", get__lenDataDictionary)
    
    def set__lenDataDictionary(self, value, options=None):
        if value == 0:
            DataDictionary = self.getb(u"DataDictionary")
            del DataDictionary
            DataDictionaryNew = BContainer.BDict({})
            DataDictionaryNew.set(u"Name", u"DataDictionary")
            DataDictionaryNew.set(u"DisplayName", u"DataDictionary")
            self._BContainer__Body[u"DataDictionary"] = DataDictionaryNew 
        else:
            raise Exception("Error PyLinXProjectController.__set_lenDataDictionary: set-values other then 0 are not accepted!")
    _dictSetCallbacks.addCallback(u"lenDataDictionary",  set__lenDataDictionary)    
    lenDataDictionary = property(get__lenDataDictionary, set__lenDataDictionary)

    # Selection_bUnlock
    ###################
    def get__Selection_bUnlock(self):
        bUnlockResult = False
        for element in self.selection:
            bUnlock = element.bUnlock
            bUnlockResult = bUnlock or bUnlockResult
        return bUnlockResult 
    _dictGetCallbacks.addCallback(u"Selection_bUnlock", get__Selection_bUnlock)
    Selection_bUnlock = property(get__Selection_bUnlock)        
        
        
    # dimActiveGraphics
    ###################
    def get__dimActiveGraphics(self):
        keys = self.activeFolder.getChildKeys()
        maxX = 0
        maxY = 0
        x = 0
        y = 0
        for key in keys:
            obj = self.activeFolder.getb(key)
            x = obj.X  
            if x > maxX:
                maxX = x
            y = obj.Y  
            if y > maxY:
                maxY = y
        return (maxX, maxY)
    _dictGetCallbacks.addCallback(u"dimActiveGraphics", get__dimActiveGraphics)
    dimActiveGraphics = property(get__dimActiveGraphics)   
    
    # idxToolSelected
    #################
    def set__idxToolSelected(self, value, options=None):
        if self.isAttr(u"idxToolSelected"):
            idxToolSelectedOld = self.get(u"idxToolSelected")
        else:
            idxToolSelectedOld = None
            
        if idxToolSelectedOld not in [None, 0]:
            oldAction = self.__listActions[idxToolSelectedOld]
            oldAction.setChecked(False)
        if value > 0 and value <= PyLinXHelper.ToolSelected.max:
            self.__listActions[value].setChecked(True)
            self._BContainer__Attributes[u"idxToolSelected"] = value
        elif value == 0:
            self._BContainer__Attributes[u"idxToolSelected"] = 0
    _dictSetCallbacks.addCallback(u"idxToolSelected",  set__idxToolSelected )
    idxToolSelected = property(lambda obj: PyLinXData.BContainer.BContainer.get(obj, u"idxToolSelected"), set__idxToolSelected)        

    # bSimulationMode
    #################
    def set_bSimulationMode(self, value, options=None):
        if value == True:
            runEngine = PyLinXRunEngine.PX_CodeAnalyser(self.mainController, self._BController__mainWindow)
            self.paste(runEngine, bForceOverwrite=True)
            pal = QtGui.QPalette()
            pal.setColor(QtGui.QPalette.Background,PX_Templ.color.backgroundSim)
            self._BController__mainWindow.ui.drawWidget.setPalette(pal)                
            self._BController__mainWindow.ui.actionRun.setEnabled(True)
            self._BController__mainWindow.ui.actionActivate_Simulation_Mode.setChecked(True)
            self._BController__mainWindow.ui.actionNewElement.setEnabled(False)
            self._BController__mainWindow.ui.actionNewPlus.setEnabled(False)
            self._BController__mainWindow.ui.actionNewMinus.setEnabled(False)
            self._BController__mainWindow.ui.actionNewMultiplication.setEnabled(False)
            self._BController__mainWindow.ui.actionNewDivision.setEnabled(False)
            self._BController__mainWindow.ui.actionStop.setEnabled(True)
            rootGraphics = self.getb(u"rootGraphics")
            rootGraphics.recur(PyLinXData.PyLinXCoreDataObjects.PX_PlottableVarDispElement, u"widgetShow", ())
        elif value == False:
            pal = QtGui.QPalette()
            pal.setColor(QtGui.QPalette.Background,PX_Templ.color.background)
            self._BController__mainWindow.ui.drawWidget.setPalette(pal)
            self._BController__mainWindow.ui.actionRun.setEnabled(False)
            self._BController__mainWindow.ui.actionActivate_Simulation_Mode.setChecked(False)
            self._BController__mainWindow.ui.actionNewElement.setEnabled(True)
            self._BController__mainWindow.ui.actionNewPlus.setEnabled(True)
            self._BController__mainWindow.ui.actionNewMinus.setEnabled(True)
            self._BController__mainWindow.ui.actionNewMultiplication.setEnabled(True)
            self._BController__mainWindow.ui.actionNewDivision.setEnabled(True)
            self._BController__mainWindow.ui.actionStop.setEnabled(False)
            rootGraphics = self.getb(u"rootGraphics")
            rootGraphics.recur(PyLinXData.PyLinXCoreDataObjects.PX_PlottableVarDispElement, u"widgetHide", ())
        else:
            raise Exception(u"Error PyLinXProjectController.set_bSimulationMode: value \"" + value +\
                            u"\" is not allowed for attribute \"bSimulationMoe\"")
        self._BContainer__Attributes[u"bSimulationMode"] = value    
        self._BController__mainWindow.emit(QtCore.SIGNAL("ctlChanged__simMode"))
    _dictSetCallbacks.addCallback(u"bSimulationMode",  set_bSimulationMode )           
    bSimulationMode = property(lambda obj: PyLinXData.BContainer.BContainer.get(obj, u"bSimulationMode"), set_bSimulationMode)        


    # bConnectorPloting
    ###################
    def set__bConnectorPloting(self, value, options=None):
        
        if self.bConnectorPloting:
            if value == False:
                self.latentGraphics.set(u"bConnectorPloting", False)
                #self.latentGraphics.set(u"bHasProxyElement", False)
                self.set(u"ConnectorPloting", None)
                self.set(u"idxToolSelected", PyLinXHelper.ToolSelected.none)
                self._BContainer__Attributes[u"bConnectorPloting"] = False
        else:      
            self._BContainer__Attributes[u"bConnectorPloting"] = True
        
    _dictSetCallbacks.addCallback(u"bConnectorPloting",  set__bConnectorPloting )       
    bConnectorPloting = property(lambda obj: PyLinXData.BContainer.BContainer.get(obj, u"bConnectorPloting"), set__bConnectorPloting)            
    
    # px_mousePressedAt_XY
    
    def set__px_mousePressedAt_XY(self, XY, options = None):
        self._BContainer__Attributes[u"px_mousePressedAt_X"] = XY[0]
        self._BContainer__Attributes[u"px_mousePressedAt_Y"] = XY[1]
        self._BController__mainWindow.emit(QtCore.SIGNAL("ctlChanged__tempDataObjectsData"))
    _dictSetCallbacks.addCallback(u"px_mousePressedAt_XY",  set__px_mousePressedAt_XY ) 
    
    def get__px_mousePressedAt_XY(self):
        return (self._BContainer__Attributes[u"px_mousePressedAt_X"], self._BContainer__Attributes[u"px_mousePressedAt_Y"])
    _dictGetCallbacks.addCallback(u"px_mousePressedAt_XY",  get__px_mousePressedAt_XY ) 
    px_mousePressedAt_XY = property(get__px_mousePressedAt_XY, set__px_mousePressedAt_XY)
    
    ######################################
    # Methods used for running simulations
    ######################################
    
    ## TODO: The mechanism of recur has to be modified by the use of lambda expressions
    # Ggf. zu verallgemeinern. Auch andere GUI-Teile koennten bei einem Exberiment zu verallgemeinern sein.

    # Method that synchronizes the DataDictionary with the data hold for graphical representation in the DataViewer
    def sync(self):
        self.recur(PyLinXData.PyLinXCoreDataObjects.PX_PlottableVarDispElement, u"sync", ())
        self.objectHandler.recorder.record()
        
    # Method that is executed when a run is stopped
    def stop_run(self):
        print "stop_run"
        self.recur(PyLinXData.PyLinXCoreDataObjects.PX_PlottableVarDispElement, u"stop_run", ())
        self.objectHandler.recorder.exit()
        self.set(u"bSimulationRuning", False)
    
    # Method to initialize a simulation run
    def runInit(self):
        self._objectHandler.runInit()
        self.set(u"bSimulationRuning", True)

    def updateDataDictionary(self):
        self._objectHandler.updateDataDictionary()
