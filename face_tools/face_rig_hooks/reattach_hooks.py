import pymel.core as pm

# This script reattaches POSELOCS to the face rig.


def reattach_pose_node(pose, zone, inputHooks, masterScale, poseDriver, poseRange, poseOverrides, poseOverrideMaps):
    oZone = pm.PyNode('{}_zone'.format(zone))

    #TODO: Make some logic that auto-splits "symmetry" into two poses, left and right.
    poseName = pose.replace('symmetry','left')
    faceJoints = oZone.members()

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
        poseLocJointName = '{}__{}__JOINT_POSELOC'.format(jointName, poseName) # eg. left_cheek_puff__right_smile__JOINT_POSELOC
        
        # Add in a 2nd POSELOC so I can have local transformations too. (But only if the pivot is offset.)
        oRoot = pm.group(em=True, n=poseLocName + '_grp')
        oLoc = pm.spaceLocator(n=poseLocName)
        oLoc.localScale.set([0.4 * masterScale]*3)
        poseLocators[jKey] = [oLoc] # adding each locator to a dictionary whose key is the joint name
        pm.parent(oLoc, oRoot)
        pm.parent(oRoot, oPoseNode)
        addJointPivot = False
        if (pivotPosition - jointPosition).length() > 0.01:
            # IF the pivot and joint position is not zero, add a second POSELOC for local rotations as well
            # Otherwise, for example, there is no way to rotate the mouth joints locally
            addJointPivot = True
            oRootJoint = pm.group(em=True, n=poseLocJointName + '_grp')
            oLocJoint = pm.spaceLocator(n=poseLocJointName)
            oLocJoint.localScale.set([0.9 * masterScale]*3)
            pm.parent(oLocJoint, oRootJoint)
            pm.parent(oRootJoint, oLoc)
            poseLocators[jKey] = [oLoc, oLocJoint] # Add BOTH locs to the dict. (Otherwise, it is a list of one.)

        oRoot.setTranslation(pivotPosition, space='world')
        oRoot.setRotation(pivotRotation, space='world')
        move_loc_position(oLoc, jointPosition) # moves the localPosition of the locator to a world coordinate
        if addJointPivot:
            oRootJoint.setTranslation(jointPosition, space='world')
            oRootJoint.setRotation(jointRotation, space='world')
            oLoc.localPositionZ.set(oLoc.localPositionZ.get() - 0.5)
        #TODO: Fix scaling. Scaling the POSELOC currently breaks the position of the _RESULT

    #####################

    # Populate the _POSE node with all of the attributes
    oTitleAttr = add_a_keyable_attribute(oPoseNode, 'double', 'arbitraryAttributes')
    oTitleAttr.lock()
    attrDict = {}
    for poseAttr in poseattributes: # The arbitrary attributes
        oPoseAttr = add_a_keyable_attribute(oPoseNode, 'double', 'pose_{}'.format(poseAttr))
        attrDict[poseAttr] = oPoseAttr

    for poseAttr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'tx2', 'ty2', 'tz2', 'rx2', 'ry2', 'rz2', 'sx2', 'sy2', 'sz2']:
        attrDict[poseAttr] = []
    for poseAttr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'tx2', 'ty2', 'tz2', 'rx2', 'ry2', 'rz2', 'sx2', 'sy2', 'sz2']:
        oTitleAttr = add_a_keyable_attribute(oPoseNode, 'double', '{}_POSE_{}'.format(poseName, poseAttr))
        oTitleAttr.lock()
        for each in faceJoints:
            jKey = each.name()
            jointName = each.name().rpartition('_')[0].replace('symmetry','left') # cut off the suffix

            doublePivot = False
            if len(poseLocators[jKey]) > 1:
                doublePivot = True
            
            # PIVOT POSITION
            pmaDriven1    = inputHooks[jKey]['driven1']
            pmaTranslate1 = inputHooks[jKey]['translate1']
            pmaRotate1    = inputHooks[jKey]['rotate1']
            #####pmaScale1     = inputHooks[jKey]['scale1']
            # JOINT POSITION
            pmaDriven2    = inputHooks[jKey]['driven2']
            pmaTranslate2 = inputHooks[jKey]['translate2']
            pmaRotate2    = inputHooks[jKey]['rotate2']
            #####pmaScale2     = inputHooks[jKey]['scale2']
            
            newAttrName = '{}_{}'.format(jointName, poseAttr)
            oPoseAttr = add_a_keyable_attribute(oPoseNode, 'double', newAttrName)
            # poseLocator is a list of the POSELOC locator(s). There is only one if the pivot is at the position of the joint.
            poseLocator1 = poseLocators[jKey][0] # from dictionary
            # eg. connect left_cheek_puff_POSELOC.tx to left_smile_POSE.left_cheek_puff_tx
            #TODO: Include scaling in the pose
            if '2' not in poseAttr:
                pm.PyNode('{}.{}'.format(poseLocator1, poseAttr)).connect(oPoseAttr)
                attrDict[poseAttr].append(oPoseAttr)
            else:
                if doublePivot:
                    poseLocator2 = poseLocators[jKey][1] # from dictionary
                    # replace 2 because the key is eg. tx2, but the attr is .tx
                    pm.PyNode('{}.{}'.format(poseLocator2, poseAttr.replace('2',''))).connect(oPoseAttr)
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
        oPlus = inputHooks[currentJoint.name()]['translate1']
        pmaIndex = oPlus.poseCount.get()
        oMult.output.connect(oPlus.input3D[pmaIndex].input3D)
        oPlus.poseCount.set(pmaIndex + 1)
    for attrX, attrY, attrZ, currentJoint in zip( attrDict['tx2'], attrDict['ty2'], attrDict['tz2'], faceJoints ):
        # Hook in the multiply for the translations
        oMult = pm.createNode('multiplyDivide', n='{}_{}_translate2_MLT'.format(poseName, currentJoint))
        attrX.connect(oMult.input1X)
        attrY.connect(oMult.input1Y)
        attrZ.connect(oMult.input1Z)
        # poseOverrideMULT only uses the X channel as a mute for all 3 oMult axes.
        poseOverrideMULT.outputX.connect(oMult.input2X)
        poseOverrideMULT.outputX.connect(oMult.input2Y)
        poseOverrideMULT.outputX.connect(oMult.input2Z)
        oPlus = inputHooks[currentJoint.name()]['translate2']
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
        oPlus = inputHooks[currentJoint.name()]['rotate1']
        pmaIndex = oPlus.poseCount.get()
        oMult.output.connect(oPlus.input3D[pmaIndex].input3D)
        oPlus.poseCount.set(pmaIndex + 1)
    for attrX, attrY, attrZ, currentJoint in zip( attrDict['rx2'], attrDict['ry2'], attrDict['rz2'], faceJoints ):
        # Hook in the multiply for the rotations
        oMult = pm.createNode('multiplyDivide', n='{}_{}_rotate2_MLT'.format(poseName, currentJoint))
        attrX.connect(oMult.input1X)
        attrY.connect(oMult.input1Y)
        attrZ.connect(oMult.input1Z)
        # poseOverrideMULT only uses the X channel as a mute for all 3 oMult axes.
        poseOverrideMULT.outputX.connect(oMult.input2X)
        poseOverrideMULT.outputX.connect(oMult.input2Y)
        poseOverrideMULT.outputX.connect(oMult.input2Z)
        oPlus = inputHooks[currentJoint.name()]['rotate2']
        pmaIndex = oPlus.poseCount.get()
        oMult.output.connect(oPlus.input3D[pmaIndex].input3D)
        oPlus.poseCount.set(pmaIndex + 1)

    '''
    ### SCALE ###
    for attrX, attrY, attrZ, currentJoint in zip( attrDict['sx'], attrDict['sy'], attrDict['sz'], faceJoints ):
        #TODO: Refactor the scale override to blend between dividing by 1.0 and dividing by pose value
        # Hook in the multiply for the scale
        oMult = pm.createNode('multiplyDivide', n='{}_{}_scale_MLT'.format(poseName, currentJoint))
        attrX.connect(oMult.input1X)
        attrY.connect(oMult.input1Y)
        attrZ.connect(oMult.input1Z)
        # poseOverrideMULT only uses the X channel as a mute for all 3 oMult axes.
        poseOverrideMULT.outputX.connect(oMult.input2X)
        poseOverrideMULT.outputX.connect(oMult.input2Y)
        poseOverrideMULT.outputX.connect(oMult.input2Z)
        oPlus = inputHooks[currentJoint.name()]['scale1']
        pmaIndex = oPlus.poseCount.get()
        oMult.output.connect(oPlus.input3D[pmaIndex].input3D)
        oPlus.poseCount.set(pmaIndex + 1)
    for attrX, attrY, attrZ, currentJoint in zip( attrDict['sx2'], attrDict['sy2'], attrDict['sz2'], faceJoints ):
        # Hook in the multiply for the scale
        oMult = pm.createNode('multiplyDivide', n='{}_{}_scale2_MLT'.format(poseName, currentJoint))
        attrX.connect(oMult.input1X)
        attrY.connect(oMult.input1Y)
        attrZ.connect(oMult.input1Z)
        # poseOverrideMULT only uses the X channel as a mute for all 3 oMult axes.
        poseOverrideMULT.outputX.connect(oMult.input2X)
        poseOverrideMULT.outputX.connect(oMult.input2Y)
        poseOverrideMULT.outputX.connect(oMult.input2Z)
        oPlus = inputHooks[currentJoint.name()]['scale2']
        pmaIndex = oPlus.poseCount.get()
        oMult.output.connect(oPlus.input3D[pmaIndex].input3D)
        oPlus.poseCount.set(pmaIndex + 1)
    '''

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






for i, each in enumerate(pm.PyNode('face_POSES').getChildren(type='transform')):
	print i, each
