import sys
import math
import numpy as np
import copy
import PlotSettings
from PyQt4 import QtGui, QtCore
from PyLinXCompiler import PyLinXRunEngine
from PyLinXData import PyLinXCoreDataObjects
import MyTableModel

class PlotterWidget(QtGui.QWidget):
    def __init__(self, varDispObj,  mainWidget = None, mainController = None, parent = None ):
        super(PlotterWidget, self).__init__(parent)
        # Members
        self.mainController = mainController
        self.DataDictionary = self.mainController.getb("DataDictionary")
        self.margin = 50
        self.FlagA = True
        self.FlagB = True
        self.checkslider = False
        self.sliderdataA = []
        self.sliderdataB = []
        
        self.dataslider = []
        self.slideridxA = 0
        self.slideridxB = 0
        
        self.zoomStack = []
        self.curveMap = {}   
        self.curveMapMemory = {}                                                            
        self.curZoom = 0      #int
        self.rubberBandIsShown = False
        self.pixmap = QtGui.QPixmap()
        self.rubberBandRect = QtCore.QRect()
        self.colorLight = self.palette().light().color()
        self.penDashLine = QtGui.QPen(QtGui.QBrush(QtCore.Qt.white), 1, QtCore.Qt.DashLine)
        self.delta_t = 0.1
        self.t     = np.array([self.delta_t*i for i in range(200)])
        self.varDispObj = varDispObj
        self.setStyleSheet("background-color:black")
        self.setAutoFillBackground(True)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.listVars = list(self.varDispObj.get(u"setVars"))
        self.colorFactory = PlotSettings.ColorFactory()
        self.dictVarColors = {}
        
        self.LineA = 137
        self.LineB = 313
        self.cout = 0
        iniSettings = PlotSettings.PlotSettings()
        self.setPlotSettings(iniSettings)       

        if self.listVars != None:
            for var in self.listVars:
                self.curveMap[var]=[]
                self.curveMapMemory[var] = []
          
        self.RunConfigDictionary = self.mainController.getb(u"RunConfigDictionary")    
        self.model = MyTableModel.MyTableModel(self)
