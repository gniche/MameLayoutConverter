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

def processLayoutFolder(currentFolder):
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
    with open(currentFolder + "default.lay", "w") as mame_layout_file:
        mame_layout_file.write(xmlstr)
        mame_layout_file.close()


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
    bz_img_shape = cv2.imread(currentFolder + bezel_name + '.png').shape
    addImageElement(mamelayout, bezel_name)

    view_elem = eT.SubElement(mamelayout, 'view')
    view_elem.set('name', bezel_name)

    bgimg = createbackgroundlayer(mamelayout, view_elem, bezel_name, currentFolder)

    offset = getoffset(bgimg, bz_img_shape)
    createScreenBoundsElem(view_elem, ini, offset)
    createViewLayer(view_elem, bz_img_shape, bezel_name, offset)


def getoffset(bgimg, bz_img_shape):
    offset = (0, 0)
    if bgimg is not None:
        print("bgImage found!!")
        offset = (bgimg.shape[0] / 2 - bz_img_shape[0] / 2, bgimg.shape[1] / 2 - bz_img_shape[1] / 2)
    return offset


def createbackgroundlayer(mamelayout, view_elem, bezel_name, currentFolder):
    bgimg = None
    if bezel_name.startswith('Bezel - '):
        bgname = bezel_name.replace('Bezel - ', 'Background - ')
        bgPngPath = currentFolder + bgname + '.png'
        bg_jpg_path = currentFolder + bgname + '.jpg'
        if os.path.exists(bgPngPath):
            bgimg = cv2.imread(bgPngPath)
            addImageElement(mamelayout, bgname)
            createViewLayer(view_elem, bgimg.shape, bgname)
        elif os.path.exists(bg_jpg_path):
            bgimg = cv2.imread(bg_jpg_path)
            cv2.imwrite(bgPngPath, bgimg)
            addImageElement(mamelayout, bgname)
            createViewLayer(view_elem, bgimg.shape, bgname)
    else:
        print("simple config for: " + bezel_name)
    return bgimg


def addImageElement(mamelayout, image_name):
    elementElem = eT.Element('element')
    mamelayout.insert(0, elementElem)
    elementElem.set('name', image_name)
    imageElem = eT.SubElement(elementElem, 'image')
    imageElem.set('file', image_name + '.png')


def createScreenBoundsElem(viewElem, ini, offset=(0, 0)):
    screenElem = eT.SubElement(viewElem, 'screen')
    screenElem.set('index', '0')  # single screen always 0
    sBoundsElem = eT.SubElement(screenElem, 'bounds')
    sBoundsElem.set('x', str(offset[1] + ini.top_l_x))
    sBoundsElem.set('y', str(offset[0] + ini.top_l_y))
    sBoundsElem.set('width', str(ini.btm_r_x - ini.top_l_x))
    sBoundsElem.set('height', str(ini.btm_r_y - ini.top_l_y))


def createViewLayer(viewElem, shape, image_name, offset=(0, 0)):
    bezelElem = eT.SubElement(viewElem, 'element')
    bezelElem.set('ref', image_name)
    bBoundsElem = eT.SubElement(bezelElem, 'bounds')
    bBoundsElem.set('x', str(offset[1]))
    bBoundsElem.set('y', str(offset[0]))
    bBoundsElem.set('width', str(shape[1]))
    bBoundsElem.set('height', str(shape[0]))


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


processLayoutFolder(folder)
