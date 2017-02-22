


'''
Created on 07.01.2015

@author: Waetzold Plaum
'''
import sys
import inspect
import string
import os
from PyQt4 import QtGui, QtCore
 

import PyLinXData.PyLinXHelper as helper    


class EasyWidget(QtGui.QWidget):
    
    class Types():
        bool            = u"bool"
        float           = u"float"
        color           = u"color"
        comboBoxItem    = u"comboBoxItem"
        int             = u"int"
        unicode         = u"unicode"
        time        = u"time" ##
        date        = u"date" ##
        SpinBox         = u"SpinBox"  ##
        DoubleSpinbox   = u"DoubleSpinbox"##
        FileDirectory   = u"FileDirectory"
        FilePath   = u"FilePath"
        listTypes = [bool, float, color, comboBoxItem, int, unicode, time, date, SpinBox, DoubleSpinbox, FileDirectory,FilePath] ##
    
    class DispOrder():
        NameValue = 0
        ValueName = 1
                    
    class ColorSelectButton(QtGui.QPushButton):
    
        def __init__(self, color = QtGui.QColor(u"white")):
            super(EasyWidget.ColorSelectButton, self).__init__()
            
            self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
            
            self.clicked.connect(self.__on_button_clicked)
            self.__color = color
            self.__pixmap = QtGui.QPixmap(48,48)
            self.__pixmap.fill(self.__color)
            self.setMaximumWidth(24)
            self.setPixMap()
            
            
        def __on_button_clicked(self):
            col = QtGui.QColorDialog.getColor(self.__color, self)
            if col.isValid():
                self.__color  = col
            self.__pixmap.fill(col)
            self.setPixMap()
            self.repaint()
            
                
        def color(self):
            return self.__color
        
        def setPixMap(self):
            icon = QtGui.QIcon(self.__pixmap)
            self.setIcon(icon)

    class LineEditTyped (QtGui.QLineEdit):
        
        def __init__(self, _type):
            super(EasyWidget.LineEditTyped, self).__init__(_type)
            
            self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        
            self.__filter = EasyWidget.FilterFocusOut(_type, self)
            self.installEventFilter(self.__filter) 

