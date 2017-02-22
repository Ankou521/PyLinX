'''
Created on 18.08.2015

@author: Waetzold Plaum
'''

# General Libraries - alphabedic order
import copy
import inspect
from PyQt4 import QtGui, QtCore #, #uic, Qt
import sys

# Project specific Libraries - alphabedic order
import PX_Dialogue_SelectDataViewer
import PX_Dialogue_SimpleStimulate
import PX_Templates as PX_Templ
import PyLinXData.PyLinXHelper as helper
import PyLinXData.PyLinXCoreDataObjects as PyLinXCoreDataObjects

class DrawWidget (QtGui.QWidget):

    def __init__(self, mainController, mainWindow, repaintEvent):
        super(DrawWidget, self).__init__()
        p = self.palette()
        p.setColor(QtGui.QPalette.Window, PX_Templ.color.background)
        self.setPalette(p)
        self.repaintEvent = repaintEvent
        self.mainController = mainController
        self.rootGraphics = mainController.getb(u"rootGraphics")
        self.latentGraphics = mainController.latentGraphics 
        self.activeGraphics = self.rootGraphics
        self.mainController.set(u"ConnectorToModify", None)
        self.mainController.set(u"idxPointModified" , None)
        self.mainWindow = mainWindow
        self.setMouseTracking(True)

        self.setFocus(QtCore.Qt.PopupFocusReason) 
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        # set button context menu policy
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        # create context menu
        self.popMenu_SimulationMode = QtGui.QMenu(self)
        iconMeasure   = QtGui.QIcon(u".//Recources//Icons//measure24.png")
        iconStimulate = QtGui.QIcon(u".//Recources//Icons//stimulate24.png")
        self.actionMeasure   = QtGui.QAction(iconMeasure,    u"Measure", self)
        self.actionStimulate = QtGui.QAction(iconStimulate , u"Stimulate", self)
        self.actionMeasure.setCheckable(True)
        self.actionStimulate.setCheckable(True)
        self.popMenu_SimulationMode.addAction(self.actionStimulate)
        self.popMenu_SimulationMode.addAction(self.actionMeasure)

        self.setEnabled(True)
        self.setAcceptDrops(True)
        
        # Connecting signals       
        self.connect(self, QtCore.SIGNAL(u"customContextMenuRequested(const QPoint&)"), self.on_context_menu)
        self.connect(self, QtCore.SIGNAL(u"dataChanged__objectHandler"), self.repaint)
        self.connect(self, QtCore.SIGNAL(u"dataChanged__latentDataObjects"), self.repaint)
        self.connect(self, QtCore.SIGNAL(u"dataChanged__coreDataObjects"), self.repaint)
        self.connect(self, QtCore.SIGNAL(u"ctlChanged__tempDataObjectsData"), self.repaint)
        self.mainWindow.connect(self.mainWindow, QtCore.SIGNAL(u"dataChanged__latentObjects"), self.repaint)
        self.mainWindow.connect(self.mainWindow, QtCore.SIGNAL(u"dataChanged__coreDataObjects"), self.repaint)
        
    def sizeHint(self):
        maxXY = self.mainController.dimActiveGraphics
        maxXY2 = self.mainWindow.get_DrawWidgetSize()
        x = max(maxXY[0] + 60, maxXY2[0]) - 2
        y = max(maxXY[1] + 40,maxXY2[1]) - 2
        size = QtCore.QSize(x,y)
        self.resize(size) 
        return size 
     
    ###################
    # Drag and Drop
    ###################
    
    def dragEnterEvent(self, event):
        event.accept()
 
    
    def __variableInSimMOde(self, coord): 
        if self.mainController.bSimulationMode:
            objInFocus = self.activeGraphics.getObjectInFocus(coord)
            if len(objInFocus) > 0:
                var = objInFocus[0]
                types = inspect.getmro(type(var))
                if PyLinXCoreDataObjects.PX_PlottableVarElement in types:
                    return var
        return None
        
    
    def dropEvent(self, e):
        var = self.__variableInSimMOde(e.pos())
        if var:
            signal = e.mimeData().text()
            command = u"@objects set ./variables/"  + var.get(u"DisplayName") + u".signalMapped " + unicode(signal)
            self.mainController.execCommand(command)
            self.emit(QtCore.SIGNAL(u"guiAction__drawWidget_dropped"))


    def getStimulationActivateCommand(self,var, values):
        strValues = repr(values).replace(" ", "")
        objPath = var.objPath
        stimFunction = values[u"StimulationFunction"]
        attributeToSet =  PX_Templ.PX_DiagData.StimAttribute[stimFunction ]
        ustrExec =  u"set " + objPath[:-1] + u"." + attributeToSet + u" " + unicode(strValues)
        return ustrExec
    
    def getMeasureCommand(self,var, values):
        listSelectedDispObj_new = []
        idx = self.mainController.get(u"idxLastSelectedDataViewer")
        for key in values:
            if u"bDataViewer_" in key:
                if values[key]:
                    listSelectedDispObj_new.append(int(key[12:]))
        if values[u"bNewDataViewer"]:
            execStr = u"new dataViewer 50 50"
            newVarDispObj = self.mainController.execCommand(execStr)
            idx = newVarDispObj.get(u"idxDataDispObj")
            listSelectedDispObj_new.append(idx)
        execStr = u"set " + var.objPath[:-1] + u".listSelectedDispObj " +\
                unicode(repr(listSelectedDispObj_new).replace(u" ", u""))
        return execStr

    def on_context_menu(self, coord):
        
        def showPopup(bStimulate, bMeasure):
            self.actionMeasure.setChecked(bMeasure)
            self.actionStimulate.setChecked(bStimulate)
            self.popMenu_SimulationMode.exec_(self.mapToGlobal(coord))
            actionMeasureIsChecked = self.actionMeasure.isChecked()
            actionStimulateIsChecked = self.actionStimulate.isChecked()
            return actionMeasureIsChecked, actionStimulateIsChecked
            
        # show context menu
        var = self.__variableInSimMOde(coord)
        if var:
            bStimulate  = var.get(u"bStimulate")
            bMeasure    = var.get(u"bMeasure")
            
            actionMeasureIsChecked, actionStimulateIsChecked = showPopup(bStimulate,bMeasure)
            
            command = None
            if actionStimulateIsChecked and not bStimulate:
                OK, values = PX_Dialogue_SimpleStimulate.PX_Dialogue_SimpleStimulate.getParams(self, var,self.mainController, self)
                if OK == True:
                    self.actionStimulate.setChecked(True)
                    command = self.getStimulationActivateCommand(var, values)
            elif not actionStimulateIsChecked and bStimulate:
                command = u"set " + var.objPath[:-1] + u".StimulationFunction None"
                
            if actionMeasureIsChecked and not bMeasure:
                OK, value = PX_Dialogue_SelectDataViewer.PX_Dialogue_SelectDataViewer.getParams( self,var,self.mainController,self)
                if OK == True:
                    self.actionMeasure.setChecked(True)
                    command = self.getMeasureCommand(var, value)
            elif not actionMeasureIsChecked and bMeasure:
                command = u"set " + var.objPath[:-1] + u".listSelectedDispObj []"
                                       
            if command != None:
                self.mainController.execCommand(command)
            

    def newProject(self, mainController):
        self.rootGraphics   = mainController.root
        self.activeGraphics = mainController.activeFolder
        self.mainController = mainController
        self.latentGraphics = mainController.latentGraphics
    
    def paintEvent(self, event = None):
        self.activeGraphics.write(self,PX_Templ.Plot_Target.Gui)
        self.latentGraphics.write(self,PX_Templ.Plot_Target.Gui)
        super(DrawWidget, self).paintEvent(event)
        
    def keyPressEvent(self, qKeyEvent):

        def __keyPressEvent_delete():
        
            objectsInFocus = list(self.mainController.selection)
            setDel = set([])
            # deleting elements and preparing a list of connectors, which has to be deleted 
            for key in self.activeGraphics._BContainer__Body:    
                element = self.activeGraphics.getb(key)
                bUnlock = element.get(u"bUnlock")
                if bUnlock: 
                    types = inspect.getmro(type(element))
                    if (PyLinXCoreDataObjects.PX_PlottableConnector in types):
                        # deleting all connectors which are connected to an object, that is deleted
                        elem0 = element.elem0
                        if elem0 in objectsInFocus:
                            setDel.add(unicode(element.ID) + u"_id" + unicode(element.ID))
                        elem1 = element.elem1
                        if elem1 in objectsInFocus:
                            setDel.add(unicode(element.ID) + u"_id" + unicode(element.ID))
                    # deleting all objects in focus
                    if (element in objectsInFocus):
                        setDel.add(element.get(u"Name"))
            # writing the command
            command = u"del"
            for delItem in setDel:
                command += " " + unicode(delItem)
                           
            self.mainController.execCommand(command)

       
        #################
        # Main Method
        #################
        
        # Deleting Objects      
        if qKeyEvent.key() == QtCore.Qt.Key_Delete:
            __keyPressEvent_delete()
        else:
            super(DrawWidget, self).keyPressEvent(qKeyEvent)
    
    def mousePressEvent(self, coord):

        def mousePressEvent_tool_none():

            objInFocusOld = list(self.mainController.selection)
            objInFocus = self.activeGraphics.getObjectInFocus(coord)
            
            # Create HighlightObject if necessary.
            #  This is not done by command since
            #  the highlight rect is not considered
            #  to be part of the data
            # selecting clicked element by command
            #######################################
            
            len_objectsInFocus  = len(objInFocus)
            if len(set(objInFocus).intersection(set(objInFocusOld))) == 0:
                if len_objectsInFocus == 0:
                    if len(self.mainController.selection) > 0:
                        self.mainController.execCommand(u"select")
                    PyLinXCoreDataObjects.PX_LatentPlottable_HighlightRect(self.latentGraphics,coord.x(), coord.y())
                else:
                    if set(objInFocus) != set(self.mainController.selection):
                        usttObj = [obj.get(u"Name") for obj in objInFocus]
                        self.mainController.execCommand(u"select " + u" ".join(usttObj))
                

                    
            # move lines of connectors
            ##########################
            
            # Detect index of line to modify and save it in active graphics
            if len_objectsInFocus == 1:
                activeObject = objInFocus[0]
                if activeObject.isAttr(u"listPoints"):
                    objectInFocus = objInFocus[0]
                    shape = objectInFocus.get(u"Shape")
                    idxPolygons = helper.point_inside_polygon(x, y, shape)
                    if len(idxPolygons) == 1:
                        idxPolygon = idxPolygons[0]
                        if idxPolygon > 0:
                            # not sent via ustr-Command, since this information is only cached at the mainController
                            # for the final command. No data is changed here.
                            _id = unicode(activeObject.ID)
                            self.mainController.set(u"ConnectModInfo", ( _id + u"_id" + _id ,idxPolygon - 1 ))
                            return 
                            
            # Connecting Elements
            #####################
            
            # connecting has been started yet
            if self.mainController.bConnectorPloting:
                keys = self.activeGraphics.getChildKeys()
                objInFocus = None
                for key in keys:
                    element = self.activeGraphics.getb(key)
                    types = inspect.getmro(type(element))
                    if PyLinXCoreDataObjects.PX_PlottableElement in types and element.get(u"bUnlock"): 
                        objInFocus, idxPin = element.isPinInFocus(x,y)
                        if objInFocus != None:
                            if len(idxPin) == 1:
                                idxPin = idxPin[0]
                            break
                
                # case connecting of elements is not finished yet. No second Element has been clicked
                if objInFocus == None:                    
                    strVal = repr((x,y)).replace(u" ", u"")
                    strCommand_xy = u"@latent set ./PX_PlottableProxyElement.xy " + strVal
                    self.mainController.execCommand(strCommand_xy)                    
                
                # Case connecting of elements is finished. Second Element is clicked
                else:
                    # idxPin determined as the index of Pins in focus
                    setIdxConnectedInPins = objInFocus.get(u"setIdxConnectedInPins")
                    if not (idxPin in setIdxConnectedInPins):
                        ConnectorPloting = self.mainController.get(u"ConnectorPloting")
                        connectorName = ConnectorPloting.get(u"Name")
                        ustrCommand = u"@latent set ./" + connectorName + ".connectInfo (\"" + objInFocus.get(u"Name") + u"\"," + unicode(idxPin) + u")"
                        self.mainController.execCommand(ustrCommand)                        
                                               
            # connecting has not been started yet
            else:
                # Starting connecting Elements
                keys = self.activeGraphics.getChildKeys()
                for key in keys:
                    element = self.activeGraphics.getb(key)
                    types = inspect.getmro(type(element))
                    if (PyLinXCoreDataObjects.PX_PlottableElement in types) \
                                and element.get(u"bUnlock"):
                        objInFocus, idxPin = element.isPinInFocus(x,y)
                        if len(idxPin) > 0:
                            idxPin = idxPin[0]                         
                        if objInFocus != None and (idxPin > -1):
                            strCommand = u"@latent new connector " + unicode( element.ID ) + u" idxOutPinConnectorPloting=" + unicode(idxPin)
                            self.mainController.execCommand(strCommand)



        def mousePressEvent_tool_newVarElement():
            self.mainController.idxToolSelected = helper.ToolSelected.none
            self.mainWindow.ui.actionNewElement.setChecked(False)
            n = PyLinXCoreDataObjects.PX_IdObject._PX_IdObject__ID + 1
            ustrCommand = u"new varElement " + u"Variable_id" + unicode(n) + u" " + unicode(X) + u" " + unicode(Y) + u" " + unicode(15)
            self.mainController.execCommand(ustrCommand)             
            
        def mousePressEvent_tool_newBasicOperator(ustrOperator):
            self.mainController.idxToolSelected = helper.ToolSelected.none
            if ustrOperator == u"+":
                self.mainWindow.ui.actionNewPlus.setChecked(False)
            elif ustrOperator == u"-":
                self.mainWindow.ui.actionNewMinus.setChecked(False)                
            elif ustrOperator == u"*":
                self.mainWindow.ui.actionNewMultiplication.setChecked(False)                
            elif ustrOperator == u"/":
                self.mainWindow.ui.actionNewDivision.setChecked(False)                        
            ustrCommand = u"new basicOperator " +  ustrOperator + " " + unicode(X) + " " + unicode(Y) 
            self.mainController.execCommand(ustrCommand)

        def mousePressEvent_tool_newVarDispObj():
            self.mainController.idxToolSelected = helper.ToolSelected.none
            self.mainWindow.ui.actionOsci.setChecked(False)
            ustrCommand = u"new varDispElement "+ unicode(X) + " " + unicode(Y)
            self.mainController.execCommand(ustrCommand)
            
                   
        #################
        # Main Method
        #################
        
        x = coord.x()
        y = coord.y()
        X = 10 * round( 0.1 * float(x))
        Y = 10 * round( 0.1 * float(y))
        toolSelected = self.mainController.idxToolSelected
        bSimulationMode = self.mainController.bSimulationMode
        
        # not passed as command since just clicking should not change the data
        self.mainController.set(u"px_mousePressedAt_X",X)
        self.mainController.set(u"px_mousePressedAt_Y",Y)
        self.mainController.set(u"px_mousePressedAt_x",x)
        self.mainController.set(u"px_mousePressedAt_y",y)

        if toolSelected == helper.ToolSelected.none:
            mousePressEvent_tool_none()

        
        if not bSimulationMode:
    
            if toolSelected == helper.ToolSelected.newVarElement:
                mousePressEvent_tool_newVarElement()
    
            elif toolSelected == helper.ToolSelected.newPlus:
                mousePressEvent_tool_newBasicOperator("+")
                
            elif toolSelected == helper.ToolSelected.newMinus:
                mousePressEvent_tool_newBasicOperator("-")

            elif toolSelected == helper.ToolSelected.newMultiplication:
                mousePressEvent_tool_newBasicOperator("*")

            elif toolSelected == helper.ToolSelected.newDivision:
                mousePressEvent_tool_newBasicOperator("/")
                   
    def mouseMoveEvent(self,coord):

        x = coord.x()
        y = coord.y()
        X = 10 * round( 0.1 * float(x))
        Y = 10 * round( 0.1 * float(y))
        toolSelected = self.mainController.idxToolSelected

        if toolSelected == helper.ToolSelected.none:

            # Moving objects
            objectsInFocus = list(self.mainController.selection)             
            if objectsInFocus != []:

                px_mousePressedAt_X = self.mainController.get(u"px_mousePressedAt_X")
                px_mousePressedAt_Y = self.mainController.get(u"px_mousePressedAt_Y")
                if px_mousePressedAt_X != sys.maxint:
                    xOffset = X - px_mousePressedAt_X 
                    yOffset = Y - px_mousePressedAt_Y
                    
                    if ((xOffset != 0) or (yOffset != 0)) and \
                            (PyLinXCoreDataObjects.PX_PlottableElement in self.mainController.Selection_types and\
                            self.mainController.Selection_bUnlock):
                        ustrCommand = u"@selection set xy (" + unicode(xOffset) + "," + unicode(yOffset) + u") -p"
                        self.mainController.execCommand(ustrCommand)

                    
                    # move line of connector.                 
                    ConnectorToModify = self.mainController.get(u"ConnectorToModify") 
                    if ConnectorToModify  != None:
                        idxPointModified = self.mainController.get(u"idxPointModified")
                        listPoints = list(ConnectorToModify.get(u"listPoints"))
                        listPointsOld = copy.copy(listPoints)
                        value = listPoints[idxPointModified]
                        if idxPointModified % 2 == 0:
                            value = value + xOffset 
                        else:
                            value = value + yOffset
                        listPoints[idxPointModified] = 10 * round( 0.1 * float(value))
                        if sum([abs(x-y) for x,y in zip(listPoints, listPointsOld)]) != 0:
                            ustrCommand = "set ./" + ConnectorToModify.get(u"Name") + ".listPoints " + repr(listPoints).replace(" ", "")
                            self.mainController.execCommand(ustrCommand)
                    
                    self.mainController.set(u"px_mousePressedAt_XY", (X,Y))

            # Ploting the selection frame
            if self.latentGraphics.isInBody(u"HighlightObject"):
                highlightObject = self.latentGraphics.getb(u"HighlightObject")
                highlightObject.X1Y1 = (coord.x(),coord.y())
                    
            # change coordinates of the proxyElement, that is a placeholder for the finally connected element
            if self.mainController.bConnectorPloting:
                proxyElem = self.mainController.latentGraphics.getb(u"PX_PlottableProxyElement")
                proxyElem.xy_temp = (X,Y)
     
    def mouseReleaseEvent(self,coord):
        
        def __removeLatentObjects():
            keys = self.latentGraphics.getChildKeys()
            for key in keys:
                if self.latentGraphics.getb(key).isAttrTrue(u"bLatent"):
                    self.latentGraphics.delete(key)
            self.repaint() # latent objects are not part of the data

        toolSelected = self.mainController.idxToolSelected

        # selecting Elements
        if toolSelected == helper.ToolSelected.none:
            #__mouseReleaseEvent_ToolSelNone()
            __removeLatentObjects()
             
        self.mainController.set(u"px_mousePressedAt_X", sys.maxint)
        self.mainController.set(u"px_mousePressedAt_Y", sys.maxint)  
           
    def mouseDoubleClickEvent(self, coord):
        
        def bDialogue(X,Y,strShape, element):
            bDialog = False
            shape = element.get(strShape)
           
            if shape != None:
                idxPolygon = helper.point_inside_polygon(X , Y,shape)
                bDialog = not (len(idxPolygon) == 0)
            return bDialog
        
        if not self.mainController.bSimulationMode:
            if self.mainController.get(u"bConnectorPloting"):
                self.mainController.execCommand("set /.bConnectorPloting False")
                
        else:
            X = coord.x()
            Y = coord.y()
            keys = self.activeGraphics.getChildKeys()
            bFocusStimulate = False
            bFocusMeasure = False
            bFocus = False
            for key in keys:
                element = self.activeGraphics.getb(key)
                types = inspect.getmro(type(element))
                if PyLinXCoreDataObjects.PX_PlottableVarElement in types:
                    bFocusStimulate = bDialogue(X,Y,u"Shape_stim", element)
                    bFocusMeasure = bDialogue(X,Y,u"Shape_meas", element)
                    if bFocusStimulate or bFocusMeasure:
                        break                    
                if PyLinXCoreDataObjects.PX_PlottableVarDispElement in types:
                    bFocus  =  bDialogue(X,Y, u"Shape", element)
                    if bFocus:
                        break
            
            if bFocusStimulate:
                OK, values = PX_Dialogue_SimpleStimulate.PX_Dialogue_SimpleStimulate.getParams(self, element, self.mainController,self)
                if OK == True:
                    self.actionStimulate.setChecked(True)
                    command = self.getStimulationActivateCommand(element, values)
                    self.mainController.execCommand(command)                
                return
            
            if bFocusMeasure:
                OK, value = PX_Dialogue_SelectDataViewer.PX_Dialogue_SelectDataViewer.getParams(self,element,self.mainController,self)
                if OK == True:
                    self.actionMeasure.setChecked(True)
                    command = self.getMeasureCommand(element, value)
                    self.mainController.execCommand(command)    
                return 
            
            if bFocus:
                if PyLinXCoreDataObjects.PX_PlottableVarDispElement in types:
                    # TODO COMMAND ???
                    element.set(u"bVarDispVisible", True)                 