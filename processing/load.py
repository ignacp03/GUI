import imageio as imageio
from PIL import Image
import xml.etree.ElementTree as ET
import numpy as np
import re as re


class VARIABLE:
    def __init__(self):
        self.name = ''
        self.value = 0



def ReadImage(imName,fast=False, getCamera = False):
    '''
    Takes a path to an image as a string and returns the image as an array.

    -- As of 15.11.2022, the variables are returned as a standard Python dictionary by default.

    A list of variables from ExpWiz are extracted from xml and returned in the
    VARIABLE data structure (variables[index].name and variables[index].value
    to get the name and value of a variable with a given index).


    The effective pixel size (accounting for magnification) is returned.

    optional: getCamera-returns string with camera 
    
    If fast=True then most of the processing is skipped and the pixel data is
    returned in an array with nothing else.
              
    
    return im, variables, pixelSize, *camera
    '''

    im = np.array(imageio.imread(imName).astype(float))
    if (fast):
        return im
    if not(getCamera):
        variables, pixelSize = GetImageMetadata(imName)
        return im, variables, pixelSize
    else:
        variables, pixelSize, camera = GetImageMetadata(imName,getCamera=True)
        return im, variables, pixelSize, camera



def GetImageMetadata(imName,getCamera = False):
    '''
    Takes a path to an image as a string and returns metadata.

    -- As of 15.11.2022, the variables are returned as a standard Python dictionary by default.

    A list of variables from ExpWiz are extracted from xml and returned in the
    VARIABLE data structure (variables[index].name and variables[index].value
    to get the name and value of a variable with a given index).

    The effective pixel size (accounting for magnification) is returned

    return variables, pixelSize,*camera
    '''
    imInfo = Image.open(imName).info
    #Get all variable names and values
    variables = []
    #<codefromJeff>
    ctr = ET.fromstring(imInfo["Control"]) # .ctr file (stored as the header a.k.a. info) parsed as XML
    varis = ctr.find('.//variables') # the part of the XML that contains the variables from ExperimentControl
    #</codefromJeff>
    #From https://stackoverflow.com/questions/4664850/find-all-occurrences-of-a-substring-in-python

    vind1 = [m.start() for m in re.finditer("<variable>\n      <name>", imInfo["Control"])]
    vind2 = [m.start() for m in re.finditer("</name>\n      <value>", imInfo["Control"])]
    numVars = len(vind1)
    itr = 0
    while (itr<numVars):
        v = VARIABLE()
        v.name = imInfo["Control"][(vind1[itr]+len("<variable>\n      <name>")):vind2[itr]]
        #<codefromJeff>
        v.value = float(varis.find('.//variable[name="' + v.name + '"]').find('value').text) # the value of the variable
        #</codefromJeff>
        variables.append(v)
        itr += 1
    events = ctr.find('.//events')
    for event in events:
        if (event.find('.//channel').text=='ImagingSplitter'):
            command = event.find('.//commandList').text
            dataList = command.split(', ')
            for item in dataList:
                if ('39k' in item.lower()):
                    v = VARIABLE()
                    v.name = 'port39K'
                    v.value = item.split(': ')[1]
                    variables.append(v)
                elif ('41k' in item.lower()):
                    v = VARIABLE()
                    v.name = 'port41K'
                    v.value = item.split(': ')[1]
                    variables.append(v)
    v = VARIABLE()
    v.name = 'CreationTime'
    v.value = imInfo[v.name]
    variables.append(v)
    variables = Variable2Dict(variables)

    #Get the pixel size in m
    pixelSize = ()
    for x in imInfo["dpi"]:
        pixelSize += (0.0254/x,)


    if getCamera == False:
        return variables, pixelSize
        #get camera
    else:
        stt = ET.fromstring(imInfo["Settings"])
        camera = stt.find('.//camera').text
        return variables, pixelSize, camera

def Variable2Dict(Variable):
    '''
    Takes a list of objects of class VARIABLE and returns the data in a dictionary
    return varDict
    '''
    varDict = {vari.name: vari.value for vari in Variable}
    return varDict


