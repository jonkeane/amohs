import hc

##### Error classes #####
class digitError(Exception):
    pass

class jointError(Exception):
    pass

class abductionError(Exception):
    pass

class oppositionError(Exception):
    pass


##### variables defining phonological specifications #####

digits = {"index", "middle", "ring", "pinky", "thumb"}

phonoJoints = {"ext":180, "midExt":150, "mid":135, "midFlex":120, "flex":90}
reverseJoints = dict(reversed(item) for item in phonoJoints.items())

phonoAbduction = {"abducted":30, "neutralAbducted":15, "adducted":0, "negativeAbducted":-15}
reverseAbduction = dict(reversed(item) for item in phonoAbduction.items())

phonoThumbAbduction = {"abducted":90, "neutralAbducted":45, "adducted":0, "negativeAbducted":-45}
reverseAbduction = dict(reversed(item) for item in phonoThumbAbduction.items())

phonoOpposition = {"opposed":90, "unopposed":0}
reverseOpposition = dict(reversed(item) for item in phonoOpposition.items())

phonoOrientations = {"default": (0,0,180), "defaultFS":(-10,0,180), "palmIn":(30,5,0), "palmDown":(30,0,180)}
reverseOrientations = dict(reversed(item) for item in phonoOrientations.items())
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
    """Checks that abduction is in the abductoin set"""
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

class arm:
    """Representation of wrist+handshape, to be expanded with elbow and shoulder later"""
    def __init__(self, handshape, orientation=None):
        self.handshape = handshape
        if orientation == None:
            self.orientation = "default"
        else:
            self.orientation = orientation
        
    def toArmTarget(self):
        wrist = hc.joint(dfFlex=phonoOrientations[self.orientation][0], dfRot=phonoOrientations[self.orientation][1], dfPro=phonoOrientations[self.orientation][2])
        return hc.armconfiguration(hand=self.handshape.toHandconfigTarget() , wrist=wrist)


