#!/usr/bin/env mayapy
# encoding: utf-8
"""
Moonbot Face Tools

Created by Chris Lesage on 2016-08.
Copyright (c) 2016 Moonbot Studios. All rights reserved.

A set of tools and scripts for generating a face rig.

The face skeleton and blendshapes are driven by poses which are
the combined delta positions of locators and attributes.
"""


#TODO: Outstanding Issues
'''
- I have to reconsider the joints vs. blendshape balance with the new Shape Editor tools. Blendshapes are way more powerful in 2016.5.
- A way to visualize how many joints, how many blendshapes and how many poses a rig has would be nice.
- A way to add/remove poses on the fly, after having built.
- Include scaling in the POSELOCs, but I'll have to make it multiplication instead of addition.
- When we upgrade past Maya 2016.5, the combinationShape node will become available.
- Create the face template via script. (LOW PRIORITY. It is fairly static, so importing it as an asset is totally feasible.)
- Connect the blendshapes via script. (This depends on them being named to match the poses in the map.)
- It would be great to have macros, so "wide mouth" was a combo of "left wide mouth" and "right wide mouth", rather than duplicating poses.
- Fix the issue where overriding a pose doesn't stop it from piping out a value to the blendshape.
    - The solution is to connect it after the multiplyDivide node that is driven by the overrides, not directly from the pose.
- I have **Macros, Overrides and Blendshapes**. It seems like there might be some conceptual overlap here...

SYMMETRY:
- Connect the right side POSLOC's in symmetry. Then, if I want to break that, I can, if I need asymmetry.
- AND create macros, so that left+right = the full pose, which is also mappable and breakable if I need to offset.
- That way, you edit 3 poses, by editing one.
'''


#SCRIPT_DIR = os.path.dirname('C:/Users/clesage/dev/tech/maya/scripts/moonbot/butterfly/')
#FACE_CTLS_FILE = os.path.join(SCRIPT_DIR, 'ctrlsface.data')
#FACE_CTLS = envtools.load_dict(FACE_CTLS_FILE)


__version__ = '0.4'
import traceback

from PySide import QtCore
from PySide import QtGui

#TODO: Integrate this so the tool can be maintained more easily. C:\moonbot\tools\tech\maya\scripts\mayaUtils\qt.py
try:
    from shiboken import wrapInstance
except:
    # future proofing for Maya 2017.
    from shiboken2 import wrapInstance 

import pymel.core as pm
import pymel.core.datatypes as dt
from pymel.util.path import path
import maya.cmds as mc
import maya.OpenMayaUI as omui

import sys
import os
import envtools
import json
from functools import wraps

DEBUG = True
DRYRUN = False


##################################
###### PySide UI Functions #######
##################################


def undo(func):
    """ Puts the wrapped `func` into a single Maya Undo action, then 
        undoes it when the function enters the finally: block
        from schworer Github """
    @wraps(func)
    def _undofunc(*args, **kwargs):
        try:
            # start an undo chunk
            mc.undoInfo(ock=True)
            return func(*args, **kwargs)
        finally:
            # after calling the func, end the undo chunk
            mc.undoInfo(cck=True)
    return _undofunc


def maya_main_window():
    ''' Return the Maya main window widget as a Python object '''
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtGui.QWidget)
    

