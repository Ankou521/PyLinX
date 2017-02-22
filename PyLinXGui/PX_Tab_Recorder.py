import sys #, os
from PyQt4 import QtCore, QtGui

import PyLinXData.PyLinXHelper as helper
import PyLinXCtl.PyLinXProjectController as ctl
import PyLinXData.PX_ObjectHandler as PX_ObjectHandler 
#import PyLinXData.PX_ObjectHandler.PX_Recorder as PX_Recorder

class PX_Tab_Recorder_TreeView(QtGui.QTreeView):

    def __init__(self, parent=None, listItems={}, mainDrawingWidget = None):
        super(PX_Tab_Recorder_TreeView, self).__init__(parent)
        self.setIconSize(QtCore.QSize(16, 16))
        self.listItems = listItems
        self.setIndentation(0)
        self.setHeaderHidden(False)
        self.mainDrawingWidget = mainDrawingWidget
             
    def doubleClickEvent(self, modelIndex):
        print u"doubleClicked"

class NamedQStandardItem(QtGui.QStandardItem):

    def __init__(self, itemString, nameFileObject = None):
        
        super(NamedQStandardItem, self).__init__(itemString)
        self.setEditable(False)  

class treeModel_Recorder(QtGui.QStandardItemModel):
    
    backgroundBrush = QtGui.QBrush( QtGui.QColor(240, 240, 240) )
    
    def __init__(self, parent = None, listSignals = [], treeView = None, tabWidget = None):
        
        super(treeModel_Recorder, self).__init__(parent)
        self.appendColumn([])
        self.appendColumn([])
        self.__treeView = treeView
        self.__tabWidget = tabWidget

          
    def loadObjects(self, objects, listChecked = []):
     
        self.clear()
        
        objects.sort()
        for i, obj in enumerate(objects):
            modelItem =  NamedQStandardItem(obj)
            if i%2 == 1:
                modelItem.setBackground(treeModel_Recorder.backgroundBrush)
            modelItem.setCheckable(True)
            if obj in listChecked:
                modelItem.setCheckState(True)
            self.appendRow(modelItem) 

        self.__treeView.setColumnWidth(0,90)
        self.__treeView.setColumnWidth(2,90)
        
        self.setHorizontalHeaderLabels([u"Variable"])
        self.__treeView.repaint()
        
    def updateObjects(self, listChecked):
        rowCount = self.rowCount()
        for i in range(rowCount):
            item = self.item(i,0)
            var = unicode(item.text())
            if var in listChecked:
                item.setCheckState(2)
                continue
            item.setCheckState(0)
    
    def setCheckboxesEnabled(self, state):
        rowCount = self.rowCount()
        for i in range(rowCount):
            item = self.item(i,0)
            item.setEnabled(state)
        
        
#     def get_recorder_VariablesToRecord(self):
#         
#         listCheckedSignals = []
#         for i in range(self.rowCount()):
#             item = self.item(i,0)
#             if item.checkState():
#                 signal = unicode(item.text())
#                 listCheckedSignals.append(signal)
#         return listCheckedSignals 
        
    def get_recorder_VariablesToRecord(self):
        
        listCheckedSignals = []
        for i in range(self.rowCount()):
            item = self.item(i,0)
            if self.__tabWidget.recorder_RecordState == PX_ObjectHandler.PX_ObjectHandler.recorderState.logSelected:
                if item.checkState():
                    signal = unicode(item.text())
                    listCheckedSignals.append(signal)
            else:
                signal = unicode(item.text())
                listCheckedSignals.append(signal)                
        return listCheckedSignals 

        

