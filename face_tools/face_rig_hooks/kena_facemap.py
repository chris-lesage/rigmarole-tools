poseattributes = [
    'left_crow_wrinkle',
    'right_crow_wrinkle',
    'forehead_wrinkle',
    'squeeze_BS',
    'bunny_wrinkle',
    'left_brow_down_corrective',
    'right_brow_down_corrective',
    ]

faceposes = [
    #TODO: Include the zone that the poses belong to. THEN shorten the pose names. But put zones into the naming conventions of the background nodes.
    #TODO: This giant list is a bit incomprehensible...
    # HEAD
 {'zone': 'head',    'pose': 'head_right_left',            'driver': 'HeadSquash_M_ctrl.tx',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'head',    'pose': 'head_squash',                'driver': 'HeadSquash_M_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'head',    'pose': 'head_stretch',               'driver': 'HeadSquash_M_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },

 # EYEBROWS
 {'zone': 'brow',    'pose': 'left_brow_squeeze',          'driver': 'Brow_L_ctrl.squeeze',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'brow',    'pose': 'right_brow_squeeze',         'driver': 'Brow_R_ctrl.squeeze',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'brow',    'pose': 'left_brow_angry',            'driver': 'Brow_L_ctrl.tx',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'brow',    'pose': 'right_brow_angry',           'driver': 'Brow_R_ctrl.tx',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'brow',    'pose': 'left_brow_down',             'driver': 'Brow_L_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'brow',    'pose': 'right_brow_down',            'driver': 'Brow_R_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'brow',    'pose': 'left_brow_sad',              'driver': 'Brow_L_ctrl.tx',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'brow',    'pose': 'right_brow_sad',             'driver': 'Brow_R_ctrl.tx',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'brow',    'pose': 'left_brow_up',               'driver': 'Brow_L_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'brow',    'pose': 'right_brow_up',              'driver': 'Brow_R_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },

 # EYES
 {'zone': 'eye',    'pose': 'left_eye_in_out',             'driver': 'Eye_L_ctrl.eyeInOut',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'eye',    'pose': 'right_eye_in_out',            'driver': 'Eye_R_ctrl.eyeInOut',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] },

 {'zone': 'eye',    'pose': 'left_eye_y_sideways',         'driver': 'Eye_L_ctrl.tx',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'eye',    'pose': 'right_eye_y_sideways',        'driver': 'Eye_R_ctrl.tx',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'eye',    'pose': 'left_eye_x_up_down',          'driver': 'Eye_L_ctrl.ty',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'eye',    'pose': 'right_eye_x_up_down',         'driver': 'Eye_R_ctrl.ty',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },

 {'zone': 'eye',    'pose': 'left_softeye_y_sideways',     'driver': 'Eye_L_ctrl.tx',    'mapping': [-1, 1, -1, 1],    'overrides': ['Eye_L_ctrl.soft_eye_follow'],    'overridemaps': [[0, 10, 1, 0]] },
 {'zone': 'eye',    'pose': 'right_softeye_y_sideways',    'driver': 'Eye_R_ctrl.tx',    'mapping': [-1, 1, -1, 1],    'overrides': ['Eye_R_ctrl.soft_eye_follow'],    'overridemaps': [[0, 10, 1, 0]] },
 {'zone': 'eye',    'pose': 'left_softeye_x_up_down',      'driver': 'Eye_L_ctrl.ty',    'mapping': [-1, 1, -1, 1],    'overrides': ['Eye_L_ctrl.soft_eye_follow'],    'overridemaps': [[0, 10, 1, 0]] },
 {'zone': 'eye',    'pose': 'right_softeye_x_up_down',     'driver': 'Eye_R_ctrl.ty',    'mapping': [-1, 1, -1, 1],    'overrides': ['Eye_R_ctrl.soft_eye_follow'],    'overridemaps': [[0, 10, 1, 0]] },

 {'zone': 'eye',    'pose': 'left_eyelid_x_up_down',       'driver': 'Eyelid_L_ctrl.ty',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'eye',    'pose': 'right_eyelid_x_up_down',      'driver': 'Eyelid_R_ctrl.ty',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'eye',    'pose': 'left_eyelid_z_spin',          'driver': 'Eyelid_L_ctrl.tx',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'eye',    'pose': 'right_eyelid_z_spin',         'driver': 'Eyelid_R_ctrl.tx',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },

 {'zone': 'eye',    'pose': 'left_upper_blink',            'driver': 'Eye_L_ctrl.upper_blink',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'eye',    'pose': 'right_upper_blink',           'driver': 'Eye_R_ctrl.upper_blink',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'eye',    'pose': 'left_lower_blink',            'driver': 'Eye_L_ctrl.lower_blink',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'eye',    'pose': 'right_lower_blink',           'driver': 'Eye_R_ctrl.lower_blink',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'eye',    'pose': 'left_upper_wideeyes',         'driver': 'Eye_L_ctrl.upper_blink',    'mapping': [-10, 0, 1, 0],    'overrides': [],    'overridemaps': [] },
 {'zone': 'eye',    'pose': 'right_upper_wideeyes',        'driver': 'Eye_R_ctrl.upper_blink',    'mapping': [-10, 0, 1, 0],    'overrides': [],    'overridemaps': [] },
 {'zone': 'eye',    'pose': 'left_lower_wideeyes',         'driver': 'Eye_L_ctrl.lower_blink',    'mapping': [-10, 0, 1, 0],    'overrides': [],    'overridemaps': [] },
 {'zone': 'eye',    'pose': 'right_lower_wideeyes',        'driver': 'Eye_R_ctrl.lower_blink',    'mapping': [-10, 0, 1, 0],    'overrides': [],    'overridemaps': [] },

 {'zone': 'eye',    'pose': 'left_pupil_small',            'driver': 'Eye_L_ctrl.pupil_dilation',    'mapping': [-10, 0, 1, 0],    'overrides': [],    'overridemaps': [] },
 {'zone': 'eye',    'pose': 'right_pupil_small',           'driver': 'Eye_R_ctrl.pupil_dilation',    'mapping': [-10, 0, 1, 0],    'overrides': [],    'overridemaps': [] },
 {'zone': 'eye',    'pose': 'left_pupil_large',            'driver': 'Eye_L_ctrl.pupil_dilation',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'eye',    'pose': 'right_pupil_large',           'driver': 'Eye_R_ctrl.pupil_dilation',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },

 # CHEEKS
 {'zone': 'cheek',    'pose': 'left_squint',               'driver': 'Eyelid_L_ctrl.squint',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'cheek',    'pose': 'right_squint',              'driver': 'Eyelid_R_ctrl.squint',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'cheek',    'pose': 'left_bunny',                'driver': 'Eyelid_L_ctrl.bunny',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] }, # the upper nose wrinkle. This would fire with sneer
 {'zone': 'cheek',    'pose': 'right_bunny',               'driver': 'Eyelid_R_ctrl.bunny',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] }, # the upper nose wrinkle. This would fire with sneer
 {'zone': 'cheek',    'pose': 'left_sneer',                'driver': 'Eyelid_L_ctrl.sneer',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] }, # cheek/eye based sne}r
 {'zone': 'cheek',    'pose': 'right_sneer',               'driver': 'Eyelid_R_ctrl.sneer',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'cheek',    'pose': 'left_cheek_puff',           'driver': 'MouthCorner_L_ctrl.cheek_puff',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'cheek',    'pose': 'right_cheek_puff',          'driver': 'MouthCorner_R_ctrl.cheek_puff',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'cheek',    'pose': 'left_cheek_suck',           'driver': 'MouthCorner_L_ctrl.cheek_puff',    'mapping': [0, -10, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'cheek',    'pose': 'right_cheek_suck',          'driver': 'MouthCorner_R_ctrl.cheek_puff',    'mapping': [0, -10, 0, 1],    'overrides': [],    'overridemaps': [] },

 # NOSE MUZZLE MOVER
 {'zone': 'nose',    'pose': 'nose_right_left',            'driver': 'Nose_M_ctrl.tx',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'nose',    'pose': 'nose_up_down',               'driver': 'Nose_M_ctrl.ty',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },
 # NOSE BENDER
 {'zone': 'nose',    'pose': 'nose_bend_right_left',       'driver': 'Nose_bend_ctrl.tx',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'nose',    'pose': 'nose_bend_up_down',          'driver': 'Nose_bend_ctrl.ty',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'nose',    'pose': 'nostril_flare',              'driver': 'Nose_bend_ctrl.nose_flare',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'nose',    'pose': 'nose_wide',                  'driver': 'Nose_bend_ctrl.nose_wide',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] }, # for mouth wide stretching
 {'zone': 'nose',    'pose': 'nose_muzzle_right_left',     'driver': 'Muzzle_M_ctrl.tx',    'mapping': [-1, 1, -1, 1],    'overrides': ['Nose_M_ctrl.nose_auto_follow'],    'overridemaps': [[0, 10, 1, 0]] },
 {'zone': 'nose',    'pose': 'nose_muzzle_up_down',        'driver': 'Muzzle_M_ctrl.ty',    'mapping': [-1, 1, -1, 1],    'overrides': ['Nose_M_ctrl.nose_auto_follow'],    'overridemaps': [[ 0, 10, 1, 0 ]] },
 
 # MOUTH LIP SYNC (8 poses clock-wise)
 {'zone': 'mouth',    'pose': 'mouth_open',                'driver': 'Mouth_M_ctrl.ty',    'mapping': [0, -1, 0, 1],   'overrides': ['Mouth_M_ctrl.tx', 'Mouth_M_ctrl.tx'],    'overridemaps': [[0, -1, 0, 1], [0, 1, 0, 1]] },
 {'zone': 'mouth',    'pose': 'mouth_ooh',                 'driver': 'Mouth_M_ctrl.tx',    'mapping': [0, -1, 0, 1],   'overrides': ['Mouth_M_ctrl.ty', 'Mouth_M_ctrl.ty'],    'overridemaps': [[0, -1, 0, 1], [0, 1, 0, 1]] },
 {'zone': 'mouth',    'pose': 'mouth_mmm',                 'driver': 'Mouth_M_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': ['Mouth_M_ctrl.tx', 'Mouth_M_ctrl.tx'],    'overridemaps': [[0, -1, 0, 1], [0, 1, 0, 1]] },
 {'zone': 'mouth',    'pose': 'mouth_wide',                'driver': 'Mouth_M_ctrl.tx',    'mapping': [0, 1, 0, 1],    'overrides': ['Mouth_M_ctrl.ty', 'Mouth_M_ctrl.ty'],    'overridemaps': [[0, -1, 0, 1], [0, 1, 0, 1]] },
 # MOUTH LIP SYNC CORNER CORRECTIVES
 {'zone': 'mouth',    'pose': 'mouth_ooh_open',            'driver': 'Mouth_M_ctrl.ty',    'mapping': [0, -1, 0, 1],   'overrides': ['Mouth_M_ctrl.tx'],    'overridemaps': [[ -1, 0, 0, 1 ]] },
 {'zone': 'mouth',    'pose': 'mouth_small_mmm',           'driver': 'Mouth_M_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': ['Mouth_M_ctrl.tx'],    'overridemaps': [[ -1, 0, 0, 1 ]] },
 {'zone': 'mouth',    'pose': 'mouth_wide_mmm',            'driver': 'Mouth_M_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': ['Mouth_M_ctrl.tx'],    'overridemaps': [[ 1, 0, 0, 1 ]] },
 {'zone': 'mouth',    'pose': 'mouth_wide_open',           'driver': 'Mouth_M_ctrl.ty',    'mapping': [0, -1, 0, 1],   'overrides': ['Mouth_M_ctrl.tx'],    'overridemaps': [[ 1, 0, 0, 1 ]] },