class FaceTools(QtGui.QDialog):
    
    def __init__(self, parent=maya_main_window()):
        super(FaceTools, self).__init__(parent)
    
    def create(self):
        ''' Create the UI '''
        self.setWindowTitle('Face Tools v' + __version__)
        self.setWindowFlags(QtCore.Qt.Tool)

        self.posemapConnected = False
        
        #TODO: Solve this path relatively
        self.iconPath = 'C:/Users/clesage/dev/tech/maya/scripts/moonbot/butterfly/icons/faceTools/'
        self.templates = 'C:/Users/clesage/dev/tech/maya/scripts/moonbot/butterfly/templates/'

        self.create_controls()
        self.create_layout()
    
        
    def create_controls(self):
        ''' Create the widgets and signals for the dialog '''

        def make_icon_button(label, pressFunction, iconName, iconWidth, width=120, bgCol='666'):
            #TODO: Find a better way to get this path
            button = QtGui.QPushButton(label)
            button.setStyleSheet('padding:2px; background-color: #{}; color: #eee; text-align:left;'.format(bgCol))
            button.clicked.connect(pressFunction)
            button.setIcon( QtGui.QIcon(self.iconPath + iconName) )
            button.setIconSize(QtCore.QSize(iconWidth,iconWidth))
            button.setMinimumWidth(width*0.5)
            button.setMaximumWidth(width+40)
            return button

        ### Rigging & Skeleton Section ###
        self.importSkeletonBtn = make_icon_button('Import Joint Template', self.importSkeletonBtn_pressed, 'importFile16.png', 16, 150)
        
        self.importControlsBtn = make_icon_button('Import Face Controls', self.importControlsBtn_pressed, 'importFile16.png', 16, 150)

        self.connectFaceMapBtn = make_icon_button('Connect Face Map', self.connectFaceMapBtn_pressed, 'connect.png', 16, 120)
        
        self.faceMapPath = QtGui.QLineEdit('../path/to/character.posemap')
        self.faceMapPath.editingFinished.connect(self.facemap_path_changed)
        #self.faceMapPath.textChanged.connect(self.facemap_path_changed)
        
        self.zoneList = QtGui.QListWidget()
        #TODO: Get the zones from the loaded face map.
        self.zoneList.addItems([
                'Head',
                'Brow',
                'Eye',
                'Nose',
                'Cheeks',
                'Mouth',
                ])
        self.zoneList.setCurrentRow(0)
        self.zoneList.setMaximumHeight(60)
        self.zoneList.setMaximumHeight(90)
        self.zoneList.currentItemChanged.connect(self.zone_selection_changed)

        self.addToZoneBtn = QtGui.QPushButton('Add to Zone')
        self.addToZoneBtn.clicked.connect(self.addToZoneBtn_pressed)
        
        self.removeFromZoneBtn = QtGui.QPushButton('Remove from Zone')
        self.removeFromZoneBtn.clicked.connect(self.removefromZoneBtn_pressed)

        ### Building Section ###
        self.buildRigBtn = QtGui.QPushButton('Build Face Rig')
        self.buildRigBtn.setFixedHeight(30)
        self.buildRigBtn.clicked.connect(self.buildRigBtn_pressed)

        self.connectBlendsBtn = QtGui.QPushButton('Connect Blendshapes')
        self.connectBlendsBtn.setFixedHeight(30)
        self.connectBlendsBtn.clicked.connect(self.connectBlendsBtn_pressed)

        ### Pose Editing Section ###
        self.poseEditBtn1 = make_icon_button('Copy', self.poseEditBtn1_pressed, 'copyPose.png', 24, 120, '5d6a5d')
        self.poseEditBtn2 = make_icon_button('Paste', self.poseEditBtn2_pressed, 'pastePose.png', 24, 120, '6a5d5d')
        self.poseEditBtn3 = make_icon_button('Combine', self.poseEditBtn3_pressed, 'combinePoses.png', 24, 120)
        self.poseEditBtn4 = make_icon_button('Mirror', self.poseEditBtn4_pressed, 'mirrorPose.png', 24, 120)
        self.poseEditBtn5 = make_icon_button('Split Mirror', self.poseEditBtn5_pressed, 'splitMirrorPose.png', 24, 120)
        self.poseEditBtn6 = make_icon_button('Reset', self.poseEditBtn6_pressed, 'resetPose.png', 24, 120)
        self.poseEditBtn7 = make_icon_button('Import (Add)', self.poseEditBtn7_pressed, 'importPoses.png', 24, 120)
        self.poseEditBtn8 = make_icon_button('Import (Replace)', self.poseEditBtn8_pressed, 'importPoses.png', 24, 120)
        self.poseEditBtn9 = make_icon_button('Save All', self.poseEditBtn9_pressed, 'saveAllPoses.png', 24, 120)

        ### Cleaning Up Section ###
        self.cleanUpBtn = QtGui.QPushButton('Clean Up Rig (destructive!)')
        self.cleanUpBtn.clicked.connect(self.cleanUpBtn_pressed)
        self.cleanUpBtn.setStyleSheet('padding:7px; text-align:center; background-color: #6a5d5d; color: #eee;')
        self.cleanUpBtn.setFixedWidth(170)

        ### Merging to Body Section ###
        self.mergeBodyBtn = QtGui.QPushButton('Create blendshape rigspecs')
        self.mergeBodyBtn.clicked.connect(self.mergeBodyBtn_pressed)

        
    def create_layout(self):
        ''' Create the layouts and add widgets '''

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.setContentsMargins(*[6]*4)

        flatStyle = False  # False draws a border around the whole section
        groupFont = QtGui.QFont('Helvetica Neue', 10, QtGui.QFont.Bold)
        groupPadding = 4  # padding at top and bottom of each section
        groupSpacing = 4  # the space between each section

        rigGroup = QtGui.QGroupBox('Rigging and Skeleton')
        rigGroup.setFlat(flatStyle)
        rigGroup.setFont(groupFont)
        riggingLayout = QtGui.QVBoxLayout()
        riggingLayout.setContentsMargins(*[2]*4)
        riggingLayout.addSpacing(groupPadding)
        buttonRow = QtGui.QHBoxLayout()
        buttonRow.setAlignment(QtCore.Qt.AlignLeft)
        buttonRow.addWidget(self.importSkeletonBtn)
        buttonRow.addWidget(self.importControlsBtn)
        riggingLayout.addLayout(buttonRow)
        buttonRow = QtGui.QHBoxLayout()
        buttonRow.addWidget(self.connectFaceMapBtn)
        buttonRow.addWidget(self.faceMapPath)
        riggingLayout.addLayout(buttonRow)
        riggingLayout.addSpacing(groupPadding)
        rigGroup.setLayout(riggingLayout)

        
        zoneGroup = QtGui.QGroupBox('Face Zones')
        zoneGroup.setFlat(flatStyle)
        zoneGroup.setFont(groupFont)
        zoneLayout = QtGui.QVBoxLayout()
        zoneLayout.setContentsMargins(*[2]*4)
        zoneLayout.addSpacing(groupPadding)
        zoneGroupLayout = QtGui.QHBoxLayout()
        zoneGroupLayout.addWidget(self.zoneList)
        zoneButtonLayout = QtGui.QVBoxLayout()
        zoneButtonLayout.setAlignment(QtCore.Qt.AlignLeft)
        zoneButtonLayout.setAlignment(QtCore.Qt.AlignBottom)
        zoneButtonLayout.setContentsMargins(*[2]*4)
        zoneButtonLayout.addWidget(self.addToZoneBtn)
        zoneButtonLayout.addWidget(self.removeFromZoneBtn)
        zoneGroupLayout.addLayout(zoneButtonLayout)
        zoneLayout.addLayout(zoneGroupLayout)
        zoneLayout.addSpacing(groupPadding)
        zoneGroup.setLayout(zoneLayout)


        buildGroup = QtGui.QGroupBox('Build')
        buildGroup.setFlat(flatStyle)
        buildGroup.setFont(groupFont)
        buildingOptionsLayout = QtGui.QHBoxLayout()
        buildingOptionsLayout.setContentsMargins(*[2]*4)

        buildingLayout = QtGui.QVBoxLayout()
        buildingLayout.setContentsMargins(*[2]*4)
        buildingLayout.addSpacing(groupPadding)
        buttonRow = QtGui.QHBoxLayout()
        buttonRow.addWidget(self.buildRigBtn)
        buttonRow.addWidget(self.connectBlendsBtn)
        buildingLayout.addLayout(buildingOptionsLayout)
        buildingLayout.addLayout(buttonRow)
        buildingLayout.addSpacing(groupPadding)
        buildGroup.setLayout(buildingLayout)
        
        poseGroup = QtGui.QGroupBox('Edit Poses')
        poseGroup.setFlat(flatStyle)
        poseGroup.setFont(groupFont)

        posingLayout = QtGui.QGridLayout()
        posingLayout.addWidget(self.poseEditBtn1, 0, 0)
        posingLayout.addWidget(self.poseEditBtn2, 0, 1)
        posingLayout.addWidget(self.poseEditBtn3, 0, 2)
        posingLayout.addWidget(self.poseEditBtn4)
        posingLayout.addWidget(self.poseEditBtn5)
        posingLayout.addWidget(self.poseEditBtn6)
        posingLayout.addWidget(self.poseEditBtn7)
        posingLayout.addWidget(self.poseEditBtn8)
        posingLayout.addWidget(self.poseEditBtn9)
        poseGroup.setLayout(posingLayout)

        cleanGroup = QtGui.QGroupBox('Optimize Rig')
        cleanGroup.setFlat(flatStyle)
        cleanGroup.setFont(groupFont)
        cleaningLayout = QtGui.QVBoxLayout()
        cleaningLayout.setAlignment(QtCore.Qt.AlignCenter)
        cleaningLayout.setContentsMargins(*[2]*4)
        cleaningLayout.addSpacing(groupPadding)
        cleaningLayout.addWidget(self.cleanUpBtn)
        cleaningLayout.addSpacing(groupPadding)
        cleanGroup.setLayout(cleaningLayout)
        
        '''
        # These buttons do nothing yet.
        mergeGroup = QtGui.QGroupBox('Merge to Body')
        mergeGroup.setFlat(flatStyle)
        mergeGroup.setFont(groupFont)
        mergingLayout = QtGui.QVBoxLayout()
        mergingLayout.setContentsMargins(*[2]*4)
        mergingLayout.addSpacing(groupPadding)
        mergingLayout.addWidget(self.mergeBodyBtn)
        mergingLayout.addSpacing(groupPadding)
        mergeGroup.setLayout(mergingLayout)
        '''

        pixmap = QtGui.QPixmap(self.iconPath + 'face.png')
        lbl = QtGui.QLabel()
        lbl.setAlignment(QtCore.Qt.AlignRight)
        lbl.setStyleSheet('padding-right:20px;')
        lbl.setPixmap(pixmap)
        mainLayout.addWidget(lbl)
        mainLayout.addWidget(rigGroup)
        mainLayout.addSpacing(groupSpacing)
        mainLayout.addWidget(zoneGroup)
        mainLayout.addSpacing(groupSpacing)
        mainLayout.addWidget(buildGroup)
        mainLayout.addSpacing(groupSpacing)
        mainLayout.addWidget(poseGroup)
        mainLayout.addSpacing(groupSpacing)
        mainLayout.addWidget(cleanGroup)
        mainLayout.addSpacing(groupSpacing)
        # mainLayout.addWidget(mergeGroup)
        mainLayout.addStretch()
        
        self.setLayout(mainLayout)
    
    
    #--------------------------------------------------------------------------
    # SLOTS
    #--------------------------------------------------------------------------

    def connectFaceMapBtn_pressed(self):
        sender = self.sender()
        templatePath = self.templates
        print('{} pressed. importing [{}]'.format(sender.text(), templatePath))
        result = pm.fileDialog2(cc='Cancel', cap='Load a template Pose Map',
                                ff='JSON (*.json)',
                                fm=1, okc='Select', dir=templatePath)
        if result is not None:
            #TODO: Add some kind of validation that this is a posemap file
            #TODO: IMPORTANT: Add this path to a metanode so it is stored in the scene.
            self.faceMapPath.setText(result[0])
            print('Face Map set to {}'.format(result[0]))
            self.posemapConnected = True
            self.connectFaceMapBtn.setIcon( QtGui.QIcon(self.iconPath + 'connected.png') )


    def importControlsBtn_pressed(self):
        sender = self.sender()
        templatePath = self.templates
        print('{} pressed. importing [{}]'.format(sender.text(), templatePath))
        result = pm.fileDialog2(cc='Cancel', cap='Import face controls template.',
                                ff='Maya Scenes (*.ma);;Maya Scenes (*.mb)',
                                fm=1, okc='Import into scene', dir=templatePath)
        if result is not None:
            #TODO: Add some kind of validation that this is a template file
            print('Imported {}'.format(result[0]))
            for f in result:
                pm.importFile(path(f), defaultNamespace=False)


    def importSkeletonBtn_pressed(self):
        sender = self.sender()
        print('{} pressed.'.format(sender.text()))
        result = pm.fileDialog2(cc='Cancel', cap='Import a template face skeleton',
                                ff='Maya Scenes (*.ma);;Maya Scenes (*.mb);;All Files (*.*)',
                                fm=1, okc='Select', dir=os.path.dirname(pm.sceneName()))
        if result is not None:
            #TODO: Add some kind of validation
            print('Importing {}'.format(result[0]))


    def addToZoneBtn_pressed(self):
        sender = self.sender()
        currentZone = self.zoneList.currentItem().text().lower()
        print('Adding selection to [{}] zone'.format(currentZone))
        add_to_zone(pm.selected(type='transform'), currentZone)


    def removefromZoneBtn_pressed(self):
        sender = self.sender()
        currentZone = self.zoneList.currentItem().text().lower()
        print('Removing selection from [{}] zone'.format(currentZone))
        remove_from_zone(pm.selected(type='transform'), currentZone)


    def buildRigBtn_pressed(self):
        sender = self.sender()
        #print('{} pressed'.format(sender.text()))
        if self.posemapConnected:
            poseMapFile = 'C:\\Users\\clesage\\dev\\tech\\maya\\scripts\\moonbot\\butterfly\\templates\\test_face_map.json'
            poseMapFile = self.faceMapPath.text()
            build_face(poseMapFile)
        else:
            print('The pose map must be connected before building.')


    def connectBlendsBtn_pressed(self):
        sender = self.sender()
        #print('{} pressed'.format(sender.text()))
        #TODO: Pass in blendshapes
        auto_connect_blendshape(None)


    def poseEditBtn1_pressed(self):
        ''' Copy Pose '''
        sender = self.sender()
        print('{} pressed'.format(sender.text()))


    def poseEditBtn2_pressed(self):
        ''' Paste Pose '''
        sender = self.sender()
        print('{} pressed'.format(sender.text()))


    def poseEditBtn3_pressed(self):
        ''' Combine Poses '''
        sender = self.sender()
        print('{} pressed'.format(sender.text()))


    def poseEditBtn4_pressed(self):
        ''' Mirror Pose '''
        sender = self.sender()
        print('{} pressed'.format(sender.text()))


    def poseEditBtn5_pressed(self):
        ''' Split Mirror Pose '''
        sender = self.sender()
        print('{} pressed'.format(sender.text()))


    def poseEditBtn6_pressed(self):
        ''' Reset Pose to Neutral/Zero '''
        sender = self.sender()
        print('{} pressed'.format(sender.text()))


    def poseEditBtn7_pressed(self):
        ''' Import Poses From File - ADD MODE - Replace only the poses in the file, and leave the rest alone. '''
        sender = self.sender()
        print('{} pressed. Importing poses from file.'.format(sender.text()))

        #TODO: Use a scene-relative path to store these poses. Not in templates
        templatePath = self.templates
        print('{} pressed. importing [{}]'.format(sender.text(), templatePath))
        result = pm.fileDialog2(cc='Cancel', cap='Import Poses',
                                ff='JSON (*.json)',
                                fm=1, okc='Choose', dir=templatePath)
        if result is not None:
            apply_poses_from_json(result[0])


    def poseEditBtn8_pressed(self):
        ''' Import Poses From File - REPLACE MODE - Replace all the poses. If a pose isn't in the file, set to init. '''
        sender = self.sender()
        print('{} pressed. Importing poses from file.'.format(sender.text()))

        #TODO: Use a scene-relative path to store these poses. Not in templates
        templatePath = self.templates
        print('{} pressed. importing [{}]'.format(sender.text(), templatePath))
        result = pm.fileDialog2(cc='Cancel', cap='Import Poses',
                                ff='JSON (*.json)',
                                fm=1, okc='Choose', dir=templatePath)
        if result is not None:
            apply_poses_from_json(result[0])


    def poseEditBtn9_pressed(self):
        ''' Save All Poses To File '''
        sender = self.sender()
        templatePath = self.templates
        print('{} pressed. importing [{}]'.format(sender.text(), templatePath))
        #TODO: Figure out how to save a file. This fileDialog looks for an existing file.
        result = pm.fileDialog2(cc='Cancel', cap='Save all poses',
                                ff='JSON (*.json)',
                                fm=1, okc='Save', dir=templatePath)
        if result is not None:
            save_all_poses(result[0])


    def cleanUpBtn_pressed(self):
        sender = self.sender()
        #print('{} pressed'.format(sender.text()))
        
        result = pm.confirmDialog(
            title='Optimize the face rig',
            message='Are you ready to clean the face rig?\n\nThis removes extra utility nodes, and removes any empty face poses. You will lose the ability to edit those empty poses. The rig will speed up dramatically.',
            button=['OK', 'Cancel'],
            defaultButton='Cancel',
            cancelButton='Cancel',
            dismissString='Cancel')

        if result == 'OK':
            disconnect_poselocs()
            clean_face_rig()
            return True
        else:
            print 'cancelling. Face was not optimized.'
            return False


    def mergeBodyBtn_pressed(self):
        sender = self.sender()
        print('{} pressed'.format(sender.text()))


    def facemap_path_changed(self):
        sender = self.sender()
        print('Text changed to "{}"'.format(sender.text()))
        

    def zone_selection_changed(self, current, previous):
        pass
        #print('Zone changed from [{}] to [{}]'.format(previous.text(), current.text()))
    

