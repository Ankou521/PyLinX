'''
Created on 18.02.2016

@author: Waetzold Plaum
'''

import numpy
import math
import os
import mdfreader
import numpy as np
from datetime import datetime

import PyLinXGui.PX_Templates as PX_Templ
from PyQt4 import QtCore
import copy
import PyLinXCtl
import PyLinXCoreDataObjects
from PyLinXData import PX_CSVObject as PX_CSVObject 


# The object handler handles the problem that each variable, class pp. may occur several times in the code. But these instances correspond to single
# objects. The object handler handles the object. Each time a new instance of the variable is createt, it is registered by the object handler. The 
# object handler also manages the recording of signals. 

class PX_ObjectHandler(PyLinXCoreDataObjects.PX_Object): 
    
    _dictSetCallbacks = copy.copy(PyLinXCoreDataObjects.PX_Object._dictSetCallbacks)
    _dictGetCallbacks = copy.copy(PyLinXCoreDataObjects.PX_Object._dictGetCallbacks)
    
    # Enumeration for the file extension of the recorder
    
    class FileExt:
        
        number=0
        dateNtima=1
        
    # Enumeration for the states of the recorder
    
    class recorderState:
        
        off = 0
        logSelected = 1
        logAll = 2
    
    def __init__(self, parent):
        if not (type(parent) == PyLinXCtl.PyLinXProjectController.PyLinXProjectController):
            raise Exception("Error PX_ObjectHandler.__init__: Invalid Type of MainController")
        super(PX_ObjectHandler, self).__init__(parent, u"ObjectHandler")
        self.set(u"bObjectInSimulationMode", False)
        
        ################################
        # Configuration of the recorder
        ################################
        
        self.set(u"recorder_BaseFileName", u"measure")
        self.set(u"recorder_FileExtension", PX_ObjectHandler.FileExt.number)
        self.set(u"recorder_SaveFolder", os.path.join(os.getcwd(), u"Measurements"))
        self.set(u"recorder_RecordState", PX_ObjectHandler.recorderState.off)
        self.set(u"recorder_VariablesToRecord", [])
        self.set(u"recorder_fileFormat", PX_Recorder.FileFormat.mdf)
        self.__mdfObject = None
        self.__dataDict = None
        self.__runConfigDictionary = None
        self.__bRecord = False
        self.__projectController = self.getRoot(PyLinXCtl.PyLinXProjectController.PyLinXProjectController)
        self.recorder = PX_Recorder(self)
        self.__variables = PyLinXCoreDataObjects.PX_Object(self, "variables")


    #######################
    # SETTER and GETTER
    #######################

    # listObjects
    def get__listObjects(self):
        return self.__variables._BContainer__Body.keys()
    _dictGetCallbacks.addCallback(u"listObjects", get__listObjects)
    listObjects = property(get__listObjects)
    
    # mapping
    def get__mapping(self):
        mapping = {}
        for key in self.__variables.getChildKeys():
            element = self.__variables.getb(key)
            nameSignal= element.signalMapped # get(u"signalMapped")
            if nameSignal!= None:
                nameVariable = element.get(u"Name")
                mapping[nameVariable] = nameSignal
        return mapping

    def set__mapping(self, mapping, options = None):
        keys = self.__variables.getChildKeys()
        for variable in mapping:
            if variable in keys:
                varObject = self.getb(variable)
                varObject.signalMapped = mapping[variable]
        return
    _dictSetCallbacks.addCallback(u"mapping", set__mapping)
    _dictGetCallbacks.addCallback(u"mapping", get__mapping)
    mapping = property(get__mapping, set__mapping)
    
    # bRecord
    def get__bRecord(self):
        return (len( self.recorder_VariablesToRecordProcessed ) > 0)
    _dictGetCallbacks.addCallback(u"bRecord", get__bRecord)
    bRecord = property(get__bRecord)
    
    # recorder_VariablesToRecordProcessed
    def get__recorder_VariablesToRecordProcessed(self):
        recorederState = self._BContainer__Attributes[u"recorder_RecordState"]
        if  recorederState == PX_ObjectHandler.recorderState.logAll:
            return self.__variables._BContainer__Body.keys()
        elif recorederState == PX_ObjectHandler.recorderState.logSelected:
            return self._BContainer__Attributes[u"recorder_VariablesToRecord"]
        else:
            return []        
    _dictGetCallbacks.addCallback(u"recorder_VariablesToRecordProcessed", get__recorder_VariablesToRecordProcessed)
    recorder_VariablesToRecordProcessed = property(get__recorder_VariablesToRecordProcessed)


    ########
    # MISC
    ########
    
    def register(self, variable):
        
        varName = variable.get(u"DisplayName")

        #  Attributes with the prefix "var." correspond to variables of the models
        
        if (varName in self.__variables._BContainer__Body):
            self._BContainer__Attributes[u"Var." + varName] += 1
            objectVar = self.__variables._BContainer__Body[varName]
            objectVar.get(u"listRefInstances").append(variable)
        else:
            objectVar = PX_ObjectVariable(self.__variables, variable)
            self._BContainer__Attributes[u"Var." + varName] = 1
            self.__projectController.mainWindow.emit(QtCore.SIGNAL(u"dataChanged__objectHandler"))
        
        return objectVar
        
        
    def unregister(self, varName):
        print "HAS TO BE IMPLEMENTED! unregister()"
    
    def runInit(self):

        for variable in self.__variables.getChildKeys():
            obj = self.__variables.getb(variable)
            obj.runInit()
        self.recorder.init()


    def updateDataDictionary(self):
        
        for variable in self.__variables.getChildKeys():
            obj = self.__variables.getb(variable)
            obj.updateDataDictionary()

   

    
