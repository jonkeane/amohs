import hs
import funcs
import csv
from os import path

class notationError(Exception):
    pass

fingerCodingKeyFile =path.join(funcs.resources_dir,'fingerCodingKey.csv')
fingerCodingKey = funcs.read_csv_data(fingerCodingKeyFile)
fingerCodingCols = funcs.dictToCols(fingerCodingKey)
bsfingerCodingCols = funcs.dictColMapper(fingerCodingKey, "base symbol")

jointCodingKeyFile =path.join(funcs.resources_dir,'jointCodingKey.csv')
jointCodingKey = funcs.read_csv_data(jointCodingKeyFile)
jointCodingCols = funcs.dictToCols(jointCodingKey)
psfjointCodingCols = funcs.dictColMapper(jointCodingKey, "psf")
ssfjointCodingCols = funcs.dictColMapper(jointCodingKey, "ssf")
nsfjointCodingCols = funcs.dictColMapper(jointCodingKey, "nsf")

abdCodingKeyFile = path.join(funcs.resources_dir,'abdCodingKey.csv')
abdCodingKey = funcs.read_csv_data(abdCodingKeyFile)
abdCodingCols = funcs.dictToCols(abdCodingKey)
psfabdCodingCols = funcs.dictColMapper(abdCodingKey, "psf")
ssfabdCodingCols = funcs.dictColMapper(abdCodingKey, "psf") #ssf is the same as the psf for abduction.

def shortToMember(string):
    map = {'I': 'index',
           'M': 'middle',
           'R': 'ring',
           'P': 'pinky',
           'T': 'thumb'
           }
    out = [map[x] for x in list(string)]
    return out
    
##### prosodic model notation class #####
class selectedFingers:
    """a class for selected fingers based on the PM notation system in Eccarius and Brentari 2008 of the type 1T-^@;1T-@;#"""
    def __init__(self, string):
        stringList = list(string)
        
        # Selected finger symbols
        # fingers
        symbolUp = stringList.pop(0).upper()
        if symbolUp not in set(fingerCodingCols["base symbol"]):
            raise notationError("Unknown base symbol in selected fingers")
        else:
            if symbolUp != "T":
                self.fing = symbolUp
		try:
                    symbolUp = stringList.pop(0)
                except IndexError:
                    symbolUp = None
            else:
                self.fing = None
        # thumb
        if symbolUp: symbolUp = symbolUp.upper()
        if symbolUp != "T":
            self.thumb = None
        else:
            self.thumb = symbolUp
            try:
                symbolUp = stringList.pop(0)
            except IndexError:
                symbolUp = None
        # opposition
        if symbolUp != "-":
            self.oppos = None
        else:
            self.oppos = symbolUp
            try:
                symbolUp = stringList.pop(0)
            except IndexError:
                symbolUp = None
        # abduction
        if symbolUp: symbolUp = symbolUp.lower()                
        if symbolUp not in set(abdCodingCols["psf"]):
            self.abd = None
        else:
            self.abd = symbolUp
            try:
                symbolUp = stringList.pop(0)
            except IndexError:
                symbolUp = None
        # joint
        if symbolUp: symbolUp = symbolUp.lower()                
        if symbolUp not in set(jointCodingCols["psf"]):
            if symbolUp == None:
                self.joint = None
            else:
                raise notationError("Unknown joint symbol in selected fingers")
        else:
            self.joint = symbolUp
        # test to ensure there's no string left.
        if len(stringList) > 0:
            raise notationError("There's still unparsed string left in the selected finger substring.")

class secondarySelectedFingers:
    """a class for secondary selected fingers based on the PM notation system in Eccarius and Brentari 2008 of the type 1T-^@;1T-@;#"""
    def __init__(self, string):
        stringList = list(string)
        # Secondary selected finger symbols
        # fingers
        symbolUp = stringList.pop(0).upper()
        if symbolUp not in set(fingerCodingCols["base symbol"]):
            raise notationError("Unknown base symbol in selected fingers")
        else:
            if symbolUp != "T":
                self.fing = symbolUp
		try:
                    symbolUp = stringList.pop(0)
                except IndexError:
                    symbolUp = None
            else:
                self.fing = None
        # thumb
        if symbolUp: symbolUp = symbolUp.upper()                
        if symbolUp != "T":
            self.thumb = None
        else:
            self.thumb = symbolUp
            try:
                symbolUp = stringList.pop(0)
            except IndexError:
                symbolUp = None
        # opposition
        if symbolUp != "-":
            self.oppos = None
        else:
            self.oppos = symbolUp
            try:
                symbolUp = stringList.pop(0)
            except IndexError:
                symbolUp = None
        # abduction doesn't exist in PM notation for secondary selected fingers, but should be and is accounted for here.
        if symbolUp: symbolUp = symbolUp.lower()                
        if symbolUp not in set(abdCodingCols["psf"]):
            self.abd = None
        else:
            self.abd = symbolUp
            try:
                symbolUp = stringList.pop(0)
            except IndexError:
                symbolUp = None
        # joint
        if symbolUp: symbolUp = symbolUp.lower()                
        if symbolUp not in set(jointCodingCols["psf"]):
            if symbolUp == None:
                self.joint = None
            else:
                raise notationError("Unknown joint symbol in secondary selected fingers")
        else:
            self.joint = symbolUp
        # test to ensure there's no string left.
        if len(stringList) > 0:
            raise notationError("There's still unparsed string left in the secondary selected finger substring.")