##################################
##### Face Rigging Functions #####
##################################


def import_json_dict(jsonFile, validation):
    ''' open a json file. Look for a validation key in the dictionary to verify the correct type of data. '''
    with open(jsonFile, 'r') as f:
        facejson = json.load(f)
    validationKey = facejson.get('validation', None)
    if validationKey == validation:
        return facejson
    else:
        pm.warning('This json does not appear to contain {} information.'.format(validation))
        return False


def export_json_dict(jsonFile, dictData, validation):
    ''' save a json file. Write a validation key in the dictionary to verify the correct type of data. '''
    with open(jsonFile, 'w') as f:
        json.dump(dictData, f, sort_keys=False, indent=4)
    print('Exported {} to {}'.format(validation, jsonFile))


#TODO: Consider how this functionality works. I haven't used it once.
# Pose Attributes can be used to drive arbitrary attributes based on the value of poses. So 2 poses could drive a wrinkle corrective for example.
poseattributes = [
    'attribute1',
    'attribute2',
    'attribute3',
    'attribute4',
]


def add_a_keyable_attribute(myObj, oDataType, oParamName, oMin=None, oMax=None, oDefault=0.0):
    """ adds an attribute that shows up in the channel box; returns the newly created attribute """
    oFullName = '.'.join( [str(myObj),oParamName] )
    if pm.objExists(oFullName):
        return pm.PyNode(oFullName)
    else:
        myObj.addAttr(oParamName, at=oDataType, keyable=True, dv=oDefault)
        myAttr = pm.PyNode(myObj + '.' + oParamName)
        if oMin != None:
            myAttr.setMin(oMin)
        if oMax != None:
            myAttr.setMax(oMax)
        pm.setAttr(myAttr, e=True, channelBox=True)
        pm.setAttr(myAttr, e=True, keyable=True)
        return myAttr


