'''
Created on 18.12.2014

@author: Waetzold Plaum
'''
# general imports
import inspect
from PyQt4 import QtCore
#import mdfreader 
#import numpy as np
import copy 
 

from PyLinXData import BContainer, PyLinXCoreDataObjects

from PyLinXCode import Code
from PyLinXCodeRef import PX_CodeRefObject, PX_CodableBasicOperator, PX_CodableVarElement

# Allgemein

class PX_CodeAnalyser(BContainer.BContainer, QtCore.QObject):
    
    class CodingVariant:
        ReadSingleVars = 0
        ReadVarsFromDataDict = 1
        
    _dictSetCallbacks = copy.copy(BContainer.BContainer._dictSetCallbacks)  
    _dictGetCallbacks = copy.copy(BContainer.BContainer._dictGetCallbacks)  
 
    def __init__(self, parent, PyLinXMainWindow):
        
        super(PX_CodeAnalyser, self).__init__(u"PX_CodeGeerator")
        QtCore.QObject.__init__(self)    
        self.__runThread = None
        self.__runThreadMessageQueue = PyLinXMainWindow.runThreadMessageQueue
        
        # Object Data
        #############
        
        self.__PyLinXMainWindow  = PyLinXMainWindow
        self.__projectController = parent
        self.__rootGraphics      = self.__projectController.getb(u"rootGraphics")
        self.__objectHandler     = self.__projectController.getb(u"ObjectHandler")
        
        # Initialize Lists of DataTypes
        
        self.__listConnectors = []
        self.__listVarElements = []
        self.__listBasicOperators = []
        
        self.__listNotConnectedOutVarElements = []
        self.__listNotConnectedInVarElements = []
        
        # Syntax Tree
        
        self.__syntaxTree = None

# Speziell
        
        # Code
        
        self.__Code = Code()
        self.__CodeStr = u""

# Allgemein
        
        # Setting Coding-Variant           
        self.set(u"CodingVariant", PX_CodeAnalyser.CodingVariant.ReadVarsFromDataDict)
        # self.set(u"CodingVariant", PX_CodeAnalyser.CodingVariant.ReadSingleVars)

        # Processing
        ############
        
        # generate Code 
        
        self.__genCode()
        
        # create global data-Dictionary

        RunConfigDictionary = BContainer.BDict({})
        RunConfigDictionary.set(u"Name", u"RunConfigDictionary")
        RunConfigDictionary.set(u"DisplayName", u"RunConfigDictionary")
        RunConfigDictionary[u"t"] = 0.0
        self.__projectController.paste(RunConfigDictionary, bForceOverwrite = True)
        self.__RunConfigDictionary = RunConfigDictionary 

        self.__DataDictionary = self.__projectController.getb(u"DataDictionary") 
        for element in self.__listVarElements:
            self.__DataDictionary[element.get(u"DisplayName")] = 0.0                 
        self.__projectController.updateDataDictionary()
            
    def __genCode(self):
        
        #############
        ## Frontend
        #############
        
        ## Lexicalic Analysis
        #####################
        
        pass
    
        ## Syntactic Analysis
        #####################
        # Here the syntax tree is generated
        
        self.__getSyntaxTree()
        
        
        ## Semantic Analysis
        ####################
        
        pass
    
        ###############
        ## Backend
        ###############
        
        ## Generate Code
        ################
        
        self.__writeCode()
    
        ## Optimize code
        ################
        
        pass
    
    def __getSyntaxTree(self):
        
        def __createSingleBranch(parent, knot):
            
            CodingVariant = self.get(u"CodingVariant")
            types = inspect.getmro(type(knot))
            if PyLinXCoreDataObjects.PX_PlottableVarElement in types:            
                knotRefObj = PX_CodableVarElement(parent,knot, CodingVariant)
            elif PyLinXCoreDataObjects.PX_PlottableBasicOperator in types:
                orderConnection = {}
                for connector in self.__listConnectors:
                    if connector.elem1 == knot:
                        idxInPin    = connector.idxInPin
                        ID_inObject = connector.elem0.ID
                        orderConnection[ID_inObject] = idxInPin
                knotRefObj = PX_CodableBasicOperator(parent,knot, CodingVariant, orderConnection)                  
            for connector in self.__listConnectors:
                if connector.elem1 == knot:
                    __createSingleBranch(knotRefObj,connector.elem0)
            return knotRefObj
                    
        
        # Creating lists of different data types
        
        childKeys = self.__rootGraphics.getChildKeys()
        
        for key in childKeys:
            element = self.__rootGraphics.getb(key)
            types = inspect.getmro(type(element))
            if PyLinXCoreDataObjects.PX_PlottableConnector in types:
                self.__listConnectors.append(element)
            if PyLinXCoreDataObjects.PX_PlottableVarElement in types:
                self.__listVarElements.append(element)
            if PyLinXCoreDataObjects.PX_PlottableBasicOperator in types:
                self.__listBasicOperators.append(element)
        
        
        # Creating lists of not connected elements
        
        setConnectedOutVarEleemnts = set([])
        for connector in self.__listConnectors:
            setConnectedOutVarEleemnts.add(connector.elem0)            
        setNotConnectedOutVarElements = set(self.__listVarElements).difference(setConnectedOutVarEleemnts)
        self.__listNotConnectedOutVarElements = list(setNotConnectedOutVarElements)


        # Currently not used
        ####################
