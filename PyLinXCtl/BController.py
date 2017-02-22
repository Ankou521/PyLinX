'''
Created on 09.08.2016

@author: Waetzold Plaum
'''
from PyQt4 import QtCore
import inspect
import copy

import PyLinXData
import PyLinXData.BContainer as BContainer 
import PyLinXData.PyLinXCoreDataObjects as PyLinXCoreDataObjects
import PyLinXData.PyLinXHelper as helper


class BController(PyLinXData.PyLinXCoreDataObjects.PX_IdObject):
    
    _dictSetCallbacks = copy.copy(PyLinXData.PyLinXCoreDataObjects.PX_IdObject._dictSetCallbacks)
    _dictGetCallbacks = copy.copy(PyLinXData.PyLinXCoreDataObjects.PX_IdObject._dictGetCallbacks)
    
    class BCommand(object):
        
        controller = None
        
        def __init__(self, commandString):
            self.__commandString = unicode(commandString) 
            self.__rawList = helper.split(self.__commandString )
            self.__context = None
            self.__bExecutable = None
            self.__listCommand = []
            self.__strCommand = u""
            self.__firstPhrase = u""
            
            self.__initialize()
            
        def __initialize(self):
            # Call order must not be changed!
            if not self.__isExecutable():
                return
            self.__determineContextAndStrCommand()             
            self.__transformStringlistToTypes() 
          
        def __isExecutable(self):
            self.__bExecutable = True
            if len(self.__rawList) == 0:
                self.__bExecutable = False
            # Comments or white space lines
            if self.__bExecutable:
                self.__firstPhrase = (self.__rawList[0]).strip()
                if self.__firstPhrase  == u"":
                    self.__bExecutable = False
                elif self.__firstPhrase[0] == u'#':
                    self.__bExecutable = False
            return self.__bExecutable
        
        # Determine target object if alias context is used
        def __determineContextAndStrCommand(self):
            if self.__firstPhrase[0] == u"@":
                if self.__firstPhrase == u"@selection":
                    self.__context = u"@selection"
                else:
                    if self.__firstPhrase in BController.BCommand.controller.dictAlias:
                        self.__context = BController.BCommand.controller.dictAlias[self.__firstPhrase]
                    else:
                        raise Exception("Error BController.BCommand.__determineContext: \"" + self.__firstPhrase  + "\" unknown Alias!")
                self.__strCommand = self.__rawList[1].strip()                    
                self.__listCommand = self.__rawList[2:]                           
            else:
                self.__strCommand = self.__rawList[0].strip()
                self.__listCommand = self.__rawList[1:]
                self.__context = BController.BCommand.controller.activeFolder
  
        # Transforming data strings to data types    
        def __transformStringlistToTypes(self):
            for i in range(0, len(self.__listCommand)):
                command_i = self.__listCommand[i]
                command_i_0 = command_i[0]
                
                #None
                if command_i == u"None":
                    self.__listCommand[i] = None
                
                # lists, sets, dicts, numeric
                elif (command_i_0 in (u"[", u"(", u"{")) or command_i.isnumeric()\
                                or (command_i   in (u"True", u"False"))\
                                or (command_i_0 == u'\"' and command_i[-1] == u'\"'):
                    self.__listCommand[i] = eval(command_i) 
                
                # other cases
                else:
                    if u"\"" in command_i:
                        command_i = command_i.replace(u"\"", u"\\\"")
                    self.__listCommand[i] = eval(u"u\"" + command_i + u"\"")
      
        def getContext(self):
            return self.__context
        
        def getListCommand(self):
            return self.__listCommand
        
        def isExecutable(self):
            return self.__bExecutable
        
        def getStrCommand(self):
            return self.__strCommand.lower()
    
    def __init__(self, root = None, mainWindow = None, bListActions = True, name = u"controller"):
        
        super(BController, self).__init__(None, name)
 
        self.__mainWindow  = mainWindow
        self.__root = root
        self.__activeFolder = None
        self.__dictAlias = BContainer.BDict({}, name = u"dictAlias")
        self.__listCommands = []
        self.paste(self.__dictAlias)
        self.set(u"LogLevel", 0)
        self.paste(BContainer.BDict({}, name="dictConstructors"))
        self._selection         = []
        BController.BCommand.controller = self
        
                
    ############
    # Properties
    ############

    def get_dictAlias(self):
        return self.__dictAlias
    
    dictAlias = property(get_dictAlias)


    def get_root(self):
        return self.__root 
        
    root = property(get_root)


    def get_activeFolder(self):
        return self.__activeFolder
    
    def set_activeFolder(self, activeFolder, options = None):
        self.__activeFolder = activeFolder
    
    activeFolder = property(get_activeFolder, set_activeFolder)
    
    def get_selection(self):
        return self._selection

    def set_selection(self, selection):
        self._selection = selection
        
    selection = property(get_selection, set_selection)    


    ###################
    # EXECUTE COMMANDS
    ###################
    
    # Execute  commands
    ####################            

    def execScript(self, script, bResetID = True):
        if bResetID: # TODO: Ownership has to be moved from PyLinXCoreDataObjects.PX_IdObject to BController
            PyLinXCoreDataObjects.PX_IdObject._PX_IdObject__ID = 0
        listScript = script.split(u"\n")
        for line in listScript:
            self.execCommand(line, color = u"darkRed")


    # Execute  command
    ####################            
            
    def execCommand(self, command, color = u"darkGray",  bConsole = False):
              
        commandObject = BController.BCommand(command)
        bLogInConsole = self.get(u"LogLevel") > 0 and not bConsole # and commandObject.isExecutable()  

        # Print Command
        if self.get(u"LogLevel") > 0 and not bConsole:
            self.__mainWindow.emit(QtCore.SIGNAL(u"ctlChanged__commandInit"),\
                                        command, \
                                        color)
        
        # Tracking of the commands
        self.__listCommands.append(command)
        
        # Execute command

        retObj = self.__execCommand(commandObject)
        if self.get(u"LogLevel") > 0:
            self.__mainWindow.emit(QtCore.SIGNAL(u"ctlChanged__commandExit"), self.activeFolder.get__path() + u"> ")
        return retObj


    # Executes specual commands 
    def __execCommand(self, commandObject):
        
        strCommand = commandObject.getStrCommand()
        listCommand = commandObject.getListCommand()
        context = commandObject.getContext()
        
        # Executing command
        if strCommand == u"set":
            return self.__execCommand_set(context, listCommand)
        elif strCommand == u"del":
            retObj = self.activeFolder.delete(listCommand)
            self.__mainWindow.emit(QtCore.SIGNAL(u"dataChanged__coreDataObjects"))
            return retObj
        elif strCommand == u"new":
            return self.__execCommand_new(context, listCommand)
        elif strCommand == u"select":
            return self.execCommand_select(listCommand)
        elif strCommand == u"cd":
            return self.__execCommand_cd(listCommand)
        elif strCommand == u"ls":
            return self.__execCommand_ls(context)
        elif strCommand == u"lsattr":
            return self.__execCommand_lsAttr(context)
        elif strCommand == u"":
            return
        else: 
            raise Exception(u"Error BController.execCommand: Unknown command \""+ strCommand +"\"")



    ####################
    # GETTER and SETTER
    ####################
    
    # mainWindow
    ############
    def get__mainWindow(self):    
        return self.__mainWindow
    _dictGetCallbacks.addCallback(u"mainWindow", get__mainWindow)
    mainWindow = property(get__mainWindow)
   
    # listCommands
    ##############
    def get__listCommands(self):
        return self.__listCommands
    _dictGetCallbacks.addCallback(u"listCommands", get__listCommands)
    listCommands = property(get__listCommands)

    # listKeys
    ##########
    def get__Selection_listKeys(self):
        return [ val.get(u"Name") for val in self._selection ]
    _dictGetCallbacks.addCallback(u"Selection_listKeys", get__Selection_listKeys)
    Selection_listKeys = property(get__Selection_listKeys)

    # Selection_types
    #################
    def get__Selection_types(self):
        setTypes = set([])
        for element in self.selection:
            types = inspect.getmro(type(element))
            setTypes = setTypes.union(set(types))
        return setTypes
    _dictGetCallbacks.addCallback(u"Selection_types", get__Selection_types)
    Selection_types = property(get__Selection_types)
    
    ####################
    # SPECIFIC COMMANDS
    ####################              

    ####################
    # Command LS
    ####################
    
    def __execCommand_ls(self, context):
        text =  context.ls(bReturn = True)
        self.__mainWindow.ui.Console.showInfoText(text, u"darkBlue")

    ####################
    # Command LS_ATTR
    ####################
    
    def __execCommand_lsAttr(self, context):
        text =  context.lsAttr(bReturn = True)
        self.__mainWindow.ui.Console.showInfoText(text, u"darkBlue")
    
    ##############
    # Command NEW
    ##############


    def __execCommand_new(self, context, listCommands):
               
        strType = listCommands[0]
        dictConstructors = self.getb("dictConstructors")
        _type = dictConstructors[strType]
        dictKWArgs = {}
        listArgs = [context]
        for command in listCommands[1:]:
            if type(command) in (unicode, str):
                if u"=" in command:
                    command = command.split(u"=")
                    dictKWArgs[command[0]] = eval(command[1])
                else:
                    listArgs.append(command)
            else:
                listArgs.append(command)
        new_object =  context.new(_type, * tuple(listArgs), **dictKWArgs)
        return new_object
    
    
    #################
    # Command SELECT
    ################# 
    
    def execCommand_select(self, command):
        
        self.selection = [self.activeFolder.getb(key) for key in command]
    
    
    ###############
    # Commande SET
    ###############
    
    def __execCommand_set(self, context, command):

        if context == u"@selection":
            return self.__execCommand_set_Selection(command)
        
        path = command[0]
        len_command = len(command)
        listPath = path.split(u".")
        len_listPath = len(listPath)
        bSubElement = (len_listPath > 1)
        if bSubElement:
            if len_listPath >1:
                attr = listPath[-1]
                pathWithoutAttribute = path[0:len(path) - len(listPath[-1]) -1]
                element = context.getObjFromPath(pathWithoutAttribute)
                retObj =  element.set(attr, command[-1])
                return retObj
        elif len_command ==2:
            return context.set(command[0], command[1])
        else:
            element = self.getObjFromPath(path)
            return  element.set(u"", command[1])
    
    # set selection
    ###############
       
    def __execCommand_set_Selection(self, command):
        bChanged = False
        for element in self.selection:
            if element.isAttr(command[0]):
                element.set(*tuple(command))
                bChanged = True
        if bChanged:
            self.__mainWindow.emit(QtCore.SIGNAL(u"dataChanged__coreDataObjects"))
                
                
    
    #############
    # Command CD
    #############

    # Method to change the active folder
    def __execCommand_cd(self, path):
        try:
            obj = self.activeFolder.getObjFromPath(path [0])
        except Exception as exp:
            errorString = u"Error PyLinXProjectController,PyLinXProjectController.cd: Failed to open " + path [0] + \
                     " - " + unicode(exp) 
            helper.error(errorString)
            return 
        if obj == None:
            errorString = u"Error PyLinXProjectController,PyLinXProjectController.cd - " + unicode(Exception) 
            helper.error(errorString)
            return
        self.activeFolder = obj
        return    
    