def add_meta_attribute(myObj, oParamName, oValue):
    '''adds a string attribute into "extra" attributes. Useful for meta information'''
    oFullName = '.'.join( [str(myObj),oParamName] )
    if pm.objExists(oFullName):
        pm.PyNode(str(FullName)).set(oValue) # if it exists, just set the value
        return pm.PyNode(oFullName)
    else:
        myObj.addAttr(oParamName, dt='string')
        oParam = pm.PyNode(str(oFullName))
        oParam.set(oValue)
        return oParam


def move_loc_position(target, source):
    """ this function reads a world coordinate 'source'
    and moves the localPosition of the target locator. """
    # a temp dumb hack until I figure out how to translate world to local coordinates.
    # your math is bad and you should feed bad
    tempLoc = pm.spaceLocator(n='ZZZ_TEMP_LOCATOR_{}'.format(target.name()))
    pm.parent(tempLoc, target)
    tempLoc.setRotation([0,0,0])
    tempLoc.setTranslation(source, space='world')
    target.localPosition.set(tempLoc.getTranslation(space='object'))
    pm.delete(tempLoc)


def connect_mirror_transform(oLeft, oRight):
    """ this connects one PyNode transform to the other to create mirror behaviour
    The nodes should have XYZ rotation order. """
    nodeName = '{}_{}_symmetry_MLT'.format(oLeft.name(), oRight.name())
    oMultT = pm.createNode('multiplyDivide', n='left' + str(i) + '_MLT')

    oLeft.tx.connect(oMultT.input1X)
    oMultT.input2X.set(-1)  # translateX
    oMultT.input2Y.set(-1)  # rotateY
    oMultT.input2Z.set(-1)  # rotateZ
    oMultT.outputX.connect(oRight.tx)
    oMultT.outputY.connect(oRight.ry)
    oMultT.outputZ.connect(oRight.rz)

    # all other axes are 1:1 connected.
    oLeft.ty.connect(oRight.ty)
    oLeft.tz.connect(oRight.tz)
    oLeft.rx.connect(oRight.rx)
    # connect scale separately so user can disconnect one axis at a time if needed.
    oLeft.sx.connect(oRight.sx)
    oLeft.sy.connect(oRight.sy)
    oLeft.sz.connect(oRight.sz)


def get_midpoint(vecA, vecB, weight=0.5):
    """Helper to get middle point between two vectors. Weight is 0.0 to 1.0 blend between the two.
    So for example, 0.0 would return the position of oObject1. 1.0 would be oObject2. 0.5 is halfway."""
    try:
        vecA = dt.Vector(vecA) # just in case it isn't already cast as a vector
        vecB = dt.Vector(vecB)
        vecC = vecB-vecA
        vecD = vecC * weight # 0.5 is default which finds the mid-point.
        vecE = vecA + vecD
        return vecE

    except Exception, e:
        # TODO: include some useful error checking
        return False


