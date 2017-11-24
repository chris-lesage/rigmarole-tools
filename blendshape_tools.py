#!/usr/bin/env mayapy
# encoding: utf-8

"""
Rigmarole Blendshape Tools
author: Chris Lesage (Rigmarole Studio)
date: December 2017

A collection of utilities for working in Autodesk Maya
with blendshapes and character rigging workflows.

The [source for Rigmarole Blendshape Tools](https://github.com/chris-lesage/rigmarole-tools) is available on
GitHub.

I wrote this because Maya's "Flip Blendshape" silently corrupted my geometry
and I realized I needed some scripts I could trust and fix.

1. Split Blendshapes - I had never found a blendshape splitting tool where
you could control the falloff. Linear falloff usually causes visible seams.

2. Vertex Smash - This just sets the positions of the vertices to match
a target geo. It is especially useful when you are working in the Shape
Editor and have "Edit" enabled on a shape. It's a fast convenient way
to load a modelled shape into a blendshape which already exists without
having to delete the existing target and reload it.

More to come, including:
* working with weight maps
* soft selection falloff support
* multiple splits (not just left/right)
* splitting on a custom axis
* undo support

"""

__version__ = '0.12'
import traceback

import pymel.core as pm
import pymel.core.datatypes as dt
import maya.cmds as mc
import maya.api.OpenMaya as om
import maya.OpenMayaUI as omui
import json
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


