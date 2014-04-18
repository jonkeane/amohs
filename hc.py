##### Error classes #####

class digitError(Exception):
    pass

class jointError(Exception):
    pass

##### checking functions that make sure values are sane

##### variables defining various specifications #####

jointWeight = {"wrist": 4,
            "cm":3,
            "mcp":3,
            "pip":2,
            "dip":1}

##### handshape class and recursion #####

class armconfiguration:
    """Representation for arm configruations"""
    def __init__(self, hand, wrist):
        
    	if isinstance(wrist, joint):
    		wrist = wrist
        else:
    		if ((type(wrist) is list) or (type(wrist) is tuple)) and len(wrist) == 3:
    			wrist = joint(dfFlex=wrist[0], dfRot=wrist[1], dfPro=wrist[2])
    		else:
    			raise digitError("The wrist joint needs a list or tuple with exactly 3 degrees of freedom specified, got %s instead." % (str(wrist)))
    	if wrist.df != 3:
    		raise digitError("The wrist joint needs 3 degrees of freedom, got %s instead." % (str(wrist.df)))
    	else:
    		self.wrist = wrist
        
        self.hand = hand
    
    def __repr__(self):
        return "%s(wrist=%r, hand=%r)" % (self.__class__.__name__, self.wrist, self.hand)
    def __str__(self):
        return """armconfiguration:
wrist: %s
hand: %s
""" % (self.wrist, self.hand)
    
    def __sub__(self, other):
        if self.wrist and other.wrist: wristDiff = self.wrist - other.wrist
        if self.hand and other.hand: handDiff = self.hand - other.hand
        return armconfigurationDelta(wrist=wristDiff, hand=handDiff)

class armconfigurationDelta(armconfiguration):
    def totalDegreesDifferent(self):
        degDiff = sum([self.wrist.totalDegreesDifferent(),
                        self.hand.totalDegreesDifferent()])
        return degDiff
        
    def weightedDegreesDifferent(self):
        degDiff = sum([self.wrist.totalDegreesDifferent()*jointWeight["wrist"],
                        self.hand.weightedDegreesDifferent()])
        return degDiff

class handconfiguration:
    """Representation for hand configruations"""
    def __init__(self, index, middle, ring, pinky, thumb):
        self.index = index
        self.middle = middle
        self.ring = ring
        self.pinky = pinky
        self.thumb = thumb
    
    def __repr__(self):
        return "%s(index=%r, middle=%r, ring=%r, pinky=%r, thumb=%r)" % (self.__class__.__name__, self.index, self.middle, self.ring, self.pinky, self.thumb)
    def __str__(self):
        return """Handconfiguration:
index: %s
middle: %s
ring: %s
pinky: %s
thumb: %s""" % (self.index, self.middle, self.ring, self.pinky, self.thumb)
    
    def __sub__(self, other):
        if self.index and other.index: indexDiff = self.index - other.index
        if self.middle and other.middle: middleDiff = self.middle - other.middle
        if self.ring and other.ring: ringDiff = self.ring - other.ring
        if self.pinky and other.pinky: pinkyDiff = self.pinky - other.pinky
        if self.thumb and other.thumb: thumbDiff = self.thumb - other.thumb
        return handconfigurationDelta(index=indexDiff, middle=middleDiff, ring=ringDiff, pinky=pinkyDiff, thumb=thumbDiff)

class handconfigurationDelta(handconfiguration):
    def totalDegreesDifferent(self):
        degDiff = sum([self.index.totalDegreesDifferent(),
                        self.middle.totalDegreesDifferent(),
                        self.ring.totalDegreesDifferent(),
                        self.pinky.totalDegreesDifferent(),
                        self.thumb.totalDegreesDifferent()])
        return degDiff

    def weightedDegreesDifferent(self):
        degDiff = sum([self.index.weightedDegreesDifferent(),
                        self.middle.weightedDegreesDifferent(),
                        self.ring.weightedDegreesDifferent(),
                        self.pinky.weightedDegreesDifferent(),
                        self.thumb.weightedDegreesDifferent()])
        return degDiff    