def create_pose_node(pose, zone, inputHooks, masterScale, poseDriver, poseRange, poseOverrides, poseOverrideMaps):
    #TODO: Make some logic that auto-splits "symmetry" into two poses, left and right.
    poseName = pose.replace('symmetry','left')
    try:
        oZone = pm.PyNode('{}_zone'.format(zone))
        faceJoints = oZone.members()
    except:
        # a zone may have no joints, but will still drive blendshapes.
        faceJoints = []

    # initialize the HOOKS and OVERRIDES nodes.
    hookName = 'face_{}_HOOKS'.format(zone)
    overName = 'face_{}_OVERRIDES'.format(zone)
    oHook = pm.PyNode(hookName)
    oOver = pm.PyNode(overName)
    posesRoot = pm.PyNode('face_POSES')

    #####################
    poseLocators = {} # first loop creates the pose locators and puts them into hierarchy
    oPoseNode = pm.group(em=True, n='{}_POSE'.format(poseName)) # eg. left_smile_POSE
    pm.parent(oPoseNode, posesRoot)

    # lock and hide all transform attrs
    for each in oPoseNode.listAttr(keyable=True):
        each.set(keyable=False, channelBox=False)

    #TODO: Low priority: Create a proper meta info scheme instead of channel box attrs.
    # Add an enum attribute with the name of the zone
    pm.addAttr(oPoseNode, ln='zone', at='enum', en=zone)
    myAttr = pm.PyNode(oPoseNode.name() + '.zone')
    pm.setAttr(myAttr, e=True, channelBox=True)
    pm.setAttr(myAttr, e=True, keyable=True)
    myAttr.lock()

    for each in faceJoints:
        jKey = each.name()
        pivotPosition = inputHooks['pivotpositions'][jKey]
        pivotRotation = inputHooks['pivotrotations'][jKey]
        jointPosition = inputHooks['jointpositions'][jKey]
        jointRotation = inputHooks['jointrotations'][jKey]
        jointName = each.name().rpartition('_')[0].replace('symmetry','left') # cut off the suffix
        #NOTE: This name is long and cumbersome
        poseLocName = '{}__{}__POSELOC'.format(jointName, poseName) # eg. left_cheek_puff__right_smile__POSELOC

        oRoot = pm.group(em=True, n=poseLocName + '_grp')
        oLoc = pm.spaceLocator(n=poseLocName)
        oLoc.localScale.set([0.4 * masterScale]*3)
        poseLocators[jKey] = oLoc # adding each locator to a dictionary whose key is the joint name
        pm.parent(oLoc, oRoot)
        pm.parent(oRoot, oPoseNode)
        oRoot.setTranslation(pivotPosition, space='world')
        oRoot.setRotation(pivotRotation, space='world')

        move_loc_position(oLoc, jointPosition) # moves the localPosition of the locator to a world coordinate
    #####################

    # Populate the _POSE node with all of the attributes
    oTitleAttr = add_a_keyable_attribute(oPoseNode, 'double', 'arbitraryAttributes')
    oTitleAttr.lock()
    attrDict = {}
    for poseAttr in poseattributes: # The arbitrary attributes
        oPoseAttr = add_a_keyable_attribute(oPoseNode, 'double', 'pose_{}'.format(poseAttr))
        attrDict[poseAttr] = oPoseAttr

    for poseAttr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']:
        attrDict[poseAttr] = []
    for poseAttr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']:
        oTitleAttr = add_a_keyable_attribute(oPoseNode, 'double', '{}_POSE_{}'.format(poseName, poseAttr))
        oTitleAttr.lock()
        for each in faceJoints:
            jKey = each.name()
            jointName = each.name().rpartition('_')[0].replace('symmetry','left') # cut off the suffix

            pmaDriven    = inputHooks[jKey]['driven']
            pmaTranslate = inputHooks[jKey]['translate']
            pmaRotate    = inputHooks[jKey]['rotate']
            #pmaScale     = inputHooks[jKey]['scale']

            newAttrName = '{}_{}'.format(jointName, poseAttr)
            oPoseAttr = add_a_keyable_attribute(oPoseNode, 'double', newAttrName)
            poseLocator = poseLocators[jKey] # from dictionary
            # eg. connect left_cheek_puff_POSELOC.tx to left_smile_POSE.left_cheek_puff_tx
            pm.PyNode('{}.{}'.format(poseLocator, poseAttr)).connect(oPoseAttr)
            attrDict[poseAttr].append(oPoseAttr)

    # Now set up the hook connection to drive it
    oHookAttr = add_a_keyable_attribute(oHook, 'double', poseName)
    oOverAttr = add_a_keyable_attribute(oOver, 'double', poseName)

    if poseDriver == 'controller.attribute':
        pass
    else:
        poseMapper = pm.createNode('remapValue', n='{}_poseMapper'.format(poseName))
        try:
            pm.PyNode(poseDriver).connect(poseMapper.inputValue)
            poseMapper.outValue.connect(oHookAttr)
            poseMapper.inputMin.set(poseRange[0])
            poseMapper.inputMax.set(poseRange[1])
            poseMapper.outputMin.set(poseRange[2])
            poseMapper.outputMax.set(poseRange[3])
        except:
            pm.warning('{} HOOK failed to connect properly'.format(poseName))
            pass
    #TODO: Create a scheme so any number of poses can drive the override. (Clamped from 0 to 1 using a remapValue)
    if poseOverrides:
        poseOverridePMA = pm.createNode('plusMinusAverage', n='{}_override_PMA'.format(poseName))
        add_a_keyable_attribute(poseOverridePMA, 'long', 'poseCount')
        poseOverridePMA.output1D.connect(oOverAttr)
        poseOverridePMA.poseCount.set(0)
        for eachOver, overRange in zip(poseOverrides, poseOverrideMaps):
            overrideName = eachOver.replace('.','_')
            overrideMapper = pm.createNode('remapValue', n='{}_{}_poseOverrideMapper'.format(poseName, overrideName))
            try:
                pm.PyNode(eachOver).connect(overrideMapper.inputValue)
                overrideMapper.inputMin.set(overRange[0])
                overrideMapper.inputMax.set(overRange[1])
                overrideMapper.outputMin.set(overRange[2])
                overrideMapper.outputMax.set(overRange[3])

                pmaIndex = poseOverridePMA.poseCount.get()
                overrideMapper.outValue.connect(poseOverridePMA.input1D[pmaIndex])
                poseOverridePMA.poseCount.set(pmaIndex + 1)
            except:
                pm.warning('{} OVERRIDE failed to connect properly'.format(poseName))
                pass

    # create an Override for each pose (not for each joint)
    # This override will mute the multiplyDivide for each joint
    poseOverrideMAP =  pm.createNode('remapValue',       n='{}_override_MAP'.format(poseName))
    poseOverrideMULT = pm.createNode('multiplyDivide',   n='{}_override_MLT'.format(poseName))
    poseOverrideMAP.outputMin.set(1.0) # this MAP node reverses so as the override turns on, the MLT multiplies off
    poseOverrideMAP.outputMax.set(0.0)
    oOverAttr.connect(poseOverrideMAP.inputValue)
    oHookAttr.connect(poseOverrideMULT.input1X)
    poseOverrideMAP.outValue.connect(poseOverrideMULT.input2X)

    # Zip the corresponding pose locator attributes and face joint.
    # The faceJoints are used as dictKeys in this section
    ### TRANSLATION ###
    if faceJoints:
        for attrX, attrY, attrZ, currentJoint in zip( attrDict['tx'], attrDict['ty'], attrDict['tz'], faceJoints ):
            # Hook in the multiply for the translations
            oMult = pm.createNode('multiplyDivide', n='{}_{}_translate_MLT'.format(poseName, currentJoint))
            attrX.connect(oMult.input1X)
            attrY.connect(oMult.input1Y)
            attrZ.connect(oMult.input1Z)
            # poseOverrideMULT only uses the X channel as a mute for all 3 oMult axes.
            poseOverrideMULT.outputX.connect(oMult.input2X)
            poseOverrideMULT.outputX.connect(oMult.input2Y)
            poseOverrideMULT.outputX.connect(oMult.input2Z)
            oPlus = inputHooks[currentJoint.name()]['translate']
            pmaIndex = oPlus.poseCount.get()
            oMult.output.connect(oPlus.input3D[pmaIndex].input3D)
            oPlus.poseCount.set(pmaIndex + 1)

        ### ROTATION ###
        for attrX, attrY, attrZ, currentJoint in zip( attrDict['rx'], attrDict['ry'], attrDict['rz'], faceJoints ):
            # Hook in the multiply for the rotations
            oMult = pm.createNode('multiplyDivide', n='{}_{}_rotate_MLT'.format(poseName, currentJoint))
            attrX.connect(oMult.input1X)
            attrY.connect(oMult.input1Y)
            attrZ.connect(oMult.input1Z)
            # poseOverrideMULT only uses the X channel as a mute for all 3 oMult axes.
            poseOverrideMULT.outputX.connect(oMult.input2X)
            poseOverrideMULT.outputX.connect(oMult.input2Y)
            poseOverrideMULT.outputX.connect(oMult.input2Z)
            oPlus = inputHooks[currentJoint.name()]['rotate']
            pmaIndex = oPlus.poseCount.get()
            oMult.output.connect(oPlus.input3D[pmaIndex].input3D)
            oPlus.poseCount.set(pmaIndex + 1)

        ### CUSTOM ATTRIBUTES ###
        #TODO: Hook in the custom attributes, and attach them to the override mute control
        for poseAttr in poseattributes:
            oAttrA = attrDict[poseAttr]
            # Hook in the multiply for the arbitrary attributes
            oMult = pm.createNode('multiplyDivide', n='{}_{}_attributes_MLT'.format(poseName, currentJoint))
            oAttrA.connect(oMult.input1X)
            # poseOverrideMULT only uses the X channel as a mute for all 3 oMult axes.
            # and the arbitrary attributes only pass one channel.
            poseOverrideMULT.outputX.connect(oMult.input2X)
            oPlus = inputHooks['poseattributes'][poseAttr]
            pmaIndex = oPlus.poseCount.get()
            oMult.outputX.connect(oPlus.input1D[pmaIndex])
            oPlus.poseCount.set(pmaIndex + 1)