class handshape:
    """Representation of handshapes using the articulatory model of handshape"""
    def __init__(self, selectedFingers, secondarySelectedFingers, thumb, nonSelectedFingers):
        self.SF = selectedFingers
        self.SSF = secondarySelectedFingers
        self.thumb = thumb
        if self.SSF and not self.SF.members.isdisjoint(self.SSF.members):
            raise digitError("The members of selected and secodnary selected finger groups overlap.")            
        self.NSF =  nonSelectedFingers
        if self.NSF and self.SSF:
            self.NSF.members = digits - (self.SF.members | self.SSF.members)
        elif self.NSF:
            self.NSF.members = digits - (self.SF.members)

        #make SSF and NSF None if there are no members
        if self.SSF and len(self.SSF.members) == 0:
            self.SSF.members = None
        if self.NSF and len(self.NSF.members) == 0:
            self.NSF.members = None

    def toHandconfigTarget(self):
        handconfig = {
        "index" : None,
        "middle" : None,
        "ring" : None,
        "pinky" : None,
        "thumb" : None
        }
        
        for finger in self.SF.members:
            if finger !=  "thumb":
                handconfig[finger] = hc.finger(
                    MCP=hc.joint(dfFlex=phonoJoints[self.SF.MCP.value],
                             dfAbd=phonoAbduction[self.SF.abd.value]),
                    PIP=hc.joint(dfFlex=phonoJoints[self.SF.PIP.value]),
                    DIP=hc.joint(dfFlex=phonoJoints[self.SF.PIP.value])
                    )
            else:
                handconfig[finger] = hc.thumb(
                    MCP=hc.joint(dfFlex=phonoJoints[self.SF.PIP.value]),
                    IP=hc.joint(dfFlex=phonoJoints[self.SF.PIP.value]),
                    CM=hc.joint(dfFlex=None,dfAbd=phonoThumbAbduction[self.SF.abd.value],dfRot=phonoOpposition[self.thumb.oppos.value])
                    )                
        if self.SSF is not None:
            for finger in self.SSF.members:
                if finger !=  "thumb":
                    handconfig[finger] = hc.finger(
                        MCP=hc.joint(dfFlex=phonoJoints[self.SSF.MCP.value],
                             dfAbd=phonoAbduction[self.SSF.abd.value]),
                    	PIP=hc.joint(dfFlex=phonoJoints[self.SSF.PIP.value]),
                    	DIP=hc.joint(dfFlex=phonoJoints[self.SSF.PIP.value])
                    	)
            	else:	
                	handconfig[finger] = hc.thumb(
                    	MCP=hc.joint(dfFlex=phonoJoints[self.SSF.PIP.value]),
                    	IP=hc.joint(dfFlex=phonoJoints[self.SSF.PIP.value]),
                    	CM=hc.joint(dfFlex=None,dfAbd=phonoThumbAbduction[self.SSF.abd.value],
							dfRot=phonoOpposition[self.thumb.oppos.value])
                    	)  

        if self.NSF is not None:
            for finger in self.NSF.members:
                if self.NSF.joints.value == "ext":
                    NSFAbd = "neutralAbducted"
                else:
                    NSFAbd = "adducted"
                if finger !=  "thumb":
                    handconfig[finger] = hc.finger(
                        MCP=hc.joint(dfFlex=phonoJoints[self.NSF.joints.value],
                             dfAbd=phonoAbduction[NSFAbd]),
                        PIP=hc.joint(dfFlex=phonoJoints[self.NSF.joints.value]),
                        DIP=hc.joint(dfFlex=phonoJoints[self.NSF.joints.value])
                        )
                else:
                    handconfig[finger] = hc.thumb(
                        MCP=hc.joint(dfFlex=phonoJoints[self.NSF.joints.value]),
                        IP=hc.joint(dfFlex=phonoJoints[self.NSF.joints.value]),
                        CM=hc.joint(dfFlex=None,dfAbd=phonoThumbAbduction[NSFAbd],
							dfRot=phonoOpposition["unopposed"])
                        )
        # Check!
        return  hc.handconfiguration(handconfig["index"], handconfig["middle"], handconfig["ring"], handconfig["pinky"], handconfig["thumb"] )
        
    def __repr__(self):
        return "%s(selectedFingers=%r, secondarySelectedFingers=%r, thumb=%r, nonSelectedFingers=%r)" % (self.__class__.__name__, self.SF, self.SSF, self.thumb, self.NSF)
    def __str__(self):
        return """Handshape:
Selected Fingers: %s
Secondary Selected Fingers: %s
Thumb: %s
Non Selected Fingers: %s
""" % (self.SF, self.SSF, self.thumb, self.NSF)

class selectedFingers:
    """The selected fingers"""
    def __init__(self, members, MCP, PIP, abd):
        # check the members
        try:
            members = fingerCheck(members)
        except digitError:
            print("Selected finger digit error.")
            raise
        self.members = members

        # ensure the that MCP is a joint instance
        if isinstance(MCP, joint):
            self.MCP = MCP
        else:
            self.MCP = joint(MCP)
            
        # ensure the that PIP is a joint instance            
        if isinstance(PIP, joint):
            self.PIP = PIP
        else:
            self.PIP = joint(PIP)

        # duplicate the PIP configuration
        self.DIP = self.PIP # how to compute?

        if isinstance(abd, abduction):
            self.abd = abd
        else:
            self.abd = abduction(abd)

    def __repr__(self):
        return "%s(members=%r, MCP=%r, PIP=%r, abd=%r)" % (self.__class__.__name__, self.members, self.MCP, self.PIP, self.abd)
    def __str__(self):
        return """
  members: %s
  MCP: %s
  PIP: %s
  abd: %s""" % (self.members, self.MCP, self.PIP, self.abd)
    