#    class FilePath(QtGui.QPushButton):
#        def __init__(self, strPath = u""):
#            super(EasyWidget.FilePath, self).__init__()
#            
#            self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
#        
#            
#            self.clicked.connect(self.showFileSelectionDialog)
#            self.strPath = strPath
#           
#       
#        def stringFilePath(self):
#            return self.strPath
#        
#        def directoryName(self, stringFilePath):
#            
#            path = self.stringFilePath()
#            if os.path.exists(path):
#                return None
#            
#          
          
          
        

    class FileDirectory(QtGui.QPushButton):
        
        def __init__(self, strPath = u""):
            super(EasyWidget.FileDirectory, self).__init__()
            
            
            self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
            self.setFocusPolicy(QtCore.Qt.StrongFocus)
            
            self.clicked.connect(self.showDialog)
            self.strPath = strPath
           
        def showDialog(self):
            self.strPath = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))

        

          
          

    class FilterFocusOut(QtCore.QObject):
        
        def __init__(self, _type, _lineEdit):
            QtCore.QObject.__init__(self)
            if _type in (EasyWidget.Types.float, EasyWidget.Types.unicode, EasyWidget.Types.int):
                self.__type = _type
            else:
                self.__type = None
            self.__lineEdit =_lineEdit 
        
        def eventFilter(self, widget, event):
            if event.type() == QtCore.QEvent.FocusOut:
                text = self.__lineEdit.text()
                if self.__type == EasyWidget.Types.int:
                    try:
                        text = int(float(text))
                    except:
                        raise Exception("Error EasyWidget.FilterFocusOut.eventFilter: Unable to cast to int!")
                elif self.__type == EasyWidget.Types.float:
                    try:
                        text = float(text)
                    except:
                        raise Exception("Error EasyWidget.FilterFocusOut.eventFilter: Unable to cast to float!")
                elif self.__type == EasyWidget.Types.unicode:
                    try:
                        text = unicode(text)
                    except:
                        raise Exception("Error EasyWidget.FilterFocusOut.eventFilter: Unable to cast to unicode!")
                self.__lineEdit.setText(str(text))  
            return False

    def __init__(self, init_list, bValuesFirst = False):

        super(EasyWidget,self).__init__()
        
         
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
         
        grid = QtGui.QGridLayout()
        self.__dictEditElements = {}
        self.__dictTypes = {}
        self.__listInitData = init_list
        
        if bValuesFirst:
            idxEdit  = 0
            idxLabel = 1
        else:
            idxEdit  = 1
            idxLabel = 0

        for counter, valDict in enumerate(init_list):
            
            keys        = valDict.keys()
            Name        = valDict[u"Name"]
            DisplayName = valDict[u"DisplayName"]
            Value       = valDict[u"Value"]
            ValueType   = valDict[u"ValueType"]
            label = QtGui.QLabel(DisplayName)
            if ValueType == EasyWidget.Types.bool:
                editElement = QtGui.QCheckBox()
                if Value == True:
                    checkState = QtCore.Qt.Checked
                elif Value == False:
                    checkState = QtCore.Qt.Unchecked
                else:
                    checkState = QtCore.Qt.PartiallyChecked
                editElement.setCheckState(checkState)
            elif ValueType == EasyWidget.Types.color:
                editElement = EasyWidget.ColorSelectButton()
            elif ValueType == EasyWidget.Types.comboBoxItem:
                editElement = QtGui.QComboBox()
                ValueList = valDict[u"ValueList"]
                for value in ValueList:
                    editElement.addItem(value)
            elif ValueType == EasyWidget.Types.float:
                editElement = EasyWidget.LineEditTyped(EasyWidget.Types.float)
                editElement.setText(str(Value))
            elif ValueType == EasyWidget.Types.int:
                editElement = EasyWidget.LineEditTyped(EasyWidget.Types.int)
                editElement.setText(str(Value))
            elif ValueType == EasyWidget.Types.unicode:
                editElement = EasyWidget.LineEditTyped(EasyWidget.Types.unicode)
                editElement.setText(str(Value))
            
            elif ValueType == EasyWidget.Types.time:                                    
                editElement = QtGui.QTimeEdit()
                      
            
            elif ValueType == EasyWidget.Types.date:                                      
                editElement = QtGui.QDateEdit()           
            
            elif ValueType == EasyWidget.Types.SpinBox:                                    
                editElement = QtGui.QSpinBox()         
            
            elif ValueType == EasyWidget.Types.DoubleSpinbox:                                
                editElement = QtGui.QDoubleSpinBox()          
            
            elif ValueType == EasyWidget.Types.FileDirectory:
                editElement = EasyWidget.FileDirectory()
            
            elif ValueType == EasyWidget.Types.FilePath:
                editElement = EasyWidget.FilePath()
                
            
            
            grid.addWidget(editElement, counter, idxEdit)
            grid.addWidget(label, counter, idxLabel)
            grid.setColumnStretch(idxLabel,1)
            
 
            
            if u"Unit" in keys:
                Unit  = valDict[u"Unit"]
                label = QtGui.QLabel(u"["+Unit+u"]")
                grid.addWidget(label, counter, 2)
                

            # Remember some data                    
            self.__dictEditElements[Name] = editElement 
            self.__dictTypes[Name] = ValueType
        
        self.setLayout(grid)
        

        
    def getValues(self):
        
        retDict = {}
        
        for valDict in self.__listInitData:
            Name        = valDict[u"Name"]
            ValueType   = valDict[u"ValueType"]
            if ValueType == EasyWidget.Types.bool:
                value       = self.__dictEditElements[Name].checkState()
                if value == QtCore.Qt.Checked:
                    value = True
                elif value == QtCore.Qt.Unchecked:
                    value = False
                else:
                    raise Exception("Error BeasyWidget.getValue: Impossible cast to bool.")                
            elif ValueType == EasyWidget.Types.color:
                value       = self.__dictEditElements[Name].color()
            elif ValueType == EasyWidget.Types.comboBoxItem:
                value       = unicode(self.__dictEditElements[Name].currentText())
            elif ValueType == EasyWidget.Types.int:
                value       = int(self.__dictEditElements[Name].text())
            elif ValueType == EasyWidget.Types.float:
                value       = float(self.__dictEditElements[Name].text())
            elif ValueType == EasyWidget.Types.unicode:
                value       = unicode(self.__dictEditElements[Name].text())
                
            elif ValueType == EasyWidget.Types.FileDirectory:
                value       = self.__dictEditElements[Name].stringFileDirectoryPath()
            
            elif ValueType == EasyWidget.Types.FilePath:
                value       = self.__dictEditElements[Name].stringFilePath()
            
            
            else:
                value = None
            retDict[Name] = value
        return retDict