def create_hooks(faceMap, masterScale):
    # create the HOOKS and OVERRIDES nodes.
    hookRoot = pm.group(em=True, n='face_HOOKS')
    overRoot = pm.group(em=True, n='face_OVERRIDES')
    posesRoot = pm.group(em=True, n='face_POSES')
    add_meta_attribute(posesRoot, facemap, '') # stores a path to the pose map

    oRigRoot = pm.PyNode('|face_RIG')
    pm.parent(hookRoot, overRoot, posesRoot, oRigRoot)
    # Get the zones from the face map file.
    # I want the HOOKS to exist even if there are no joints in the zone set.
    for zone in faceMap['faceposes'].keys():
        hookName = 'face_{}_HOOKS'.format(zone)
        overName = 'face_{}_OVERRIDES'.format(zone)
        oHook = pm.spaceLocator(n=hookName)
        oOver = pm.spaceLocator(n=overName)
        oHook.localScale.set([0.5 * masterScale]*3)
        oOver.localScale.set([0.5 * masterScale]*3)

        for each in oHook.listAttr(keyable=True):
            each.set(keyable=False, channelBox=False)
        for each in oOver.listAttr(keyable=True):
            each.set(keyable=False, channelBox=False)
        pm.parent(oHook, hookRoot)
        pm.parent(oOver, overRoot)


def add_to_zone(oColl, zone):
    oldSel = pm.selected()
    if not pm.objExists('{}_zone'.format(zone)):
        oZone = pm.createNode('objectSet', n='{}_zone'.format(zone))
    else:
        oZone = pm.PyNode('{}_zone'.format(zone))
    [oZone.add(x) for x in oColl]
    pm.select(oldSel)


def remove_from_zone(oColl, zone):
    oldSel = pm.selected()
    if not pm.objExists('{}_zone'.format(zone)):
        oZone = pm.createNode('objectSet', n='{}_zone'.format(zone))
    else:
        oZone = pm.PyNode('{}_zone'.format(zone))
    for each in oColl:
        if each in oZone:
            oZone.remove(each)
    pm.select(oldSel)


def create_joint_drivers(masterScale):
    """ This function builds the skeleton hierarchy and the end-result nodes and pivots.
    Returns a dictionary of the final plusMinusAverage nodes that all the poses drive """

    # Here I get all the zones from the sets rather than from the pose map.
    oRigRoot = pm.PyNode('|face_RIG')
    oSkeletonRoot = pm.PyNode('|face_RIG|face_skeleton_RIG')
    allZones = pm.ls('*_zone', type='objectSet')
    allJoints = set(pm.ls([x.members() for x in allZones]))
    inputHooks = {}

    jointRoot = list(allJoints)[0].root() # grab one of the joints and find the skeleton root
    pm.parent(jointRoot, oSkeletonRoot)

    # 'poseCount' is an attribute to keep track of how many poses are fed into each plusMinusAverage node.
    # This is so I can reliably append. I'm sure there is a better Maya way, but there are also index bugs.
    inputHooks['poseattributes'] = {}
    inputHooks['pivotpositions'] = {}
    inputHooks['pivotrotations'] = {}
    inputHooks['jointpositions'] = {}
    inputHooks['jointrotations'] = {}

    aaRoot = pm.group(em=True, n='attributeJnt_grp')
    pm.parent(aaRoot, oRigRoot)
    for i, poseAttr in enumerate(poseattributes): # The arbitrary attributes
        # Generate the special arbitrary attribute joints in this loop
        aaGroup = pm.group(em=True, n='{}_attrJnt_grp'.format(poseAttr))
        pm.select(None)
        aaJoint = pm.joint(n='{}_attr_jnt'.format(poseAttr))
        aaJoint.radius.set(1.0 * masterScale)
        pm.select(None)
        pm.parent(aaJoint, aaGroup)
        pm.parent(aaGroup, aaRoot)
        aaGroup.tx.set( (i*0.4)+2.0 ) #TODO: This should be a part of the skeleton, and constrained by a driver rig (so it can bake)

        # add all together with PMA, and clamp from 0-1 with remapValue
        #TODO: I might also have to clamp the input. But HOOKS will usually have a sane driver amount... But right now, if you keep driving the pose and the Attribute is set to 0.1, when you get to 10 on the HOOK, the attribute will reach 1.
        pmaAttr = pm.createNode('plusMinusAverage', n='custom_{}_PlusA_PMA'.format(poseAttr))
        pmaRemap = pm.createNode('remapValue', n='custom_{}_RemapA_MAP'.format(poseAttr))
        add_a_keyable_attribute(pmaAttr, 'long', 'poseCount')
        pmaAttr.output1D.connect(pmaRemap.inputValue)
        pmaRemap.outValue.connect(aaJoint.translateY)
        #pmaAttr.input1D[0]

        inputHooks['poseattributes'][poseAttr] = pmaAttr

    for each in allJoints:
        jKey = each.name()
        jointBaseName = each.name().rpartition('_')[0]
        # Add a plusMinusAverage for each driven joint and store it in a dictionary.
        # This dict will be referenced by all the zones and poses.
        # A dict, because here I am iterating on all joints. Later I'll be iterating on pose sets of joints.
        inputHooks[jKey] = {}

        offsetCtlName = jointBaseName + '_offset_ctrl'
        offsetCtlZeroName = jointBaseName + '_offsetCtrl_zero'
        drivenName = jointBaseName + '_driven'
        zeroName   = jointBaseName + '_zero'

        ##### Set up the pivot hierarchy
        # The requirements right now are a _posepivot locator parented underneath the joint and placed at an arbitrary position.
        jointPosition = each.getTranslation(space='world')
        jointRotation = each.getRotation(space='world')
        inputHooks['jointpositions'][jKey] = jointPosition
        inputHooks['jointrotations'][jKey] = jointRotation
        pivotPositionLoc = [x for x in each.getChildren() if 'posepivot' in x.name()]
        if len(pivotPositionLoc) > 0:
            pivotPosition = pivotPositionLoc[0].getTranslation(space='world')
            pivotRotation = pivotPositionLoc[0].getRotation(space='world')
            pm.delete(pivotPositionLoc)
            inputHooks['pivotpositions'][jKey] = pivotPosition
            inputHooks['pivotrotations'][jKey] = pivotRotation
        else:
            # If no _posepivot is found, use the joint's position instead.
            pivotPosition = each.getTranslation(space='world')
            pivotRotation = each.getRotation(space='world')
            inputHooks['pivotpositions'][jKey] = pivotPosition
            inputHooks['pivotrotations'][jKey] = pivotRotation

        oOffsetCtl = pm.spaceLocator(n=offsetCtlName)
        oOffsetCtlZero = pm.group(em=True, n=offsetCtlZeroName)
        oDriven = pm.spaceLocator(n=drivenName)
        oDrivenRoot = pm.group(em=True, n=zeroName)
        oOffsetCtl.localScale.set([0.5 * masterScale]*3)
        oDriven.localScale.set([0.5 * masterScale]*3)

        oOffsetCtl.setTranslation(     jointPosition, space='world')
        oOffsetCtlZero.setTranslation( jointPosition, space='world')
        oDriven.setTranslation(        pivotPosition, space='world')
        oDrivenRoot.setTranslation(    pivotPosition, space='world')

        oOffsetCtl.setRotation(        pivotRotation, space='world')
        oOffsetCtlZero.setRotation(    pivotRotation, space='world')
        oDriven.setRotation(           pivotRotation, space='world')
        oDrivenRoot.setRotation(       pivotRotation, space='world')

        try:
            pm.parent(oDrivenRoot, each.getParent())
        except:
            pass
        pm.parent(oDriven, oDrivenRoot)
        pm.parent(oOffsetCtlZero, oDriven)
        pm.parent(oOffsetCtl, oOffsetCtlZero)
        pm.parent(each, oOffsetCtl) #TODO: Eventually abstract the skeleton and constrain it

        pmaTranslate = pm.createNode('plusMinusAverage', n='{}_translate_PMA'.format(drivenName))
        pmaRotate    = pm.createNode('plusMinusAverage', n='{}_rotate_PMA'.format(drivenName))
        #pmaScale     = pm.createNode('plusMinusAverage', n='{}_scale_PMA'.format(drivenName))
        add_a_keyable_attribute(pmaTranslate, 'long', 'poseCount')
        add_a_keyable_attribute(pmaRotate, 'long', 'poseCount')
        #add_a_keyable_attribute(pmaScale, 'long', 'poseCount')

        pmaTranslate.output3D.connect(oDriven.translate)
        pmaRotate.output3D.connect(oDriven.rotate)
        #pmaScale.output3D.connect(oDriven.scale)

        inputHooks[jKey]['driven'] = oDriven
        inputHooks[jKey]['translate'] = pmaTranslate
        inputHooks[jKey]['rotate'] = pmaRotate
        #inputHooks[jKey]['scale'] = pmaScale

    return inputHooks


