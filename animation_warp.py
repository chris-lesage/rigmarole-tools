import pymel.core as pm
import maya.cmds as cmds
from pymel.util.path import path
from functools import wraps

"""
The idea behind this tool:
I use two curves. The SOURCE animation is projected on to this curve with closestPoint constraints.
The offset is saved in a constrained locator. The TARGET animation is projected OUT of the second curve.
The tangent space of the curves is used to offset the animation, thus warping it with no sliding. (It will stretch.)
The warp curve is bent by using a splineIK rig

### INITIAL SETUP
In Step 1: Select the character-space or world-space nodes. Controls such as IK feet or spines.

#TODO:
- If a keyable attribute has incoming connections (for example a pairBlend or animBlendNodeAdditiveScale) then a key is not added in connect_together_keyframes(). I should check for local (non-referenced) connections and then also connect the WARP rig.
- Path cannot scale when scaled from the master control
- Check. What happens to non-keyable settings attributes? They need to get set to match the source rig.
- Add a "bake animation" button
- WIP: Add "add" and "remove" buttons to the GUI
- Add a pre-check to make sure the character is referenced.
- Add a way to run this on a non-referenced character? Is that worth it?
"""

def undo(func):
    """Puts the wrapped `func` into a single Maya Undo action, then
    undoes it when the function enters the finally: block
    from schworer Github
    """
    @wraps(func) # by using wraps, the decorated function maintains its name and docstring.
    def _undofunc(*args, **kwargs):
        try:
            # start an undo chunk
            cmds.undoInfo(ock=True)
            return func(*args, **kwargs)
        finally:
            # after calling the func, end the undo chunk
            cmds.undoInfo(cck=True)
    return _undofunc


def skin_geometry(oJoints, oGeo, pName):
    """A simple skinCluster command with my preferred prefs."""
    return pm.skinCluster(
            oJoints,
            oGeo,
            bindMethod=0, # closest distance
            dropoffRate=1.0,
            maximumInfluences=1,
            normalizeWeights=1, # interactive
            obeyMaxInfluences=False,
            skinMethod=0, # classic linear
            removeUnusedInfluence=0,
            weightDistribution=1, # neighbors
            name=pName,
        )


