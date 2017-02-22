import sys
import math
import numpy as np
import copy

from PyQt4 import QtGui, QtCore
class PlotSettings(QtGui.QWidget):
    def __init__(self):
        super(PlotSettings, self).__init__()
        self.minX = -10.0
        self.maxX = 0
        self.numXTicks = 5
        self.minY = 0
        self.maxY = 10.0
        self.numYTicks = 5
        self.bWalkingAxis = False
    # This function increments or drcrements minX, minY, maxX, maxY.Basically the function is used in PlotterWidget- KeyPressedEvent(). 
    def scroll(self,dx,dy, xMax = None):  

        stepX = self.spanX() / self.numXTicks
        minX = self.minX + dx * stepX
        maxX = self.maxX  + dx * stepX

        if minX < 0:
            spanX = self.spanX()
            self.minX = 0
            self.maxX = spanX
        elif xMax != None:
            if maxX > xMax:
                spanX = self.spanX()
                self.maxX = xMax
                self.minX = xMax - spanX
            else:
                self.maxX = maxX
                self.minX = minX                
        else:
            self.maxX = maxX
            self.minX = minX
        
        stepY = self.spanY() / self.numYTicks
        self.minY += dy * stepY
        self.maxY += dy * stepY
    #Used by mouseReleaseEvent() to round of axis parameters to nice values and to determine appropriate ticks for each axis.takes one axix at a time.
    def adjust(self):
        self.minX, self.maxX, self.numXticks = self.adjustAxis(self.minX, self.maxX, self.numXTicks)
        self.minY, self.maxY, self.numYticks = self.adjustAxis(self.minY, self.maxY, self.numYTicks)      #****check******

    def spanX(self):
        return self.maxX - self.minX

    def spanY(self):
        return self.maxY - self.minY
    
    def adjustAxis(self, mini, maxi, numTicks):            
        MinTicks = 4
        grossStep = (maxi - mini) / MinTicks
        step = math.pow(10.0, math.floor(math.log10(grossStep))) 
        
        if 5*step < grossStep:
            step *= 5
        elif 2*step < grossStep:
            step *= 2
            
        numTicks = int(math.ceil(maxi / step)) - math.floor(mini / step)
        
        if numTicks < MinTicks:
            numTicks = MinTicks
        mini = math.floor(mini / step) * step
        maxi = math.ceil(maxi / step) * step

        return mini, maxi, numTicks
    
    def setBWalkingAxis(self, boolean):
        if boolean == False:
            self.bWalkingAxis = False
        elif boolean == True:
            self.bWalkingAxis = True
        else:
            raise Exception("Error!")

    def addVar(self, varName):
        
        print "self.listVars (0)", self.listVars

        global DataDictionary
        if varName not in DataDictionary:
            raise Exception(u"Error: Variable could not be displayed!")
        else:
            if not varName in self.listVars: 
                self.listVars.append(varName)
        print "self.listVars (1)", self.listVars
            
    def delVar(self, varName):
        
        global DataDictionary
        if varName not in DataDictionary:
            raise Exception(u"Error: Variable could not be deleted!")
        else:
            self.listVars.pop(varName)
            
class ColorFactory(object):
    
    def __init__(self):
        super(ColorFactory, self).__init__()
        self.listColor = [QtCore.Qt.red, \
                          QtCore.Qt.green, \
                          QtCore.Qt.lightGray,\
                          QtCore.Qt.cyan, \
                          QtCore.Qt.magenta, \
                          QtCore.Qt.yellow]
        self.idxColor = 0
        
    def getColor(self):
        idx = self.idxColor
        self.idxColor = (self.idxColor + 1) % len(self.listColor)
        return self.listColor[idx] 