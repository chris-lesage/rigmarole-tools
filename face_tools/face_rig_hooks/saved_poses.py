'''
### SNIPPET: Get all the non-zero poses from the face-hooks rig. Write it as a dictionary.

poseLocs = pm.ls('*__POSELOC', type='transform')
print 'poseLocDict = {'
for each in poseLocs:
	trans = [round(x, 7) for x in each.t.get()]
	rots = [round(x, 7) for x in each.r.get()]
	if abs(sum(trans)) > 0 or abs(sum(rots)) > 0:
		both = trans + rots
		print '    "{}": {},'.format(each.name(), both)
		
print '}'
'''

### SNIPPET: With my manually created dictionary, recreate the poses.

poseLocDict = {
    "L_eye__left_eye_in_out__POSELOC": [0.45, 0.0, 0.0, 0.0, 0.0, 0.0],
    "L_eye__left_eye_x_up_down__POSELOC": [0.0, 0.0, 0.0, 0.0, 0.0, 30.0],
    "L_eye__left_eye_y_sideways__POSELOC": [0.0, 0.0, 0.0, 0.0, 30.0, 0.0],
    "L_softEye__left_softeye_x_up_down__POSELOC": [0.0, 0.0, 0.0, 0.0, 0.0, 20.0],
    "L_softEye__left_softeye_y_sideways__POSELOC": [0.0, 0.0, 0.0, 0.0, 10.0, 0.0],
    "R_eye__right_eye_in_out__POSELOC": [0.45, 0.0, 0.0, 0.0, 0.0, 0.0],
    "R_eye__right_eye_x_up_down__POSELOC": [0.0, 0.0, 0.0, 0.0, 0.0, 30.0],
    "R_eye__right_eye_y_sideways__POSELOC": [0.0, 0.0, 0.0, 0.0, 30.0, 0.0],
    "R_softEye__right_softeye_x_up_down__POSELOC": [0.0, 0.0, 0.0, 0.0, 0.0, 20.0],
    "R_softEye__right_softeye_y_sideways__POSELOC": [0.0, 0.0, 0.0, 0.0, 10.0, 0.0],
    "headSquash1__head_right_left__POSELOC": [0.0, 0.0, 0.0, 0.0, 0.0, -7.88],
    "headSquash1__head_squash__POSELOC": [0.0, -0.5, 0.0, 0.0, 0.0, 0.0],
    "headSquash1__head_stretch__POSELOC": [0.0, 0.5, 0.0, 0.0, 0.0, 0.0],
    "headSquash2__head_right_left__POSELOC": [0.0, 0.0, 0.0, 0.0, 0.0, -7.88],
    "headSquash2__head_squash__POSELOC": [0.0, -0.5, 0.0, 0.0, 0.0, 0.0],
    "headSquash2__head_stretch__POSELOC": [0.0, 0.5, 0.0, 0.0, 0.0, 0.0],
    "headSquash3__head_right_left__POSELOC": [0.0, 0.0, 0.0, 0.0, 0.0, -7.88],
    "headSquash3__head_squash__POSELOC": [0.0, -0.5, 0.0, 0.0, 0.0, 0.0],
    "headSquash3__head_stretch__POSELOC": [0.0, 0.5, 0.0, 0.0, 0.0, 0.0],
    "jaw__jaw_back_forward__POSELOC": [1.5, 0.0, 0.0, 0.0, 0.0, 0.0],
    "jaw__jaw_right_left__POSELOC": [0.0, 0.0, -2.0, 0.0, 0.0, 0.0],
    "jaw__mouth_open__POSELOC": [0.0, 0.0, 0.0, 0.0, 0.0, -40.0],
    "jaw__muzzle_up_down__POSELOC": [0.0, 0.0, 0.0, 0.0, 0.0, 15.0],
    "jaw_swing__muzzle_right_left__POSELOC": [0.0, 0.0, 0.0, 0.0, 30.0, 0.0],
    "muzzle__muzzle_up_down__POSELOC": [0.0, 0.0, 0.0, 0.0, 0.0, 15.0],
    "muzzle_swing__muzzle_right_left__POSELOC": [0.0, 0.0, 0.0, 0.0, 30.0, 0.0],
    "nose_muzzle__muzzle_right_left__POSELOC": [0.028779, -0.0, -0.7491381, 8.4766528, 0.0, 0.0],
    "nose_muzzle__nose_muzzle_up_down__POSELOC": [0.0, 0.0, 0.0, 0.0, 0.0, 15.0],
    "nose_muzzle__nose_right_left__POSELOC": [0.0, 0.0, 0.0, 0.0, -5.0, 0.0],
    "nose_muzzle__nose_up_down__POSELOC": [0.0, 0.0, 0.0, 0.0, 0.0, 5.0],
    "nose_swing__nose_muzzle_right_left__POSELOC": [0.0, 0.0, 0.0, 0.0, 30.0, 0.0],
}

for key, xforms in poseLocDict.items():
    try:
        oLoc = pm.PyNode(key.replace('_skin',''))
        oLoc.t.set( xforms[0:3] )
        oLoc.r.set( xforms[3:6] )
    except:
        print 'FAIL: {}'.format(key)
        continue