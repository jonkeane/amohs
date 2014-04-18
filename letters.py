import hs
import funcs

import csv
from os import path

##### Error classes #####
class specificationError(Exception):
    pass


##### Read in csvs with letter specifications #####
lettersFile =path.join(funcs.resources_dir,'lettersFromArtModel.csv')
lettersKey = funcs.read_csv_data(lettersFile)
lettersCols = funcs.dictToCols(lettersKey)
letterCodingCols = funcs.dictColMapper(lettersKey, "letter")

def letterToArm(letter):
    """converts a letter to an articulatory model representation of handshape"""
    try:
        let = letterCodingCols[letter]
    except KeyError:
        print("That is not a recognized letter")
        raise
    
    psf = hs.selectedFingers(
        members = let["psf-members"].split(","), 
        MCP=let["psf-mcp"], 
        PIP=let["psf-pip"], 
        abd=hs.abduction(let["psf-abd"])
        )
    
    if(let["ssf-members"] == "None"):
        ssf = None
    else:
        ssf = hs.secondarySelectedFingers(
            members = let["ssf-members"].split(","), 
            MCP=let["ssf-mcp"], 
            PIP=let["ssf-pip"],
            abd=hs.abduction(let["ssf-abd"])
            )        
    if(let["thumb-oppos"] == "None"):
        thmb = None
    else:
        thmb = hs.thumb(oppos=let["thumb-oppos"])
        
    if(let["nsf-joints"] == "None"):
        nsf = None
    else:
        nsf = hs.nonSelectedFingers(joints=let["nsf-joints"])    
    
    handshape = hs.handshape(
        selectedFingers = psf,
        secondarySelectedFingers = ssf,
        thumb = thmb,
        nonSelectedFingers = nsf
        )
    orientation = let["orientation"]
        
    return hs.arm(handshape=handshape, orientation=orientation)
        
def printAllLetters():
    for letter in lettersKey:
    	 print("####################")
    	 print(letter["letter"])
    	 print(letterToArm(letter["letter"]).toArmTarget())

def ntuples(lst, n):
    return zip(*[lst[i:]+lst[:i-1] for i in range(n)])
         
def measureContour(string, method="unweighted"):
    stringTup = tuple(string)
    cost = []
    for pair in ntuples(stringTup,2):
        c =  letterToArm(pair[0]).toArmTarget()-letterToArm(pair[1]).toArmTarget()
        if method == "unweighted":
            c = c.totalDegreesDifferent()
        elif method == "weighted":
            c = c.weightedDegreesDifferent()
        else:
            raise specificationError("No recognized method for measuring contour.")
        cost.append(c)
    return sum(cost)
    
    
def similarity(stringA, stringB, method="unweighted"):
    if len(stringA) != len(stringB):
        raise specificationError("The strings are not of the same length, cannot compare without some sort of editing")
    cost = []
    for pair in zip(stringA,stringB):
        c =  letterToArm(pair[0]).toArmTarget()-letterToArm(pair[1]).toArmTarget()
        if method == "unweighted":
            c = c.totalDegreesDifferent()
        elif method == "weighted":
            c = c.weightedDegreesDifferent()
        else:
            raise specificationError("No recognized method for measuring contour.")
        cost.append(c)
    return sum(cost)    
    

         

        
foo = letterToArm("p")
bar = letterToArm("k")

baz = foo.toArmTarget()-bar.toArmTarget()
