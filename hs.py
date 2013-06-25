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

    def __repr__(self):
        return "handshape(selectedFingers=%s, secondarySelectedFingers=%s, thumb=%s, nonSelectedFingers=%s)" % (self.SF, self.SSF, self.thumb, self.NSF)

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
        return "selectedFingers(members=%s, MCP=%s, PIP=%s, abd=%s)" % (self.members, self.MCP, self.PIP, self.abd)

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
        return "secondarySelectedFingers(members=%s, MCP=%s, PIP=%s, abd=%s)" % (self.members, self.MCP, self.PIP, self.abd)

    
class thumb:
    """the thumb"""
    def __init__(self, oppos=None):
        if isinstance(oppos, opposition):
            self.oppos = oppos
        else:
            self.oppos = opposition(oppos)
    def __repr__(self):
        return "thumb(oppos=%s)" % (self.oppos)
    
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
        return "nonSelectedFingers(joints=%s, members=%s)" % (self.joints, self.members)



##### abstract articulator classes #####

class joint:
    """a joint object"""
    def __init__(self, value, kind="Phonological feature"):
        if kind == "Phonological feature":
            try:
                value = jointCheck(value, joints = phonoJoints)
            except jointError:
                print("The joint is not in the set of phonologically specified joint features.")
                raise
        elif kind == "Angle target":
            try:
                value = jointCheck(value, joints = reverseJoints)
            except jointError:
                print("The joint is not in the set of phonologically specified joint angle targets.")
                raise
        self.value = value
        self.kind = kind

    def angleTarget(self):
        try:
            self.value = phonoJoints[self.value]
        except KeyError:
            print("The phonological target is not one of the specified joint features.")
            raise
        self.kind = "Angle target"

    def phonoFeature(self):
        try:
            self.value = reverseJoints[self.value]
        except KeyError:
            print("The angle is not one of the specified phonological targets.")
            raise
        self.kind = "Phonological feature"

    def __repr__(self):
        return "joint(value='%s', kind='%s')" % (self.value, self.kind)


class opposition:
    """an oppotision object"""
    def __init__(self, value, kind="Phonological feature"):
        if kind == "Phonological feature":
            try:
                value = oppositionCheck(value, oppositions = phonoOpposition)
            except oppositionError:
                print("The opposition is not in the set of phonologically specified opposition features.")
                raise
        elif kind == "Angle target":
            try:
                value = oppositionCheck(value, oppositions = reverseOpposition)
            except oppositionError:
                print("The opposition is not in the set of phonologically specified opposition angle targets.")
                raise
        self.value = value
        self.kind = kind

    def angleTarget(self):
        try:
            self.value = phonoOpposition[self.value]
        except KeyError:
            print("The phonological target is not one of the specified opposition features.")
            raise
        self.kind = "Angle target"

    def phonoFeature(self):
        try:
            self.value = reverseOpposition[self.value]
        except KeyError:
            print("The angle is not one of the specified phonological targets.")
            raise
        self.kind = "Phonological feature"

    def __repr__(self):
        return "opposition(value='%s', kind='%s')" % (self.value, self.kind)


class abduction:
    """a abduction object"""
    def __init__(self, value, kind="Phonological feature"):
        if kind == "Phonological feature":
            try:
                value = abdCheck(value, abds = phonoAbduction)
            except abductionError:
                print("The abduction is not in the set of phonologically specified abduction features.")
                raise
        elif kind == "Angle target":
            try:
                value = abdCheck(value, abds = reverseAbduction)
            except abductionError:
                print("The abduction is not in the set of phonologically specified abduction angle targets.")
                raise
        self.value = value
        self.kind = kind

        
    def angleTarget(self):
        try:
            self.value = phonoAbduction[self.value]
        except KeyError:
            print("The phonological target is not one of the specified abduction features.")
            raise
        self.kind = "Angle target"
        
    def phonoFeature(self):
        try:
            self.value = reverseAbduction[self.value]
        except KeyError:
            print("The angle is not one of the specified phonological targets.")
            raise
        self.kind = "Phonological feature"
        
    def __repr__(self):
        return "abduction(value='%s', kind='%s')" % (self.value, self.kind)
    


##### testing #####

foo = handshape(
    selectedFingers = selectedFingers(members = "pinky", MCP=joint("ext"), PIP="ext", abd=abduction("adducted")),
    secondarySelectedFingers = secondarySelectedFingers(members=["index"], MCP=None, PIP=None, abd=None),
    thumb = thumb(oppos=None),
    nonSelectedFingers = nonSelectedFingers(joints="flex")
    )