#        setConnectedInVarEleemnts = set([])
#        for connector in self.__listConnectors:
#            setConnectedInVarEleemnts.add(connector.elem1)            
#        setNotConnectedInVarElements = set(self.__listVarElements).difference(setConnectedInVarEleemnts)
#        self.__listNotConnectedInVarElements = list(setNotConnectedInVarElements)        

        # Creating the Syntax Tree
        
        rootRef = PX_CodeRefObject(self, self.__rootGraphics)
        for notConnectedOutElement in self.__listNotConnectedOutVarElements:
            __createSingleBranch(rootRef, notConnectedOutElement) 
        self.__syntaxTree = rootRef 

# Speziell

    def __writeCode(self):
        
        self.__Code.append(u"def main(DataDictionary):\n")
        CodingVariant = self.get(u"CodingVariant")
        
        if CodingVariant == PX_CodeAnalyser.CodingVariant.ReadSingleVars:
            self.__Code.append(u"    Variables = DataDictionary.keys()")
            self.__Code.append(u"    execStr = u\"\"")
            self.__Code.append(u"    for variable in Variables:")
            self.__Code.append(u"        if variable[0] != u\"*\":")
            self.__Code.append(u"            execStr += (variable + u\" = DataDictionary[\\\"\" + variable +\"\\\"]\\n\")")   
            self.__Code.append(u"    exec(execStr)\n")
        
        self.__Code.changeIndent(1)
        
        keys = self.__syntaxTree.getChildKeys()
        for key in keys:
            child = self.__syntaxTree.getb(key)
            child.getCode(self.__Code)
            
        if CodingVariant == PX_CodeAnalyser.CodingVariant.ReadSingleVars:          
            self.__Code.append(u"\n    execStr = u\"\"")
            self.__Code.append(u"    for variable in Variables:")
            self.__Code.append(u"        if variable[0] != \"*\":")
            self.__Code.append(u"            execStr += (u\"DataDictionary[\\\"\" + variable + \"\\\"] = \" + variable + u\"\\n\" )")
            self.__Code.append(u"    exec(execStr)\n")
            
        self.__Code.append(u"\nmain(DataDictionary)")

        self.__CodeStr = self.__Code.getCodeStr()
        print "BEGIN---------------"
        print self.__CodeStr
        print "END-----------------"