class PX_Tab_Recorder(QtGui.QWidget):
    
    def __init__(self, mainController):
        
        super(QtGui.QWidget,self).__init__()
        self.listItems={}
        myBoxLayout = QtGui.QVBoxLayout()
        self.setLayout(myBoxLayout)
        self.toolbar = QtGui.QToolBar()
        self.mainController = mainController
        self.__objectHandler = mainController.getb(u"ObjectHandler")
        objects = self.__objectHandler.listObjects
        self.widget = PX_Tab_Recorder_TreeView(self, self.listItems)  
        self.model = treeModel_Recorder(self,objects, self.widget, self)
        #self.model = treeModel_Recorder(self,objects, self )
        self.__recorder_RecordState =  PX_ObjectHandler.PX_ObjectHandler.recorderState.off
        self.__recorder_VariablesToRecord = self.__objectHandler.get(u"recorder_VariablesToRecord")
        self.__recorder_fileFormat = self.__objectHandler.get(u"recorder_fileFormat")

        self.listItems = {}
        
        # Initialize Model
        VariablesToRecord = self.__objectHandler.listObjects
        self.model.loadObjects(VariablesToRecord)

        
        self.widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.widget.setModel(self.model)
        
        myBoxLayout.addWidget(self.toolbar)
        myBoxLayout.addWidget(self.widget)

        ## Tool-Bar

        self.toolbar.setIconSize (QtCore.QSize(16,16))
        
        # Add Action to Toolbar
        
        self.__actionRecordFull = helper.loadAction(widget=self,\
                                                    IconPath =u"./Recources/Icons/recordFull16.png",\
                                                    ToolTip=u"Record all Variables",\
                                                    ShortCut=u"Ctrl+L", \
                                                    Callback=self.recordAll, \
                                                    ToolBar=self.toolbar, \
                                                    checkable = True)
        self.__actionRecordPart = helper.loadAction(widget=self,  \
                                                    IconPath =u"./Recources/Icons/recordPart16.png", \
                                                    ToolTip=u"Record selected Variables",\
                                                    ShortCut=u"Ctrl+M", \
                                                    Callback=self.recordPart, \
                                                    ToolBar=self.toolbar, \
                                                    checkable = True)
        
        emptyWidget = QtGui.QWidget()
        emptyWidget.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        self.toolbar.addWidget(emptyWidget)
        
        
        # Selector for output file format
        self.__comboBoxFileFormat = QtGui.QComboBox()
        self.__comboBoxFileFormat.addItem(u"mdf")
        self.__comboBoxFileFormat.addItem(u"csv")
        self.__comboBoxFileFormat.setToolTip(u"Select Output FIle Format")
        self.__comboBoxFileFormat.currentIndexChanged.connect(self.__onIndexComboFileForamtChangeed)
        self.toolbar.addWidget(self.__comboBoxFileFormat)

        
        self.toolbar.setStyleSheet(u".QToolBar {border: 0px;}")
        self.SignalFileName = None
        self.repaint()
        
        
    ####################
    # Properties
    ####################
    
    def get_recorder_RecordState(self):
        return self.__recorder_RecordState

    recorder_RecordState = property(get_recorder_RecordState)


    ####################
    # Methods
    ####################

    def __onIndexComboFileForamtChangeed(self, index):
        if index == 0:
            self.__recorder_fileFormat = PX_ObjectHandler.PX_Recorder.FileFormat.mdf
        elif index == 1:
            self.__recorder_fileFormat = PX_ObjectHandler.PX_Recorder.FileFormat.csv
    
    def updateWidget(self):
        listObjects = self.__objectHandler.listObjects
        self.model.loadObjects(listObjects, self.__recorder_VariablesToRecord)

        
    def recordPart(self):
                
        if self.__actionRecordPart.isChecked():
            self.__recorder_RecordState =  PX_ObjectHandler.PX_ObjectHandler.recorderState.logSelected
        else:
            self.__recorder_RecordState =  PX_ObjectHandler.PX_ObjectHandler.recorderState.off
        self.__recorder_VariablesToRecord = self.model.get_recorder_VariablesToRecord()
        self.repaint()
    
    def recordAll(self):
        
        if self.__actionRecordFull.isChecked():
            self.__recorder_RecordState =  PX_ObjectHandler.PX_ObjectHandler.recorderState.logAll
        else:
            self.__recorder_RecordState =  PX_ObjectHandler.PX_ObjectHandler.recorderState.off
        self.__recorder_VariablesToRecord = self.model.get_recorder_VariablesToRecord()
        self.repaint()
    
    # called bevore a run is started. Get the recorder data from the GUI
    def runInit(self):
        
        command = u"@objects set recorder_RecordState " + unicode(self.__recorder_RecordState)
        self.mainController.execCommand(command)
        
        command2 = u"@objects set recorder_VariablesToRecord " + unicode(repr(self.__recorder_VariablesToRecord)\
                                                                 .replace(u" ", u""))
        self.mainController.execCommand(command2)
        
        command3 = u"@objects set recorder_fileFormat " + unicode(self.__recorder_fileFormat)
        self.mainController.execCommand(command3)

        
    
    def repaint(self):
        
        if self.__recorder_RecordState == PX_ObjectHandler.PX_ObjectHandler.recorderState.logAll: 
            self.__actionRecordFull.setChecked(True)
            self.model.setCheckboxesEnabled(False)
        else:
            self.__actionRecordFull.setChecked(False)
            self.model.setCheckboxesEnabled(True)
            
        if self.__recorder_RecordState == PX_ObjectHandler.PX_ObjectHandler.recorderState.logSelected: 
            self.__actionRecordPart.setChecked(True)
        else:
            self.__actionRecordPart.setChecked(False)
            
         
        self.model.updateObjects(self.__recorder_VariablesToRecord)
        super(PX_Tab_Recorder, self).repaint()
        
    def addListWidgetItem(self, listItemName = None):
        if listItemName == None:
            listItemName='Item '+str(len(self.listItems.keys()))        
        self.listItems[listItemName]=None 
        self.rebuildListWidget() 

    def newProject(self, mainController):
        self.mainController = mainController 
        self.__objectHandler = mainController.getb(u"ObjectHandler")

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
    
    dialog_1 = PX_Tab_Recorder(mainController)
    dialog_1.show()
    dialog_1.resize(480,320)
    sys.exit(app.exec_()) 