class AnimationWarping:
    def __init__(self):
        self.name = 'anim_warp_UI'
        self.title = 'Animation Warp'
        self.version = 0.97
        self.author = 'Chris Lesage - http://chrislesage.com'
        
        self.fileList = {}
        self.segmentOption = []

        self.pick1Button = None
        self.pick2Button = None
        self.warpButton = None
        self.blueColor = [0.5, 0.5, 0.64]
        self.redColor = [0.62, 0.4, 0.4]
        self.greenColor = [0.4, 0.57, 0.4]

        self.segments = 20
        self.numberOfVParams = 0
        self.rootControls = []
        self.targetRootControls = []
        self.warpRig = []
        self.targetRigRoot = []
        # constraint locators on the warp curve. Dict key will be name of controller
        self.warpHooks = {} 
        self.oCurve1 = []
        self.oCurve2 = []
        self.ui()
        
        
    def ui(self):
        if (pm.window(self.name, q=1, exists=1)):
            pm.deleteUI(self.name)
            
        windowTitle = self.title + ' v' + str(self.version)
        with pm.window(self.name, title=windowTitle, width=50, height=100, menuBar=False) as win:
            with pm.verticalLayout() as layout:
                with pm.horizontalLayout() as buttonRow:
                    buttonLabel = 'Step 1: Select IK and Mover Controls'
                    self.pick1Button = pm.button(
                            label=buttonLabel,
                            command=pm.Callback(self.get_mover_controls),
                            backgroundColor=self.redColor,
                            )
                    pm.button(label='Add', command=pm.Callback(self.add_controls, self.pick1Button, 'rootControls'))
                    pm.button(label='Remove', command=pm.Callback(self.clear_controls, self.pick1Button, 'rootControls'))
                buttonRow.redistribute(80, 20, 20)
                
                self.fileList['rootControls'] = pm.textScrollList(allowMultiSelection=True, width=180)
                self.fileList['rootControls'].selectCommand = pm.Callback(self.test_select, self.fileList['rootControls'])
                self.fileList['valid_rootControls'] = False
                self.fileList['rootControls'].append('no controllers selected')
                
                with pm.horizontalLayout() as buttonRow:
                    buttonLabel = 'Step 2: Select ALL Controls'
                    self.pick2Button = pm.button(
                            label=buttonLabel,
                            command=pm.Callback(self.get_all_character_controls),
                            backgroundColor=self.redColor,
                            )
                    pm.button(label='Add', command=pm.Callback(self.add_controls, self.pick2Button, 'allControls'))
                    pm.button(label='Remove', command=pm.Callback(self.clear_controls, self.pick2Button, 'allControls'))
                buttonRow.redistribute(80, 20, 20)

                self.fileList['allControls'] = pm.textScrollList(allowMultiSelection=True, width=180)
                self.fileList['valid_allControls'] = False
                self.fileList['allControls'].append('no controllers selected')

                with pm.horizontalLayout() as segmentSlider:
                    pm.text(label ='Number of Segments:')
                    self.segmentOption = pm.intField(
                            value=self.segments,
                            minValue=5,
                            maxValue=200,
                            changeCommand=pm.Callback(self.change_segments)
                            )
                self.warpButton = pm.button(
                        label='Step 3: Warp',
                        command=pm.Callback(self.do_the_thing),
                        backgroundColor=self.redColor,
                        )
                layout.redistribute(8, 20, 8, 20, 5, 8)
                    
        pm.showWindow()
                
    
    def change_segments(self):
        # note: there is also a redundant catch for this when do_the_thing() runs in case user didn't hit enter
        self.segments = self.segmentOption.getValue()


    def check_all_identical(self, coll):
        """check a collection to make sure it is all identical"""
        return len(set(coll)) == 1


    def update_scroll_list(self, oColl, targetList):
        if oColl:
            self.fileList[targetList].removeAll()
            for each in oColl:
                self.fileList[targetList].append(each)


    def update_warp_color(self):
        if self.fileList['valid_allControls'] and self.fileList['valid_rootControls']:
            self.warpButton.setBackgroundColor(self.blueColor)
        else:
            self.warpButton.setBackgroundColor(self.redColor)


    def get_all_character_controls(self):
        """This is a list of ALL the controls in your character. The animator must choose them
        because this script can't predict their naming convention, or custom needs."""
        oColl = pm.selected()
        # test for all identical namespaces (one character at a time!)
        if (oColl and self.check_all_identical([x.namespace() for x in pm.selected()])):
            self.allControls = oColl
            self.update_scroll_list(oColl, 'allControls')
            self.fileList['valid_allControls'] = True
            self.pick2Button.setBackgroundColor(self.blueColor)
        else:
            pm.warning('Pick all your controls from a single character!')
            self.fileList['valid_allControls'] = False
        self.update_warp_color()


    def get_mover_controls(self):
        """The mover controls are all IK and world-space controls in the character.
        These will get attached to the warp path. All FK controls will be driven by animation as usual. """
        oColl = pm.selected()
        # test for all identical namespaces (one character at a time!)
        if (oColl and self.check_all_identical([x.namespace() for x in pm.selected()])):
            self.rootControls = oColl
            self.update_scroll_list(oColl, 'rootControls')
            self.fileList['valid_rootControls'] = True
            self.pick1Button.setBackgroundColor(self.blueColor)
        else:
            pm.warning('Pick some controls from a single character!')
            self.fileList['valid_rootControls'] = False
        self.update_warp_color()

    
    def test_select(self, fileList):
        print('yes!')


    def add_controls(self, pickButton, listKey):
        selectMessage = 'no controllers selected'
        print('add controls clicks - {}'.format(listKey))
        fileList = self.fileList[listKey]
        print(fileList.getAllItems())
        return False

        self.update_scroll_list([selectMessage], listKey)
        #TODO: Add a check if the list is valid and populated
        # example 'valid_rootcontrols' or 'valid_allControls'
        self.fileList['valid_{}'.format(listKey)] = True
        pickButton.setBackgroundColor(self.redColor)
        self.update_warp_color()


    def clear_controls(self, pickButton, listKey):
        selectMessage = 'no controllers selected'
        self.update_scroll_list([selectMessage], listKey)
        self.fileList['valid_{}'.format(listKey)] = False
        pickButton.setBackgroundColor(self.redColor)
        self.update_warp_color()


    def create_closest_point_constraint(self, prefix, inputCurve, oRoot):
        oCurve = inputCurve
        oPoint = pm.createNode('closestPointOnSurface', name=prefix + '_closestPointOnSurface')
        # a transform bound to the curve
        oLocPos = pm.group(name=prefix + '_cpConstraintPos', em=True)
        # a transform that is the closestPoint constraint driver
        oLocIn = pm.group(name=prefix + '_cpConstraintIn', em=True)
        
        pm.parent(oLocPos, oLocIn, oRoot)
        oCurve.local.connect(oPoint.inputSurface)
        oLocIn.translate.connect(oPoint.inPosition)
        oPoint.position.connect(oLocPos.translate)
        
        return [oLocIn, oLocPos, oPoint]


    def create_follicle(self, oNurbs, uPos=0.0, vPos=0.0):
        # manually place and connect a follicle onto a nurbs surface.
        #TODO: Set a name for the follicle
        oFoll = pm.createNode('follicle')
        oFoll.v.set(0) # hide the little red shape of the follicle
        oNurbs = oNurbs.getShape()
        
        oNurbs.local.connect(oFoll.inputSurface)
        oNurbs.worldMatrix[0].connect(oFoll.inputWorldMatrix)
        oFoll.outRotate.connect(oFoll.getParent().rotate)
        oFoll.outTranslate.connect(oFoll.getParent().translate)
        oFoll.parameterU.set(uPos)
        oFoll.parameterV.set(vPos)
        oFoll.getParent().t.lock()
        oFoll.getParent().r.lock()
        
        return oFoll


    def connect_together_keyframes(self, sourceControls, targetControls):
        """add a keyframe on frame 0, on every control that isn't already keyed. This is necessary,
        because if the animator adds a keyframe LATER, the two controls won't be linked to each other."""
        curveTypes = [
                pm.nodetypes.AnimCurveTA,
                pm.nodetypes.AnimCurveTL,
                pm.nodetypes.AnimCurveTT,
                pm.nodetypes.AnimCurveTU,
                ]
        for eachControl in sourceControls:
            for sourceAttr in eachControl.listAttr(keyable=True, visible=True, settable=True):
                animCurve = [x for x in sourceAttr.inputs() if type(x) in curveTypes]
                if animCurve:
                    pass
                elif sourceAttr.type() == 'string':
                    pass
                else:
                    oValue = sourceAttr.get()
                    paramName = str(sourceAttr).split('.')[-1]
                    pm.setKeyframe(eachControl, hierarchy='none', v=oValue, t=0, at=paramName)

        # connect SOURCE rig anim curves to TARGET rig attributes. (Both controls will share one curve.)
        for sourceControl, targetControl in zip(sourceControls, targetControls):
            sourceAttrs = sourceControl.listAttr(keyable=True, visible=True, settable=True)
            targetAttrs = targetControl.listAttr(keyable=True, visible=True, settable=True)

            for sourceAttr, targetAttr in zip(sourceAttrs, targetAttrs):
                animCurve = [x for x in sourceAttr.inputs() if type(x) in curveTypes]
                if animCurve:
                    #TODO: also if it is a connection from the scene (not referenced) grab that plug too!
                    # For example, pairBlends
                    animCurve[0].output.connect(targetAttr, f=True)
        # Remove animation from the target rig, because it will be driven by the warp path.
        for oNode in self.targetRootControls:
            oNode.tx.disconnect()
            oNode.ty.disconnect()
            oNode.tz.disconnect()
            oNode.rx.disconnect()
            oNode.ry.disconnect()
            oNode.rz.disconnect()


    def import_another_reference(self, oRig, newNamespace):
        # new rig's namespace gets changed to WARP_namespace
        # original straight rig keeps original namespace
        originalNamespace = oRig.parentNamespace()
        # get the full path of the reference file
        referenceFile = path(self.rootControls[0].referenceFile())
        
        #rename the original rig's namespace to the new warp name
        referenceFile = oRig.referenceFile()
        
        #TODO: Switch to PyMEL
        refFile = cmds.file(str(referenceFile), r=True, type='mayaAscii', gl=True,
                loadReferenceDepth='all', namespace=newNamespace)
        refNode = pm.PyNode(pm.referenceQuery( refFile, referenceNode=True))
        refNode2 = pm.PyNode(pm.referenceQuery( refNode, nodes=True)[0])
        return refNode2

        
    def create_warp_rig(self, pNamespace):
        # create the main path curves
        # this number drives a multDivide node which drives follicles along the warp nurbsPlane 
        self.numberOfVParams = ((self.segments-1)*5)-1
        vCount = self.numberOfVParams
        # segments-1 so there are no trailing joints
        #TODO: animCurvePoints is deprecated I think...
        animCurvePoints = [(0,0,i) for i in range((self.segments-1)*5)]
        # create the 5x sparse ikSpline curve
        warpCurvePoints = [(0,0,i*5) for i in range(self.segments)]

        oRig = pm.group(name=pNamespace + 'path_warp_RIG', em=True)
        #animCurve = pm.curve( name=pNamespace + 'aw_anim_curve', d=3, p=animCurvePoints )
        animCurve = pm.nurbsPlane(ax=(0,1,0), ch=False, d=3, name=pNamespace + 'aw_anim_curve', p=(0,0,-0.5), u=0, v=vCount)[0]
        warpCurve = pm.nurbsPlane(ax=(0,1,0), ch=False, d=3, name=pNamespace + 'aw_warp_curve', p=(0,0,-0.5), u=0, v=vCount)[0]
        ikSplineCurve = pm.curve( name=pNamespace + 'aw_warp_IKSpline', d=3, p=warpCurvePoints )
        oAnimMaster = pm.circle(name=pNamespace + 'aw_Anim_Master', ch=False, r=2.0, nr=(0,1,0))[0]
        oWarpMaster = pm.circle(name=pNamespace + 'aw_Warp_Master', ch=False, r=3.0, nr=(0,1,0))[0]

        animCurve.scale.set(1,1,vCount)
        warpCurve.scale.set(1,1,vCount)
        animCurve.rotate.set(0,180,0)
        warpCurve.rotate.set(0,180,0)
        animCurve.visibility.set(1)
        warpCurve.visibility.set(1)
        pm.makeIdentity(animCurve, apply=True)
        pm.makeIdentity(warpCurve, apply=True)
        
        oAnimMaster.getShape().overrideEnabled.set(1)
        oWarpMaster.getShape().overrideEnabled.set(1)
        ikSplineCurve.getShape().overrideEnabled.set(1)
        ikSplineCurve.getShape().overrideDisplayType.set(2)
        ikSplineCurve.visibility.set(0)
        oAnimMaster.getShape().overrideColor.set(13)
        oWarpMaster.getShape().overrideColor.set(17)

        pm.parent(animCurve, warpCurve, ikSplineCurve, oAnimMaster, oWarpMaster, oRig)

        # create the anim path chain
        pm.select(None)
        oJoints = []
        for i in range((self.segments-1)*5): # segments-1 so there are no trailing joints
            oJoint = pm.joint( p=(0,0,i), name='{}aw_Anim_joint_{:02}'.format(pNamespace, i))
            oJoint.radius.set(0.15)
            oJoint.overrideEnabled.set(1)
            oJoint.overrideColor.set(13)
            oJoints.append(oJoint)
        oJoint.root().visibility.set(0)
        pm.parent(oJoint.root(), oAnimMaster)
        oSkin = skin_geometry(oJoints, animCurve, '{}{}_skincluster'.format(pNamespace, animCurve.name()))
        # the skinCluster gets offset, so manually set the weights to corresponding bones
        for i, each in enumerate(oJoints):
            if i<=1:
                pm.skinPercent( oSkin, animCurve.cv[0:3][0], transformValue=[(oJoints[0], 1)])
            else:
                pm.skinPercent( oSkin, animCurve.cv[0:3][i+1], transformValue=[(oJoints[i], 1)])

        # create the warp path chain
        pm.select(None)
        oJoints = []
        for i in range((self.segments-1)*5): # segments-1 so there are no trailing joints
            oJoint = pm.joint( p=(0,0,i), name='{}aw_Warp_joint_{:02}'.format(pNamespace, i))
            oJoint.radius.set(0.3)
            oJoint.overrideEnabled.set(1)
            oJoint.overrideColor.set(17)
            oJoints.append(oJoint)
        oJoint.root().visibility.set(0)
        pm.parent(oJoint.root(), oWarpMaster)
        oSkin = skin_geometry(oJoints, warpCurve, '{}{}_skincluster'.format(pNamespace, warpCurve.name()))
        # the skinCluster gets offset, so manually set the weights to corresponding bones
        for i, each in enumerate(oJoints):
            if i<=1:
                pm.skinPercent( oSkin, warpCurve.cv[0:3][0], transformValue=[(oJoints[0], 1)])
            else:
                pm.skinPercent( oSkin, warpCurve.cv[0:3][i+1], transformValue=[(oJoints[i], 1)])

        #create the ikspline
        oHandle = pm.ikHandle(
                name = pNamespace + 'warp_ikSplineHandle',
                createCurve=False,
                curve=ikSplineCurve,
                startJoint=oJoints[0],
                endEffector=oJoints[-1],
                createRootAxis=False,
                parentCurve=False,
                rootOnCurve=False,
                rootTwistMode=True,
                solver='ikSplineSolver'
                )
        pm.parent(oHandle[0], oRig)
        oHandle[0].visibility.set(0)
        ikSplineCurve.visibility.set(0)

        animCurve.getShape().overrideEnabled.set(1)
        animCurve.getShape().overrideDisplayType.set(2)
        warpCurve.getShape().overrideEnabled.set(1)
        warpCurve.getShape().overrideDisplayType.set(2)

        pm.select(None)
        oLambert = pm.shadingNode('lambert', asShader=True, name=pNamespace + 'warp_control_material')
        oLambert.color.set(1,1,0)
        oLambert.transparency.set(0.4,0.4,0.4)
        pm.select(warpCurve.getShape())
        pm.hyperShade(warpCurve.getShape(), assign=oLambert)

        # create the IK Spline Control chain
        oJoints = []
        oBuffer = None
        pm.select(None)
        for i in range(self.segments):
            pName = '{}aw_Control_joint_{:02}'.format(pNamespace, i)
            oPos = (0,0,i*5)
            oJoint = pm.joint( p=oPos, name=pName )
            oJoints.append(oJoint)
            #TODO: Better to just use nurbs curves for controllers I think... Maybe dense circle "spheres"
            oShape = pm.sphere(axis=(0,1,0), ch=False, degree=3, radius=0.4, p=(0,0,0))
            pm.select(oShape[0].getShape())
            pm.hyperShade( oShape, assign=oLambert )

            pm.parent(oShape[0].getShape(), oJoint, r=True, s=True)
            pm.delete(oShape[0])

            oRoot = pm.group(name=pName + '_ROOT', em=True)
            oRoot.setTranslation(oPos)
            pm.parent(oJoint, oRoot)
            # oBuffer means parent the current root to the last joint.
            if oBuffer:
                pm.parent(oRoot, oBuffer)
            oJoint.radius.set(0.8)
            oJoint.drawStyle.set(2)
            oBuffer = oJoint

        pm.parent(oJoint.root(), oWarpMaster)
        oSkin = skin_geometry(oJoints, ikSplineCurve, '{}_skincluster'.format(ikSplineCurve.name()))
        # the skinCluster gets offset, so manually set the weights to corresponding bones
        for i, eachJoint in enumerate(oJoints):
            pm.skinPercent( oSkin, ikSplineCurve.cv[i], transformValue=[(eachJoint, 1)])
        
        pm.select(None)
        self.oCurve1 = animCurve
        self.oCurve2 = warpCurve
        return oRig


    @undo
    def do_the_thing(self):
        if self.fileList['valid_allControls'] == False or self.fileList['valid_rootControls'] == False:
            pm.warning('You need to select controls first!')
            return False

        # Note: if animator doesn't hit enter when changing segments option, this catches the value anyway.
        self.segments = self.segmentOption.getValue()
        ### check for valid controls
        warpName = 'WARP_' + str(self.rootControls[0].parentNamespace())
        warpNamespace = 'WARP_' + str(self.rootControls[0].namespace())

        self.targetRigRoot = self.import_another_reference(self.rootControls[0], warpName)
        self.warpRig = self.create_warp_rig(warpNamespace)

        #NOTE: rootControls and targetRootControls refer only to the Step 1. IK mover controls.
        # get the corresponding targetRootControls by changing the namespace
        self.targetRootControls = [pm.PyNode(ctrl.swapNamespace(warpNamespace)) for ctrl in self.rootControls]
        
        setName = self.rootControls[0].namespace().replace(':','_').replace('WARP','') + '_WARP_BAKE_CONTROLS'
        pm.sets(self.targetRootControls, n=setName)
        
        oWarpRig = self.warpRig
        
        originalNamespace = self.rootControls[0].namespace()
        oCurve1 = self.oCurve1
        oCurve2 = self.oCurve2

        oRoot = pm.group(name=originalNamespace + 'anim_warp_Rig', em=True)
        oWarpControllers = pm.group(name=originalNamespace + 'Anim_Warp_Controllers', em=True)
        pm.parent(oWarpControllers, self.warpRig, oRoot) #NOTE: parenting the reference under the oRoot node
        oWarpControllers.visibility.set(0)
        
        pm.select(None)

        for each in self.rootControls:
            oName = each.name().replace(':','_') # strip colons from namespace
            vector1 = pm.group(name=oName + '_vector1', em=True)
            vector2 = pm.group(name=oName + '_vector2', em=True)
            offset_vector1 = pm.group(name=oName + '_offset_vector1', em=True)
            offset_vector2 = pm.group(name=oName + '_offset_vector2', em=True)

            ### create a duplicate of offset_vector2 which will be in a nice user-friendly hierarchy
            offset_vector3 = pm.spaceLocator(name=oName + '_WARP')
            self.warpHooks[each.name()] = offset_vector3
            offset_vector3.getShape().localScaleX.set(0.1)
            offset_vector3.getShape().localScaleY.set(0.1)
            offset_vector3.getShape().localScaleZ.set(0.1)

            ### create a closestPoint constraint on oCurve1. Result is cpConstraintIn and cpConstraintPos nulls.
            oClosePoint = self.create_closest_point_constraint(oName, oCurve1, oRoot)

            ### create a pointOnCurveInfo node on oCurve2

            # To get twisting and loop-de-looping, use a nurbs plane. The following binds follicles to the plane. 
            #This drives the follicle, but divided by the number of spans. (The follicle goes 0 to 1.)
            oFoll = self.create_follicle(oCurve2, uPos=0.5, vPos=0.0)
            pm.rename(oFoll.getParent(), oName + 'FOLL')
            pm.parent(oFoll.getParent(), oRoot)
            oMult = pm.shadingNode('multiplyDivide', asUtility=True, name=oName + 'foll_multiply')
            #TODO: This should likely be divided by the scale of the rig. But then it never reaches the end!
            oMult.input2X.set(1)
            oMult.operation.set(2) # set to divide instead of multiply.
            oClosePoint[2].parameterV.connect(oMult.input1X)
            oMult.outputX.connect(oFoll.parameterV) # the curve1 parameter is driving the follicle on the nurbs plane.
            
            ### drive vector2.translate by pointOnCurveInfo.position
            pm.parentConstraint(oFoll.getParent(), vector2, w=1.0, mo=True)

            ### pointConstraint cpConstraintIn to EACH control
            pm.pointConstraint(each, oClosePoint[0], w=1, mo=False)

            ### pointConstraint vector1 to cpConstraintPos
            pm.pointConstraint(oClosePoint[1], vector1, w=1.0, mo=False)

            ### tangent constraint vector1 to oCurve1
            #pm.tangentConstraint(oCurve1, vector1, aim=(0,0,1)) # in theory this doesn't need an upvector because source path stays in place.
            ### tangent constraint vector2 to oCurve2
            # NURBSMOD pm.tangentConstraint(oCurve2, vector2)

            pm.parent(vector1, vector2, oRoot)
            ### parent offset_vector1 under vector1 and 0,0,0 out the transforms
            pm.parent(offset_vector1, vector1)
            offset_vector1.resetFromRestPosition()
            ### parent offset_vector2 under vector2
            pm.parent(offset_vector2, vector2)
            offset_vector2.resetFromRestPosition()
            ### parent offset_vector3 under "Anim_Warp_Controllers"
            pm.parent(offset_vector3, oWarpControllers)

            ### connect translate,rotate,scale params from offset_vector1 to offset_vector2.
            offset_vector1.translate.connect(offset_vector2.translate)
            offset_vector1.rotate.connect(offset_vector2.rotate)
            offset_vector1.scale.connect(offset_vector2.scale)
            
            ### parent constrain offset_vector3 to offset_vector2
            pm.parentConstraint(offset_vector2, offset_vector3, w=1.0, mo=False)

            ### parentConstraint offset_vector1 to the EACH control on the SOURCE RIG (no offset)
            pm.parentConstraint(each, offset_vector1, w=1.0, mo=False)

        ### Reference another of the same character. Prepend it with "WARP" or something
        ### For every single keyable attribute on all of the controls on Source Rig: (Except the 9 root controls)
        ### Connect the animation curve to the Target Rig. If there isn't a key, set one on frame 0.

        sourceControls = [pm.PyNode(ctrl) for ctrl in self.fileList['allControls'].getAllItems()]
        targetControls = [pm.PyNode(ctrl.swapNamespace(warpNamespace)) for ctrl in sourceControls]
        self.connect_together_keyframes(sourceControls, targetControls)

        for rootCtrl, targetRootCtrl in zip(self.rootControls, self.targetRootControls):
            oHook = self.warpHooks[rootCtrl.name()] # each hook has a corresponding controller by dict key.
            pm.parentConstraint(oHook, targetRootCtrl, w=1.0, mo=True)

        pm.deleteUI(self.name)
        pm.warning('Warp setup complete. Use the yellow controller to warp your animation.')

AnimationWarping()