#     Just for testing
    def closeEvent(self, event):
        print self.getValues()
        
        
if __name__ == u"__main__":
        
    app = QtGui.QApplication(sys.argv)
    
    init_list = [{ u"Name": u"stim_Frequency",u"DisplayName":  u"Frequency", u"ValueType": u"float", u"Unit": u"Hz", u"Value":0.},\
                 { u"Name": u"constVal",      u"DisplayName":  u"Value",     u"ValueType": u"int", u"Value":5},\
                 { u"Name": u"stim_Phrase",    u"DisplayName":  u"Phrase",     u"ValueType": u"unicode", u"Value":0.},\
                 { u"Name": u"constVal2",      u"DisplayName":  u"Value",     u"ValueType": u"bool", u"Value":True},\
                 { u"Name": u"stim_Frequency2",u"DisplayName":  u"Frequency", u"ValueType": u"bool", u"Value":False},\
                 { u"Name": u"stim_Phase2",    u"DisplayName":  u"Phase",     u"ValueType": u"bool", u"Value":False},\
                 { u"Name": u"colTest2",       u"DisplayName":  u"Farbe der Welt",     u"ValueType": u"color", u"Value":QtGui.QColor(u"white")},\
                 { u"Name": u"stim_Frequency3",u"DisplayName":  u"Frequency", u"ValueType": u"bool",  u"Value":False},\
                 { u"Name": u"stim_Phase3",    u"DisplayName":  u"Phase",     u"ValueType": u"float", u"Value":0.,u"Unit": u"Hz"},\
                 { u"Name": u"valSpin",       u"DisplayName":  u"Value from ComboBox", u"ValueType": u"comboBoxItem", \
                        u"Value": u"One", u"ValueList": [u"one", u"two", u"three"], u"Value": "two", u"Unit": "Wz"},\
                 {u"Name" : u"timeEdit", u"DisplayName" : u"Time", u"ValueType" : u"time", u"Value":0.},\
                 {u"Name" : u"dateEdit", u"DisplayName" : u"Date", u"ValueType" : u"date", u"Value":0.},\
                 {u"Name" : u"spinbox_label", u"DisplayName" : u"SpinBox", u"ValueType" : u"SpinBox", u"Value":0.},\
                 {u"Name" : u"doublespinbox_label", u"DisplayName" : u"DoubleSpinbox", u"ValueType" : u"DoubleSpinbox", u"Value":0.},\
                 {u"Name" : u"FileDirectory_label", u"DisplayName" : u"FileDirectory", u"ValueType" : u"FileDirectory", u"Value":0.},\
                 {u"Name" : u"FilePath_label", u"DisplayName" : u"FilePath", u"ValueType" : u"FilePath", u"Value":0.},
                  
                 ]
    
    easyWidget = EasyWidget(init_list, False)
    easyWidget.show()
    app.exec_()
    
    


