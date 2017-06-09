'''
Created on 08.02.2016

@author: Waetzold Plaum
'''
import copy
import inspect
from PyQt4 import QtCore
#from PyQt4.QtCore import QString

import PyLinXCoreDataObjects 
import PyLinXData.PyLinXHelper as helper
import PyLinXData.PX_CSVObject as csvlib
import PyLinXCtl.PyLinXProjectController #as PyLinXProjectController  

# This is quite unusual, bus this class has to be built in this way, because
# we want to to prepare for a dual license distribution model. It might be clever
# to encapsulate the two library or one of the two so that both libraries can be 
# used via the same interface. 
#
# 0 corresponding to quasi GPL

licenseOption = 0

if licenseOption == 0:
    try:
        import mdfreader #as mdflib
    except:
        raise Exception(u"Error PX_Signals: Library mdfreader is missing! Please catch up for...")


class PX_SignalsFolder(PyLinXCoreDataObjects.PX_IdObject):
    
    _dictSetCallbacks = copy.copy(PyLinXCoreDataObjects.PX_IdObject._dictSetCallbacks)
    _dictGetCallbacks = copy.copy(PyLinXCoreDataObjects.PX_IdObject._dictGetCallbacks)
    
    def __init__(self,parent, projectController = None):
        
        super(PX_SignalsFolder, self).__init__(parent, u"signalFiles")
        self.__projectController = projectController

        
    ##############
    # GET-Methods
    ##############

    # Object specific GETTERs
    #########################
    
    def get_signal(self, attr):
        listAttr = attr.split(u"|")
        if len(listAttr) != 2:
            raise Exception(u"PX_Signals.PX_SignalsFolder: Invalid Attribute")
            return
        signalFileName = listAttr[1] 
        signalName = listAttr[0]
        signalFile = self.getb(signalFileName)
        return signalFile.get(signalName)

    # static GETTERs
    ################   
    
    def get__bSignalLoaded(self):
        bSignalLoaded = False
        
        for key in self.getChildKeys():
            obj = self.getb(key)
            types = inspect.getmro(type(obj))
            if PX_Signals in types:
                bSignalLoaded = True
        return bSignalLoaded
    _dictGetCallbacks.addCallback(u"bSignalLoaded", get__bSignalLoaded)
    bSignalLoaded = property(get__bSignalLoaded)
                
    def get__signals(self):
        listWithFullNames = []
        for key in  self.getChildKeys():
            signal = self.getb(key)
            signalsName = signal.get(u"Name")
            listSignals = signal.get(u"signals")
            listWithFullNames.extend([(signalName, signalsName) for signalName in listSignals])
        return listWithFullNames
    _dictGetCallbacks.addCallback(u"signals", get__signals)
    signals = property(get__signals)
    
    def get__variablesLoadedInFolder(self):
        listWithFullNames = []
        for key in  self.getChildKeys():
            signal = self.getb(key)
            signalsName = signal.get(u"Name")
            listSignals = signal.get(u"signals")
            masterSignals = signal.get(u"masterSignals")
            setSignalsFiltered = set(listSignals).difference(set(masterSignals ) ) 
            listWithFullNames.extend([(signalName, signalsName) for signalName in setSignalsFiltered])
        return listWithFullNames            
    _dictGetCallbacks.addCallback(u"variablesLoadedInFolder", get__variablesLoadedInFolder)
    variablesLoadedInFolder  = property(get__variablesLoadedInFolder)
        
    ###############
    # PASTE Method
    ###############
    
    def paste(self, obj, name = None, bForceOverwrite = False, pathkey = None):
        types = inspect.getmro(type(obj))
        if PX_Signals in types:
            name = obj.get(u"Name")
            #listVirtualAttributes = []
            for key in obj.get(u"signals"):
                virtualAttribute =  key + u"|" + name
                self._dictGetCallbacks.addCallback(virtualAttribute, lambda: self.get_signal(virtualAttribute))
        return super(PX_SignalsFolder, self).paste(obj, name, bForceOverwrite, pathkey)

