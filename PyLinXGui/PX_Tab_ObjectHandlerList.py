import sys #, os
from PyQt4 import QtCore, QtGui

#import PyLinXData.PyLinXHelper as helper
import PyLinXCtl.PyLinXProjectController as ctl
#import matplotlib.pyplot as pyplot

class QListWidget_ObjHandler(QtGui.QListWidget):
    def __init__(self, parent=None, listItems={}):
        super(QListWidget_ObjHandler, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setIconSize(QtCore.QSize(124, 124))
        self.doubleClicked.connect(self.doubleClickEvent)
        self.listItems = listItems

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
            
    def doubleClickEvent(self, modelIndex):
        print u"doubleClocked"



class NamedQListWidgetItem(QtGui.QListWidgetItem):

    def __init__(self, itemString, nameFileObject = None):
        
        super(NamedQListWidgetItem, self).__init__(itemString)
            

class PX_Tab_ObjectHandlerList(QtGui.QWidget):
    
    def __init__(self, mainController):
        
        super(QtGui.QWidget,self).__init__()
        self.listItems={}
        myBoxLayout = QtGui.QVBoxLayout()
        self.setLayout(myBoxLayout)
        self.toolbar = QtGui.QToolBar()
        self.mainController = mainController
        self.__objectHandler = mainController.getb(u"ObjectHandler")        

        self.listItems = {}

        self.myListWidget = QListWidget_ObjHandler(self, self.listItems)  
        self.myListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        
        myBoxLayout.addWidget(self.toolbar)
        myBoxLayout.addWidget(self.myListWidget)

        ## Tool-Bar

        self.toolbar.setIconSize (QtCore.QSize(16,16))
        
        self.toolbar.setStyleSheet(u".QToolBar {border: 0px;}")
        self.SignalFileName = None
        
        # Signals
        #########
        
        self.connect(self.mainController.mainWindow, QtCore.SIGNAL(u"dataChanged__objectHandler"), self.repaint )
        
        self.repaint()
        
    def repaint(self):
        listObjects = self.__objectHandler.listObjects
        self.listItems = {}
        for _object in listObjects:
            listItem = NamedQListWidgetItem( _object)
            self.addListWidgetItem(listItem)
        super(PX_Tab_ObjectHandlerList, self).repaint()
        
    def addListWidgetItem(self, listItemName = None):
        if listItemName == None:
            listItemName='Item '+str(len(self.listItems.keys()))        
        self.listItems[listItemName]=None 
        self.rebuildListWidget() 

    def rebuildListWidget(self):
        self.myListWidget.clear()
        items=self.listItems.keys()
        if len(items)>1: items.sort()
        for listItemName in items:
            listItem = NamedQListWidgetItem( listItemName, self.SignalFileName)
            self.listItems[listItemName]=listItem
            self.myListWidget.addItem(listItem)
            
    def newProject(self, mainController):
        self.mainController = mainController
        self.__objectHandler = self.mainController.getb(u"ObjectHandler")
            

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainController = ctl.PyLinXProjectController(bListActions = False)
    
    # Example-Data
    
    script = u"new varElement TestVar_0 150 90 15 refName=\"TestVar_0\"\n\
new varElement Variable_id4 150 140 15 refName=\"Variable_id4_1\" \n\
new varElement Variable_id4 400.0 100.0 15 refName=\"Variable_id4_2\"\n\
new basicOperator + 300.0 100.0 name=u\"Operator_1\"\n\
new connector TestVar_0 Operator_1 idxInPin=1\n\
new connector Variable_id4_1 Operator_1 idxInPin=0\n\
new connector Operator_1 Variable_id4_2 idxInPin=0"
            
    mainController.execScript(script)    
    
    dialog_1 = PX_Tab_ObjectHandlerList(mainController)
    dialog_1.show()
    dialog_1.resize(480,320)
    sys.exit(app.exec_()) 