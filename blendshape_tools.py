#!/usr/bin/env mayapy
# encoding: utf-8

__version__ = '0.10'
#import traceback

#TODO: Check out that shim thing someone published on Github
try:
    import PySide2.QtCore as QtCore
    import PySide2.QtGui as QtGui
    import PySide2.QtWidgets as QtWidgets
except ImportError:
    print("failed to import PySide2, {}".format(__file__))
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtGui
    import PySide.QtWidgets as QtWidgets

try:
    # future proofing for Maya 2017.
    from shiboken2 import wrapInstance
except ImportError:
    from shiboken import wrapInstance

import pymel.core as pm
import pymel.core.datatypes as dt
import maya.cmds as mc
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import time

from functools import wraps


#TODO: Implement undo for the OM mesh functions. Right now it is a one-way function. Quite dangerous.

def undo(func):
    """Puts the wrapped `func` into a single Maya Undo action, then
    undoes it when the function enters the finally: block
    from schworer Github
    """
    @wraps(func) # by using wraps, the decorated function maintains its name and docstring.
    def _undofunc(*args, **kwargs):
        try:
            # start an undo chunk
            mc.undoInfo(ock=True)
            return func(*args, **kwargs)
        finally:
            # after calling the func, end the undo chunk
            mc.undoInfo(cck=True)
    return _undofunc


def timer(func):
    """ Puts the wrapped func into a timer for profiling """
    @wraps(func)
    def _timerfunc(*args, **kwargs):
        try:
            timeStart = time.clock()
            return func(*args, **kwargs)
        finally:
            # stop the timer
            timeStop = time.clock()
            print('{} execution time: {} seconds.'.format(func.__name__, timeStop-timeStart))
    return _timerfunc
            

# easing functions from Robert Penner
def linearTween(t, b, c, d):
    return c*t/d + b

def easeInOutCubic(t, b, c, d):
    t /= d/2
    if t < 1:
        return c/2*t*t*t + b
    t -= 2
    return c/2*(t*t*t + 2) + b

def easeInOutQuad(t, b, c, d):
    t /= d/2
    if t < 1:
        return c/2*t*t + b
    t-=1
    return -c/2 * (t*(t-2) - 1) + b