class PX_Signals (PyLinXCoreDataObjects.PX_IdObject):
    
    _dictSetCallbacks = copy.copy(PyLinXCoreDataObjects.PX_IdObject._dictSetCallbacks)
    _dictGetCallbacks = copy.copy(PyLinXCoreDataObjects.PX_IdObject._dictGetCallbacks)            
    
    class fileType:
        mdf = "mdf"
        csv = "csv"
    
    def __init__(self, parent, path):
        
        dataObject = mdfreader.mdf(path)
        fileType = PX_Signals.fileType.mdf
        
#         try:
#             print "path", path
#             dataObject = mdfreader.mdf(path)
#             fileType = PX_Signals.fileType.mdf
#              
#         
#         except Exception as exc:
#             
#             try:
#                 dataObject = csvlib.CSVObject(path).data()
#                 fileType = PX_Signals.fileType.csv
#             
#             except Exception as exc2:
#             
#                 strExp = str(exc)
#                 strExp2 = str(exc2)
#                 strText = u"Unable to open file - " + strExp + " - " + strExp2  
#                 helper.error(strText)
#                 return

        name = u"Signal"
        super(PX_Signals, self).__init__(parent, name, bIdSuffix = True, headObject = dataObject)
        self.set("fileType", fileType)
        
        self._BContainer__Attributes[u"pathMdfFile"] = path
        for key in self._BContainer__Head:
            # Interesting Python-Syntax: Wrong:             
            # lambdaExpression = lambda key: self.get_signal(key)            
            lambdaExpression = lambda value = key: self.get_signal(value)  
            self._dictGetCallbacks.addCallback(key, lambdaExpression)
        self.__projectController = parent.getRoot(PyLinXCtl.PyLinXProjectController.PyLinXProjectController)      
        
        self.__projectController.mainWindow.emit(QtCore.SIGNAL(u"dataChanged__signals"))

    ################
    # GETTER-Methods
    ################
    
    # object specific
    #################

    def get_signal(self, signalName):  
        fileType = self.get(u"fileType")
        if fileType  == PX_Signals.fileType.mdf:
            return self.__get_signal_mdf(signalName)
        elif fileType  == PX_Signals.fileType.csv:
            return self.__get_signal_csv(signalName)
    
    def __get_signal_mdf(self, signalName):
        
        signalDict = None
        if signalName in self._BContainer__Head:
            channelData = self._BContainer__Head.getChannelData(signalName)
            if channelData.dtype.kind not in ('S', 'U'):
                signalDict = {}
                if len(list(self._BContainer__Head.masterChannelList.keys())) == 1:  # Case of resampled signals
                    timeSignalName = list(self._BContainer__Head.masterChannelList.keys())[0]
                else:
                    timeSignalName = self._BContainer__Head.getChannelMaster(signalName)
                if not timeSignalName:
                    timeSignalName = u"master"
                if timeSignalName in self._BContainer__Head:
                    signalDict[u"time"] = self._BContainer__Head.getChannelData(timeSignalName)
                    signalDict[u"xlabel"] = timeSignalName  + u" " + self._BContainer__Head.getChannelUnit(timeSignalName)
                signalDict[u"values"] = channelData
                signalDict[u"title"] = self._BContainer__Head.getChannelDesc(signalName)
                if self._BContainer__Head.getChannelUnit(signalName) == {}:
                    signalDict[u"ylabel"] = signalName
                else: 
                    signalDict[u"ylabel"] = signalName + u" [" + self._BContainer__Head.getChannelUnit(signalName) + u"]"
        #print "signalDict: ", signalDict
        return signalDict
    
    def __get_signal_csv(self, signalName):
        
        return self._BContainer__Head[signalName]
        
    # static
    ########
    
    # signals
    def get__signals(self):
        return self.geth().keys()        
    _dictGetCallbacks.addCallback(u"signals", get__signals)    
    
    # masterSignals
    def get__masterSignals(self):
        listMasterSignals = []
        for key in  self.geth().keys():
            signal = self.geth()[key]
            masterType = signal[u"masterType"]
            if masterType == 1: # Case MasterSigna,
                listMasterSignals.append(key)
        return listMasterSignals
    _dictGetCallbacks.addCallback(u"masterSignals", get__masterSignals)    
        
    # signalsFullData
    def get__signalsFullData(self):
        dictSignals = {}
        for key in self.geth().keys():
            dictSignals[key] = self.get_signal(key)
        return dictSignals
    _dictGetCallbacks.addCallback(u"signalsFullData", get__signalsFullData)      