########################################################       
    def getTableModel(self):
        return self.model
    
    def adjust(self):
        self.zoomStack[self.curZoom].adjust()
        self.refreshPixmap()
        
    def setBWalkingAxis(self, boolean):
        self.zoomStack[self.curZoom].setBWalkingAxis(boolean)
        self.refreshPixmap()
    
    def updateValues(self):
        self.listVars = list(self.varDispObj.get(u"setVars"))
        self.t = np.append(self.t, self.RunConfigDictionary[u"t"])
        self.settings.minX = self.t[-1] - 201 * self.RunConfigDictionary[u"delta_t"]
        self.settings.maxX = self.t[-1]
        if self.listVars != None:
            if len(self.listVars) > 0:
                for var in self.listVars:
                    if self.t[-1] == 0:
                        self.curveMap[var]=   []
                        self.curveMapMemory[var] = []                        
                    if var not in self.curveMap:
                        self.curveMap[var]=   []
                        self.curveMapMemory[var] = []
                    if len(self.curveMap[var]) > 200:
                        self.curveMapMemory[var].append(self.curveMap[var].pop(0))
                    self.curveMap[var].append(QtCore.QPointF(self.settings.maxX,\
                                                  self.DataDictionary[var]))         
                self.refreshPixmap()

                QtGui.QWidget.update(self)
                
        if self.cout <100:       
            for numline in range(len(self.listVars)):
                if self.settings.maxY < self.curveMap[self.listVars[numline]][-1].y():
                    self.settings.maxY = self.curveMap[self.listVars[numline]][-1].y() +5
                    self.refreshPixmap()
                if self.settings.minY > self.curveMap[self.listVars[numline]][-1].y():
                    self.settings.minY = self.curveMap[self.listVars[numline]][-1].y() -5
                    self.refreshPixmap()  
            self.cout = self.cout +1      
    
    def setPlotSettings(self,settings):                         
        self.zoomStack = []
        self.zoomStack.append(settings)
        self.curZoom = 0
        self.refreshPixmap()

    def setCurveData(self, idNum, data):
        self.curveMap[idNum] = data
        
    def clearCurve(self, idNum):
        if self.curveMap.has_key(idNum):
            self.curveMap.remove(idNum)
        self.refreshPixmap()
        
    def minimumSizeHint(self):
        return QtCore.QSize(0*self.margin,2*self.margin)
         
    def sizeHint(self):
        return QtCore.QSize(12*self.margin,8*self.margin)
    
    def zoomOut(self):
        if(self.curZoom > 0):
            self.refreshPixmap()
        
    def zoomIn(self):
        if(self.curZoom < len(self.zoomStack) - 1):
            self.curZoom = self.curZoom + 1
            self.refreshPixmap()
    
    def paintEvent(self, event):
        painter = QtGui.QStylePainter(self)             
        painter.drawPixmap(0, 0, self.pixmap)
        
        if self.rubberBandIsShown: 
            painter.setPen(self.palette().light().color()) 
            painter.drawRect(self.rubberBandRect.normalized().adjusted(0,0,-1,-1)) 
            painter.setPen(QtCore.Qt.red) 
        
        if self.hasFocus(): 
            option = QtGui.QStyleOptionFocusRect() 
            option.initFrom(self) 
            option.backgroundColor = self.palette().dark().color() 
            option.backgroundColor = self.palette().shadow().color() 
            painter.drawPrimitive(QtGui.QStyle.PE_FrameFocusRect, option)
        
    def resizeEvent(self, event):
        self.refreshPixmap()
    
    def mousePressEvent(self, event):
        rect = QtCore.QRect( self.margin, self.margin, self.width() - 2*self.margin, self.height() - 2*self.margin)
        if (event.button() == QtCore.Qt.LeftButton):
            if (rect.contains(event.pos())):
                self.rubberBandIsShown = True
                self.rubberBandRect.setTopLeft(event.pos())
                self.rubberBandRect.setBottomRight(event.pos())
                self.updateRubberBandRegion()
                self.setCursor(QtCore.Qt.CrossCursor)
        
        if self.checkslider == True:
            if self.sliderA.containsPoint(event.pos(), QtCore.Qt.OddEvenFill):
                self.FlagA = False
                self.FlagB = True
                
            if self.sliderB.containsPoint(event.pos(), QtCore.Qt.OddEvenFill):
                self.FlagB = False
                self.FlagA = True
                
        self.dataslider = []        
        for var in self.listVars:
            self.dataslider.append(self.curveMap[var])
            
    def mouseMoveEvent(self,event):
        rect = QtCore.QRect( self.margin, self.margin, self.width() - 2*self.margin, self.height() - 2*self.margin)
        if self.rubberBandIsShown:
            self.updateRubberBandRegion()
            self.rubberBandRect.setBottomRight(event.pos())
            self.updateRubberBandRegion()
      
        if self.checkslider == True:
            if self.FlagA == False:
                self.LineA = event.pos().x()
                if self.LineA < self.margin:
                    self.LineA = self.margin
                    self.refreshPixmap()     
                    
                elif self.LineB - self.LineA <=10:
                    self.LineA = self.LineB - 10
                    self.refreshPixmap()
                
                else:
                    self.refreshPixmap()
   
            if self.FlagB == False:
                self.LineB = event.pos().x()
                if self.LineB > self.width() -  self.margin:
                    self.LineB = self.width() -  self.margin
                    self.refreshPixmap()
                    
                elif self.LineB - self.LineA <=10:
                    self.LineB = self.LineA + 10
                    self.refreshPixmap()
                    
                else:
                    self.refreshPixmap()
                    
            self.sliderdataA = []
            self.sliderdataB = []                    
            for kk in range(len(self.dataslider)):
                if len(self.dataslider[kk]) > 0:
                    xa = self.LineA
                    self.dxa = (xa - rect.left())*self.settings.spanX()/(rect.width()-1)+self.settings.minX
                    for i in range(len(self.dataslider[kk])):
                        if self.dataslider[kk][i].x() > self.dxa:
                            self.slideridxA = i
                            break
                    self.sliderdataA.append(self.dataslider[kk][self.slideridxA].y())
                    xb = self.LineB
                    self.dxb = (xb - rect.left())*self.settings.spanX()/(rect.width()-1)+self.settings.minX
                    
                    for i in range(len(self.dataslider[kk])):
                        if self.dataslider[kk][i].x() > self.dxb:
                            self.slideridxB= i
                            break
                    self.sliderdataB.append(self.dataslider[kk][self.slideridxB].y())
            
            
    def printSlider(self):
        rect = QtCore.QRect( self.margin, self.margin, self.width() - 2*self.margin, self.height() - 2*self.margin)
        xa = self.LineA
        self.dxa = (xa - rect.left())*self.settings.spanX()/(rect.width()-1)+self.settings.minX
        xb = self.LineB
        self.dxb = (xb - rect.left())*self.settings.spanX()/(rect.width()-1)+self.settings.minX          
                   
            
    def mouseReleaseEvent(self,event):
        if (event.button() == QtCore.Qt.LeftButton) and self.rubberBandIsShown :
            self.rubberBandIsShown = False
            self.updateRubberBandRegion()
            self.unsetCursor()
            
            rect =  self.rubberBandRect.normalized()
            if rect.width() < 4 or rect.height() < 4 :
                return
            
            self.__zoomToRect(rect)
            self.zoomIn()
        self.model.dataChanged.emit(self.model.index(0,0), self.model.index(3,3))
        self.FlagA = True
        self.FlagB = True

    def __zoomToRect(self, rect, bAdjust = True):
        
            prevSettings = self.zoomStack[self.curZoom]                    
            settings = PlotSettings.PlotSettings()
            dx = prevSettings.spanX() / (self.width() - 2*self.margin)
            dy = prevSettings.spanY() / (self.height()- 2*self.margin)
            
            settings.minX = prevSettings.minX + dx * (rect.left() - self.margin)
            settings.maxX = settings.minX + dx * (rect.right() - rect.left())
            settings.maxY = prevSettings.maxY - dy * (rect.top() - self.margin)
            settings.minY = settings.maxY - dy * (rect.bottom() - rect.top())
            xaa = self.dxa- settings.minX
            self.LineA = self.margin + (xaa * (self.width()-100)/(settings.maxX - settings.minX))
            xbb = self.dxb- settings.minX
            self.LineB = self.margin + (xbb * (self.width()-100)/(settings.maxX - settings.minX))
            
            self.zoomStack.append(settings)
         
    def keyPressEvent(self, event):
        e = event.key()
        if e == QtCore.Qt.Key_Plus:
            self.zoomIn()
            
        elif e == QtCore.Qt.Key_Minus:
            self.zoomOut()
        
        elif e == QtCore.Qt.Key_Left:
            self.zoomStack[self.curZoom].scroll(-1,0)
            self.refreshPixmap()
            
        elif e == QtCore.Qt.Key_Right:
            self.zoomStack[self.curZoom].scroll(+1,0)
            self.refreshPixmap()
            
        elif e == QtCore.Qt.Key_Down:
            self.zoomStack[self.curZoom].scroll(0, -1)
            self.refreshPixmap()
            
        elif e == QtCore.Qt.Key_Up:
            self.zoomStack[self.curZoom].scroll(0, +1)
            self.refreshPixmap()
            
        else:
            super(PlotterWidget, self).keyPressEvent(event)
    
    def wheelEvent(self, event):
        modifier = QtGui.QApplication.keyboardModifiers()
        border = 15
        zoonRatio = 0.86      
        rect_zoom_x = QtCore.QRect( self.margin + border, self.margin, self.width() - 2*self.margin - border, self.height() - 2*self.margin + border)
        rect_zoom_y = QtCore.QRect( self.margin - border, self.margin, self.width() - 2*self.margin + border, self.height() - 2*self.margin - border)
        
        if self.LineB > self.width() -  self.margin:
            self.LineB = self.width() -  self.margin
            
        if self.LineA > self.width() -  self.margin:
            self.LineA = self.LineB-10
        
        if modifier == QtCore.Qt.ControlModifier:
            numDegrees = event.delta( ) / 8
            self.numTicks = numDegrees / 15
            
            if self.numTicks > 0:
                zoomFac = zoonRatio
            elif self.numTicks < 0:
                zoomFac = 1 / zoonRatio
            else:
                zoomFac = 1.0
                
            x = event.x()
            y = event.y()

            if (rect_zoom_x.contains(event.pos())):
                deltaX = self.width() -self.margin - x  
                facX = float(deltaX) / (self.width() - 2 * self.margin)
                rectZoom_width = zoomFac * (self.width() - 2 * self.margin)
                rectZoom_x = x - (1 - facX) * rectZoom_width
                    
            else:
                rectZoom_width = self.width() - 2 * self.margin
                rectZoom_x = self.margin

            if (rect_zoom_y.contains(event.pos())):
                deltaY = self.height() - self.margin - y 
                facY = float(deltaY) / (self.height() - 2 * self.margin)
                rectZoom_height = zoomFac * (self.height() - 2 * self.margin)
                rectZoom_y = y - (1 - facY) * rectZoom_height
            else:
                rectZoom_height = self.height() - 2 * self.margin
                rectZoom_y      = self.margin
            
            rectZoom = QtCore.QRect(rectZoom_x, rectZoom_y,rectZoom_width,rectZoom_height )             
            self.__zoomToRect(rectZoom)
            
            self.zoomIn()  

        else:
            numDegrees = event.delta() / 8
            numTicks = numDegrees / 15;
            if modifier == QtCore.Qt.ShiftModifier:
                self.zoomStack[self.curZoom].scroll(-numTicks,0, xMax = self.t[-1] )
            else:
                self.zoomStack[self.curZoom].scroll(0, numTicks)

            self.refreshPixmap()

        event.accept()
    
    def updateRubberBandRegion(self):
        rect =  self.rubberBandRect.normalized() 
        self.update(rect.left(), rect.top(), rect.width(), 1)
        self.update(rect.left(), rect.top(),1, rect.height())
        self.update(rect.left(), rect.bottom(), rect.width(), 1)
        self.update(rect.right(), rect.top(),1 , rect.height())

    def refreshPixmap(self):
        self.pixmap = QtGui.QPixmap(self.size())
        self.pixmap.fill(self, 0,0)
        
        painter = QtGui.QPainter(self.pixmap)
        painter.initFrom(self)
        
        self.drawGrid(painter)
        
        if self.checkslider == True:
            self.drawSlider(painter)
        self.drawCurves(painter)
        
        if self.LineB > self.width() -  self.margin:
            self.LineB = self.width() -  self.margin
            
        if self.LineA > self.width() -  self.margin:
            self.LineA = self.LineB-10

        if hasattr(self, 'dxa'):
            if self.FlagA == True and self.FlagB == True:
                if self.dxa > 0:
                    xaa = self.dxa- self.settings.minX
                    self.LineA = self.margin + (xaa * (self.width()-100)/(self.settings.maxX - self.settings.minX))
                    xbb = self.dxb- self.settings.minX
                    self.LineB = self.margin + (xbb * (self.width()-100)/(self.settings.maxX - self.settings.minX))
    
                    if self.LineB > self.width() -  self.margin:
                        self.LineB = self.width() -  self.margin
                
                    if self.LineA > self.width() -  self.margin:
                        self.LineA = self.LineB-10
        self.update()
 
    def drawGrid(self, painter):   
        
        def __drawXAxis():
            painter.setPen(self.penDashLine)
            painter.drawLine(x, rect.top(), x, rect.bottom())
            painter.setPen(self.colorLight)
            painter.drawLine(x, rect.bottom(), x, rect.bottom() + 5 )
            painter.drawText(x - 50, rect.bottom() + 5, 100, 20, 
                             QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop,  unicode('%0.2f' % label)) 
        
        rect = QtCore.QRect( self.margin, self.margin, self.width() - 2* self.margin, self.height() - 2* self.margin)
            
        if not rect.isValid():
            return
        settings = self.zoomStack[self.curZoom]
        # Draw vertical Lines
        deltaX = settings.spanX() / settings.numXTicks
        minXAxis = math.floor(settings.minX / deltaX)*deltaX                      
        if settings.bWalkingAxis:      
            minXAxisPx = rect.left() - ( float(settings.minX - minXAxis) / settings.spanX() ) * rect.width()  
            for i in range(settings.numXTicks +1):                
                x = minXAxisPx + ( i * (rect.width() - 1) / settings.numXTicks)
                if x >= rect.left():
                    label = minXAxis + ( i * deltaX )
                    __drawXAxis()

        else:
            for i in range(settings.numXTicks +1):              
                x = rect.left() + ( i * (rect.width() - 1) / settings.numXTicks)
                label = settings.minX + (  i * settings.spanX() / settings.numXTicks )
                __drawXAxis()
        
        #Draw horizontal Lines
        deltaY = settings.spanY() / settings.numYTicks
        for j in range(settings.numYTicks + 1):
            
            y = rect.bottom() - ( j * (rect.height() - 1) / settings.numYTicks)
            label = settings.minY + ( j * deltaY )
            painter.setPen(self.penDashLine)            
            painter.drawLine(rect.left(), y, rect.right(), y)
            painter.setPen(self.colorLight)
            painter.drawLine(rect.left() - 5, y, rect.left(), y )
            painter.drawText(rect.left() - self.margin, y - 10,self.margin - 5,  20, 
                             QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, unicode('%0.2f' % label))          #***********
            
        painter.drawRect(rect.adjusted(0, 0, -1, -1))
        
    def drawSlider(self, painter):
        pen = QtGui.QPen(QtCore.Qt.yellow, 1, QtCore.Qt.SolidLine)
        
        painter.setPen(pen)
        painter.drawLine(self.LineA, 50, self.LineA, self.height() - self.margin-2)
        pen.setStyle(QtCore.Qt.DashLine)  
        
        painter.drawLine(self.LineB, 50, self.LineB , self.height() - self.margin-2)
 
        pen.setStyle(QtCore.Qt.DashLine)  
        pen = QtGui.QPen(QtCore.Qt.white, 1, QtCore.Qt.SolidLine)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.gray)

        self.sliderA = QtGui.QPolygon([QtCore.QPoint( self.LineA - 5, 35 ), QtCore.QPoint( self.LineA + 5, 35 ),
                   QtCore.QPoint( self.LineA + 5, 45), QtCore.QPoint( self.LineA, 50 ),
                   QtCore.QPoint( self.LineA - 5, 45 )])
        painter.drawPolygon(self.sliderA)
        
        self.sliderB = QtGui.QPolygon([ QtCore.QPoint( self.LineB - 5, 35 ), QtCore.QPoint( self.LineB + 5, 35 ),
                           QtCore.QPoint( self.LineB + 5, 45), QtCore.QPoint( self.LineB, 50 ),
                           QtCore.QPoint( self.LineB - 5, 45 )])
        painter.drawPolygon(self.sliderB)
        painter.setPen(QtCore.Qt.white)
        painter.setFont(QtGui.QFont('Decorative', 6))
        painter.drawText(QtCore.QPoint(self.LineA-2, 43) , 'A') 
        painter.setFont(QtGui.QFont('Decorative', 6))
        painter.drawText(QtCore.QPoint(self.LineB - 2, 43) , 'B')

    
    def drawCurves(self,  painter):
        colorForIds = [QtCore.Qt.red, QtCore.Qt.green, QtCore.Qt.blue, QtCore.Qt.cyan, QtCore.Qt.magenta, QtCore.Qt.yellow]
        self.settings = self.zoomStack[self.curZoom]
        
        rect = QtCore.QRect( self.margin, self.margin, self.width() - 2*self.margin, self.height() - 2*self.margin)
        
        if not rect.isValid():
            return
        
        painter.setClipRect(rect.adjusted(1, 1, -1, -1)) 
        i = 0
        for var in self.listVars:
            data = self.curveMap[var]
            polyline = QtGui.QPolygonF()
            
            for j in range(len(data)): 
                dx = data[j].x() - self.settings.minX 
                dy = data[j].y() - self.settings.minY
                x = rect.left() + (dx * (rect.width()-1)/self.settings.spanX()) 
                y = rect.bottom() - (dy * (rect.height()-1)/self.settings.spanY()) 
                polyline.append(QtCore.QPointF(x,y))

            if var in self.dictVarColors:
                color = self.dictVarColors[var]
            else:
                color = self.colorFactory.getColor()
                self.dictVarColors[var] = color
            painter.setPen(color) 
            painter.drawPolyline(polyline)
            i += 1
            
    def stop_run(self):
        self.cout = 0
        for var in self.listVars: 
            copyValues = copy.copy(self.curveMap[var])
            copyValuesMemory = copy.copy(self.curveMapMemory[var])
            self.curveMap[var] = copyValuesMemory
            self.curveMap[var].extend(copyValues )
        self.refreshPixmap()
    
    def checkTrue(self):
        self.checkslider = True
        self.refreshPixmap()
        
    def checkFalse(self):
        self.checkslider =False
        self.refreshPixmap()
        
    def setLine(self):
        rect = QtCore.QRect( self.margin, self.margin, self.width() - 2*self.margin, self.height() - 2*self.margin)
        self.LineA = self.margin + (self.width()-100)/4
        xa = self.LineA
        self.dxa = (xa - rect.left())*self.settings.spanX()/(rect.width()-1)+self.settings.minX
        self.LineB = self.margin + 3*(self.width()-100)/4
        xb = self.LineB
        self.dxb = (xb - rect.left())*self.settings.spanX()/(rect.width()-1)+self.settings.minX
        