class secondarySelectedFingers:
    """The secondary selected fingers"""
    def __init__(self, members=None, MCP=None, PIP=None, abd=None):
        # check the members
        try:
            members = fingerCheck(members)
        except digitError:
            print("Selected finger digit error.")
            raise
        self.members = members

        # ensure the that MCP is a joint instance
        if isinstance(MCP, joint):
            self.MCP = MCP
        else:
            self.MCP = joint(MCP)
            
        # ensure the that PIP is a joint instance            
        if isinstance(PIP, joint):
            self.PIP = PIP
        else:
            self.PIP = joint(PIP)

        # duplicate the PIP configuration
        self.DIP = self.PIP # how to compute?

        if isinstance(abd, abduction):
            self.abd = abd
        else:
            self.abd = abduction(abd)

        # if members is empty, set all to None:
        if len(members) == 0:
            self.MCP = None
            self.PIP = None
            self.abd = None
            
    def __repr__(self):
        return "%s(members=%r, MCP=%r, PIP=%r, abd=%r)" % (self.__class__.__name__, self.members, self.MCP, self.PIP, self.abd)
    def __str__(self):
        return """
  members: %s
  MCP: %s
  PIP: %s
  abd: %s
""" % (self.members, self.MCP, self.PIP, self.abd)
    
class thumb:
    """the thumb"""
    def __init__(self, oppos=None):
        if isinstance(oppos, opposition):
            self.oppos = oppos
        else:
            self.oppos = opposition(oppos)
    def __repr__(self):
        return "%s(oppos=%r)" % (self.__class__.__name__, self.oppos)
    def __str__(self):
        return """"
  Opposition: %s
""" % (self.oppos)
    
class nonSelectedFingers:
    """the non selected fingers"""
    def __init__(self, joints=None, members = set()):
        try:
            members = fingerCheck(members)
        except digitError:
            print("Nonselected finger digit error.")
            raise
        self.members = members
        # ensure the that joints is a joint instance            
        if isinstance(joints, joint):
            self.joints = joints
        else:
            self.joints = joint(joints)        

        ## # if members is empty, set joints to None: breaks because the members are defined by handshape class.
        ## if len(members) == 0:
        ##     self.joints = None
        
    def __repr__(self):
        return "%s(joints=%r, members=%r)" % (self.__class__.__name__, self.joints, self.members)
    def __str__(self):
        return """
  members: %s
  joints: %s
""" % (self.members, self.joints)



##### abstract articulator classes #####

class joint:
    """a joint object"""
    def __init__(self, value):
        try:
            value = jointCheck(value, joints = phonoJoints)
        except jointError:
            print("The joint is not in the set of phonologically specified joint features.")
            raise
        self.value = value

    def __repr__(self):
        return "%s(value=%r)" % (self.__class__.__name__, self.value)
    def __str__(self):
        return "%s" % (self.value)

class opposition:
    """an oppotision object"""
    def __init__(self, value):
        try:
            value = oppositionCheck(value, oppositions = phonoOpposition)
        except oppositionError:
            print("The opposition is not in the set of phonologically specified opposition features.")
            raise
        self.value = value

    def __repr__(self):
        return "%s(value=%r)" % (self.__class__.__name__, self.value)
    def __str__(self):
        return "%s" % (self.value)

class abduction:
    """a abduction object"""
    def __init__(self, value):
        try:
            value = abdCheck(value, abds = phonoAbduction)
        except abductionError:
            print("The abduction is not in the set of phonologically specified abduction features.")
            raise
        self.value = value
        
    def __repr__(self):
        return "%s(value=%r)" % (self.__class__.__name__, self.value)
    def __str__(self):
        return "%s" % (self.value)    


##### testing #####

foo = handshape(
    selectedFingers = selectedFingers(members = ["index", "middle"], MCP=joint("ext"), PIP="ext", abd=abduction("adducted")),
    secondarySelectedFingers = None,
    thumb = thumb(oppos=None),
    nonSelectedFingers = nonSelectedFingers(joints="flex")
    )

bar = foo.toHandconfigTarget()

baz = arm(handshape=foo, orientation="defaultFS")

qux = baz.toArmTarget()

