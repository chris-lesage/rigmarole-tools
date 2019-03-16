import pymel.core as pm
import pymel.core.datatypes as dt
import sys
import os
import envtools

import dolby_face_map as facemap
reload(facemap)
#sys.path.append('C:/Users/clesage/dev/tech/maya/scripts/moonbot/butterfly/utils/')
faceposes = facemap.get_face_map()

#TODO: Outstanding Issues
'''
- Save the facemap as some kind of a JSON or similar format?
- Include scaling, but I'll have to make it multiplication instead of addition.
- Include a tool to optimize all un-used poses. 1000's of MultiplyDivide nodes could be cleared on empty POSLOCS
- Create the face template via script.
- Connect the blendshapes via script.
- It would be great to have macros, so "wide mouth" was a combo of "left wide mouth" and "right wide mouth".
- Fix the issue where overriding a pose doesn't stop it from piping out a value to the blendshape.
    - (I need current value and current output to be distinct.)
- I have **Macros, Overrides and Blendshapes**. It seems like there might be some conceptual overlap here...

SYMMETRY:
- Connect the right side POSLOC's in symmetry. Then, if I want to break that, I can, if I need asymmetry.
- AND create macros, so that left+right = the full pose, which is also mappable and breakable if I need to offset.
- That way, you edit 3 poses, by editing one.


'''

#SCRIPT_DIR = os.path.dirname('C:/Users/clesage/dev/tech/maya/scripts/moonbot/butterfly/')
#FACE_CTLS_FILE = os.path.join(SCRIPT_DIR, 'ctrlsface.data')
#FACE_CTLS = envtools.load_dict(FACE_CTLS_FILE)


# set up a rig definition that takes each pose.
# the pose has:
    # a name
    # a mirrored pair (or none)
    # a mapping controller attribute
    # a mapping range from inputMin to inputMax and outputMin to outputMax


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


def move_loc_position(target, source):
    """ this function reads a world coordinate 'source'
    and moves the localPosition of the target locator. """
    # a temp dumb hack until I figure out how to translate world to local coordinates.
    # your math is bad and you should feed bad
    tempLoc = pm.spaceLocator(n='testiscool_{}'.format(target.name()))
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
        faceJoints = None

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
            overrideMapper = pm.createNode('remapValue', n='{}_{}_poseOverrideMapper'.format(poseName, eachOver))
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


def create_hooks(masterScale):
    # create the HOOKS and OVERRIDES nodes.
    hookRoot = pm.group(em=True, n='face_HOOKS')
    overRoot = pm.group(em=True, n='face_OVERRIDES')
    posesRoot = pm.group(em=True, n='face_POSES')
    for oZone in pm.ls('*_zone', type='objectSet'):
        zone = oZone.name().replace('_zone','')
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


def create_joint_drivers(masterScale):
    """ This function builds the skeleton hierarchy and the end-result nodes and pivots.
    Returns a dictionary of the final plusMinusAverage nodes that all the poses drive """

    allZones = pm.ls('*_zone', type='objectSet')
    allJoints = set(pm.ls([x.members() for x in allZones]))
    inputHooks = {}

    # 'poseCount' is an attribute to keep track of how many poses are fed into each plusMinusAverage node.
    # This is so I can reliably append. I'm sure there is a better Maya way, but there are also index bugs.
    inputHooks['poseattributes'] = {}
    inputHooks['pivotpositions'] = {}
    inputHooks['pivotrotations'] = {}
    inputHooks['jointpositions'] = {}
    inputHooks['jointrotations'] = {}
    for i, poseAttr in enumerate(poseattributes): # The arbitrary attributes
        # Generate the special arbitrary attribute joints in this loop
        aaGroup = pm.group(em=True, n='{}_attrJnt_grp'.format(poseAttr))
        pm.select(None)
        aaJoint = pm.joint(n='{}_attr_jnt'.format(poseAttr))
        aaJoint.radius.set(1.0 * masterScale)
        pm.select(None)
        pm.parent(aaJoint, aaGroup)
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


### MAIN CONSTRUCTION FUNCTIONS ###
def build_face():
    """ Takes the input joints and zone sets and builds the poses out. """
    masterScale = 0.2
    create_hooks(masterScale)
    inputHooks = create_joint_drivers(masterScale)

    for poseInfo in faceposes:
        zone             = poseInfo['zone']
        pose             = poseInfo['pose']
        poseDriver       = poseInfo['driver']
        poseRange        = poseInfo['mapping']
        poseOverrides    = poseInfo['overrides']
        poseOverrideMaps = poseInfo['overridemaps']

        create_pose_node(pose, zone, inputHooks, masterScale, poseDriver, poseRange, poseOverrides, poseOverrideMaps)
    print 'done'
