'''
Created on 11.01.2017

@author: xtong
'''

import copy
from PyQt4 import QtGui
from PyQt4 import QtCore
              
class PX_CommandConsole(QtGui.QTextEdit):
    
    color = {}
    black = QtGui.QColor(u"black")
    darkGray = QtGui.QColor(u"darkGray")
    darkRed = QtGui.QColor(u"darkRed")
    darkBlue = QtGui.QColor(u"darkBlue")
    color[u"darkGray"] = darkGray 
    color[u"black"]   = black
    color[u"darkRed"] = darkRed
    color[u"darkBlue"] = darkBlue
    
    def __init__(self, parent = None, mainController = None):

        super(PX_CommandConsole, self).__init__(parent)
        self.setWordWrapMode(QtGui.QTextOption.WrapAnywhere)            
        self.setUndoRedoEnabled(False)
        self.__mainController = mainController
        self.prompt = mainController.activeFolder.get__path() + u"> "
        self.commandExit(self.prompt)

        textFont = QtGui.QFont()
        textFont.setFamily("monospace [Consolas]")
        textFont.setFixedPitch(True)
        textFont.setStyleHint(QtGui.QFont.TypeWriter)
        self.setFont(textFont)

            
    def newProject(self, mainController):
        self.__mainController = mainController
              
    def showMessage(self, path, message, colorStr = "black"):
        color = PX_CommandConsole.color[colorStr]
        self.setTextColor(PX_CommandConsole.black)           
        self.setFontWeight(QtGui.QFont.Bold)
        self.append(path)
        self.setFontWeight(QtGui.QFont.Light)   
        self.textCursor().movePosition(QtGui.QTextCursor.End)
        self.setTextColor(color)
        self.insertPlainText(message)
        self.moveCursor(QtGui.QTextCursor.End)
        
    def showInfoText(self, text, colorStr = "darkBlue"):
        if text != None:
            color = PX_CommandConsole.color[colorStr]
            self.moveCursor(QtGui.QTextCursor.End)
            self.setTextColor(color)
            self.setFontWeight(QtGui.QFont.Light)
            self.insertPlainText(text)
            self.moveCursor(QtGui.QTextCursor.End)

    def commandInit(self, command, colorStr = "black"):
        color = PX_CommandConsole.color[colorStr]
        self.moveCursor(QtGui.QTextCursor.End)
        self.setTextColor(color)
        self.setFontWeight(QtGui.QFont.Light) 
        self.insertPlainText(command + u"\n")
        self.moveCursor(QtGui.QTextCursor.End)
           
    def commandExit(self, path):
        self.promt = path + "> "
        self.setTextColor(PX_CommandConsole.black)
        self.setFontWeight(QtGui.QFont.Black)
        self.insertPlainText( path)
        self.moveCursor(QtGui.QTextCursor.End)
    
    def getCommand(self):
        doc = self.document()
        curr_line = unicode(doc.findBlockByLineNumber(doc.lineCount() - 1).text())
        curr_line = curr_line.rstrip()
        curr_line = curr_line[len(self.promt ) - 2 :]  
        return curr_line   
    
    def _blockCount(self):
        cmd = self.getCommand()
        return (len(cmd) + 1) 
    
    def runCommand(self, event):
        command = self.getCommand()
        super(PX_CommandConsole, self).keyPressEvent(event)
        self.__mainController.execCommand(command, bConsole = True)

    def mousePressEvent(self, event):
        super(PX_CommandConsole, self).mousePressEvent(event)

    def mouseMoveEvent( self, event ):
        super(PX_CommandConsole, self).mouseMoveEvent(event)
            
    def mouseReleaseEvent(self, event):
        super(PX_CommandConsole, self).mouseReleaseEvent(event)
        
    def keyPressEvent(self, event):
        bNotLastLine = (self.textCursor().blockNumber() < self.document().blockCount() - 1) 
        bLastLine = (self.textCursor().blockNumber() == self.document().blockCount() - 1)
        bLineMaxColumnNumber = 139
        LineColumnNumber = self.textCursor().columnNumber()
        bCharactorCount = self._blockCount()
        len_promt = len(self.prompt)
        
        if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
            self.runCommand(event)
            return 
        
        if bNotLastLine:
            return 
                      
        elif event.key() == (QtCore.Qt.Key_Left):
            if bCharactorCount < bLineMaxColumnNumber:
                if LineColumnNumber <= len_promt:
                    return
            else:
                if LineColumnNumber == 0:
                    return
            
        elif event.key() == QtCore.Qt.Key_Delete:
            if bNotLastLine:
                return
            else:
                if LineColumnNumber <= len_promt:
                    return                
                
        elif event.key() == QtCore.Qt.Key_Backspace:
            if bCharactorCount < bLineMaxColumnNumber:
                if bLastLine:
                    if LineColumnNumber == len_promt:
                        return
            else:
                if bLastLine:
                    if LineColumnNumber == 0:
                        return

        super(PX_CommandConsole, self).keyPressEvent(event)
        