class PX_ObjectVariable(PyLinXCoreDataObjects.PX_Object):
    
    _dictSetCallbacks = copy.copy(PyLinXCoreDataObjects.PX_Object._dictSetCallbacks)
    _dictGetCallbacks = copy.copy(PyLinXCoreDataObjects.PX_Object._dictGetCallbacks)
    
    _stimMethods = [u"stim_const", u"stim_sine", u"stim_ramp", u"stim_pulse", u"stim_step", u"stim_random"]
    _stimVariablesByMethod = {}
    _stimVariablesByMethod[u"stim_const"]   = [u"stim_const_val"]
    _stimVariablesByMethod[u"stim_sine"]    = [u"stim_sine_frequency", \
                                               u"stim_sine_offset", \
                                               u"stim_sine_amplitude", \
                                               u"stim_sine_phase"]
    _stimVariablesByMethod[u"stim_ramp"]    = [u"stim_ramp_frequency", \
                                               u"stim_ramp_offset", \
                                               u"stim_ramp_amplitude", \
                                               u"stim_ramp_phase"]
    _stimVariablesByMethod[u"stim_pulse"]   = [u"stim_pulse_frequency", \
                                               u"stim_pulse_offset", \
                                               u"stim_pulse_amplitude", \
                                               u"stim_pulse_phase"]
    _stimVariablesByMethod[u"stim_step"]    = [u"stim_step_phase",\
                                               u"stim_step_amplitude",\
                                               u"stim_step_offset"]
    _stimVariablesByMethod[u"stim_random"]  = [u"stim_random_offset",\
                                               u"stim_random_amplitude"]
    
    def __init__(self, parent, variable):
        
        name = variable.get(u"DisplayName")
        super(PX_ObjectVariable, self).__init__(parent, name)
        self._BContainer__Attributes[u"listRefInstances"] = [variable]
        self.__refVariable = variable
        self.__projectController = self.getRoot(PyLinXCtl.PyLinXProjectController.PyLinXProjectController)
        self.__signalhandler = self.__projectController.getb(u"signalFiles")
        self.__DataDictionary = self.__projectController.getb(u"DataDictionary")
        
        self.set(u"StimulationFunction", None)
        self.listSelectedDispObj = []
        #self.stim_const_val = 0.
        self.__time = None
        self.__signal = None
        self.__iteratorSignal = None
        self.__RunConfigDictionary = None
        self.__stimulateBySignal = False
        self.__lenSignal = None 
        
        self.__stimFuntion = self.updateDataDictionary_const_val
        
        
        # Initializing the special parameters for the stimulation
        #########################################################
        
        self.__stim_const_val = 0.
        self.__stim_sine_frequency = 0.
        self.__stim_sine_offset = 0.
        self.__stim_sine_amplitude = 0.
        self.__stim_sine_phase = 0.
        self.__stim_ramp_frequency = 0.
        self.__stim_ramp_phase = 0.
        self.__stim_ramp_offset = 0.
        self.__stim_ramp_amplitude = 0.
        self.__stim_pulse_frequency = 0.
        self.__stim_pulse_phase = 0.
        self.__stim_pulse_amplitude = 0.
        self.__stim_pulse_offset = 0.
        self.__stim_step_phase = 0.
        self.__stim_step_offset = 0.
        self.__stim_step_amplitude = 0.
        self.__stim_random_offset = 0.
        self.__stim_random_amplitude = 0.

    ####################
    # GETTER and SETTER
    ####################    
 
    # bMeasure
    def get__bMeasure(self):
        listSelectedDispObj = self.listSelectedDispObj
        if len(listSelectedDispObj) > 0:
            return True
        return False
    _dictGetCallbacks.addCallback(u"bMeasure", get__bMeasure)


    bMeasure = property(get__bMeasure)
    
    # objPath
    def get__objPath(self):
        objPath = super(PX_ObjectVariable, self).get__path()
        return objPath
    _dictGetCallbacks.addCallback(u"objPath", get__objPath)    
    objPath = property(get__objPath)
    
    # bStimulate
    def get__bStimulate(self):
        return (self.get(u"StimulationFunction") != None)
    _dictGetCallbacks.addCallback(u"bStimulate", get__bStimulate)
    bStimulate = property(get__bStimulate)
    
    # signalMapped
    def get__signalMapped(self):
        StimulationFunction = self.get(u"StimulationFunction")
        if StimulationFunction != None:
            if u"Signal_" in StimulationFunction:
                return StimulationFunction
        return None
    _dictGetCallbacks.addCallback(u"signalMapped", get__signalMapped)

    def set__signalMapped(self, value, options = None):
        if value == 0:
            value = None
        self._BContainer__Attributes[u"StimulationFunction"] = value
        self.__projectController.mainWindow.emit(QtCore.SIGNAL(u"dataChanged__mapping"))
    _dictSetCallbacks.addCallback(u"signalMapped", set__signalMapped)
    signalMapped = property(get__signalMapped, set__signalMapped)
    
    #StimulationFunciton
    def get__StimulationFunction(self):
        return (self._BContainer__Attributes[u"StimulationFunction"])
    _dictGetCallbacks.addCallback(u"StimulationFunction", get__StimulationFunction)
    
    def set__StimulationFunction(self, val, options = None):
        self._BContainer__Attributes[u"StimulationFunction"] = val
        self.__projectController.mainWindow.emit(QtCore.SIGNAL(u"dataChanged__coreDataObjects"))
    _dictSetCallbacks.addCallback(u"StimulationFunction", set__StimulationFunction)
    StimulationFunction = property(get__StimulationFunction, set__StimulationFunction)
    
    
    # general helper methods
    
    def __get(self, listAttributes):
        retDict = {}
        for attr in listAttributes:
            retDict[attr] = self.get(attr)
        return retDict
    
    def __set(self, value, listAttr, stimFunction):
        if set(value.keys()) == set(listAttr):
            self.__setStimFunction(stimFunction)
            retObj = super(PX_ObjectVariable, self).set("", value)
            self.__projectController.mainWindow.emit(QtCore.SIGNAL(u"dataChanged__objectHandler"))
            return retObj
        else:
            raise Exception(u"Error PX_ObjectVariable.__set: Variables are not matching! " +\
                            unicode(set(value.keys())) + " != " + unicode(set(listAttr) ) )
    
    # stim_const
    def get__stim_const(self):
        return self.__get( PX_ObjectVariable._stimVariablesByMethod[u"stim_const"])
    _dictGetCallbacks.addCallback(u"stim_const", get__stim_const)

    def set__stim_const(self, value, options = None):
        return self.__set(value, PX_ObjectVariable._stimVariablesByMethod[u"stim_const"] + [u"StimulationFunction"], u"stim_const")
    _dictSetCallbacks.addCallback(u"stim_const", set__stim_const)
    stim_const = property(get__stim_const, set__stim_const)
    
    # stim_sine
    def get__stim_sine(self):
        return self.__get( PX_ObjectVariable._stimVariablesByMethod[u"stim_sine"] )
    _dictGetCallbacks.addCallback(u"stim_sine", get__stim_sine)

    def set__stim_sine(self, value, options = None):
        return self.__set(value, PX_ObjectVariable._stimVariablesByMethod[u"stim_sine"] + [u"StimulationFunction"], u"stim_sine")
    _dictSetCallbacks.addCallback(u"stim_sine", set__stim_sine)
    stim_sine = property(get__stim_sine, set__stim_sine)

    # stim_ramp   
    def get__stim_ramp(self):
        return self.__get( PX_ObjectVariable._stimVariablesByMethod[u"stim_ramp"] )
    _dictGetCallbacks.addCallback(u"stim_ramp", get__stim_ramp)
    
    def set__stim_ramp(self, value, options = None):
        return self.__set(value, PX_ObjectVariable._stimVariablesByMethod[u"stim_ramp"] + [u"StimulationFunction"], u"stim_ramp")
    _dictSetCallbacks.addCallback(u"stim_ramp", set__stim_ramp)
    stim_ramp = property(get__stim_ramp, set__stim_ramp)
    
    # stim_pulse        
    def get__stim_pulse(self): 
        return self.__get( PX_ObjectVariable._stimVariablesByMethod[u"stim_pulse"] )        
    _dictGetCallbacks.addCallback(u"stim_pulse", get__stim_pulse)        
    
    def set__stim_pulse(self, value, options = None):
        return self.__set(value, PX_ObjectVariable._stimVariablesByMethod[u"stim_pulse"] + [u"StimulationFunction"], u"stim_pulse")     
    _dictSetCallbacks.addCallback(u"stim_pulse", set__stim_pulse)
    stim_pulse = property(get__stim_pulse, set__stim_pulse)    
        
    # stim_step
    def get__stim_step(self):
        return self.__get( PX_ObjectVariable._stimVariablesByMethod[u"stim_step"] )   
    _dictGetCallbacks.addCallback(u"stim_step", get__stim_step)        

    def set__stim_step(self, value, options = None):
        return self.__set(value, PX_ObjectVariable._stimVariablesByMethod[u"stim_step"] + [u"StimulationFunction"], u"stim_step")     
    _dictSetCallbacks.addCallback(u"stim_step", set__stim_step)
    stim_step = property(get__stim_step, set__stim_step)
        
    # stim_random
    def get__stim_random(self):
        return self.__get( PX_ObjectVariable._stimVariablesByMethod[u"stim_random"] )         
    _dictGetCallbacks.addCallback(u"stim_random", get__stim_random)

    def set__stim_random(self, value, options = None):
        return self.__set(value, PX_ObjectVariable._stimVariablesByMethod[u"stim_random"] + [u"StimulationFunction"], u"stim_random")    
    _dictSetCallbacks.addCallback(u"stim_random", set__stim_random)
    stim_random = property(get__stim_random, set__stim_random)
    
    # listSelectedDispObj
    def get__listSelectedDispObj(self):
        return self._BContainer__Attributes[u"listSelectedDispObj"]
        
    def set__listSelectedDispObj(self, value, options = None):
        if not u"listSelectedDispObj" in self._BContainer__Attributes:
            self._BContainer__Attributes[u"listSelectedDispObj"] = []
        name = self.get(u"Name")
        rootGraphics = self.mainController.getb(u"rootGraphics")
        rootGraphics.recur(PyLinXCoreDataObjects.PX_PlottableVarDispElement, \
                           u"labelAdd", (name, value))
        # delete the elements, that are in the old list but not in the new
        listSelectedDispObj = self.listSelectedDispObj
        list_del = list( set(listSelectedDispObj).difference(set(value)))            
        rootGraphics.recur(PyLinXCoreDataObjects.PX_PlottableVarDispElement, \
                           u"labelRemove", (name, list_del))
        self._BContainer__Attributes[u"listSelectedDispObj"] = value
        self.__projectController.mainWindow.emit(QtCore.SIGNAL(u"dataChanged__coreDataObjects"))
        
        
    _dictSetCallbacks.addCallback(u"listSelectedDispObj", set__listSelectedDispObj)
    listSelectedDispObj = property(get__listSelectedDispObj, set__listSelectedDispObj)
    
    def __setStimFunction(self, attr):
        for key, value in PX_Templ.PX_DiagData.StimAttribute.iteritems():
            if value == attr:
                break
        self.set(u"StimulationFunction", key)
        
    ###################################
    # METHODS USED DURING SIMULATION       
    ###################################
        
    def runInit(self):
        
        self.__RunConfigDictionary = self.__projectController.getb(u"RunConfigDictionary")
        self.__StimulationFunction = self.get(u"StimulationFunction")

        StimulationFunction = self.get(u"StimulationFunction")
        if StimulationFunction == u"Constant":
            #self.__stim_const_val        = self.stim_const_val #self.get(u"stim_const_val")
            self.__stim_const_val        = self.get(u"stim_const_val")
            self.__stimFuntion           = self.updateDataDictionary_const_val
        elif StimulationFunction == u"Sine":
            self.__stim_sine_frequency   = self.get(u"stim_sine_frequency")  
            self.__stim_sine_offset      = self.get(u"stim_sine_offset")     
            self.__stim_sine_amplitude   = self.get(u"stim_sine_amplitude")            
            self.__stimFuntion           = self.updateDataDictionary_stim_sine
        elif StimulationFunction == u"Ramp":
            self.__stim_ramp_frequency   = self.get(u"stim_ramp_frequency")
            self.__stim_ramp_phase       = self.get(u"stim_ramp_phase")
            self.__stim_ramp_offset      = self.get(u"stim_ramp_offset")
            self.__stim_ramp_amplitude   = self.get(u"stim_ramp_amplitude")                
            self.__stimFuntion           = self.updateDataDictionary_stim_ramp
        elif StimulationFunction == u"Pulse":
            self.__stim_pulse_frequency  = self.get(u"stim_pulse_frequency")
            self.__stim_pulse_phase      = self.get(u"stim_pulse_phase")
            self.__stim_pulse_amplitude  = self.get(u"stim_pulse_amplitude")
            self.__stim_pulse_offset     = self.get(u"stim_pulse_offset")            
            self.__stimFuntion = self.updateDataDictionary_stim_pulse
        elif StimulationFunction ==  u"Step":
            self.__stim_step_phase       = self.get(u"stim_step_phase")
            self.__stim_step_offset      = self.get(u"stim_step_offset")
            self.__stim_step_amplitude   = self.get(u"stim_step_amplitude")            
            self.__stimFuntion = self.updateDataDictionary_stim_step
        elif StimulationFunction ==  u"Random":
            self.__stim_random_offset    = self.get(u"stim_random_offset")
            self.__stim_random_amplitude = self.get(u"stim_random_amplitude")                   
            self.__stimFuntion = self.updateDataDictionary_stim_random

        if  self.signalMapped  == None:
            self.__time = None
            self.__signal = None
            self.__iteratorSignal = None
            self.__stimulateBySignal = False
            self.__lenSignal = None
            return 
     
        # Stimulation by Signal
        self.__stimulateBySignal = True
        self.__stimFuntion = self.updateDataDictionary_stim_signal
        signalObject = self.__signalhandler.get(self.signalMapped) 
        signal = signalObject[u"values"]
        time = signalObject[u"time"]
        self.__time = time
        self.__signal = signal
        self.__iteratorSignal = 0
        self.__lenSignal_minus_1 = len(signal) - 1

    
    def updateDataDictionary(self):
        if self.bStimulate:
            self.__stimFuntion()

    def updateDataDictionary_const_val(self):
        self.__DataDictionary[ self.get(u"DisplayName") ] = self.__stim_const_val

    def updateDataDictionary_stim_sine(self):
        t = self.__RunConfigDictionary[u"t"]
        value = self.__stim_sine_offset + self.__stim_sine_amplitude * math.sin(2 * math.pi * self.__stim_sine_frequency * t )
        self.__DataDictionary[ self.get(u"DisplayName") ] = value
       
    def updateDataDictionary_stim_ramp(self):
        t = self.__RunConfigDictionary[u"t"]
        ratio = (t +  self.__stim_ramp_phase) / self.__stim_ramp_frequency
        value = self.__stim_ramp_offset + self.__stim_ramp_amplitude * (ratio - math.ceil(ratio) )
        self.__DataDictionary[ self.get(u"DisplayName") ] = value
    
    def updateDataDictionary_stim_pulse(self):
        t = self.__RunConfigDictionary[u"t"]
        ratio = (t +  self.__stim_pulse_phase) / self.__stim_pulse_frequency
        if ratio < 0.5:
            value = self.__stim_pulse_offset
        else:
            value = self.__stim_pulse_offset + self.__stim_pulse_amplitude
        self.__DataDictionary[ self.get(u"DisplayName") ] = value            
    
    def updateDataDictionary_stim_step(self):
        t = self.__RunConfigDictionary[u"t"]
        if self.__stim_step_phase > t:
            value = self.__stim_step_offset
        else:
            value = self.__stim_step_offset + self.__stim_step_amplitude
        self.__DataDictionary[ self.get(u"DisplayName") ] = value     
    
    def updateDataDictionary_stim_random(self):
        value = self.__stim_random_offset + self.__stim_random_amplitude * numpy.random.rand() 
        self.__DataDictionary[ self.get(u"DisplayName") ] = value  
    
    def updateDataDictionary_stim_signal(self):

        t = self.__RunConfigDictionary[u"t"]
        
        # find highest iterator for which tSignal < signal and

        while (self.__iteratorSignal < self.__lenSignal_minus_1):
            if self.__time[self.__iteratorSignal] < t: 
                if self.__time[self.__iteratorSignal + 1] >= t:
                    break
                else:
                    self.__iteratorSignal += 1
            else:
                break
            
        self.__DataDictionary[ self.get(u"DisplayName") ] =  self.__signal[self.__iteratorSignal]
     
        
