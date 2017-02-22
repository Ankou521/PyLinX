'''
Created on 11.02.2016

@author: Waetzold Plaum
'''

from PyQt4 import QtGui
import sys

import PyLinXGui.PX_Tab_Recorder as PX_Tab_Recorder
import PyLinXGui.PX_Tab_SignalSelect as PX_Tab_SignalSelect
import PyLinXGui.PX_Tab_ObjectHandlerList as PX_Tab_ObjectHandlerList
import PyLinXGui.PX_CommandConsole as PX_CommandConsole

class PX_TabWidget_main(QtGui.QTabWidget):
    
    class DisplayRole:
        # DisplayRoles:
        onlyInEditMode          = 0
        onlyInSimulationMode    = 1
        inEditAndSimulationMode = 2
        
    
    def __init__(self, parent = None, mainController = None, TabPosition = QtGui.QTabWidget.East):
        
        super(PX_TabWidget_main, self).__init__(parent)
        
        self.__dictWidgets = {}
        self.__projectController = mainController
        self.setTabPosition(TabPosition)
        self.setWindowTitle('PyQt QTabWidget Add self and Widgets Inside Tab')

    def newProject(self, mainController):
        self.__projectController = mainController
        for strTitle in self.__dictWidgets:
            _tuple = self.__dictWidgets[strTitle]
            widget = _tuple[0]
            if type(widget) in (PX_Tab_Recorder.PX_Tab_Recorder,\
                          PX_Tab_ObjectHandlerList.PX_Tab_ObjectHandlerList,\
                          PX_Tab_SignalSelect.PX_Tab_SignalSelect,\
                          PX_CommandConsole.PX_CommandConsole):
                widget.newProject(mainController)
    
    def adjoinTab(self, widget, strTitle, displayRole, priority = 0):
        
        # priority: 1 is the highest priority, 0 is the lowest
        
        if strTitle not in self.__dictWidgets:
            self.__dictWidgets[strTitle] = (widget, displayRole, priority)
            return True
        else:
            return False
        
    def updateTabs(self):
        
        def decideAddTab(bSimulationMode, displayRole):
            return     (bSimulationMode and displayRole in (PX_TabWidget_main.DisplayRole.onlyInSimulationMode,\
                            PX_TabWidget_main.DisplayRole.inEditAndSimulationMode)) or\
                  ((not bSimulationMode) and displayRole in (PX_TabWidget_main.DisplayRole.onlyInEditMode,\
                            PX_TabWidget_main.DisplayRole.inEditAndSimulationMode))                                           
        
        self.clear()
        
        bSimulationMode = self.__projectController.bSimulationMode
        
        maxPriority = self.getMaxPriority()
        listSortedTabs = (maxPriority + 1) * [[None]]
        for strTitle in self.__dictWidgets:
            _tuple = self.__dictWidgets[strTitle]
            listSortedTabs[_tuple[2]].append((_tuple[0], _tuple[1], strTitle))
            widget = _tuple[0]
            if type(widget) == PX_Tab_Recorder.PX_Tab_Recorder:
                widget.updateWidget()
        for i in range(1, maxPriority + 1):
            listSortedTabs_i = listSortedTabs[i]
            for j in range(len(listSortedTabs_i)):
                listSortedTabs_i_j = listSortedTabs_i[j]
                if listSortedTabs_i_j == None:
                    continue
                listSortedTabs_i_j_1  = listSortedTabs_i_j [1]
                if decideAddTab(bSimulationMode, listSortedTabs_i_j_1):                                           
                    self.addTab(listSortedTabs_i_j[0], listSortedTabs_i_j[2])
        listSortedTabs_0 = listSortedTabs[0]
        for j in range(len(listSortedTabs_0)):
            listSortedTabs_0_j = listSortedTabs_0[j]
            if decideAddTab(bSimulationMode, listSortedTabs_0_j):  
                self.addTab(listSortedTabs_0_j[0], listSortedTabs_0_j[2])

    def getMaxPriority(self):
        maxPriority = 0
        for strTitle in self.__dictWidgets:
            _tuple = self.__dictWidgets[strTitle]
            priority = _tuple[2]
            if priority > maxPriority:
                maxPriority = priority
        return maxPriority



if __name__ == '__main__':
    
    app     = QtGui.QApplication(sys.argv)
    tabs    = PX_TabWidget_main()
    tab1 = QtGui.QWidget()
    tabs.addTab(tab1, "test")
    tabs.show()
    sys.exit(app.exec_())