# Allgemein

    #class SimulationThread(BContainer.BContainer,  QtCore.QThread ):
    class SimulationThread( QtCore.QThread ):
        
        def __init__(self, CodeGenerator,  mainDrawWidget, runConfigDictionary, dataDictionary):
            QtCore.QThread.__init__(self)
            self.__CodeGenerator            = CodeGenerator
            self.__runThreadMessageQueue    = CodeGenerator._PX_CodeAnalyser__runThreadMessageQueue
            self.__drawWidget               = mainDrawWidget
            self.__signalUpdated            = QtCore.pyqtSignal(str)
            self.__RunConfigDictionary      = runConfigDictionary
            self.__DataDictionary           = dataDictionary
            self.__bRecord = False
            
        def __del__(self):
            self.exit(0)
            
        def run(self):

            #i = 0
            while 1:
                #i += 1
                #print i
                self.__CodeGenerator.run_()
                # Synchronize the data in DataDictionary with the data stored in the DataViewer-GUI
                self.emit(QtCore.SIGNAL(u"simState__cycleDone"))
                # Trigger Repaint
                self.emit(QtCore.SIGNAL(u"dataChanged__coreDataObjects"))
                
                if not self.__runThreadMessageQueue.empty():
                    try:
                        message = self.__runThreadMessageQueue.get()
                    except:
                        message = None
                else:
                    message = None
                # Maybe some day we have to implement a more sophisticated protocoll
                if message != None:
                    if self.__bRecord:
                        self.__runExitInTread()
                    self.__runThreadMessageQueue.task_done()
                    self.emit(QtCore.SIGNAL(u"simState__exit"))
                    return                      
                
        
    def startRun(self, drawWQidget, stopEvent, repaintEvent):
        
        # connecting the signal "simState__init" to the main controller
        ###############################################################
        
        #TODO has to be moved to project controller
        self.__PyLinXMainWindow.ui.drawWidget.connect(self, QtCore.SIGNAL(u"simState__init"),self.__projectController.runInit)
              
        # initializing the Run
        ######################
        
        self.__runInit()
        self.emit(QtCore.SIGNAL(u"simState__init"))        
        
        # creatubg tge run thread
        #########################
        
        self.__runThread = PX_CodeAnalyser.SimulationThread(self, self.__PyLinXMainWindow.ui.drawWidget, self.__RunConfigDictionary,\
                                                                            self.__DataDictionary)

# speziell
        
        # Connecting signals to the run thread
        ######################################
        
        # has to be moved to project controller
        self.__PyLinXMainWindow.ui.drawWidget.connect(self.__runThread, QtCore.SIGNAL(u"dataChanged__coreDataObjects"), self.__PyLinXMainWindow.ui.drawWidget.repaint,\
                                                                            QtCore.Qt.BlockingQueuedConnection)
        self.__PyLinXMainWindow.ui.drawWidget.connect(self.__runThread, QtCore.SIGNAL(u"simState__cycleDone"),\
                                                   self.__projectController.sync,QtCore.Qt.BlockingQueuedConnection)
        self.__PyLinXMainWindow.ui.drawWidget.connect(self.__runThread, QtCore.SIGNAL(u"simState__exit"),self.__projectController.stop_run)
        

# allgemein

        # Starting the run thread
        #########################
        
        self.__runThread.start()       

    def __runInit(self):
        
        print "RUN INIT"
        
        self.delta_t = 0.02
        self.t = - self.delta_t
        self.__RunConfigDictionary[u"t"] = self.t
        self.__RunConfigDictionary[u"delta_t"] = self.delta_t
        # running the exec command on bytecode is more efficient then running on code string
        self.__ByteCode = compile(self.__CodeStr, "<string>", "exec")

    def run(self): 
        import cProfile 
        cProfile.runctx("self.run_()", globals(), locals(), "profile.stat")


    def run_(self):
        self.t+= self.delta_t
        self.__RunConfigDictionary[u"t"] = self.t
        self.__projectController.updateDataDictionary()
        
# speziell

#         DataDictionary = self.__DataDictionary
#         exec(self.__ByteCode, globals(), locals()) 
        try:
            DataDictionary = self.__DataDictionary
            exec(self.__ByteCode, globals(), locals())
        except Exception as exc:
            strExp = str(exc)
            print "Error executing code! -- " + strExp