'''
Created on 02.09.2015

@author: Waetzold Plaum
'''
import copy

from PyLinXData.BContainer import BList

class Code(BList):
    
    _dictSetCallbacks = copy.copy(BList._dictSetCallbacks)
    _dictGetCallbacks = copy.copy(BList._dictGetCallbacks)
        
    def __init__(self):
        
        super(Code, self).__init__(name="Code")
        
        self.__nIndent = 0
        
    def appendLine(self, stri):
        
        Code = self.__nIndent * u"    "
        Code += stri
        self.append(Code)
                
    def getCodeStr(self):
        
        stri = u""
        for codeLine in self:
            stri += codeLine
            stri += "\n"
        return stri
    
    def changeIndent(self, delta):
        
        result = self.__nIndent + delta 
        if result >= 0:
            self.__nIndent += delta
        else:
            self.__nIndent = 0
            
    def printList(self):
        printstr = u"["
        for item in self:
            printstr += str(item) + u","
        printstr += u"]"
        print printstr    