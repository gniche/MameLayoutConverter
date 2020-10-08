import cv2
import xml.etree.ElementTree as eT
from xml.dom import minidom
import os
import re
from pathlib import Path

indexPattern = re.compile(r'.*\(\d+\)')

filepath = r'G:\Games\Consoles+Emulation\Pegasus FE\Marquees Bezels Art_\Rocketlauncher Bezels\RL MAME 16_9 Bezels'
# currentGame = '1on1gov'
currentGame = '3countb'
folder = filepath + '\\' + currentGame + '\\'


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def processGameBezelFolder(currentFolder):
    mamelayout = eT.Element('mamelayout')
    mamelayout.set('version', '2')

    for filename in os.listdir(currentFolder):
        if filename.endswith('.ini'):
            bezel_name = Path(filename).stem
            addView(mamelayout, currentFolder, bezel_name)
            # item1.text = 'item1abc'
            # item2.text = 'item2abc'
    xmlstr = minidom.parseString(eT.tostring(mamelayout)).toprettyxml(indent="   ")
    print(xmlstr)
    # create a new XML file with the results
    # myfile = open("items2.xml", "w")
    # myfile.write(mydata)


class Ini:
    def __init__(self):
        self.top_l_x = 0
        self.top_l_y = 0
        self.btm_r_x = 0
        self.btm_r_y = 0

    def __str__(self):
        return f"topLeftX:{self.top_l_x}, topLeftY:{self.top_l_y}, " \
               f"bottomRightX:{self.btm_r_x}, bottomRightY:{self.btm_r_y}"


def addView(mamelayout, currentFolder, bezel_name):
    ini = readIni(currentFolder, bezel_name)
    bzImg = cv2.imread(currentFolder + bezel_name + '.png')
    addImageElement(mamelayout, bezel_name)

    view_elem = eT.SubElement(mamelayout, 'view')
    view_elem.set('name', bezel_name)

    createScreenBoundsElem(view_elem, ini)
    createBezelLayerElem(view_elem, bzImg, bezel_name)
    if bezel_name.startswith('Bezel - '):
        try:
            bgname = bezel_name.replace('Bezel - ', 'Background - ')
            if os.path.exists(bgname + '.png'):
                bgimg = cv2.imread(currentFolder + bgname + '.png')
                addImageElement(mamelayout, bgname)
                createBezelLayerElem(view_elem, bgimg, bgname)
        except AttributeError as err:
            print("No background image found:" + err)


def addImageElement(mamelayout, bezelName):
    elementElem = eT.SubElement(mamelayout, 'element')
    elementElem.set('name', bezelName)
    imageElem = eT.SubElement(elementElem, 'image')
    imageElem.set('file', bezelName + '.png')


def createScreenBoundsElem(viewElem, ini):
    screenElem = eT.SubElement(viewElem, 'screen')
    screenElem.set('index', '0')  # single screen always 0
    sBoundsElem = eT.SubElement(screenElem, 'bounds')
    sBoundsElem.set('x', str(ini.top_l_x))
    sBoundsElem.set('y', str(ini.top_l_y))
    sBoundsElem.set('width', str(ini.btm_r_x - ini.top_l_x))
    sBoundsElem.set('height', str(ini.btm_r_y - ini.top_l_y))


def createBezelLayerElem(viewElem, img, bezel_name):
    bezelElem = eT.SubElement(viewElem, 'bezel')
    bezelElem.set('element', bezel_name)
    bBoundsElem = eT.SubElement(bezelElem, 'bounds')
    bBoundsElem.set('x', '0')
    bBoundsElem.set('y', '0')
    bBoundsElem.set('width', str(img.shape[0]))
    bBoundsElem.set('height', str(img.shape[1]))


def readIni(currentFolder, bezel_name):
    bezelFile = open(currentFolder + bezel_name + '.ini', "r")
    line = bezelFile.readline()
    ini = Ini()

    while line:
        line = bezelFile.readline()
        spt = line.split('=')
        if spt[0] == 'Bezel Screen Top Left X Coordinate':
            ini.top_l_x = int(spt[1].rstrip())
        elif spt[0] == 'Bezel Screen Top Left Y Coordinate':
            ini.top_l_y = int(spt[1].rstrip())
        elif spt[0] == 'Bezel Screen Bottom Right X Coordinate':
            ini.btm_r_x = int(spt[1].rstrip())
        elif spt[0] == 'Bezel Screen Bottom Right Y Coordinate':
            ini.btm_r_y = int(spt[1].rstrip())
    # print(ini)
    return ini


processGameBezelFolder(folder)
