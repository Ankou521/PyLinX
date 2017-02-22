import sys
import math
import numpy as np
import copy
from PyQt4 import QtGui, QtCore
class MyTableModel(QtCore.QAbstractTableModel):
    
    def __init__(self, plotterWidget, parent= None, *args ):
        QtCore.QAbstractTableModel.__init__(self, parent , *args)
        
        self.plotterWidget = plotterWidget
        
    def rowCount(self, parent):
        if self.plotterWidget.checkslider == False:
            return len(self.plotterWidget.listVars)
        else:
            return len(self.plotterWidget.listVars)

    def columnCount(self, parent):
        if self.plotterWidget.checkslider == False:
            return 4
        else:
            return 4
        
    def data(self, index, role):
        for ii in range(len(self.plotterWidget.listVars)):
            self.plotterWidget.sliderdataA.append(0)
            self.plotterWidget.sliderdataB.append(0)
        if self.plotterWidget.checkslider == False:
            if not index.isValid():
                return QtCore.QVariant()
            
            elif role == QtCore.Qt.BackgroundRole:
                if index.column() == 0:
                    retVal = self.plotterWidget.dictVarColors[self.plotterWidget.listVars[index.row()]]
                    return QtGui.QBrush(retVal)
            #######################
            elif role != QtCore.Qt.DisplayRole:
                return None
            
            elif index.column()==2:
                
                retVal = self.plotterWidget.curveMap[self.plotterWidget.listVars[index.row()]][-1].y() 
                return retVal 
            
            elif index.column()==1:
                retVal = self.plotterWidget.listVars[index.row()]               
                return retVal
            
            elif role == QtCore.Qt.CheckStateRole:
                return("")

            return QtCore.QVariant("")
        else:
            if not index.isValid():
                return QtCore.QVariant()
            
            elif role == QtCore.Qt.BackgroundRole:
                if index.column() == 0:
                    retVal = self.plotterWidget.dictVarColors[self.plotterWidget.listVars[index.row()]]
                    return QtGui.QBrush(retVal)
                
            elif role != QtCore.Qt.DisplayRole:
                return None
            
            elif index.column()==2:
                retVal = self.plotterWidget.sliderdataB[index.row()]  
                return retVal 
            
            elif index.column()==1:
                retVal = self.plotterWidget.sliderdataA[index.row()]  
                return retVal
            
            elif index.column()==3:
                retVal = self.plotterWidget.sliderdataA[index.row()] - self.plotterWidget.sliderdataB[index.row()]   
                return retVal 
            
            elif role == QtCore.Qt.CheckStateRole:
                return("")

            return QtCore.QVariant("")
    
    def headerData(self,col,orientation,role):   
        if self.plotterWidget.checkslider == False:
            self.headerdata =['color','Label','Data','']
        else:
            self.headerdata = ['color','Slider A','Slider B','Diff']
               
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.headerdata[col])
        return QtCore.QVariant()
    
    def flags(self,index):
        return(QtCore.Qt.ItemIsEnabled| QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable)
    