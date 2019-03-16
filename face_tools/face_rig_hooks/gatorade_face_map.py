# FACE MAP FOR GATORADE - mamaBolt

def get_face_map():
    faceposes = [
        #TODO: Include the zone that the poses belong to. THEN shorten the pose names. But put zones into the naming conventions of the background nodes.
        #TODO: This giant list is a bit incomprehensible...
        # HEAD
        {'zone': 'head',    'pose': 'head_right_left',            'driver': 'M_headSquash_ctrl.tx',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'head',    'pose': 'head_squash',                'driver': 'M_headSquash_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'head',    'pose': 'head_stretch',               'driver': 'M_headSquash_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },

        # EYEBROWS
        {'zone': 'brow',    'pose': 'left_brow_squeeze',          'driver': 'L_brow1_ctrl.squeeze',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'brow',    'pose': 'right_brow_squeeze',         'driver': 'R_brow1_ctrl.squeeze',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },

        {'zone': 'brow',    'pose': 'left_brow1_up',              'driver': 'L_brow1_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'brow',    'pose': 'right_brow1_up',             'driver': 'R_brow1_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'brow',    'pose': 'left_brow1_down',            'driver': 'L_brow1_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'brow',    'pose': 'right_brow1_down',           'driver': 'R_brow1_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },

        {'zone': 'brow',    'pose': 'left_brow2_up',              'driver': 'L_brow2_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'brow',    'pose': 'right_brow2_up',             'driver': 'R_brow2_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'brow',    'pose': 'left_brow2_down',            'driver': 'L_brow2_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'brow',    'pose': 'right_brow2_down',           'driver': 'R_brow2_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },

        {'zone': 'brow',    'pose': 'left_brow3_up',              'driver': 'L_brow3_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'brow',    'pose': 'right_brow3_up',             'driver': 'R_brow3_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'brow',    'pose': 'left_brow3_down',            'driver': 'L_brow3_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'brow',    'pose': 'right_brow3_down',           'driver': 'R_brow3_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },

        {'zone': 'brow',    'pose': 'left_brow4_up',              'driver': 'L_brow4_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'brow',    'pose': 'right_brow4_up',             'driver': 'R_brow4_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'brow',    'pose': 'left_brow4_down',            'driver': 'L_brow4_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'brow',    'pose': 'right_brow4_down',           'driver': 'R_brow4_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },


        # UPPER EYELIDS
        {'zone': 'eye',    'pose': 'left_upper_lid1_up',          'driver': 'L_upperLid1_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'right_upper_lid1_up',         'driver': 'R_upperLid1_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'left_upper_lid1_down',        'driver': 'L_upperLid1_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'right_upper_lid1_down',       'driver': 'R_upperLid1_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },

        {'zone': 'eye',    'pose': 'left_upper_lid2_up',          'driver': 'L_upperLid2_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'right_upper_lid2_up',         'driver': 'R_upperLid2_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'left_upper_lid2_down',        'driver': 'L_upperLid2_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'right_upper_lid2_down',       'driver': 'R_upperLid2_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },

        {'zone': 'eye',    'pose': 'left_upper_lid3_up',          'driver': 'L_upperLid3_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'right_upper_lid3_up',         'driver': 'R_upperLid3_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'left_upper_lid3_down',        'driver': 'L_upperLid3_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'right_upper_lid3_down',       'driver': 'R_upperLid3_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },

        {'zone': 'eye',    'pose': 'left_upper_lid4_up',          'driver': 'L_upperLid4_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'right_upper_lid4_up',         'driver': 'R_upperLid4_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'left_upper_lid4_down',        'driver': 'L_upperLid4_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'right_upper_lid4_down',       'driver': 'R_upperLid4_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },

        # LOWER EYELIDS
        {'zone': 'eye',    'pose': 'left_lower_lid1_up',          'driver': 'L_lowerLid1_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'right_lower_lid1_up',         'driver': 'R_lowerLid1_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'left_lower_lid1_down',        'driver': 'L_lowerLid1_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'right_lower_lid1_down',       'driver': 'R_lowerLid1_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },

        {'zone': 'eye',    'pose': 'left_lower_lid2_up',          'driver': 'L_lowerLid2_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'right_lower_lid2_up',         'driver': 'R_lowerLid2_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'left_lower_lid2_down',        'driver': 'L_lowerLid2_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'right_lower_lid2_down',       'driver': 'R_lowerLid2_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },

        {'zone': 'eye',    'pose': 'left_lower_lid3_up',          'driver': 'L_lowerLid3_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'right_lower_lid3_up',         'driver': 'R_lowerLid3_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'left_lower_lid3_down',        'driver': 'L_lowerLid3_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'right_lower_lid3_down',       'driver': 'R_lowerLid3_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },

        {'zone': 'eye',    'pose': 'left_lower_lid4_up',          'driver': 'L_lowerLid4_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'right_lower_lid4_up',         'driver': 'R_lowerLid4_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'left_lower_lid4_down',        'driver': 'L_lowerLid4_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'right_lower_lid4_down',       'driver': 'R_lowerLid4_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },

        # EYES
        {'zone': 'eye',    'pose': 'left_eye_in_out',             'driver': 'L_eye_ctrl.eyeInOut',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'right_eye_in_out',            'driver': 'R_eye_ctrl.eyeInOut',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'left_eye_y_sideways',         'driver': 'L_eye_ctrl.tx',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'right_eye_y_sideways',        'driver': 'R_eye_ctrl.tx',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'left_eye_x_up_down',          'driver': 'L_eye_ctrl.ty',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'right_eye_x_up_down',         'driver': 'R_eye_ctrl.ty',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },

        {'zone': 'eye',    'pose': 'left_softeye_y_sideways',     'driver': 'L_eye_ctrl.tx',    'mapping': [-1, 1, -1, 1],    'overrides': ['L_eye_ctrl.eyelidsFollow'],    'overridemaps': [[0, 10, 1, 0]] },
        {'zone': 'eye',    'pose': 'right_softeye_y_sideways',    'driver': 'R_eye_ctrl.tx',    'mapping': [-1, 1, -1, 1],    'overrides': ['R_eye_ctrl.eyelidsFollow'],    'overridemaps': [[0, 10, 1, 0]] },
        {'zone': 'eye',    'pose': 'left_softeye_x_up_down',      'driver': 'L_eye_ctrl.ty',    'mapping': [-1, 1, -1, 1],    'overrides': ['L_eye_ctrl.eyelidsFollow'],    'overridemaps': [[0, 10, 1, 0]] },
        {'zone': 'eye',    'pose': 'right_softeye_x_up_down',     'driver': 'R_eye_ctrl.ty',    'mapping': [-1, 1, -1, 1],    'overrides': ['R_eye_ctrl.eyelidsFollow'],    'overridemaps': [[0, 10, 1, 0]] },

        {'zone': 'eye',    'pose': 'left_pupil_small',            'driver': 'L_eye_ctrl.pupil_dilation',    'mapping': [-10, 0, 1, 0],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'right_pupil_small',           'driver': 'R_eye_ctrl.pupil_dilation',    'mapping': [-10, 0, 1, 0],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'left_pupil_large',            'driver': 'L_eye_ctrl.pupil_dilation',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'right_pupil_large',           'driver': 'R_eye_ctrl.pupil_dilation',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },

        {'zone': 'eye',    'pose': 'left_squint',                 'driver': 'L_eye_ctrl.squint',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'eye',    'pose': 'right_squint',                'driver': 'R_eye_ctrl.squint',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] },

        # NOSE
        {'zone': 'nose',    'pose': 'left_nose',                  'driver': 'M_nose_ctrl.tx',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'nose',    'pose': 'right_nose',                 'driver': 'M_nose_ctrl.tx',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'nose',    'pose': 'up_nose',                    'driver': 'M_nose_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'nose',    'pose': 'down_nose',                  'driver': 'M_nose_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'nose',    'pose': 'wide_nose',                  'driver': 'M_nose_ctrl.nose_wide',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] }, # for mouth wide stretching

        {'zone': 'nose',    'pose': 'left_nose_muzzle',           'driver': 'M_muzzle_ctrl.tx',    'mapping': [0, 1, 0, 1],    'overrides': ['M_muzzle_ctrl.nose_auto_follow'],    'overridemaps': [[0, 10, 1, 0]] },
        {'zone': 'nose',    'pose': 'right_nose_muzzle',          'driver': 'M_muzzle_ctrl.tx',    'mapping': [0, -1, 0, 1],    'overrides': ['M_muzzle_ctrl.nose_auto_follow'],    'overridemaps': [[0, 10, 1, 0]] },
        {'zone': 'nose',    'pose': 'up_nose_muzzle',             'driver': 'M_muzzle_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': ['M_muzzle_ctrl.nose_auto_follow'],    'overridemaps': [[ 0, 10, 1, 0 ]] },
        {'zone': 'nose',    'pose': 'down_nose_muzzle',           'driver': 'M_muzzle_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': ['M_muzzle_ctrl.nose_auto_follow'],    'overridemaps': [[ 0, 10, 1, 0 ]] },

        # LIPS
        {'zone': 'mouth',    'pose': 'right_upper_lip_up',        'driver': 'R_upperLip_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'mid_upper_lip_up',          'driver': 'M_upperLip_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'left_upper_lip_up',         'driver': 'L_upperLip_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },

        {'zone': 'mouth',    'pose': 'right_upper_lip_down',      'driver': 'R_upperLip_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'mid_upper_lip_down',        'driver': 'M_upperLip_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'left_upper_lip_down',       'driver': 'L_upperLip_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },

        {'zone': 'mouth',    'pose': 'right_lower_lip_up',        'driver': 'R_lowerLip_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'mid_lower_lip_up',          'driver': 'M_lowerLip_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'left_lower_lip_up',         'driver': 'L_lowerLip_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },

        {'zone': 'mouth',    'pose': 'right_lower_lip_down',      'driver': 'R_lowerLip_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'mid_lower_lip_down',        'driver': 'M_lowerLip_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'left_lower_lip_down',       'driver': 'L_lowerLip_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },

        # MOUTH AND LIP SYNC
        #TODO: Split this into 8-quadrants
        {'zone': 'mouth',    'pose': 'mouth_open',                'driver': 'M_mouth_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'mouth_mmm',                 'driver': 'M_mouth_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'mouth_narrow',              'driver': 'M_mouth_ctrl.tx',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'mouth_wide',                'driver': 'M_mouth_ctrl.tx',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] }, #TODO: Drive left and right - instance poses? Macros?
        #NOTE: Pucker and Purse are driving 3 split shapes. I don't need all the splits.
        {'zone': 'mouth',    'pose': 'mouth_upper_pucker',        'driver': 'M_mouth_ctrl.upper_pucker',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'mouth_upper_purse',         'driver': 'M_mouth_ctrl.upper_pucker',    'mapping': [0, -10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'mouth_lower_pucker',        'driver': 'M_mouth_ctrl.lower_pucker',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'mouth_lower_purse',         'driver': 'M_mouth_ctrl.lower_pucker',    'mapping': [0, -10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'jaw_back_forward',          'driver': 'M_mouth_ctrl.jaw_back_forward',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'left_jaw',                  'driver': 'M_mouth_ctrl.jaw_side_to_side',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'right_jaw',                 'driver': 'M_mouth_ctrl.jaw_side_to_side',    'mapping': [0, -10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'left_muzzle',               'driver': 'M_muzzle_ctrl.tx',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'right_muzzle',              'driver': 'M_muzzle_ctrl.tx',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'up_muzzle',                 'driver': 'M_muzzle_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'down_muzzle',               'driver': 'M_muzzle_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },

        {'zone': 'mouth',    'pose': 'left_lips_move',            'driver': 'M_lipsMover_ctrl.tx',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'right_lips_move',           'driver': 'M_lipsMover_ctrl.tx',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'up_lips_move',              'driver': 'M_lipsMover_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'down_lips_move',            'driver': 'M_lipsMover_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },

        # MOUTH AND LIP SYNC
        {'zone': 'mouth',    'pose': 'left_mouth_smile',          'driver': 'L_mouthCorner_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'right_mouth_smile',         'driver': 'R_mouthCorner_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'left_frown',                'driver': 'L_mouthCorner_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'right_frown',               'driver': 'R_mouthCorner_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'left_mouth_narrow',         'driver': 'L_mouthCorner_ctrl.tx',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'right_mouth_narrow',        'driver': 'R_mouthCorner_ctrl.tx',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'left_mouth_wide',           'driver': 'L_mouthCorner_ctrl.tx',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'right_mouth_wide',          'driver': 'R_mouthCorner_ctrl.tx',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'left_mouth_sneer',          'driver': 'L_mouthCorner_ctrl.sneer',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] }, # mouth based sneer
        {'zone': 'mouth',    'pose': 'right_mouth_sneer',         'driver': 'R_mouthCorner_ctrl.sneer',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] },

        # CHEEKS
        {'zone': 'mouth',    'pose': 'left_cheek_puff',           'driver': 'L_mouthCorner_ctrl.cheek_puff',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'right_cheek_puff',          'driver': 'R_mouthCorner_ctrl.cheek_puff',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'left_cheek_suck',           'driver': 'L_mouthCorner_ctrl.cheek_puff',    'mapping': [0, -10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'right_cheek_suck',          'driver': 'R_mouthCorner_ctrl.cheek_puff',    'mapping': [0, -10, 0, 1],    'overrides': [],    'overridemaps': [] },

        # TEETH
        {'zone': 'mouth',    'pose': 'upper_teeth_LR',            'driver': 'M_upperTeeth_ctrl.tx',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'lower_teeth_LR',            'driver': 'M_lowerTeeth_ctrl.tx',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },
        
        {'zone': 'mouth',    'pose': 'upper_teeth_UD',            'driver': 'M_upperTeeth_ctrl.ty',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'lower_teeth_UD',            'driver': 'M_lowerTeeth_ctrl.ty',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },

        {'zone': 'mouth',    'pose': 'upper_teeth_IO',            'driver': 'M_upperTeeth_ctrl.teethInOut',    'mapping': [-10, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'lower_teeth_IO',            'driver': 'M_lowerTeeth_ctrl.teethInOut',    'mapping': [-10, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
        
        {'zone': 'mouth',    'pose': 'upper_gum_height',          'driver': 'M_upperTeeth_ctrl.gumHeight',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'lower_gum_height',          'driver': 'M_lowerTeeth_ctrl.gumHeight',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'upper_teeth_height',        'driver': 'M_upperTeeth_ctrl.teethHeight',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'lower_teeth_height',        'driver': 'M_lowerTeeth_ctrl.teethHeight',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
        #NOTE: teeth width works on both upper and lower. So I'll just put it on the upper teeth control
        {'zone': 'mouth',    'pose': 'teeth_wide',                'driver': 'M_upperTeeth_ctrl.teethWidth',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'teeth_narrow',              'driver': 'M_upperTeeth_ctrl.teethWidth',    'mapping': [0, -10, 0, 1],    'overrides': [],    'overridemaps': [] },

        {'zone': 'mouth',    'pose': 'upper_teeth_tiltL',         'driver': 'M_upperTeeth_ctrl.teethTilt',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'upper_teeth_tiltR',         'driver': 'M_upperTeeth_ctrl.teethTilt',    'mapping': [0, -10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'lower_teeth_tiltL',         'driver': 'M_lowerTeeth_ctrl.teethTilt',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'lower_teeth_tiltR',         'driver': 'M_lowerTeeth_ctrl.teethTilt',    'mapping': [0, -10, 0, 1],    'overrides': [],    'overridemaps': [] },

    ]

    return faceposes