def auto_connect_blendshape(oBlendshapes):
    """ Pass in a list of blendshape nodes. This will connect them to the rig. """
    if DRYRUN:
        print('connecting blendshapes to rig - DRY RUN ONLY')
        return False

    hookNodes = pm.ls('*_HOOKS', type='transform')
    blendShapeTransfer = []
    for oBlendshape in oBlendshapes:
        targetBlendshapeNode = oBlendshape.name()
        sourceBlends = [x for x in oBlendshape.listHistory(future=False, levels=5) if type(x) == pm.nodetypes.BlendShape] or None
        if sourceBlends:
            sourceBlend = sourceBlends[0]
            for eachWeight in sourceBlend.weight:
                blendshapeName = pm.aliasAttr(eachWeight, q=True)
                attributeName = blendshapeName.replace('_BS','')
                try:
                    matchHooks = pm.PyNode('{}_override_MLT.outputX'.format(attributeName))
                    print(matchHooks)
                    matchHooks.connect(eachWeight, force=True)
                except:
                    pm.warning('{} failed to connect.'.format(eachWeight))


##################################################
############# POSE OPERATIONS ####################
##################################################


# These functions are for doing edit operations on _POSE nodes.
# If the _POSE is connected to the POSELOC locators, move the locators. Otherwise, set the data in the _POSE node directly.

def copy_pose(inPose, outPose):
    ''' take inPose and copy to outPose. If outPose is not specified, copy to a clipboard for pasting '''
    pass


def paste_pose(outPose):
    ''' paste to outPose from a built in pose clipboard '''
    pass


def reset_pose(inPoses):
    ''' reset a pose to 0,0,0 neutral '''
    pass


def combine_poses(inPoses, outPose):
    ''' Take a combination LIST (inPoses) of 2 or more poses and add them into a result, outPose
    An example usage would be combining mouth_wide and smile to get a wide_smile corrective pose '''

    try:
        oInPoses = [pm.PyNode(x + '_POSE') for x in inPoses]
        oOutPose = pm.PyNode(outPose + '_POSE')

    except:
        pm.warning('Your poses appear to be missing.')
        return False

    # check that all poses belong to the same zone
    allPoses = [x for x in oInPoses]
    allPoses.extend([oOutPose])
    testZones = len(set([pm.attributeQuery('zone', node=x, listEnum=1)[0] for x in oInPoses]))
    if testZones > 1:
        pm.warning('These poses are not part of the same zone')
        return False

    ignoreScaleAttrs = ['sx', 'sy', 'sz', 'sx2', 'sy2', 'sz2']

    allAttrs = [param for param in oOutPose.listAttr(keyable=True, visible=True, settable=True) if
                param.isLocked() == False]
    for eachAttr in allAttrs:
        # check that the attr does not end in ignoreScaleAttrs
        if not any(eachAttr.endswith(x) for x in ignoreScaleAttrs):
            combinedResult = sum(
                [pm.PyNode(eachAttr.name().replace(oOutPose.name(), x.name())).get() for x in oInPoses])
        else:
            combinedResult = None
            # Else we are dealing with scale, so multiply the results instead of sum()
            # TODO: Implement scale. For now, ignore it.
            # combinedResult = reduce(lambda x, y: x*y, [ pm.PyNode(eachAttr.name().replace(oOutPose.name(), x.name())).get() for x in oInPoses ])
            # if abs(combinedResult) != 1.0:
            #    print eachAttr, round(combinedResult, 6)
        if combinedResult != None:
            poseLoc = eachAttr.inputs(scn=True, plugs=True) or None
            if poseLoc:
                print poseLoc[0]
                editAttr = poseLoc[0]
            else:
                editAttr = eachAttr
            editAttr.set(combinedResult)


def capture_poses(sourceCtrls, outPose):
    ''' Take a selection of offset ctrls and move the POSELOCS to match '''

    #TODO: Implement this or remove it... This was useful for post-rigging feedback. An animator can adjust a pose and then have it feed back into the rig.
    poseName = outPose.replace('_POSE', '')
    inNamespace = sourceCtrls[0].namespace()
    for source in sourceCtrls:
        if source.getTranslation().length() + source.getRotation().length() > 0.01:
            try:
                targetName = source.name().replace(inNamespace, '').replace('_offset_ctrl', '')
                target = '{}__{}__JOINT_POSELOC'.format(targetName, poseName)
                oTarget = pm.PyNode(target)
                try:
                    oJoint = pm.PyNode(source.replace('_offset_ctrl', '_skin'))
                    oJointMove = pm.PyNode(
                        source.replace('_offset_ctrl', '_skin').replace(inNamespace, ''))
                except:
                    oJoint = pm.PyNode(source.replace('_offset_ctrl', '_jnt'))
                    oJointMove = pm.PyNode(
                        source.replace('_offset_ctrl', '_jnt').replace(inNamespace, ''))
                offsetT = oTarget.getTranslation(space='world') + (
                oJoint.getTranslation(space='world') - oJointMove.getTranslation(space='world'))
                offsetR = oTarget.getRotation() + (oJoint.getRotation() - oJointMove.getRotation())
                oTarget.setTranslation(offsetT, space='world')
                oTarget.setRotation(offsetR, space='world')
                oTarget.r.set([pm.PyNode(oTarget + x).get() + (
                pm.PyNode(oJoint + x).get() - pm.PyNode(oJointMove + x).get()) for x in
                               ['.rx', '.ry', '.rz']])
                # oTarget.setTranslation(source.getTranslation(space='world'), space='world')
                # oTarget.setRotation(source.getRotation(space='world'), space='world')
            except:
                print "{} doesn't appear to have a JOINT POSELOC.".format(source)


def mirror_pose(inPose, leftToRight=True, flip=False):
    ''' take a pose and mirror it symmetrically. ie. Copy the left side to the right side.
    If flip is True, flip both sides. '''
    pass


def split_mirror_pose(inPose, outLeftPose, outRightPose):
    ''' take a full input pose and output the left side to one pose, and the right side to another pose '''
    #TODO: Can I figure out a way to blend? Should middle controls be 0.5?
    pass


def subtract_pose(inPose1, inPose2, outPose):
    ''' take inPose1, subtract the values from inPose2, and return the result of outPose '''
    pass