class finger:
    """A finger"""
    def __init__(self, MCP, PIP, DIP):
        # ensure the that MCP is a joint instance, and has 2 degrees of freedom specified.
	if isinstance(MCP, joint):
		MCP = MCP
        else:
		if ((type(MCP) is list) or (type(MCP) is tuple)) and len(MCP) == 2:
			MCP = joint(dfFlex=MCP[0], dfAbd=MCP[1])
		else:
			raise digitError("The MCP joint needs a list or tuple with exactly 2 degrees of freedom specified, got %s instead." % (str(MCP)))
	if MCP.df != 2:
		raise digitError("The MCP joint needs 2 degrees of freedom, got %s instead." % (str(MCP.df)))
	else:
		self.MCP = MCP
        
        # ensure the that PIP is a joint instance, and has 1 degree of freedom specified.
	if isinstance(PIP, joint):
		PIP = PIP
        else:
		PIP = joint(PIP)
	if PIP.df != 1:
		raise digitError("The PIP joint needs 1 degree of freedom, got %s instead." % (str(PIP.df)))
	else:
		self.PIP = PIP
        
        # ensure the that DIP is a joint instance, and has 1 degree of freedom specified.
	if isinstance(DIP, joint):
		DIP = DIP
        else:
		DIP = joint(DIP)
	if DIP.df != 1:
		raise digitError("The DIP joint needs 1 degree of freedom, got %s instead." % (str(DIP.df)))
	else:
		self.DIP = DIP
    
    def __repr__(self):
        return "%s(MCP=%r, PIP=%r, DIP=%r)" % (self.__class__.__name__, self.MCP, self.PIP, self.DIP)
    def __str__(self):
        return """
  MCP: %s
  PIP: %s
  DIP: %s""" % (self.MCP, self.PIP, self.DIP)
    
    def __sub__(self, other):
        if self.MCP and other.MCP: MCPDiff = self.MCP - other.MCP
        if self.DIP and other.DIP: PIPDiff = self.PIP - other.PIP
        if self.PIP and other.PIP: DIPDiff = self.DIP - other.DIP
        return fingerDelta(MCP=MCPDiff, PIP=PIPDiff, DIP=DIPDiff)

class fingerDelta(finger):
    def totalDegreesDifferent(self):
        degDiff = sum([self.MCP.totalDegreesDifferent(),self.PIP.totalDegreesDifferent(),self.DIP.totalDegreesDifferent()])
        return degDiff

    def weightedDegreesDifferent(self):
        degDiff = sum([self.MCP.totalDegreesDifferent()*jointWeight["mcp"],self.PIP.totalDegreesDifferent()*jointWeight["pip"],self.DIP.totalDegreesDifferent()]*jointWeight["dip"])
        return degDiff

class thumb:
    """the thumb"""
    def __init__(self, CM, MCP, IP):
        # ensure the that CM is a joint instance, and has 2 degrees of freedom specified.
	if isinstance(CM, joint):
		CM = CM
        else:
		if ((type(CM) is list) or (type(CM) is tuple)) and len(CM) == 2:
			CM = joint(dfFlex=CM[0], dfAbd=CM[1])
		else:
			raise digitError("The CM joint needs a list or tuple with exactly 2 degrees of freedom specified, got %s instead." % (str(CM)))
	if CM.df != 2:
		raise digitError("The CM joint needs 2 degrees of freedom, got %s instead." % (str(CM.df)))
	else:
		self.CM = CM
        
        # ensure the that MCP is a joint instance, and has 1 degree of freedom specified.
	if isinstance(MCP, joint):
		MCP = MCP
        else:
		MCP = joint(MCP)
	if MCP.df != 1:
		raise digitError("The MCP joint needs 1 degree of freedom, got %s instead." % (str(MCP.df)))
	else:
		self.MCP = MCP
        
        # ensure the that IP is a joint instance, and has 1 degree of freedom specified.
	if isinstance(IP, joint):
		IP = IP
        else:
		IP = joint(IP)
	if IP.df != 1:
		raise digitError("The IP joint needs 1 degree of freedom, got %s instead." % (str(IP.df)))
	else:
		self.IP = IP
    
    def __repr__(self):
        return "%s(CM=%r, MCP=%r, IP=%r)" % (self.__class__.__name__, self.CM, self.MCP, self.IP)
    
    def __str__(self):
        return """
  CM: %s
  MCP: %s
  IP: %s""" % (self.CM, self.MCP, self.IP)
    
    def __sub__(self, other):
        if self.CM and other.CM: CMDiff = self.CM - other.CM
        if self.MCP and other.MCP: MCPDiff = self.MCP - other.MCP
        if self.IP and other.IP: IPDiff = self.IP - other.IP
        return thumbDelta(CM=CMDiff, MCP=MCPDiff, IP=IPDiff)

