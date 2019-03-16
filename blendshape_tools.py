
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

IDEAS:
- "Make shape live". Imagine you have a sculpted smile. A static mesh. Save that shape. Neutralize it, and then store the saved shape as a temporary blendshape on the neutralized mesh. That way, you can erase or delta smooth the shape relative to whatever neutral geo you chose.
"""

__version__ = '0.14'
import traceback

import pymel.core as pm
import pymel.core.datatypes as dt
import maya.cmds as mc
import maya.OpenMaya as omo # Open Maya Old
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

def lerp_values(lower, upper, segments, inclusive=True):
    ''' lerp values and optionally include the first and last values '''
    if segments == 1:
        yield (lower + upper) * 0.5
    else:
        for each in xrange(segments):
            if each in [0, segments-1] and not inclusive:
                pass
            else:
                yield (each / float(segments-1)) * (float(upper)-float(lower)) + lower


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
        #TODO: Set up a serializer to set and get the options dictionary on the optionsNode
        self.buttons = {}
        self.options = {}
        self.options['splitBlendDegree'] = 4
        self.options['softness'] = 0.0
        self.options['neutralGeo'] = None
        self.options['geoToSplit'] = []
        self.options['splitMarkers'] = []
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

                with pm.horizontalLayout() as geoToSplitLayout:
                    neutralLoad = pm.button(
                        label='Select Split Markers',
                        command=pm.Callback(self.load_split_markers),
                        )
                    self.buttons['splitMarkersField'] = pm.textField()
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

                with pm.horizontalLayout() as softnessLayout:
                    label = pm.text(label='Softness')
                    self.buttons['softnessLevel'] = pm.floatField(
                        value=0.0,
                        changeCommand=pm.Callback(self.change_splits),
                        precision=2,
                        )
                    self.buttons['softnessSlider'] = pm.intSlider(value=0, minValue=0, maxValue=100,
                        changeCommand=pm.Callback(self.change_softness_slider),
                        )
                softnessLayout.redistribute(10, 5, 45)

                btn = pm.button(
                    label='Split Blendshapes',
                    command=pm.Callback(self.template_btn, 'split', self.split_blendshapes_btn),
                    )

                btn = pm.button(
                    label='Split Blendshapes By Soft Selection',
                    command=pm.Callback(self.template_btn, 'split', self.split_blendshapes_by_selection_btn),
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

            mainLayout.redistribute(10, 10, 10, 10, 20, 20, 20, 20, 20, 20, 20, 20, 10, 10, 10, 20)
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

    def load_split_markers(self):
        markerField = self.buttons['splitMarkersField']
        if pm.selected():
            markerField.setText(', '.join([x.name() for x in pm.selected()]))
            self.options['splitMarkers'] = pm.selected()
        else:
            pm.warning('Please select objects or locators to use as split markers.')
            


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
        if self.options['neutralGeo']:
            neutralBB = self.options['neutralGeo'].getBoundingBox()
        else:
            neutralBB = dt.BoundingBox()
            neutralBB.expand([-5.0, -5.0, -5.0])
            neutralBB.expand([5.0, 5.0, 5.0])
        splitHelpers = []
        for i, each in enumerate(lerp_values(neutralBB.min()[0], neutralBB.max()[0], numSplits)):
            oLoc = pm.spaceLocator(n='width_indicator_{}'.format(i+1))
            oLoc.localScale.set(0, neutralBB.height() * 1.5, 0)
            oLoc.localPositionZ.set(neutralBB.max()[2] + 0.5)
            oLoc.tx.set(each)
            splitHelpers.append(oLoc)
        if self.options['splitMarkers'] == []:
            self.buttons['splitMarkersField'].setText(', '.join([x.name() for x in splitHelpers]))
            self.options['splitMarkers'] = splitHelpers
   
    def change_softness_slider(self):
        softnessLevel = float(self.buttons['softnessSlider'].getValue()) * 0.01
        self.buttons['softnessLevel'].setValue(softnessLevel)
        self.options['softness'] = softnessLevel

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

    def split_blendshapes_by_selection_btn(self):
        #TODO: Set all of these options in the GUI or by selection
        #TODO: Add a way to interact with this by script too. Not just GUI.
        #TODO: Clean up the UX on this process.

        if self.options['neutralGeo']:
            neutral = self.options['neutralGeo']
        else:
            pm.warning('First select a neutral geometry')
            return False

        neutralBB = neutral.getBoundingBox()
        if pm.selected():
            geoToSplit = pm.PyNode(self.find_node_by_component(pm.selected())).getTransform()
        else:
            pm.warning('Nothing selected. This function works on a vertex selection. Please select vertices.')
            return False

        pm.delete(pm.ls('ZZZ_OUTPUT*'))
        positiveResult = pm.duplicate(neutral, n='ZZZ_OUTPUT_{}_Positive'.format(geoToSplit.name()))[0]
        negativeResult = pm.duplicate(neutral, n='ZZZ_OUTPUT_{}_Negative'.format(geoToSplit.name()))[0]
        # unlock translate. Common use is to duplicate a geo who is skinned and blendshaped.
        for eachGeo in [positiveResult, negativeResult]:
            eachGeo.tx.unlock()
            eachGeo.ty.unlock()
            eachGeo.tz.unlock()
        positiveResult.setTranslation(geoToSplit.getTranslation())
        negativeResult.setTranslation(geoToSplit.getTranslation())
        self.split_blendshapes_by_selection(positiveResult, negativeResult, geoToSplit, neutral)
        positiveResult.tx.set(neutralBB.width() * 1.2)
        negativeResult.tx.set(neutralBB.width() * -1.2)


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

        #TODO: Major feature: Imagine football lips. Those need to be split in 2 or more overlapping stages. Either the user needs a way to easily script this, or think of UI/UX ways to make this a simple thing to do multiple stages of splits. For instance, split the soft center of the football lips. Then hard split the symmetry of the remainder to get the 2 corners. How could you approach this?

        # get all the split lines and their positions
        splitLines = self.options['splitMarkers']
        if not splitLines:
            pm.warning('Please select objects or locators to use as split markers')
            return False
        splitLinesPos = [each.getTranslation(space='world')[0] for each in splitLines]
        # tack None on to the ends of the list. When it is None, the weight will interpolate out forever.
        splitLinesSorted = [None] + sorted(splitLinesPos) + [None]
        # pair up [0,1,2], [1,2,3], [2,3,4], etc.
        splitLinesPairs = zip(splitLinesSorted, splitLinesSorted[1:], splitLinesSorted[2:])

        #TODO: Add softness as a GUI option
        # define a bit of bleed over past the split line edges.
        #TODO: There is a flaw. If softness is soft enough to bleed over 3 shapes, you get an additive accumulation. :<
        softness = self.options['softness']
        degree = self.options['splitBlendDegree']
        # if there are not multiple splits (ie. just a symmetry split) then softness bleed isn't needed. TODO: TEST THAT ASSUMPTION
        if len(splitLines) < 3: softness = 0.0

        pm.delete(pm.ls('ZZZ_OUTPUT*'))
        for geoCounter, eachSplit in enumerate(geoToSplit):
            for splitCount, (lower, mid, upper) in enumerate(splitLinesPairs):
                #TODO: Add a scheme which creates temporary shapes. Then, once you are happy with the result you "commit" and it names them properly for you. This way you can test, iterate and then keep your changes and do the next split. But before you commit, the script keeps deleting the temp shapes.
                resultGeo = pm.duplicate(neutral, n='ZZZ_OUTPUT_{}_{}'.format(eachSplit.name(), geoCounter+1))[0]
                resultGeo.setTranslation(eachSplit.getTranslation())
                self.split_blendshapes(resultGeo, eachSplit, neutral, lower, mid, upper, softness, degree)
                resultGeo.tx.set((neutralBB.width() * 1.2) * (splitCount+1))


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
        selection.add(geo.name())
        dagPath = selection.getDagPath(0)
        return dagPath

    def find_node_by_component(self, geo):
        ''' assumes a component selection and gets first index. Might be a better way to do this. '''
        selection = om.MSelectionList()
        dagPath = om.MDagPath()
        selection.add(geo[0].name())
        dagPath = selection.getDagPath(0)
        return dagPath.fullPathName()

    def hard_selection_weights(self):
        ''' create and return a list of the selection weights. Selected = 1.0
        Unselected = 0.0. This is used instead of soft selection when that mode is turned off. '''
        #TODO: Would be nice to rewrite this using the new API. Low priority.
        #TODO: Debug on multiple selections

        # temporary hack. Turn off symmetry when reading MRichSelection until I learn to use symmetry.
        # as far as my tests go, this maintains the symmetrical selection but reads it like a whole selection.
        # otherwise, only one half will be reading by MRichSelection. How does getSymmetry() work?
        symmetryOn = mc.symmetricModelling(q=True, symmetry=True)
        if symmetryOn:
            mc.symmetricModelling(e=True, symmetry=False)

        selection = omo.MSelectionList()
        omo.MGlobal.getActiveSelectionList(selection)
        dagPath = omo.MDagPath()
        component = omo.MObject()
        stat = selection.getDagPath(0, dagPath, component)
        compFn = omo.MFnSingleIndexedComponent(component)
        geoIter = omo.MItGeometry(dagPath)
        selectedIds = omo.MIntArray()
        compFn.getElements(selectedIds)

        pointCount = geoIter.exactCount()
        weightArray = [0.0] * pointCount

        for element in selectedIds:
            weightArray[element] = 1.0

        # Put the symmetry back to the way it was.
        mc.symmetricModelling(e=True, symmetry=symmetryOn)
        return weightArray


    def soft_selection_weights(self):
        ''' create and return a list of the soft selection weights '''
        #TODO: Would be nice to rewrite this using the new API. Low priority.
        #TODO: Debug on multiple selections

        # temporary hack. Turn off symmetry when reading MRichSelection until I learn to use symmetry.
        # as far as my tests go, this maintains the symmetrical selection but reads it like a whole selection.
        # otherwise, only one half will be reading by MRichSelection. How does getSymmetry() work?
        symmetryOn = mc.symmetricModelling(q=True, symmetry=True)
        if symmetryOn:
            mc.symmetricModelling(e=True, symmetry=False)

        selection = omo.MSelectionList()
        softSelection = omo.MRichSelection()
        omo.MGlobal.getRichSelection(softSelection)
        #softSelection.getSymmetry(selection)
        softSelection.getSelection(selection)

        dagPath = omo.MDagPath()
        selection.getDagPath(0, dagPath)
        component = omo.MObject()
        geoIter = omo.MItGeometry(dagPath)
        pointCount = geoIter.exactCount()
        #TODO: MFloatArray and MDoubleArray had strange inconsistencies. But a list might be slow.
        weightArray = [0.0] * pointCount

        iter = omo.MItSelectionList(selection, omo.MFn.kMeshVertComponent)
        #NOTE: since I commented out the while loop, this should just work on the first selected transform.
        #while not iter.isDone():
        iter.getDagPath(dagPath, component)
        fnComp = omo.MFnSingleIndexedComponent(component)
        if fnComp.hasWeights():
            for i in range(fnComp.elementCount()):
                element = fnComp.element(i)
                weight = fnComp.weight(i).influence()
                invert = -weight + 1.0
                weightArray[element] = weight
        #iter.next()

        # Put the symmetry back to the way it was.
        mc.symmetricModelling(e=True, symmetry=symmetryOn)
        return weightArray


    @timer
    def split_blendshapes_by_selection(self, positiveGeo, negativeGeo, geoSculpt, geoNeutral):
        """ Take a deformed mesh a neutral mesh and create a split based on a soft component selection."""

        # Query if in soft mode AND component selection mode.
        useWeights = False
        softSelectionOn = mc.softSelect(q=True, sse=True)
        componentMode = mc.selectMode(q=True, component=True)
        if componentMode:
            if softSelectionOn:
                weightMap = self.soft_selection_weights()
            else:
                weightMap = self.hard_selection_weights()
        else:
            pm.warning('This function works with a vertex selection. Please select vertices.')
            return False

        # THE SPLIT RESULT LEFT
        dagPathLeft = self.get_dagpath(positiveGeo)
        # THE SPLIT RESULT RIGHT
        dagPathRight = self.get_dagpath(negativeGeo)
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

            # iterate over one of the neutral geometries to get clean xpos readings.
            for i in xrange(geoIterLeft.numVertices):
                # the weight result is a value from 0.0 to 1.0
                weight = weightMap[i]

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
    def split_blendshapes(self, geoResult, geoDelta, geoNeutral, lower, mid, upper, softness, degree):
        """ Take a deformed mesh a neutral mesh and create a left and right split for blendshape creation.
        To be fairly safe, it first duplicates the neutral geometry and then modifies the duplicates. """
        #TODO: Grab the neutral geometry from the shapeOrig? So I can work in-pose
        #TODO: Design these functions to work well with the Shape Editor if possible.
        #TODO: Auto set up a test blendshape so you can scrub and test the result quickly.

        # split the interpolation into 2 segments for ease in and ease out.
        # This is a little bit hacky and bad and you should feel bad.
        # | width1  |  width2  |
        useWeight1 = True
        useWeight2 = True
        if lower == None:
            useWeight1 = False
        else:
            width1 = (mid-lower)
            lower1 = lower - (width1 * softness)
            upper1 = mid + (width1 * softness)
            width1 = (upper1-lower1)
            # protect from division by zero
            width1 += 0.0001
        if upper == None:
            useWeight2 = False
        else:
            width2 = (upper-mid)
            lower2 = mid - (width2 * softness)
            upper2 = upper + (width2 * softness)
            width2 = (upper2-lower2)
            # protect from division by zero
            width2 += 0.0001

        easeFunction = self.easeFunctions[degree]

        # THE SPLIT RESULT
        dagPathResult = self.get_dagpath(geoResult)
        # THE SCULPTED SHAPE
        dagPath1 = self.get_dagpath(geoDelta)
        # THE NEUTRAL BASE SHAPE
        dagPath2 = self.get_dagpath(geoNeutral)

        #TODO: Add space as an option
        space = om.MSpace.kObject
        try:
            # initialize a geometry iterator for the geos
            geoIterResult = om.MFnMesh(dagPathResult)
            geoIter1 = om.MFnMesh(dagPath1)
            geoIter2 = om.MFnMesh(dagPath2)

            # get the positions of all the vertices in chosen space
            pArrayResult = geoIterResult.getPoints(space)
            pArray1 = geoIter1.getPoints(space)
            pArray2 = geoIter2.getPoints(space)

            # iterate over one of the neutral geometries to get clean xpos readings.
            for i in xrange(geoIterResult.numVertices):
                # this bit normalizes the x position relative to the width.
                # Anything below width will be 0.0. Anything above will be 1.0
                # Anything between the width will blend with the chosen easeInOut curve.

                xpos = pArrayResult[i].x
                if useWeight1:
                    xposNormalized1 = ((xpos/width1) + 1.0) - (upper1/width1)
                    xposClamped1 = sorted([xposNormalized1, 0.0, 1.0])[1]
                    weight1 = easeFunction(xposClamped1, 0.0, 1.0, 1.0)
                else:
                    weight1 = 1.0
                if useWeight2:
                    xposNormalized2 = ((xpos/width2) + 1.0) - (upper2/width2)
                    xposClamped2 = sorted([xposNormalized2, 0.0, 1.0])[1]
                    weight2 = easeFunction(xposClamped2, 0.0, 1.0, 1.0)
                    weight2 = -weight2 + 1.0
                else:
                    weight2 = 1.0

                # blend the results together. The 2 ends are 1, so they don't ease out.
                weight = weight1 * weight2

                leftVector = self.get_midpoint(pArrayResult[i], pArray1[i], weight)
                pArrayResult[i].x = leftVector.x
                pArrayResult[i].y = leftVector.y
                pArrayResult[i].z = leftVector.z

            # update the surface of the geometry with the changes
            geoIterResult.setPoints(pArrayResult)
            geoIterResult.updateSurface()
        except: raise


    @timer
    def vertex_smash(self, geoObject, geoTarget):
        """ Move the vertices of one geo to match the other geo
        This is especially used for loading blendshapes when 'Edit' is enabled in the Shape Editor """
        # get the dag path for the shapeNode using an API selection list
        dagPath = self.get_dagpath(geoObject)
        dagPath2 = self.get_dagpath(geoTarget)

        # Query if in soft mode AND component selection mode.
        useWeights = False
        softSelectionOn = mc.softSelect(q=True, sse=True)
        componentMode = mc.selectMode(q=True, component=True)
        if componentMode:
            if softSelectionOn:
                weightMap = self.soft_selection_weights()
            else:
                weightMap = self.hard_selection_weights()
            useWeights = True

        space = om.MSpace.kObject

        try:
            #TODO: Include world/local as space options
            # initialize a geometry iterator for both geos
            geoIter1 = om.MFnMesh(dagPath)
            geoIter2 = om.MFnMesh(dagPath2)
            # get the positions of all the vertices in world space
            pArray1 = geoIter1.getPoints(space)
            pArray2 = geoIter2.getPoints(space)

            if useWeights:
                for i in xrange(geoIter1.numVertices):
                    weight = weightMap[i]
                    resultVector = self.get_midpoint(pArray1[i], pArray2[i], weight)
                    pArray2[i].x = resultVector.x
                    pArray2[i].y = resultVector.y
                    pArray2[i].z = resultVector.z

            # update the surface of the geometry with the changes
            geoIter1.setPoints(pArray2)
            geoIter1.updateSurface()
        except: raise


# Create UI object
blendshape_tools = RigmaroleBlendshapeTools()