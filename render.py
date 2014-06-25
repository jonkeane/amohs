import hc
import funcs
import string # for testing
import letters # for testing

import yaml, csv, math, subprocess
from os import path, makedirs

##### Error classes #####
class specificationError(Exception):
    pass

##### Path to deafult in the base pose to alter #####
baseHCposeFile = path.join(funcs.resources_dir,"fsBaseOpticalClosedToOpen.yml")

##### Establish joint angles for the base hand #####
index = hc.finger(MCP=(180,5), PIP=180, DIP=180)
middle = hc.finger(MCP=(180,2), PIP=180, DIP=180)
ring = hc.finger(MCP=(180,-2), PIP=180, DIP=180)
pinky = hc.finger(MCP=(180,-4), PIP=180, DIP=180)
thmb = hc.thumb(CM=hc.joint(dfFlex=15, dfAbd=9, dfRot=27, dfPro=None), MCP=180, IP=180)
wrist = (0,0,0) # the wrist values here are not those in the pose file, these need to be changed in the future

baseHC = hc.armconfiguration(hc.handconfiguration(index, middle, ring, pinky, thmb), wrist)

def ntz(value):
    """Change a none to zero"""
    if value == None:
        value = 0
    return value
    
def renderImage(hc, imageOutFile, baseHCposeFile=baseHCposeFile, baseHC=baseHC):
    ##### Read in the base pose to alter #####
    baseHCposefile = open(baseHCposeFile, "r")
    baseHCpose = yaml.load(baseHCposefile)
    baseHCposefile.close()

    newHCpose = baseHCpose
    diff = baseHC - hc
    
    fingMap = {"finger4": 'index',
              "finger3": 'middle',
              "finger2": 'ring',
              "finger1": 'pinky',
              "finger5": 'thumb'}
              
    fingerJointMap = {"joint1": 'MCP',
                "joint2": 'PIP',
                "joint3": 'DIP'}

    thumbJointMap = {"joint1": 'CM',
                "joint2": 'MCP',
                "joint3": 'IP'}
    
    for fingerJoint in baseHCpose['hand_joints']:
        finger = fingerJoint[0:7]
        joint = fingerJoint[7:13]
        if finger[0:-1] != "finger" or joint[0:-1] != "joint":
            continue
            
        if fingMap[finger] == "thumb":
            jointMove = getattr(getattr(diff.hand, fingMap[finger]), thumbJointMap[joint])
            if joint == "joint1":
                # these joint mappings are wrong wrong wrong.
                jointMatrix = [(ntz(jointMove.dfFlex)*math.pi)/180, (ntz(jointMove.dfAbd)*math.pi)/180 , (ntz(jointMove.dfRot)*math.pi)/180 ]
            elif joint == "joint2" or joint == "joint3":
                jointMatrix = [(ntz(jointMove.dfFlex)*math.pi)/180, (ntz(jointMove.dfAbd)*math.pi)/180 , (ntz(jointMove.dfRot)*math.pi)/180 ]
            newJoints = [i - j for i, j in zip(baseHCpose['hand_joints'][fingerJoint], jointMatrix)]
            newHCpose['hand_joints'][fingerJoint] = newJoints  
        else:
            jointMove = getattr(getattr(diff.hand, fingMap[finger]), fingerJointMap[joint])
            jointMatrix = [(ntz(jointMove.dfFlex)*math.pi)/180, (ntz(jointMove.dfAbd)*math.pi)/180 , (ntz(jointMove.dfRot)*math.pi)/180 ]
            newJoints = [i - j for i, j in zip(baseHCpose['hand_joints'][fingerJoint], jointMatrix)]
            newHCpose['hand_joints'][fingerJoint] = newJoints
    
    wristMatrix = [(ntz(diff.wrist.dfFlex)*math.pi)/180, (ntz(0)*math.pi)/180 , (ntz(diff.wrist.dfPro)*math.pi)/180 ]
    newHCpose['hand_joints']['metacarpals'] = [i - j for i, j in zip(baseHCpose['hand_joints']['metacarpals'], wristMatrix)]
    
    
    rootMatrix = [(ntz(0)*math.pi)/180, ((ntz(diff.wrist.dfPro)*math.pi)/180)*-(3/4), ((ntz(diff.wrist.dfPro)*math.pi)/180)*(5/4) ]
    newHCpose['hand_joints']['carpals'] = [i - j for i, j in zip(baseHCpose['hand_joints']['carpals'], rootMatrix)]
    
        
    # make tmp directory if it doesn't exist
    if not path.exists(path.join(funcs.resources_dir,"tmp")):
        makedirs(path.join(funcs.resources_dir,"tmp"))
    
    poseOutFilePath = path.join(funcs.resources_dir,''.join(["tmp/",path.basename(imageOutFile),"poseOut.yml"]))
    print(poseOutFilePath)
    poseOutFile = open(poseOutFilePath, 'w') 
    poseOutFile.write("%YAML:1.0\n")
    yaml.dump(newHCpose, poseOutFile)
    poseOutFile.close()
    
    
    cmd = [path.join(funcs.resources_dir,"imageGen"), path.join(funcs.resources_dir,"hand_model/scene_spec.yml"), poseOutFilePath, imageOutFile]
    devnull = open('/dev/null', 'w')
    subprocess.call(cmd, stdout=devnull, stderr=subprocess.STDOUT)
    
##### Tests ######
#ensure that all articulatory model specifications are readable
if not path.exists("./let"):
   makedirs("./let")
for ltr in letters.lettersCols['letter']:
    try:
        AMarm = letters.letterToArm(ltr)
    except:
        print("error with "+ltr+". can't convert from articulatory specifications to AM handshape")   
        break
    pth = path.join("./let/",''.join(["am-",ltr,".png"]))
    print(pth)
    renderImage(AMarm.toArmTarget(), pth)    
    
    # try:
    #     PMarm = hs.arm(handshape=letters.letterToPM(ltr).toAMhandshape(), orientation=letters.letterCodingCols[ltr]["orientation"])
    # except:
    #     print("Error with "+ltr+". can't convert from PM notation to AM handshape")
    #     break
    # renderImage(PMarm.toArmTarget(), path.join("./let/",''.join(["pm-",ltr,".png"])))   