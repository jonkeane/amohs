##### Error classes #####

class digitError(Exception):
    pass

class jointError(Exception):
    pass


##### variables defining phonological specifications #####

digits = {"index", "middle", "ring", "pinky", "thumb"}

phonoJoints = {"ext":90, "mid":45, "flex":0}
reverseJoints = dict(reversed(item) for item in phonoJoints.items())

phonoAbduction = {"abducted":30, "adducted":0, "neg. abudcted":-15}
reverseAbduction = dict(reversed(item) for item in phonoAbduction.items())

phonoOpposition = {"opposed":90, "unopposed":0}
reverseOpposition = dict(reversed(item) for item in phonoOpposition.items())

##### checking functions that make sure values are sane

def fingerCheck(members, digits = digits):
    """Checks that members are all in the digits set"""
    # ensure that members is a set
    if members == None:
        members = set()
    elif type(members) is str:
        members = set([members])
    else:
        members = set(members)
    if not digits.issuperset(members):
        raise digitError("At least one of the members provided is not in the digits set.")
    return members

def jointCheck(joint, joints = phonoJoints):
    """Checks that joint is in the joints set"""
    if joint == None:
        joint = "ext"
    if not joint in joints:
        raise jointError("The joint provided is not in the joint set.")
    return joint

def abdCheck(abd, abds = phonoAbduction):
    """Checks that joint is in the joints set"""
    if abd == None:
        abd = "adducted"
    if not abd in abds:
        raise abductionError("The abduction provided is not in the abduction set.")
    return abd


def oppositionCheck(oppos, oppositions = phonoOpposition):
    """Checks that joint is in the joints set"""
    if oppos == None:
        oppos = "opposed"
    if not oppos in oppositions:
        raise oppositionError("The opposition provided is not in the opposition set.")
    return oppos


##### handshape class and recursion #####

class handconfiguration:
    """Representation for hand configruations"""
    def __init__(self, index, middle, ring, pinky, thumb):
        self.index = index
        self.middle = middle
        self.ring = ring
        self.pinky = pinky
        self.thumb = thumb

    def __repr__(self):
        return "handshape(index=%s, middle=%s, ring=%s, pinky=%s, thumb=%s)" % (self.index, self.middle, self.ring, self.pinky, self.thumb)

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
        return "finger(MCP=%s, PIP=%s, DIP=%s)" % (self.MCP, self.PIP, self.DIP)
    
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
        return "thumb(CM=%s, MCP=%s, IP=%s)" % (self.CM, self.MCP, self.IP)

##### abstract articulator classes #####

class joint:
    """a joint object"""
    def __init__(self, dfFlex, dfAbd=None, dfRot=None):
	    if type(dfFlex) is not int:
		    raise jointError("The value for flexion must be a single integer. Got %s instead." % (str(dfFlex)))
	    self.dfFlex = dfFlex
	    self.dfAbd = dfAbd
	    self.dfRot = dfRot

	    # Count the number of degrees of freedom that are being used to return the dfs.
	    self.df = sum([int(item != None) for item in (self.dfFlex,self.dfAbd,self.dfRot )])
	    
    def __repr__(self):
        return "joint(dfFlex='%s', dfAbd='%s', dfRot='%s')" % (self.dfFlex, self.dfAbd, self.dfRot)


##### testing #####

index = finger(MCP=(0,0), PIP=0, DIP=0)
middle = finger(MCP=(0,0), PIP=0, DIP=0)
ring = finger(MCP=(0,0), PIP=0, DIP=0)
pinky = finger(MCP=(0,0), PIP=0, DIP=0)
thumb = thumb(CM=(0,0), MCP=0, IP=0)

foo = handconfiguration(index, middle, ring, pinky, thumb)
