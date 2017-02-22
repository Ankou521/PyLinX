'''
Created on 02.09.2015

@author: Waetzold Plaum
'''
import copy

from PyLinXData import PyLinXCoreDataObjects
import PyLinXRunEngine 

################################################
# internal classes used for code-generation
# they should "know" all the global information
# of the run-engine
################################################

class PX_CodeRefObject(PyLinXCoreDataObjects.PX_IdObject):
    
    '''
    classdocs
    '''
    _dictSetCallbacks = copy.copy(PyLinXCoreDataObjects.PX_IdObject._dictSetCallbacks)
    _dictGetCallbacks = copy.copy(PyLinXCoreDataObjects.PX_IdObject._dictGetCallbacks)

    def __init__(self, parent, refObj):
        '''
        Constructor
        '''
        name = refObj.get(u"Name") + u"_REF"
        super(PX_CodeRefObject, self).__init__(parent, name)
        self._BContainer__Head = refObj
        
        
    def get_ref(self):
        return self._BContainer__Head
    
    ref = property(get_ref)
        

class PX_CodableBasicOperator(PX_CodeRefObject):
    
    _dictSetCallbacks = copy.copy(PX_CodeRefObject._dictSetCallbacks)
    _dictGetCallbacks = copy.copy(PX_CodeRefObject._dictGetCallbacks)
    
    def __init__(self,parent, knot, CodingVariant, orderConnection):
        super(PX_CodableBasicOperator, self).__init__(parent, knot)
        self.__orderConnection = orderConnection
        
    def getCode(self,Code):
        lenBody = len(self._BContainer__Body)
        if lenBody != 2:
            print "TODO: Error-Handling (2)"
        else:
            keys = self.getChildKeys()
            objs = [self.getb(key).get_ref() for key in keys]   # list of corresponding core data objects
            variables = {}
            
            # Notice: Python convention of negative list indices !!!
            # Dict of the variable strings left and right of the operator
            #         reading the mapping                   Code of the variable Variable generated 
            #         ID -> Order of connection             by the code-Ref object of connected elements 
            variables[self.__orderConnection[objs[0].ID]] = self.getb(keys[0]).getCode(Code)
            variables[self.__orderConnection[objs[1].ID]] = self.getb(keys[1]).getCode(Code)
            operator = self.ref._BContainer__Head
            
            return u"( " + variables[-1] + u" " + operator + u" " + variables[-2] + u" ) "


class PX_CodableVarElement(PX_CodeRefObject):
            
    _dictSetCallbacks = copy.copy(PX_CodeRefObject._dictSetCallbacks)
    _dictGetCallbacks = copy.copy(PX_CodeRefObject._dictGetCallbacks)
    
    def __init__(self,parent, knot, CodingVariant):
        super(PX_CodableVarElement, self).__init__(parent, knot)
        self.CodingVariant = CodingVariant
        
    def getCode(self, Code):
        name = self.ref.get(u"DisplayName") 
        if self.__elementIsConnected():
            _input = self.getb(self.getChildKeys()[0])
            code_to_add = self.__getCode_getVarName(name) + u" = " + _input.getCode(Code)
            # So far this is the ONLY part of the code generator, where a new line of code is added to the generated core code! 
            Code.appendLine(code_to_add)
        return self.__getCode_getVarName(name)
    
    def __elementIsConnected(self):
        lenBody = len(self._BContainer__Body)
        return (lenBody == 1)
        
    def __getCode_getVarName(self, rawName):
        if self.CodingVariant == PyLinXRunEngine.PX_CodeAnalyser.CodingVariant.ReadSingleVars:
            retName = rawName
        elif self.CodingVariant == PyLinXRunEngine.PX_CodeAnalyser.CodingVariant.ReadVarsFromDataDict:
            retName =  u"DataDictionary[u\"" + rawName + u"\"]"
        return retName