# MOUTH
 {'zone': 'mouth',    'pose': 'mouth_back_forward',        'driver': 'Mouth_M_ctrl.jaw_back_forward',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'mouth',    'pose': 'mouth_right_left',          'driver': 'Mouth_M_ctrl.jaw_side_to_side',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'mouth',    'pose': 'mouth_upper_lip_up',        'driver': 'Mouth_M_ctrl.upper_lip_UpDown',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'mouth',    'pose': 'mouth_upper_lip_down',      'driver': 'Mouth_M_ctrl.upper_lip_UpDown',    'mapping': [0, -10, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'mouth',    'pose': 'mouth_lower_lip_up',        'driver': 'Mouth_M_ctrl.lower_lip_UpDown',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'mouth',    'pose': 'mouth_lower_lip_down',      'driver': 'Mouth_M_ctrl.lower_lip_UpDown',    'mapping': [0, -10, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'mouth',    'pose': 'mouth_lower_pucker',        'driver': 'Mouth_M_ctrl.lower_pucker',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'mouth',    'pose': 'mouth_lower_purse',         'driver': 'Mouth_M_ctrl.lower_pucker',    'mapping': [0, -10, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'mouth',    'pose': 'mouth_upper_pucker',        'driver': 'Mouth_M_ctrl.upper_pucker',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'mouth',    'pose': 'mouth_upper_purse',         'driver': 'Mouth_M_ctrl.upper_pucker',    'mapping': [0, -10, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'mouth',    'pose': 'muzzle_right_left',         'driver': 'Muzzle_M_ctrl.tx',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'mouth',    'pose': 'muzzle_up_down',            'driver': 'Muzzle_M_ctrl.ty',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },

 # LEFT MOUTH CORNERS (8 poses)
 {'zone': 'mouth',    'pose': 'left_frown',                'driver': 'MouthCorner_L_ctrl.ty',    'mapping': [0, -1, 0, 1],   'overrides': ['MouthCorner_L_ctrl.tx', 'MouthCorner_L_ctrl.tx'],    'overridemaps': [[0, -1, 0, 1], [0, 1, 0, 1]] },
 {'zone': 'mouth',    'pose': 'left_mouth_narrow',         'driver': 'MouthCorner_L_ctrl.tx',    'mapping': [0, -1, 0, 1],   'overrides': ['MouthCorner_L_ctrl.ty', 'MouthCorner_L_ctrl.ty'],    'overridemaps': [[0, -1, 0, 1], [0, 1, 0, 1]] },
 {'zone': 'mouth',    'pose': 'left_mouth_smile',          'driver': 'MouthCorner_L_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': ['MouthCorner_L_ctrl.tx', 'MouthCorner_L_ctrl.tx'],    'overridemaps': [[0, -1, 0, 1], [0, 1, 0, 1]] },
 {'zone': 'mouth',    'pose': 'left_mouth_wide',           'driver': 'MouthCorner_L_ctrl.tx',    'mapping': [0, 1, 0, 1],    'overrides': ['MouthCorner_L_ctrl.ty', 'MouthCorner_L_ctrl.ty'],    'overridemaps': [[0, -1, 0, 1], [0, 1, 0, 1]] },
# LEFT MOUTH CORNER CORRECTIVES 
 {'zone': 'mouth',    'pose': 'left_narrow_frown',         'driver': 'MouthCorner_L_ctrl.ty',    'mapping': [0, -1, 0, 1],   'overrides': ['MouthCorner_L_ctrl.tx'],    'overridemaps': [[ -1, 0, 0, 1 ]] },
 {'zone': 'mouth',    'pose': 'left_mouth_narrow_smile',   'driver': 'MouthCorner_L_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': ['MouthCorner_L_ctrl.tx'],    'overridemaps': [[ -1, 0, 0, 1 ]] },
 {'zone': 'mouth',    'pose': 'left_mouth_wide_smile',     'driver': 'MouthCorner_L_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': ['MouthCorner_L_ctrl.tx'],    'overridemaps': [[ 1, 0, 0, 1 ]] },
 {'zone': 'mouth',    'pose': 'left_wide_frown',           'driver': 'MouthCorner_L_ctrl.ty',    'mapping': [0, -1, 0, 1],   'overrides': ['MouthCorner_L_ctrl.tx'],    'overridemaps': [[ 1, 0, 0, 1 ]] },
 # RIGHT MOUTH CORNERS (8 poses)
 {'zone': 'mouth',    'pose': 'right_frown',                'driver': 'MouthCorner_R_ctrl.ty',    'mapping': [0, -1, 0, 1],   'overrides': ['MouthCorner_R_ctrl.tx', 'MouthCorner_R_ctrl.tx'],    'overridemaps': [[0, -1, 0, 1], [0, 1, 0, 1]] },
 {'zone': 'mouth',    'pose': 'right_mouth_narrow',         'driver': 'MouthCorner_R_ctrl.tx',    'mapping': [0, 1, 0, 1],   'overrides': ['MouthCorner_R_ctrl.ty', 'MouthCorner_R_ctrl.ty'],    'overridemaps': [[0, -1, 0, 1], [0, 1, 0, 1]] },
 {'zone': 'mouth',    'pose': 'right_mouth_smile',          'driver': 'MouthCorner_R_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': ['MouthCorner_R_ctrl.tx', 'MouthCorner_R_ctrl.tx'],    'overridemaps': [[0, -1, 0, 1], [0, 1, 0, 1]] },
 {'zone': 'mouth',    'pose': 'right_mouth_wide',           'driver': 'MouthCorner_R_ctrl.tx',    'mapping': [0, -1, 0, 1],    'overrides': ['MouthCorner_R_ctrl.ty', 'MouthCorner_R_ctrl.ty'],    'overridemaps': [[0, -1, 0, 1], [0, 1, 0, 1]] },
# RIGHT MOUTH CORNER CORRECTIVES 
 {'zone': 'mouth',    'pose': 'right_narrow_frown',         'driver': 'MouthCorner_R_ctrl.ty',    'mapping': [0, -1, 0, 1],   'overrides': ['MouthCorner_R_ctrl.tx'],    'overridemaps': [[ 1, 0, 0, 1 ]] },
 {'zone': 'mouth',    'pose': 'right_mouth_narrow_smile',   'driver': 'MouthCorner_R_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': ['MouthCorner_R_ctrl.tx'],    'overridemaps': [[ 1, 0, 0, 1 ]] },
 {'zone': 'mouth',    'pose': 'right_mouth_wide_smile',     'driver': 'MouthCorner_R_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': ['MouthCorner_R_ctrl.tx'],    'overridemaps': [[ -1, 0, 0, 1 ]] },
 {'zone': 'mouth',    'pose': 'right_wide_frown',           'driver': 'MouthCorner_R_ctrl.ty',    'mapping': [0, -1, 0, 1],   'overrides': ['MouthCorner_R_ctrl.tx'],    'overridemaps': [[ -1, 0, 0, 1 ]] },

 {'zone': 'mouth',    'pose': 'left_mouth_round',          'driver': 'MouthCorner_L_ctrl.round_mouth',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'mouth',    'pose': 'right_mouth_round',         'driver': 'MouthCorner_R_ctrl.round_mouth',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'mouth',    'pose': 'left_mouth_tight',          'driver': 'MouthCorner_L_ctrl.round_mouth',    'mapping': [0, -10, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'mouth',    'pose': 'right_mouth_tight',         'driver': 'MouthCorner_R_ctrl.round_mouth',    'mapping': [0, -10, 0, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'mouth',    'pose': 'left_mouth_sneer',          'driver': 'MouthCorner_L_ctrl.sneer',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'mouth',    'pose': 'right_mouth_sneer',         'driver': 'MouthCorner_R_ctrl.sneer',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] },

 {'zone': 'mouth',    'pose': 'lips_move_sideways',        'driver': 'LipsMover_M_ctrl.tx',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'mouth',    'pose': 'lips_move_up_down',         'driver': 'LipsMover_M_ctrl.ty',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'mouth',    'pose': 'lips_puff',                 'driver': 'Mouth_M_ctrl.lip_puff',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] },
 {'zone': 'mouth',    'pose': 'lips_spin',                 'driver': 'Mouth_M_ctrl.lip_spin',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] },

]