class RigmaroleBlendshapeTools(object):
    def __init__(self):
        self.title = 'Rigmarole Blendshape Tools'
        self.name = self.title.lower().replace(' ', '_')
        self.version = __version__
        
        self.easeFunctions = {
            1: linearTween,
            2: easeInOutCubic, # 2 not implemented. Same as 3.
            3: easeInOutCubic,
            4: easeInOutQuad,
            }

        self.create_options()
        self.create_ui()
    
    def create_options(self):
        # create a node to hold option attributes in your scene.
        # An optionVar would try to remember settings between different scenes.
        # Attributes will remain even when you come back to a rig later.
        if pm.objExists('rigmarole_blendshape_tools'):
            self.optionsNode = pm.PyNode('rigmarole_blendshape_tools')
        else:
            self.optionsNode = pm.group(em=True, n='rigmarole_blendshape_tools')
        #TODO: Set up a serializer to set and get the options dictionary on the optionsNode
        self.buttons = {}
        self.options = {}
        self.options['splitBlendDegree'] = 4
        self.options['neutralGeo'] = None
        self.options['geoToSplit'] = []
        self.options['smashGeo'] = []
        self.options['numberOfSplits'] = 1
        
    
    ##################################
    ###### PySide UI Functions #######
    ##################################

    def create_ui(self):
        """Create the UI"""
        if pm.window(self.name, q=True, exists=True):
            pm.deleteUI(self.name)

        with pm.window(self.name, title='{} v{}'.format(self.title, self.version), menuBar=True) as win:
            with pm.verticalLayout() as mainLayout:
                
                pm.separator()
                pm.text(label='Split Blendshapes')
                pm.separator()

                with pm.horizontalLayout() as easeButtons:
                    # A collection of radio buttons to choose which degree of blending to use.
                    easeColl = pm.iconTextRadioCollection( 'itRadCollection' )
                    ease1 = pm.iconTextRadioButton(
                            st='iconAndTextHorizontal',
                            i1='linearCurveProfile.png',
                            label='linear 1',
                            onCommand=pm.Callback(self.set_blend_degree, 1),
                            )
                    ease3 = pm.iconTextRadioButton(
                            st='iconAndTextHorizontal',
                            i1='cone.xpm',
                            label='cubic 3',
                            onCommand=pm.Callback(self.set_blend_degree, 3),
                            )
                    ease4 = pm.iconTextRadioButton(
                            st='iconAndTextHorizontal',
                            i1='cone.xpm',
                            label='quadratic 4',
                            onCommand=pm.Callback(self.set_blend_degree, 4),
                            sl=True,
                            )
                pm.separator()

                with pm.horizontalLayout() as neutralLayout:
                    neutralLoad = pm.button(
                        label='Select Neutral Geo',
                        command=pm.Callback(self.load_neutral_geo),
                        )
                    self.buttons['neutralField'] = pm.textField()
                    #shapeOrigLoad = pm.button(label='Choose ShapeOrig')
                neutralLayout.redistribute(10, 50)

                with pm.horizontalLayout() as geoToSplitLayout:
                    neutralLoad = pm.button(
                        label='Select Split Geo',
                        command=pm.Callback(self.load_blendshapes_to_split),
                        )
                    self.buttons['splitField'] = pm.textField()
                geoToSplitLayout.redistribute(10, 50)

                with pm.horizontalLayout() as numberOfSplitsLayout:
                    label = pm.text(label='Number of splits')
                    self.buttons['numberOfSplits'] = pm.intField(
                        value=1,
                        changeCommand=pm.Callback(self.change_splits),
                        )
                    self.buttons['numSplitsSlider'] = pm.intSlider(value=1, minValue=1, maxValue=8,
                        changeCommand=pm.Callback(self.change_splits_slider),
                        )
                    neutralLoad = pm.button(
                        label='Create Split Helpers',
                        command=pm.Callback(self.create_split_helpers),
                        )
                numberOfSplitsLayout.redistribute(10, 5, 35, 10)

                btn = pm.button(
                    label='Split Blendshapes',
                    command=pm.Callback(self.template_btn, 'split', self.split_blendshapes_btn),
                    )

                pm.separator()
                pm.text(label='Vertex Smash')
                pm.separator()

                with pm.horizontalLayout() as smashLayout:
                    chooseBtn = pm.button(
                        label='Choose Geo to Change:',
                        command=pm.Callback(self.choose_smash),
                        )
                    self.buttons['smashField'] = pm.textField()
                    #TODO: Allow user to edit this field with text, and validate the input for existing geo.
                    btn = pm.button(
                        label='Vertex Smash',
                        command=pm.Callback(self.template_btn, 'vertex smash', self.vertex_smash_btn),
                        )
                smashLayout.redistribute(10, 40, 10)

            mainLayout.redistribute(10, 10, 10, 10, 20, 20, 20, 20, 20, 10, 10, 10, 20)
        pm.showWindow()


    #--------------------------------------------------------------------------
    # SLOTS
    #--------------------------------------------------------------------------

    def choose_smash(self):
        smashField = self.buttons['smashField']
        if pm.selected():
            smashField.setText(pm.selected()[0].name())
            self.options['smashGeo'] = pm.selected()[0]
        else:
            pm.warning('Please select geometry you wish to vertex smash.')
        

    def load_neutral_geo(self):
        neutralField = self.buttons['neutralField']
        if pm.selected():
            neutralField.setText(pm.selected()[0].name())
            self.options['neutralGeo'] = pm.selected()[0]
        else:
            pm.warning('Please select geometry to use as neutral')
   
    def load_blendshapes_to_split(self):
        splitField = self.buttons['splitField']
        if pm.selected():
            splitField.setText(', '.join([x.name() for x in pm.selected()]))
            self.options['geoToSplit'] = pm.selected()
        else:
            pm.warning('Please select geometry to use as neutral')

    def change_splits_slider(self):
        numSplitsSlider = self.buttons['numSplitsSlider']
        numSplitsField = self.buttons['numberOfSplits']
        print(numSplitsSlider.getValue())
        numSplitsField.setValue(numSplitsSlider.getValue())
        self.options['numberOfSplits'] = numSplitsSlider.getValue()

    def change_splits(self):
        numSplitsSlider = self.buttons['numSplitsSlider']
        numSplitsField = self.buttons['numberOfSplits']
        self.options['numberOfSplits'] = numSplitsField.getValue()

    def create_split_helpers(self):
        numSplits = self.options['numberOfSplits']
        print('#TODO: Create locators with {} splits'.format(numSplits))
   
    def set_blend_degree(self, degree):
        self.options['splitBlendDegree'] = degree
        print('degree: {}'.format(degree))

    def template_btn(self, message, func):
        #print(message)
        func()

    def vertex_smash_btn(self):
        # First select the geo you want to match, then select the geo you want to change.
        geo = self.options['smashGeo']
        #TODO: Implement support for component and soft selections
        target = pm.selected()[0]
        self.vertex_smash(geo, target)

    def split_blendshapes_btn(self):
        #TODO: Set all of these options in the GUI or by selection
        #TODO: Add a way to interact with this by script too. Not just GUI.

        if self.options['neutralGeo']:
            neutral = self.options['neutralGeo']
        else:
            pm.warning('First select a neutral geometry')
            return False

        #TODO: Set up some more checks to make sure topology of current selection matches neutral geo
        #TODO: Collect all warnings together instead of individual errors. Let the user know everything they are missing.
        #TODO: Support multiple selections? Might need multiple neutral geo. Imagine eyebrows, eyelashes, etc. It would be tedious to select each neutral separately. OR have a pair-matched list?
        geoToSplit = self.options['geoToSplit']
        if not geoToSplit:
            pm.warning('Select geometry to be split')
            return False
        else:
            for eachSplit in geoToSplit:
                if len(eachSplit.vtx) != len(neutral.vtx):
                    pm.warning('The topology between {} and your shape do not seem to match.'.format(eachSplit.name()))
                    return False

        neutralBB = neutral.getBoundingBox()

        #TODO: Set up a width_indicator rig widget to visualize how things will split.
        width = abs(pm.PyNode('width_indicator').tx.get())
        
        pm.delete(pm.ls('ZZZ_OUTPUT*'))
        for i, eachSplit in enumerate(geoToSplit):
            #TODO: Add a scheme which creates temporary shapes. Then, once you are happy with the result you "commit" and it names them properly for you. This way you can test, iterate and then keep your changes and do the next split. But before you commit, the script keeps deleting the temp shapes.
            leftResult = pm.duplicate(neutral, n='ZZZ_OUTPUT_{}_Left'.format(eachSplit.name()))[0]
            rightResult = pm.duplicate(neutral, n='ZZZ_OUTPUT_{}_Right'.format(eachSplit.name()))[0]
            leftResult.setTranslation(eachSplit.getTranslation())
            rightResult.setTranslation(eachSplit.getTranslation())
            degree = self.options['splitBlendDegree']
            self.split_blendshapes(leftResult, rightResult, eachSplit, neutral, width, degree)
            leftResult.tx.set(neutralBB.width() * 1.2)
            rightResult.tx.set(neutralBB.width() * -1.2)


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
        selection = om.MSelectionList()
        dagPath = om.MDagPath()
        try:
            selection.add(geo.name())
            dagPath = selection.getDagPath(0)
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

        #TODO: Add space as an option
        space = om.MSpace.kObject
        try:
            # initialize a geometry iterator for the geos
            geoIterLeft = om.MFnMesh(dagPathLeft)
            geoIterRight = om.MFnMesh(dagPathRight)
            geoIter1 = om.MFnMesh(dagPath1)
            geoIter2 = om.MFnMesh(dagPath2)

            # get the positions of all the vertices in chosen space
            pArrayLeft = geoIterLeft.getPoints(space)
            pArrayRight = geoIterRight.getPoints(space)
            pArray1 = geoIter1.getPoints(space)
            pArray2 = geoIter2.getPoints(space)

            width += 0.0001 # protect from division by zero
            # iterate over one of the neutral geometries to get clean xpos readings.
            for i in xrange(geoIterLeft.numVertices):
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
            geoIterLeft.setPoints(pArrayLeft)
            geoIterRight.setPoints(pArrayRight)
            geoIterLeft.updateSurface()
            geoIterRight.updateSurface()
        except: raise


    @timer
    def vertex_smash(self, geoObject, geoTarget):
        """ Move the vertices of one geo to match the other geo
        This is especially used for loading blendshapes when 'Edit' is enabled in the Shape Editor """
        # get the dag path for the shapeNode using an API selection list
        dagPath = self.get_dagpath(geoObject)
        dagPath2 = self.get_dagpath(geoTarget)

        space = om.MSpace.kObject

        try:
            #TODO: Include world/local as space options
            # initialize a geometry iterator for both geos
            geoIter = om.MFnMesh(dagPath)
            geoIter2 = om.MFnMesh(dagPath2)
            # get the positions of all the vertices in world space
            pArray2 = geoIter2.getPoints(space)
            # update the surface of the geometry with the changes
            geoIter.setPoints(pArray2)
            geoIter.updateSurface()
        except: raise


# Create UI object
blendshape_tools = RigmaroleBlendshapeTools()