#############################################
## Recorder Class
#############################################

class PX_Recorder(PyLinXCoreDataObjects.PX_Object):
    
    _dictSetCallbacks = copy.copy(PyLinXCoreDataObjects.PX_Object._dictSetCallbacks)    
    
    class FileFormat:
        mdf = "mdf"
        csv = "csv"
    
    def __init__(self, parent, name = "recorder"): 
        super(PX_Recorder, self).__init__(parent, name)
        self.__DataDictionary = None
        self.__RunConfigDictionary = None
        self.__bRecord = False
        
    def init(self):

        self.__DataDictionary = self.mainController.getb(u"DataDictionary")
        self.__RunConfigDictionary = self.mainController.getb(u"RunConfigDictionary")
        self.__objectHandler = self.getRoot(PX_ObjectHandler)
        
        # The data would be accessible in self.__parent, but they should be copied before the run is started due to 
        # data consistency
        self.__recorder_BaseFileName                = self.__objectHandler.get(u"recorder_BaseFileName")
        self.__recorder_FileExtension               = self.__objectHandler.get(u"recorder_FileExtension")
        self.__recorder_fileFormat                  = self.__objectHandler.get(u"recorder_fileFormat")
        self.__recorder_SaveFolder                  = self.__objectHandler.get(u"recorder_SaveFolder")
        self.__recorder_RecordState                 = self.__objectHandler.get(u"recorder_RecordState")
        self.__bRecord                              = self.__objectHandler.bRecord
        self.__recorder_VariablesToRecordProcessed  = self.__objectHandler.recorder_VariablesToRecordProcessed
        
        self.__dataDict = {}
        
        # Preparomg time signal
        self.__dataDict[u"time_1"] = {}
        self.__dataDict["time_1"]["data"] = np.array([], np.float64)
        self.__dataDict["time_1"]["description"] = "Time"
        self.__dataDict["time_1"]["master"] = u"time_1"
        self.__dataDict["time_1"]["masterType"] = 1 
        self.__dataDict["time_1"]["unit"] = u"s"
        
        # Preparing each variable to record
        for var in self.__recorder_VariablesToRecordProcessed:
            self.__dataDict[var] = {}
            self.__dataDict[var]["data"] = np.array([], np.float64)
            self.__dataDict[var]["description"] = u""
            self.__dataDict[var]["master"] = u"time_1"
            self.__dataDict[var]["masterType"] = 1 
            self.__dataDict[var]["unit"] = u""

    def record(self):
        
        if self.__bRecord: 
            time = self.__RunConfigDictionary[u"t"]
            self.__dataDict[u"time_1"][u"data"] = np.append(self.__dataDict[u"time_1"][u"data"], time)
            for var in self.__recorder_VariablesToRecordProcessed:
                val = self.__DataDictionary[var]
                self.__dataDict[var][u"data"] = np.append(self.__dataDict[var]["data"], val)
            
    def exit(self):
        
        if self.__bRecord:
            if self.__recorder_fileFormat == self.FileFormat.mdf:
                self.__exit_mdf()
            elif self.__recorder_fileFormat == self.FileFormat.csv:
                self.__exit_csv()
        
        
    def __exit_csv(self):
        
        csvObject = PX_CSVObject.CSVObject()
        listVarsToSave = [u"time_1"]
        listVarsToSave.extend(self.__recorder_VariablesToRecordProcessed)
        for var in listVarsToSave:
            csvObject.addChannel({u"values": self.__dataDict[var][u"data"], \
                                  u"label": str(var), \
                                  u"unit": str(self.__dataDict[var][u"unit"]), \
                                  u"type": "f16"})
            
        dt = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = str(os.path.join(self.__recorder_SaveFolder,self.__recorder_BaseFileName + u"_" + dt + u".csv"))
        csvObject.write(filename, ["PyLinXItemFile", "record", "CrLf", "Tab"])
    
    
    def __exit_mdf(self):
           
        mdfObject = mdfreader.mdf()
        
        listVarsToSave = [u"time_1"]
        listVarsToSave.extend(self.__recorder_VariablesToRecordProcessed)
        for var in listVarsToSave :          
            mdfObject.add_channel(0, str(var),\
                       self.__dataDict[var][u"data"],\
                       master_channel   = str("time_1"), \
                       master_type      = self.__dataDict[var][u"masterType"],\
                       unit             = str(self.__dataDict[var][u"unit"]),\
                       description      = str(self.__dataDict[var][u"description"]),\
                       conversion       = None)
    
        dt = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = str(os.path.join(self.__recorder_SaveFolder,self.__recorder_BaseFileName + u"_" + dt + u".dat"))
        mdfObject.write(filename)        
        