def apply_poses_from_json(storedFacePoses):
    poses = import_json_dict(storedFacePoses, 'storedFacePoses')
    #TODO: I don't store empty poses. So I should have an option to ADD or REPLACE on existing poses. If it is REPLACE, then all poses should be init to 0 first. ADD would set only the poses it finds and leave the others alone. It would set the pose according to the file. It wouldn't be additive.
    if poses:
        for pose, poseAttrs in poses['poseData'].items():
            for attr, value in poseAttrs.items():
                fullAttr = '{}.{}'.format(pose, attr)
                try:
                    # If a POSELOC exists, transform it. Otherwise, set the attr directly
                    # POSELOCs are locators that drive the pose data via transforms for easy editing.
                    oAttr = pm.PyNode(fullAttr)
                except:
                    # if the attribute doesn't exist in the rig.
                    pm.warning('{} could not be found in the rig.'.format(fullAttr))
                    continue
                if oAttr:
                    try:
                        oInputs = oAttr.inputs(plugs=True)
                        if oInputs:
                            oInputs[0].set(value)
                        else:
                            oAttr.set(value)
                    except:
                        pm.warning('{} could not be set.'.format(fullAttr))


def save_all_poses(savePoseFile):
    ''' Writes out all poses to a dictionary. If the pose is 0, it leaves it empty to save data '''
    #TODO: Scale is 1,1,1. Write support for scale attributes too
    poseLocs = pm.ls('*_POSE', type='transform')
    ignoreAttrs = ['.zone', '.arbitraryAttributes'] # these are unecessary category separators and meta data

    storedFacePoses = {}
    storedFacePoses['validation'] = 'storedFacePoses'
    storedFacePoses['poseData'] = {}
    for each in poseLocs:
        storedFacePoses['poseData'][each.name()] = {}
        poseKey = storedFacePoses['poseData'][each.name()]
        # Discard 0.0 poses and save as an empty dict. It vastly lowers the amount of data stored.
        # strip the object name from poseNames
        poseNames = [str(param.rpartition('.')[-1]) for param in each.listAttr(keyable=True, visible=True, settable=True) if param not in ignoreAttrs and param.isLocked() == False and param.get() != 0]
        # round poseData to 7 to avoid unreadable scientific notation.
        poseData = [round(pm.getAttr(param), 7) for param in each.listAttr(keyable=True, visible=True, settable=True) if param not in ignoreAttrs and param.isLocked() == False and param.get() != 0]

        for eachAttr, eachValue in zip(poseNames, poseData):
            poseKey[eachAttr] = eachValue

    export_json_dict(savePoseFile, storedFacePoses, 'storedFacePoses')


##################################################
###### MAIN FACE BUILDING FUNCTION ###############
##################################################


@undo
def build_face(posemapFile):
    if DRYRUN:
        print('build face rig function - DRY RUN ONLY')
        return False

    """ Takes the input joints and zone sets and builds the poses out. """
    masterScale = 0.2
    
    oRigRoot = pm.group(em=True, n='|face_RIG')
    oSkeletonRoot = pm.group(em=True, n='face_skeleton_RIG')
    pm.parent(oSkeletonRoot, oRigRoot)
    faceMap = import_json_dict(posemapFile, 'poseMap')
    create_hooks(faceMap, masterScale)
    inputHooks = create_joint_drivers(masterScale)

    numberOfPoses = sum([len(faceMap['faceposes'][x]) for x in faceMap['faceposes'].keys()])

    gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar')
    mc.progressBar( gMainProgressBar,
            edit=True,
            beginProgress=True,
            isInterruptable=True,
            status='"Building Face Poses ...',
            maxValue=numberOfPoses)


    for zone, zonevalue in faceMap['faceposes'].items():
        for pose in zonevalue:
            poseName = pose['pose']
            poseDriver = pose['driver']
            poseRange = pose['mapping']
            # d.get() returns a specified default if the key isn't found. In this case, None
            poseOverrides = pose.get('overrides', None)
            poseOverrideMaps = pose.get('overridemaps', None)

            create_pose_node(poseName, zone, inputHooks, masterScale, poseDriver, poseRange, poseOverrides, poseOverrideMaps)
            if mc.progressBar(gMainProgressBar, query=True, isCancelled=True ):
                #TODO: Figure out how to make the undo decorator step back when break
                break
            mc.progressBar(gMainProgressBar, edit=True, step=1)
    mc.progressBar(gMainProgressBar, edit=True, endProgress=True)
    print('Face rig successfully built.')
    return True


##################################################
######### CLEANING AND OPTIMIZING ################
##################################################


def disconnect_poselocs():
    """ _POSELOC locators are for editing pose attributes using transforms.
    Once the rig is edited, they can be removed to increase rig performance.
    The POSE node can continue to be edited directly via the attributes. """
    #TODO: Eventually create a non-linear way to re-add the nodes for a pose if you want to edit it later.
    if DRYRUN:
        print('poselocs deleted - DRY RUN ONLY')
        return False

    for oPos in pm.ls('*_POSE', type='transform'):
        pm.delete(oPos.getChildren(ad=True, type='transform'))


def clean_face_rig():
    """ Runs through the rig. If the pose deltas are empty, then remove the corresponding utility nodes.
    In a typical rig this can reduce multiplyDivide nodes from 10000 to 2000. The FPS from 14 to 75!
    But this process is DESTRUCTIVE! Run this once you are sure you are done editing poses. """
    #TODO: Eventually create a non-linear way to re-add the nodes for a pose if you want to edit it later.
    if DRYRUN:
        print('clean face rig function - DRY RUN ONLY')
        return False

    def analyze_face():
        print('# All Nodes: {}'.format(len(pm.ls('*'))))
        print('# MLT Nodes: {}'.format(len(pm.ls(type='multiplyDivide'))))
        print('# MAP Nodes: {}'.format(len(pm.ls(type='remapValue'))))
        print('# JNT Nodes: {}'.format(len(pm.ls(type='joint'))))
        print('# TRS Nodes: {}'.format(len(pm.ls(type='transform'))))
        print('# ADD Nodes: {}'.format(len(pm.ls(type='plusMinusAverage'))))

    if DEBUG:
        analyze_face()

    for oPos in pm.ls('*_POSE', type='transform'):
        poseMLT = set( oPos.outputs(type='multiplyDivide') )
        for each in poseMLT:
            # track back to the MLT input to separate out each pose translate, rotate and scale.
            # sum the abs() values to see if the pose delta is empty.
            poseDelta = sum([abs(x.get()) for x in each.inputs(type='transform', plugs=True)])
            if poseDelta < 0.001:
                pm.delete(each)

    if DEBUG:
        analyze_face()

    allZones = pm.ls('*_zone', type='objectSet')
    pm.delete(allZones)
    print('The rig has been cleaned. Unused MLT and MAP nodes have been removed. Zone sets have been deleted.')
    return True


if __name__ == '__main__':
    # Development workaround for PySide winEvent error (Maya 2014)
    # Make sure the UI is deleted before recreating
    #BUG: I'm still hitting that frozen window error occasionally.
    try:
        face_tools.deleteLater()
    except:
        pass
    
    # Create minimal UI object
    face_tools = FaceTools()
    
    # Delete the UI if errors occur to avoid causing winEvent
    # and event errors (in Maya 2014)
    try:
        face_tools.create()
        face_tools.show()
    except:
        face_tools.deleteLater()
        traceback.print_exc()
