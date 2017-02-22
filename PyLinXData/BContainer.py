'''
Created on 15.09.2014

@author: Waetzold Plaum

'''

## @package BContainer
# This module contains the core data objekt "BContainer" and directly derived standard classes. They are aimed to build  
# transparent tree structures


import copy
import inspect
from PyQt4 import QtCore


# helper Class for the callback functions for the set and get methods
######################################################################

class dictCallbacks(dict):
    
    def __init__(self, * args, **kwargs):
        super(dictCallbacks, self).__init__(*args, **kwargs)
        
    def addCallback(self, attr, callback):
        self[attr] = callback


## Base class of the B object modell

class BContainer(object):

    #########################################
    # Dictionary for the set-callback methods
    #########################################
    
    _dictSetCallbacks = dictCallbacks({})
    _dictGetCallbacks = dictCallbacks({})
    
    ##############
    ## Constructor
    ##############
    
    def __init__(self, name = u"<no Name>", parent = None, headObject = None):
        
        
        # Attention: There are twoe versions von _dictGetCallbacks and _dictSetCallbacks
        # One that holds the static Callbacks and one that holds the object specific callbacks! 
        self._dictGetCallbacks = dictCallbacks({})
        self._dictGetCallbacks = dictCallbacks({})
        
        # Element for saving the main or global information ot the knot
        self.__Head = headObject
        # Dict of Elements indexed by "name"
        self.__Body = {}
        # reference to the root knot
        #self.__parent = parent

        self.__Attributes                 = {} 
        self.__Attributes[u"Type"]        = 0
        self.__Attributes[u"Name"]        = name
        self.__Attributes[u"DisplayName"] = name
        self.__parent = None
        if parent != None:
            parent.paste(self)        
       
    ## print method
    
    def __str__(self):
        print u"================================="
        print list.__str__(self)
        print u"---------------------------------"
        self.lsAttr()
        print u"---------------------------------"
        self.ls()
        print u"================================="
        return ""
    
    
    ## Method to get the attribute of an element uniquely identificied by the value of another attribute
    
    def call(self, attributeKey, value, attrubuteReturn = None):
        
        listElements = self.getbCond(attributeKey, value, attrubuteReturn)
        if len(listElements) != 1:
            raise Exception("Fatal Error BContainer.call: inconsistent IDs!")
        return listElements[0]
    
    ## Method for deleting BContainers
    
    def delete(self, name = None):
        
        if name in self.__Body:
            obj = self.__Body.pop(name)
            keys = obj.__Body.keys()
            for childKey in keys:
                obj.delete(childKey)
            del obj
        elif name == None:
            keys = self.__Body.keys()
            for childKey in keys:
                self.delete(childKey)
            

    #################
    ## GET-Methods ##
    #################
            
    def get(self, attr, bComplex = False):
        if attr in type(self)._dictGetCallbacks:
            return type(self)._dictGetCallbacks[attr](self)
        elif attr in self._dictGetCallbacks:
            return self._dictGetCallbacks[attr]()
        else:
            if bComplex:
                return self.__get_complex(attr)
            elif u"." in attr:
                listAttr = attr.split(u".")
                obj = self.getRoot().getObjFromPath(listAttr[0])
                return obj.get(listAttr[1])
            else:
                return self.__Attributes[attr]
        
            
    def __get_complex(self, attr):
        types = inspect.getmro(type(attr))
        if dict in types:
            dictReturn = {}
            for key in attr:
                len_key = len(key)
                if len_key > 0:
                    if key[0] == u"@":
                        childObj = self.getb(key[1:])
                        getDict = attr[key]
                        childObjReturn = childObj.__get_complex(getDict)
                        dictReturn[key] = childObjReturn
                    else:
                        objReturn = self.get(key)
                        dictReturn [key] = objReturn
                else:
                    raise Exception(u"Error BContainer.__get_complex: key of length 0.")
            return dictReturn
        else:
            raise Exception("Error BContainer.get: No valid type for collective set. Use dict!")        
    
    def get__path(self):
        return self.__get__path()
    _dictGetCallbacks.addCallback(u"path", get__path)
    path = property(get__path)
    
    def __get__path(self, path = u""):
        #print "__get__path", path
        if self.__parent == None:
            return u"/" + path
        else:
            try:
                return self.__parent.__get__path( self.__parent.key(self) + u"/" +  path)
            except:
                print u"Error!"
                print u"self.__parent", self.__parent
                print u"path", path

    ###############
    # SET-METHODE
    ###############
    
    ##  Method to add or set an attribute
    
    def set(self,  attr, setObj, options = None):
        
        _type = type(self)
        if attr in _type._dictSetCallbacks:
            _type._dictSetCallbacks[attr](self,setObj, options)
        elif attr in self._dictSetCallbacks:
            self._dictSetCallbacks[attr](setObj, options)            
        else:
            if attr in _type._dictGetCallbacks:
                raise Exception(u"BContainer.set: Attribute " + attr + u" is write-protected! Please implement a set-method to write this \
                attribute or remove the get-method to remove write-protection!" )
            # None or empty string as attribute indicates complex set command with a whole dict to be set.
            elif attr == None or attr == u"": 
                types = inspect.getmro(type(setObj))
                if dict in types:
                    return self.__set_dict(setObj, options)
                else:
                    raise Exception("Error BContainer.set: No valid type for collective set. Use dict!")
            elif options == None: 
                self.__Attributes[attr] = setObj
                if attr == u"listPoints":
                    print self.__Attributes
            elif options == u"-p":
                val = self.get(attr)
                types = inspect.getmro(type(val))
                if (float in types) or (int in types):
                    self.set(attr,  val + setObj)
                elif tuple in types:
                    self.set(attr, tuple([a + b for a, b in zip(val, setObj ) ] ) )
                elif list in types:
                    self.set(attr, [a + b for a, b in zip(val, setObj ) ] )
                
    def __set_dict(self, setObj, options):
        for key in setObj:
            len_key = len(key)
            if len_key > 0:
                if key[0] == u"@":
                    childObj = self.getb(key[1:])
                    setObjChild = setObj[key]
                    childObj.__set_dict(setObjChild, options)
                else:
                    self.set(key, setObj[key], options)
            else:
                raise Exception(u"Error BContainer.__set_dict: key of length 0.")    

        
    def getb(self,name):
        if name in self.__Body:
            return self.__Body.get(name)
        else:
            self.ls()
            raise Exception(u"Error BContainer.getb: Element \"" + name +"\" in " + unicode(type(self)) + u" does not exist.")
    
    def getbCond(self, attrib, value, returnAttribute = None):
        listChilds = []
        for key in self.__Body:
            element = self.__Body[key]
            if element.isAttr(attrib):
                if element.get(attrib) == value:
                    if returnAttribute == None:
                        listChilds.append(element)
                    else:
                        listChilds.append(element.get(returnAttribute))
        return listChilds
        
        
    ## Method that gets the head of a container
     
    def geth(self):
        return self.__Head
    
    ## Method that returns the parent element
    
    def getParent(self):
        return self.__parent
    
    def getRoot(self, _type = None):
        if _type == None:
            if self.__parent == None:
                return self
            else:
                return self.__parent.getRoot()
        else:
            types = inspect.getmro(type(self))
            if _type in types:
                return self
            else:
                if self.__parent == None:
                    return self
                else:
                    return self.__parent.getRoot(_type) 
    
    ## Method that returns True if the attribute exists
    
    def isAttr(self, attr):
        return (attr in self.__Attributes) or (attr in self._dictGetCallbacks) or (attr in type(self)._dictGetCallbacks)
    
    ## Method that returns true, if an attribute exists and has the value "True", otherwise it returns "False" 

    def isAttrTrue(self, attr):      
        if self.isAttr(attr):
            return self.get(attr) == True
        else:
            return False
        
    ## Method that determines if there exists an element for a certain key
    
    def isInBody(self, key):
        return key in self.__Body  
    
    ## Method that gets all attributes
    
    def getAttrs(self):
        return self.__Attributes.keys()
     
    ## Method that gets all keys of the child elements
    
    def getChildKeys(self):
        return self.__Body.keys()
    
    ## Method for getting all childs 
    
    def getChilds(self):
        return [self.__Body[key] for key in self.__Body]
    
    ## gets key of an objekt in Body
    def key(self, obj):
        for key in self.__Body:
            objComp = self.__Body[key]
            if objComp == obj:
                return key  
        return None
            
    def ls(self,  bReturn = False):
        listLs = []
        for key in self.__Body:
            elem = self.getb(key)
            listLs.append((unicode(elem.get("Name")), unicode(type(elem))))
        if len(listLs) > 0:
            return self.__printLsList(sorted(listLs), bReturn)
        
    def lsAttr(self,  bReturn = False):
        listLsAttr = []
        _type = type(self)
        for attr in self.__Attributes:
            listLsAttr.append( (unicode(attr), u"-",  unicode(self.__Attributes[attr]) ) )            
        for attr in self._dictGetCallbacks:
            listLsAttr.append( (unicode(attr), u"v",  unicode(self.get(attr)) ) )      
        for attr in _type._dictGetCallbacks:
            listLsAttr.append( (unicode(attr), u"v",  unicode(self.get(attr)) ) )
        for i, line in enumerate(listLsAttr):
            line_0 = line[0]
            line_1 = line[1]
            if    ( (line_0 in  self._dictGetCallbacks) and not (line_0 in  self._dictSetCallbacks) ) or\
                  ( (line_0 in _type._dictGetCallbacks) and not (line_0 in _type._dictSetCallbacks) ):
                line_1 += 'r'
            else:
                line_1 += 'w'
            listLsAttr[i] = (line[0], line_1, line[2])
        if len(listLsAttr) > 0:
            return self.__printLsList(sorted(listLsAttr), bReturn)            
          
    def __printLsList(self, lsList, bReturn = False):
        len_lsList = len(lsList)
        if len_lsList == 0:
            return
        else:
            len_lsList_0 = len(lsList[0])
            if len_lsList_0 == 0:
                return
        len_cell = []
        max_len_cell = []
        unicode_key = []
        unicode_whitespace = []
        for i in range(len_lsList_0):
            if i < len_lsList_0 - 1:
                len_cell.append([])
                unicode_key.append([])
                unicode_whitespace.append([])
                len_cell[i] = [ len(row[i]) for row in lsList ]
                max_len_cell.append(max(len_cell[i]))
            else:
                len_cell.append([])
                len_cell[i] = [ 0 ] * len(lsList)
                max_len_cell.append(0)
        ustrPrint = u""
        for i in range(len_lsList):
            for j in range(len(lsList[i])):
                ustrPrint += lsList[i][j]
                ustrPrint += u" " * (max_len_cell[j] - len_cell[j][i] + 1)
            #if i < len_lsList - 1:
            ustrPrint += u"\n"
        if bReturn == False:
            print ustrPrint + u"\n"
        else:
            return ustrPrint
            

    # moves an element
    
    def mv(self, path0, path1):
               
        if type(path0) in (str, unicode):
            objSource       = self.getObjFromPath(path0)
        else:
            objSource       = path0
        parentSource    = objSource.getParent()
        parentSource.__Body.pop(parentSource.key(objSource))
        if type(path1) in (str, unicode):
            parentTarget    = self.getObjFromPath(path1)
        else:
            parentTarget = path1
        parentTarget.paste(objSource)

    
    def getObjFromPath(self,path):
        
        #bFolder = False 
        if not ( type(path)  in (list, QtCore.QStringList)):
            path = str(path).split(u"/")
            if type(path) == QtCore.QStringList:
                path = list(path)
            if path[-1] == u"":
                path.pop(-1)
                #bFolder = True
        
        len_path = len(path)   
         
        if len_path == 0:
            return self
        
        path_0 = path[0]
        
        if path_0 == u"..":
            if self.__parent != None:
                return self.__parent.getObjFromPath(path[1:])
            else:
                raise Exception("Error BContainer.getObjFromPath: Syntax Error 1")
        elif path_0 == u"":
            root = self.getRoot()
            if root != None:
                return root.getObjFromPath(path[1:])
            else:
                raise Exception("Error BContainer.getObjFromPath: Syntax Error 2")
        elif path_0 == u"." and len_path > 1:
            return self.getObjFromPath(path[1:])
        else:
            if len_path == 1:
                path = path[0].split(u".")
                if len(path) > 1:
                    path = ".".join(path[0:-1])
                else:
                    path = path[0]
                if path == self.get("Name"):
                    return self                
                try:
                    obj = self.getb(path)
                except Exception as exc:
                    print "Error BContainer.getObjFromPath"
                    print "path: ", path , "len(path)", len(path)
                    print "self.ls():" , self.ls()
                    print str(exc)
                return obj
            else:
                #TODO Chance hasByID mechanism. Hash by unicoe(ID)
                # so far a quick and dirty workaround
                obj = self.getb(path[0])
                return obj.getObjFromPath(path[1:]) 
    
    # function creating a new object and pasting it to the parent knot
    
    def new(self, _type, *args, **kwargs):
        newObject = _type(*args , **kwargs)
        return newObject

    ## This method pastes an object into another one.
                
    def paste(self, obj, name = None, bForceOverwrite = False, pathkey = None):
        
        
        types = inspect.getmro(type(obj))
            
        if BContainer in types: 
            key = obj.get(u"Name")
        else:
            if name == None: 
                raise Exception(u"Error BContainer.py: No key for paste-function!")
            else:
                key = name
        
        if key in self.__Body.keys():
            if bForceOverwrite:
                self.__Body[key] = obj
                obj.__parent = self                
            else:
                raise Exception(u"Key already in use. Set bForceOverwrite=True to enforce overwriting!")        
        else:
            self.__Body[key] = obj
            if(BContainer in types):
                obj.__parent = self
    
    def recur(self, typeinfo, strFunction, tupleArgs, bSubTypes = False):
            
        if bSubTypes:
            types = inspect.getmro(type(self))
        else:
            types = [type(self)]
        bCallFunction = (typeinfo in types)

        if bCallFunction:
            if len(tupleArgs) > 0:
                strExec = u"self." + strFunction + u"(" + u"*tupleArgs" + u")"
            else:
                strExec = u"self." + strFunction + u"()"
            exec(strExec)
                
        for key in self.__Body:
            element = self.__Body[key]
            element.recur(typeinfo, strFunction, tupleArgs, bSubTypes)


                    
        
class BList(BContainer, list):
    
    _dictSetCallbacks = copy.copy(BContainer._dictSetCallbacks)
    _dictGetCallbacks = copy.copy(BContainer._dictGetCallbacks)
    
    def __init__(self, *args, **kwargs):
        
        list.__init__(self, *args)
        BContainer.__init__(self, **kwargs)
        


class BDict(BContainer, dict):
    
    _dictSetCallbacks = copy.copy(BContainer._dictSetCallbacks)
    _dictGetCallbacks = copy.copy(BContainer._dictGetCallbacks)
    
    def __init__(self, *args, **kwargs):
        
        dict.__init__(self, *args)
        BContainer.__init__(self, **kwargs)

