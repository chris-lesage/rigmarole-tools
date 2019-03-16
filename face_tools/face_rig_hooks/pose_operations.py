# These functions are for doing edit operations on _POSE nodes.
# If the _POSE is connected to the POSELOC locators, move the locators. Otherwise, set the data in the _POSE node directly.

def copy_pose(inPose, outPose):
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

    allAttrs = [param for param in oOutPose.listAttr(keyable=True, visible=True, settable=True) if param.isLocked() == False]
    for eachAttr in allAttrs:
        # check that the attr does not end in ignoreScaleAttrs
        if not any(eachAttr.endswith(x) for x in ignoreScaleAttrs):
            combinedResult = sum([ pm.PyNode(eachAttr.name().replace(oOutPose.name(), x.name())).get() for x in oInPoses ])
        else:
            combinedResult = None
            # Else we are dealing with scale, so multiply the results instead of sum()
            #TODO: Implement scale. For now, ignore it.
            #combinedResult = reduce(lambda x, y: x*y, [ pm.PyNode(eachAttr.name().replace(oOutPose.name(), x.name())).get() for x in oInPoses ])
            #if abs(combinedResult) != 1.0:
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

    'kena_face_poses_v2:kena_rig_08:left_crease4_offset_ctrl'
    'kena_face_poses_v2:kena_rig_08:left_crease4_skin'
    
    poseName = outPose.replace('_POSE','')
    inNamespace = sourceCtrls[0].namespace()
    for source in sourceCtrls:
        if source.getTranslation().length() + source.getRotation().length() > 0.01:
            try:
                targetName = source.name().replace(inNamespace, '').replace('_offset_ctrl','')
                target = '{}__{}__JOINT_POSELOC'.format(targetName, poseName)
                oTarget = pm.PyNode(target)
                try:
                    oJoint = pm.PyNode(source.replace('_offset_ctrl','_skin'))
                    oJointMove = pm.PyNode(source.replace('_offset_ctrl','_skin').replace(inNamespace,''))
                except:
                    oJoint = pm.PyNode(source.replace('_offset_ctrl','_jnt'))
                    oJointMove = pm.PyNode(source.replace('_offset_ctrl','_jnt').replace(inNamespace,''))
                offsetT = oTarget.getTranslation(space='world') + (oJoint.getTranslation(space='world') - oJointMove.getTranslation(space='world'))
                offsetR = oTarget.getRotation() + (oJoint.getRotation() - oJointMove.getRotation())
                oTarget.setTranslation(offsetT, space='world')
                oTarget.setRotation(offsetR, space='world')
                oTarget.r.set([pm.PyNode(oTarget+x).get() + (pm.PyNode(oJoint+x).get()-pm.PyNode(oJointMove+x).get()) for x in ['.rx', '.ry', '.rz']])
                #oTarget.setTranslation(source.getTranslation(space='world'), space='world')
                #oTarget.setRotation(source.getRotation(space='world'), space='world')
            except:
                print "{} doesn't appear to have a JOINT POSELOC.".format(source)
    

def mirror_pose(inPose):
    ''' take a pose and flip it symmetrically '''
    pass


def split_mirror_pose(inPose, outLeftPose, outRightPose):
    ''' take a full input pose and output left and right poses '''
    pass


def subtract_pose(inPose1, inPose2, outPose):
    ''' take inPose1, subtract the values from inPose2, and return the result of outPose '''
    pass