class nonSelectedFingers:
    """a class for non selected fingers based on the PM notation system in Eccarius and Brentari 2008 of the type 1T-^@;1T-@;#"""
    def __init__(self, string):
        stringList = list(string)
        # joint
        symbolUp = stringList.pop(0)
        if symbolUp not in set(jointCodingCols["nsf"]):
            if symbolUp is None:
                self.joint = None
            else:
                raise notationError("Unknown joint symbol in nonselected fingers")
        else:
            self.joint = symbolUp
        # test to ensure there's no string left.
        if len(stringList) > 0:
            raise notationError("There's still unparsed string left in the nonselected finger substring.")

class pmHandshape:
    """a class based on the PM notation system in Eccarius and Brentari 2008 of the type 1T-^@;1T-@;#"""
    def __init__(self, string):
        strings = string.split(";")
        self.SF = selectedFingers(strings.pop(0))
        try:
            stringUp = strings.pop(0)
            if stringUp in set(jointCodingCols["nsf"]):
                self.SSF = None
                self.NSF = nonSelectedFingers(stringUp)
            else:
                self.SSF = secondarySelectedFingers(stringUp)
                try:
                    stringUp = strings.pop(0)
                    self.NSF = nonSelectedFingers(stringUp)
                except IndexError:
                    self.NSF = None
        except IndexError:
            self.SSF = None
            self.NSF = None
        if len(strings) > 0:
            raise notationError("There's still unparsed string left: "+str(strings))
            
    def toAMhandshape(self):
        # set default value for the thumb: opposed
        oppos = "opposed"
        # translate the selected fingers        
        if self.SF.fing:
            sfMem = shortToMember(bsfingerCodingCols[self.SF.fing]['fingers'])
        if self.SF.thumb and self.SF.thumb == "T" :
            try:
                sfMem.append("thumb")
            except UnboundLocalError:
                sfMem = ["thumb"]            
        if self.SF.oppos and self.SF.oppos == "-":
            oppos = "unopposed"
        else:
            oppos = "opposed"
        if self.SF.abd:
            sfAbd = psfabdCodingCols[self.SF.abd]['abd']
        else:
            sfAbd = None
        if self.SF.joint:
            sfMCP = psfjointCodingCols[self.SF.joint]['MCP']
            sfPIP = psfjointCodingCols[self.SF.joint]['PIP']
        else:
            sfMCP = psfjointCodingCols['empty']['MCP']
            sfPIP = psfjointCodingCols['empty']['PIP']
        sf =  hs.selectedFingers(members = sfMem, MCP=sfMCP, PIP=sfPIP, abd=sfAbd)
        # translate the secondary selected fingers
        if self.SSF:
            if self.SSF.fing:
                ssfMem = shortToMember(bsfingerCodingCols[self.SSF.fing]['fingers'])
            if self.SSF.thumb and self.SSF.thumb == "T" :
                try:
                    ssfMem.append("thumb")
                except UnboundLocalError:
                    ssfMem = ["thumb"]
            if self.SSF.oppos and self.SSF.oppos == "-":
                oppos = "unopposed"
            else:
                oppos = "opposed"
            if self.SSF.abd:
                ssfAbd = ssfabdCodingCols[self.SSF.abd]['abd']
            else:
                ssfAbd = None
            if self.SSF.joint:
                ssfMCP = ssfjointCodingCols[self.SSF.joint]['MCP']
                ssfPIP = ssfjointCodingCols[self.SSF.joint]['PIP']
            else:
                ssfMCP = ssfjointCodingCols['empty']['MCP']
                ssfPIP = ssfjointCodingCols['empty']['PIP']
            ssf = hs.secondarySelectedFingers(members = ssfMem, MCP=ssfMCP, PIP=ssfPIP, abd=ssfAbd)
        else:
            ssf = None
        # translate the nonselected fingers
        if self.NSF:
            if self.NSF.joint:
                ssfJoints = nsfjointCodingCols[self.NSF.joint]['MCP']
            else:
                ssfJoints = None
            nsf = hs.nonSelectedFingers(joints=ssfJoints)
        else:
            nsf = None
        thumb = hs.thumb(oppos=oppos)
        AMhandshape = hs.handshape(selectedFingers = sf, secondarySelectedFingers = ssf, thumb = thumb, nonSelectedFingers = nsf )
        return AMhandshape

##### test #####
foo = pmHandshape("1;#")
bar = foo.toAMhandshape()
baz = bar.toHandconfigTarget()

foo1 = pmHandshape("DT@;/")
bar1 = foo1.toAMhandshape()

baz1 = bar1.toHandconfigTarget()