class thumbDelta(thumb):
    def totalDegreesDifferent(self):
        degDiff = sum([self.MCP.totalDegreesDifferent(),self.IP.totalDegreesDifferent(),self.CM.totalDegreesDifferent()])
        return degDiff

    def weightedDegreesDifferent(self):
        degDiff = sum([self.MCP.totalDegreesDifferent()*jointWeight["mcp"],self.IP.totalDegreesDifferent()*jointWeight["dip"],self.CM.totalDegreesDifferent()*jointWeight["cm"]])
        return degDiff


##### abstract articulator classes #####

class joint:
    """a joint object"""
    def __init__(self, dfFlex=None, dfAbd=None, dfRot=None, dfPro=None):
        if dfFlex and type(dfFlex) is not int:
		    raise jointError("The value for flexion must be a single integer. Got %s instead." % (str(dfFlex)))
        if dfAbd and type(dfAbd) is not int:
		    raise jointError("The value for abduction must be a single integer. Got %s instead." % (str(dfAbd)))
        if dfRot and type(dfRot) is not int:
		    raise jointError("The value for rotation must be a single integer. Got %s instead." % (str(dfRot)))
        if dfPro and type(dfPro) is not int:
		    raise jointError("The value for pronation must be a single integer. Got %s instead." % (str(dfPro)))
        
        self.dfFlex = dfFlex
        self.dfAbd = dfAbd
        self.dfRot = dfRot
        self.dfPro = dfPro
	    
	    # Count the number of degrees of freedom that are being used to return the dfs.
        self.df = sum([int(item != None) for item in (self.dfFlex,self.dfAbd,self.dfRot,self.dfPro )])
    
    def __sub__(self, other):
        dfFlexDiff = None
        dfAbdDiff = None
        dfRotDiff = None
        dfProDiff = None
        if self.dfFlex is not None and other.dfFlex is not None: dfFlexDiff = self.dfFlex - other.dfFlex
        if self.dfAbd is not None and other.dfAbd is not None: dfAbdDiff = self.dfAbd - other.dfAbd
        if self.dfRot is not None and other.dfRot is not None: dfRotDiff = self.dfRot - other.dfRot
        if self.dfPro is not None and other.dfPro is not None: dfProDiff = self.dfPro - other.dfPro
        return jointDelta(dfFlex=dfFlexDiff, dfAbd=dfAbdDiff, dfRot=dfRotDiff, dfPro=dfProDiff)
    
    def __repr__(self):
        return "%s(dfFlex=%r, dfAbd=%r, dfRot=%r, dfPro=%r)" % (self.__class__.__name__, self.dfFlex, self.dfAbd, self.dfRot, self.dfPro)
    def __str__(self):
        return """dfFlex: %s, dfAbd: %s, dfRot: %s, dfPro: %s""" % (self.dfFlex, self.dfAbd, self.dfRot, self.dfPro)

class jointDelta(joint):
    def totalDegreesDifferent(self):
        if self.dfFlex is None:
            dfFlexDiff = 0
        else:
            dfFlexDiff = abs(self.dfFlex)
        if self.dfAbd is None:
            dfAbdDiff = 0
        else:
            dfAbdDiff = abs(self.dfAbd)
        if self.dfRot is None:
            dfRotDiff = 0
        else:
            dfRotDiff = abs(self.dfRot)
        if self.dfPro is None:
            dfProDiff = 0
        else:
            dfProDiff = abs(self.dfPro)
        degDiff = sum([dfFlexDiff,dfAbdDiff,dfRotDiff,dfProDiff])
        return degDiff


##### testing #####

index = finger(MCP=(0,-15), PIP=0, DIP=0)
middle = finger(MCP=(30,0), PIP=90, DIP=0)
ring = finger(MCP=(0,0), PIP=0, DIP=0)
pinky = finger(MCP=(0,0), PIP=0, DIP=0)
thmb = thumb(CM=(0,0), MCP=0, IP=0)
wrist = (0,0,0)

hc1 = handconfiguration(index, middle, ring, pinky, thmb)

arm1 = armconfiguration(hc1, wrist)

index = finger(MCP=(0,0), PIP=0, DIP=0)
middle = finger(MCP=(90,0), PIP=90, DIP=0)
ring = finger(MCP=(90,0), PIP=0, DIP=0)
pinky = finger(MCP=(0,0), PIP=0, DIP=0)
thmb = thumb(CM=(0,0), MCP=0, IP=0)
wrist = (0,0,0)

hc2 = handconfiguration(index, middle, ring, pinky, thmb)

arm2 = armconfiguration(hc1, wrist)

hcDiff = hc1-hc2

armDiff = arm1-arm2

