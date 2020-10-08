import cv2
import xml.etree.ElementTree as eT
from xml.dom import minidom
import os
import re

indexPattern = re.compile(r'.*\(\d+\)')

filepath = r'G:\Games\Consoles+Emulation\Pegasus FE\Marquees Bezels Art_\Rocketlauncher Bezels\RL MAME 16_9 Bezels'
currentGame = '1on1gov'
bezelName = 'Bezel'
currentFolder = filepath + '\\' + currentGame + '\\'


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def run():
    mamelayout = eT.Element('mamelayout')
    mamelayout.set('version', '2')

    for filename in os.listdir(currentFolder):
        if filename.endswith('.ini'):
            bezelName = filename.lstrip(currentFolder).rstrip('.ini')
            addView(mamelayout, currentFolder, bezelName)

            # item1.text = 'item1abc'
            # item2.text = 'item2abc'
            # create a new XML file with the results
            # myfile = open("items2.xml", "w")
            # myfile.write(mydata)

    xmlstr = minidom.parseString(eT.tostring(mamelayout)).toprettyxml(indent="   ")
    print(xmlstr)


class Ini:
    def __init__(self):
        self.top_l_x = 0
        self.top_l_y = 0
        self.btm_r_x = 0
        self.btm_r_y = 0

    def __str__(self):
        return f"topLeftX:{self.top_l_x}, topLeftY:{self.top_l_y}, " \
               f"bottomRightX:{self.btm_r_x}, bottomRightY:{self.btm_r_y}"


def addBgToXml(bezelxml):
    if bezelName.startswith('Bezel - '):
        try:
            bgImg = cv2.imread(currentFolder + bezelName.replace('Bezel - ', 'Background - ') + '.png')

        except cv2.Error as err:
            print("No background image found:" + err)




def addView(mamelayout, currentFolder, bezelName):
    ini = readIni(bezelName)
    bzImg = cv2.imread(currentFolder + bezelName + '.png')
    bezelxml = createXml(mamelayout, ini, bzImg)
    addBgToXml(bezelxml)

def createXml(mamelayout, ini, bzImg):
    elementElem = eT.SubElement(mamelayout, 'element')
    elementElem.set('name', 'bezel')

    imageElem = eT.SubElement(elementElem, 'image')
    imageElem.set('file', bezelName + '.png')

    viewElem = eT.SubElement(mamelayout, 'view')
    viewElem.set('name', bezelName)

    screenElem = eT.SubElement(viewElem, 'screen')
    screenElem.set('index', '0')

    createScreenBoundsElem(screenElem, ini)

    bezelElem = createBezelElem(viewElem)

    createBezelBoundsElem(bezelElem, bzImg)

def createBezelElem(viewElem):
    bezelElem = eT.SubElement(viewElem, 'bezel')
    bezelElem.set('element', 'bezel')
    return bezelElem


def createScreenBoundsElem(screenElem, ini):
    sBoundsElem = eT.SubElement(screenElem, 'bounds')
    sBoundsElem.set('x', str(ini.top_l_x))
    sBoundsElem.set('y', str(ini.top_l_y))
    sBoundsElem.set('width', str(ini.btm_r_x - ini.top_l_x))
    sBoundsElem.set('height', str(ini.btm_r_y - ini.top_l_y))


def createBezelBoundsElem(bezelElem, bzImg):
    bBoundsElem = eT.SubElement(bezelElem, 'bounds')
    bBoundsElem.set('x', '0')
    bBoundsElem.set('y', '0')
    bBoundsElem.set('width', str(bzImg.shape[0]))
    bBoundsElem.set('height', str(bzImg.shape[1]))


def readIni(bezelName):
    bezelFile = open(currentFolder + bezelName + '.ini', "r")
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
    print(ini)
    return ini


run()