def maya_main_window():
    """Return the Maya main window widget as a Python object."""
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class RigmaroleBlendshapeTools(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(RigmaroleBlendshapeTools, self).__init__(parent)
        self.easeFunctions = {
            1: linearTween,
            2: easeInOutCubic, # 2 not implemented. Same as 3.
            3: easeInOutCubic,
            4: easeInOutQuad,
            }

    ##################################
    ###### PySide UI Functions #######
    ##################################

    def create_ui(self):
        """Create the UI"""
        self.setWindowTitle('Title Here v' + __version__)
        self.resize(280, 160)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.create_controls()
        self.create_layout()

    def create_controls(self):
        """Create the widgets and signals for the dialog"""

        cRed    = '745a54'
        cBlue   = '5d5d6a'
        cGreen  = '597a59'
        borderStyle = 'border:1px solid #3a3a3a'

        self.addButtons = {}
        eachButton = 'Split Blendshapes'
        #TODO Set up a button construction function
        self.addButtons[eachButton] = QtWidgets.QPushButton('{} Button'.format(eachButton))
        self.addButtons[eachButton].clicked.connect(self.template_btn(eachButton, self.split_blendshapes_btn))
        self.addButtons[eachButton].setStyleSheet(
                '{}; padding:5px; max-width:180px;\
                background-color: #{}; color: #eee;'.format(borderStyle, cBlue))

        eachButton = 'Vertex Smash'
        self.addButtons[eachButton] = QtWidgets.QPushButton('{} Button'.format(eachButton))
        self.addButtons[eachButton].clicked.connect(self.template_btn(eachButton, self.vertex_smash_btn))
        self.addButtons[eachButton].setStyleSheet(
                '{}; padding:5px; max-width:180px;\
                background-color: #{}; color: #eee;'.format(borderStyle, cBlue))

    def create_layout(self):
        """Create the layouts and add widgets"""

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(*[6]*4)

        flatStyle = True  # False draws a border around the whole section
        groupFont = QtGui.QFont('Helvetica Neue', 10, QtGui.QFont.Bold)
        labelFont=QtGui.QFont()
        #labelFont.setBold(True)
        groupPadding = 4  # padding at top and bottom of each section
        groupSpacing = 4  # the space between each section

        guideGroup = QtWidgets.QGroupBox('Group Title Here')
        guideGroup.setFlat(flatStyle)
        guideGroup.setFont(groupFont)

        buttonLayout = QtWidgets.QVBoxLayout()
        buttonLayout.setAlignment(QtCore.Qt.AlignLeft)
        buttonLayout.setAlignment(QtCore.Qt.AlignBottom)
        buttonLayout.setContentsMargins(*[2]*4)

        for eachButton in self.addButtons.values():
            buttonLayout.addWidget(eachButton)
        guideGroup.setLayout(buttonLayout)

        mainLayout.addWidget(guideGroup)
        mainLayout.addSpacing(groupSpacing)
        mainLayout.addStretch()

        self.setLayout(mainLayout)


    #--------------------------------------------------------------------------
    # SLOTS
    #--------------------------------------------------------------------------

    def template_btn(self, message, func):
        # def do() a tip from Mattias so I don't have to use lambda to pass
        # arguments to a button signal. But I don't know why it works.
        def do():
            sender = self.sender()
            #print(message)
            func()
        return do

    def vertex_smash_btn(self):
        # First select the geo you want to match, then select the geo you want to change.
        target, geo = pm.selected()[0:2]
        self.vertex_smash(geo, target)

    def split_blendshapes_btn(self):
        #TODO: Set all of these options in the GUI or by selection
        #TODO: Add a way to interact with this by script too. Not just GUI.
        # create a sphere and add noise
        pm.delete(pm.ls('ZZZ_OUTPUT*'))

        #TODO: Set up a width_indicator rig widget to visualize how things will split.
        width = abs(pm.PyNode('width_indicator').tx.get())
        sculpted = pm.PyNode('sphere_deformed')
        neutral = pm.PyNode('sphere_neutral')

        leftSplit = pm.duplicate(neutral, n='ZZZ_OUTPUT_blendshape_Left')[0]
        rightSplit = pm.duplicate(neutral, n='ZZZ_OUTPUT_blendshape_Right')[0]
        leftSplit.setTranslation(sculpted.getTranslation())
        rightSplit.setTranslation(sculpted.getTranslation())
        leftSplit.v.set(1)
        rightSplit.v.set(1)
        self.split_blendshapes(leftSplit, rightSplit, sculpted, neutral, width, 4)
        leftSplit.tx.set(12)
        rightSplit.tx.set(-12)
        

    #################################
    ####### Rigging Functions #######
    #################################

    def get_midpoint(self, vecA, vecB, weight=0.5):
        """Helper to get middle point between two vectors. Weight is 0.0 to 1.0 blend between the two.
        So for example, 0.0 would return the position of oObject1. 1.0 would be oObject2. 0.5 is halfway."""
        vecC = vecB-vecA
        vecD = vecC * weight # 0.5 is default which finds the mid-point.
        vecE = vecA + vecD
        return vecE

    def get_dagpath(self, geo):
        # get the dag path for the shapeNode using an API selection list
        selectionLeft = om.MSelectionList()
        dagPath = om.MDagPath()
        try:
            selectionLeft.add(geo)
            selectionLeft.getDagPath(0, dagPath)
        except: raise
        return dagPath
        
    @timer
    def split_blendshapes(self, geoSplitLeft, geoSplitRight, geoSculpt, geoNeutral, width, degree):
        """ Take a deformed mesh a neutral mesh and create a left and right split for blendshape creation.
        To be fairly safe, it first duplicates the neutral geometry and then modifies the duplicates. """
        #TODO: Grab the neutral geometry from the shapeOrig? So I can work in-pose
        #TODO: Design these functions to work well with the Shape Editor if possible.
        #TODO: Auto set up a test blendshape so you can scrub and test the result quickly.

        easeFunction = self.easeFunctions[degree]
        
        # THE SPLIT RESULT LEFT
        dagPathLeft = self.get_dagpath(geoSplitLeft)
        # THE SPLIT RESULT RIGHT
        dagPathRight = self.get_dagpath(geoSplitRight)
        # THE SCULPTED SHAPE
        dagPath1 = self.get_dagpath(geoSculpt)
        # THE NEUTRAL BASE SHAPE
        dagPath2 = self.get_dagpath(geoNeutral)
        
        try:        
            # initialize a geometry iterator for the geos
            geoIterLeft = om.MItGeometry(dagPathLeft)
            geoIterRight = om.MItGeometry(dagPathRight)
            geoIter1 = om.MItGeometry(dagPath1)
            geoIter2 = om.MItGeometry(dagPath2)
            # get the positions of all the vertices in world space
            pArrayLeft = om.MPointArray()
            pArrayRight = om.MPointArray()
            pArray1 = om.MPointArray()
            pArray2 = om.MPointArray()

            #TODO: Add space as an option
            space = om.MSpace.kObject
            geoIterLeft.allPositions(pArrayLeft, space) # the split.
            geoIterRight.allPositions(pArrayRight, space) # the split.
            geoIter1.allPositions(pArray1, space) # the sculpt
            geoIter2.allPositions(pArray2, space) # the neutral base
            
            width += 0.0001 # protect from division by zero
            # iterate over one of the neutral geometries to get clean xpos readings.
            for i in xrange(pArrayLeft.length()):
                # this bit normalizes the x position relative to the width.
                # Anything below width will be 0.0. Anything above will be 1.0
                # Anything between the width will blend with the chosen easeInOut curve.
                xpos = pArrayLeft[i].x
                xposNormalized = ((xpos/width) + 1.0) * 0.5
                xposClamped = sorted([xposNormalized, 0.0, 1.0])[1]
                # the weight result is a value from 0.0 to 1.0
                weight = easeFunction(xposClamped, 0.0, 1.0, 1.0)

                leftVector = self.get_midpoint(pArrayLeft[i], pArray1[i], weight)
                rightVector = self.get_midpoint(pArrayLeft[i], pArray1[i], -weight + 1.0)
                pArrayLeft[i].x = leftVector.x
                pArrayLeft[i].y = leftVector.y
                pArrayLeft[i].z = leftVector.z
                pArrayRight[i].x = rightVector.x
                pArrayRight[i].y = rightVector.y
                pArrayRight[i].z = rightVector.z
            
            # update the surface of the geometry with the changes
            geoIterLeft.setAllPositions(pArrayLeft)
            geoIterRight.setAllPositions(pArrayRight)
            meshFn = om.MFnMesh(dagPathLeft)
            meshFn.updateSurface()
            meshFn = om.MFnMesh(dagPathRight)
            meshFn.updateSurface()
        except: raise


    @timer
    def vertex_smash(self, geoObject, geoTarget):
        """ Move the vertices of one geo to match the other geo
        This is especially used for loading blendshapes when 'Edit' is enabled in the Shape Editor """
        # get the dag path for the shapeNode using an API selection list
        dagGeo = self.get_dagpath(geoObject)
        dagTarget = self.get_dagpath(geoTarget)
        
        try:        
            #TODO: Include world/local as space options
            # initialize a geometry iterator for both geos
            geoIter = om.MItGeometry(dagGeo)
            geoIter2 = om.MItGeometry(dagTarget)
            # get the positions of all the vertices in world space
            pArray = om.MPointArray()
            pArray2 = om.MPointArray()
            geoIter.allPositions(pArray)
            geoIter2.allPositions(pArray2)
            # update the surface of the geometry with the changes
            geoIter.setAllPositions(pArray2)
            meshFn = om.MFnMesh(dagGeo)
            meshFn.updateSurface()
        except: raise


#TODO: Clean up this ridiculous mess. What is the best way to load PySide UIs?
# Development workaround for PySide winEvent error (Maya 2014)
# Make sure the UI is deleted before recreating
try:
    blendshape_tools
    blendshape_tools.deleteLater()
except NameError:
    pass

# Create UI object
blendshape_tools = RigmaroleBlendshapeTools()

# Delete the UI if errors occur to avoid causing winEvent and event errors
try:
    blendshape_tools.create_ui()
    blendshape_tools.show()
except:
    traceback.print_exc()
    blendshape_tools.deleteLater()
