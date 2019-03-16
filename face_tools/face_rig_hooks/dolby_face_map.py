# FACE MAP FOR DOLBY - Dolby Girl

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
        {'zone': 'nose',    'pose': 'nose_left',                  'driver': 'M_nose_ctrl.tx',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'nose',    'pose': 'nose_right',                 'driver': 'M_nose_ctrl.tx',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'nose',    'pose': 'nose_up',                    'driver': 'M_nose_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'nose',    'pose': 'nose_down',                  'driver': 'M_nose_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'nose',    'pose': 'nose_wide',                  'driver': 'M_nose_ctrl.nose_wide',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] }, # for mouth wide stretching
        {'zone': 'nose',    'pose': 'nose_flare',                 'driver': 'M_nose_ctrl.nose_flare',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'nose',    'pose': 'left_bunny',                 'driver': 'M_nose_ctrl.left_bunny',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'nose',    'pose': 'right_bunny',                'driver': 'M_nose_ctrl.right_bunny',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },

        {'zone': 'nose',    'pose': 'nose_muzzle_left',           'driver': 'M_muzzle_ctrl.tx',    'mapping': [0, 1, 0, 1],    'overrides': ['M_muzzle_ctrl.nose_auto_follow'],    'overridemaps': [[0, 10, 1, 0]] },
        {'zone': 'nose',    'pose': 'nose_muzzle_right',          'driver': 'M_muzzle_ctrl.tx',    'mapping': [0, -1, 0, 1],    'overrides': ['M_muzzle_ctrl.nose_auto_follow'],    'overridemaps': [[0, 10, 1, 0]] },
        {'zone': 'nose',    'pose': 'nose_muzzle_up_down',        'driver': 'M_muzzle_ctrl.ty',    'mapping': [-1, 1, -1, 1],    'overrides': ['M_muzzle_ctrl.nose_auto_follow'],    'overridemaps': [[ 0, 10, 1, 0 ]] },

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

         # MOUTH LIP SYNC (8 poses clock-wise)
         {'zone': 'mouth',    'pose': 'mouth_open',                'driver': 'M_mouth_ctrl.ty',    'mapping': [0, -1, 0, 1],   'overrides': ['M_mouth_ctrl.tx', 'M_mouth_ctrl.tx'],    'overridemaps': [[0, -1, 0, 1], [0, 1, 0, 1]] },
         {'zone': 'mouth',    'pose': 'mouth_ooh',                 'driver': 'M_mouth_ctrl.tx',    'mapping': [0, -1, 0, 1],   'overrides': ['M_mouth_ctrl.ty', 'M_mouth_ctrl.ty'],    'overridemaps': [[0, -1, 0, 1], [0, 1, 0, 1]] },
         {'zone': 'mouth',    'pose': 'mouth_mmm',                 'driver': 'M_mouth_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': ['M_mouth_ctrl.tx', 'M_mouth_ctrl.tx'],    'overridemaps': [[0, -1, 0, 1], [0, 1, 0, 1]] },
         {'zone': 'mouth',    'pose': 'mouth_wide',                'driver': 'M_mouth_ctrl.tx',    'mapping': [0, 1, 0, 1],    'overrides': ['M_mouth_ctrl.ty', 'M_mouth_ctrl.ty'],    'overridemaps': [[0, -1, 0, 1], [0, 1, 0, 1]] },
         # MOUTH LIP SYNC CORNER CORRECTIVES
         {'zone': 'mouth',    'pose': 'mouth_ooh_open',            'driver': 'M_mouth_ctrl.ty',    'mapping': [0, -1, 0, 1],   'overrides': ['M_mouth_ctrl.tx'],    'overridemaps': [[ -1, 0, 0, 1 ]] },
         {'zone': 'mouth',    'pose': 'mouth_small_mmm',           'driver': 'M_mouth_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': ['M_mouth_ctrl.tx'],    'overridemaps': [[ -1, 0, 0, 1 ]] },
         {'zone': 'mouth',    'pose': 'mouth_wide_mmm',            'driver': 'M_mouth_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': ['M_mouth_ctrl.tx'],    'overridemaps': [[ 1, 0, 0, 1 ]] },
         {'zone': 'mouth',    'pose': 'mouth_wide_open',           'driver': 'M_mouth_ctrl.ty',    'mapping': [0, -1, 0, 1],   'overrides': ['M_mouth_ctrl.tx'],    'overridemaps': [[ 1, 0, 0, 1 ]] },

        #NOTE: Pucker and Purse are driving 3 split shapes. I don't need all the splits.
        {'zone': 'mouth',    'pose': 'upper_pucker',              'driver': 'M_mouth_ctrl.upper_pucker',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'lower_pucker',              'driver': 'M_mouth_ctrl.lower_pucker',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'upper_purse',               'driver': 'M_mouth_ctrl.upper_pucker',    'mapping': [0, -10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'lower_purse',               'driver': 'M_mouth_ctrl.lower_pucker',    'mapping': [0, -10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'upper_lip_forward',         'driver': 'M_mouth_ctrl.upper_lip_forward',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'lower_lip_forward',         'driver': 'M_mouth_ctrl.lower_lip_forward',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'jaw_back_forward',          'driver': 'M_mouth_ctrl.jaw_back_forward',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'jaw_left',                  'driver': 'M_mouth_ctrl.jaw_side_to_side',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'jaw_right',                 'driver': 'M_mouth_ctrl.jaw_side_to_side',    'mapping': [0, -10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'muzzle_left',               'driver': 'M_muzzle_ctrl.tx',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'muzzle_right',              'driver': 'M_muzzle_ctrl.tx',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'muzzle_up_down',            'driver': 'M_muzzle_ctrl.ty',    'mapping': [-1, 1, -1, 1],    'overrides': [],    'overridemaps': [] },

        {'zone': 'mouth',    'pose': 'lips_move_left',            'driver': 'M_lipsMover_ctrl.tx',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'lips_move_right',           'driver': 'M_lipsMover_ctrl.tx',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'lips_move_up',              'driver': 'M_lipsMover_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'lips_move_down',            'driver': 'M_lipsMover_ctrl.ty',    'mapping': [0, -1, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'lip_puff',                  'driver': 'M_lipsMover_ctrl.lip_puff',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'mouth_tilt_right',          'driver': 'M_lipsMover_ctrl.mouth_tilt',    'mapping': [0, -10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'mouth_tilt_left',           'driver': 'M_lipsMover_ctrl.mouth_tilt',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },

        # MOUTH AND LIP SYNC

        # LEFT MOUTH CORNERS (8 poses)
        {'zone': 'mouth',    'pose': 'left_frown',               'driver': 'L_mouthCorner_ctrl.ty',    'mapping': [0, -1, 0, 1],   'overrides': ['L_mouthCorner_ctrl.tx', 'L_mouthCorner_ctrl.tx'],    'overridemaps': [[0, -1, 0, 1], [0, 1, 0, 1]] },
        {'zone': 'mouth',    'pose': 'left_narrow',              'driver': 'L_mouthCorner_ctrl.tx',    'mapping': [0, -1, 0, 1],   'overrides': ['L_mouthCorner_ctrl.ty', 'L_mouthCorner_ctrl.ty'],    'overridemaps': [[0, -1, 0, 1], [0, 1, 0, 1]] },
        {'zone': 'mouth',    'pose': 'left_smile',               'driver': 'L_mouthCorner_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': ['L_mouthCorner_ctrl.tx', 'L_mouthCorner_ctrl.tx'],    'overridemaps': [[0, -1, 0, 1], [0, 1, 0, 1]] },
        {'zone': 'mouth',    'pose': 'left_wide',                'driver': 'L_mouthCorner_ctrl.tx',    'mapping': [0, 1, 0, 1],    'overrides': ['L_mouthCorner_ctrl.ty', 'L_mouthCorner_ctrl.ty'],    'overridemaps': [[0, -1, 0, 1], [0, 1, 0, 1]] },
        # LEFT MOUTH CORNER CORRECTIVES 
        {'zone': 'mouth',    'pose': 'left_narrow_frown',        'driver': 'L_mouthCorner_ctrl.ty',    'mapping': [0, -1, 0, 1],   'overrides': ['L_mouthCorner_ctrl.tx'],    'overridemaps': [[ -1, 0, 0, 1 ]] },
        {'zone': 'mouth',    'pose': 'left_narrow_smile',        'driver': 'L_mouthCorner_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': ['L_mouthCorner_ctrl.tx'],    'overridemaps': [[ -1, 0, 0, 1 ]] },
        {'zone': 'mouth',    'pose': 'left_wide_smile',          'driver': 'L_mouthCorner_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': ['L_mouthCorner_ctrl.tx'],    'overridemaps': [[ 1, 0, 0, 1 ]] },
        {'zone': 'mouth',    'pose': 'left_wide_frown',          'driver': 'L_mouthCorner_ctrl.ty',    'mapping': [0, -1, 0, 1],   'overrides': ['L_mouthCorner_ctrl.tx'],    'overridemaps': [[ 1, 0, 0, 1 ]] },
        # RIGHT MOUTH CORNERS (8 poses)
        {'zone': 'mouth',    'pose': 'right_frown',              'driver': 'R_mouthCorner_ctrl.ty',    'mapping': [0, -1, 0, 1],   'overrides': ['R_mouthCorner_ctrl.tx', 'R_mouthCorner_ctrl.tx'],    'overridemaps': [[0, -1, 0, 1], [0, 1, 0, 1]] },
        {'zone': 'mouth',    'pose': 'right_narrow',             'driver': 'R_mouthCorner_ctrl.tx',    'mapping': [0, 1, 0, 1],   'overrides': ['R_mouthCorner_ctrl.ty', 'R_mouthCorner_ctrl.ty'],    'overridemaps': [[0, -1, 0, 1], [0, 1, 0, 1]] },
        {'zone': 'mouth',    'pose': 'right_smile',              'driver': 'R_mouthCorner_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': ['R_mouthCorner_ctrl.tx', 'R_mouthCorner_ctrl.tx'],    'overridemaps': [[0, -1, 0, 1], [0, 1, 0, 1]] },
        {'zone': 'mouth',    'pose': 'right_wide',               'driver': 'R_mouthCorner_ctrl.tx',    'mapping': [0, -1, 0, 1],    'overrides': ['R_mouthCorner_ctrl.ty', 'R_mouthCorner_ctrl.ty'],    'overridemaps': [[0, -1, 0, 1], [0, 1, 0, 1]] },
        # RIGHT MOUTH CORNER CORRECTIVES 
        {'zone': 'mouth',    'pose': 'right_narrow_frown',       'driver': 'R_mouthCorner_ctrl.ty',    'mapping': [0, -1, 0, 1],   'overrides': ['R_mouthCorner_ctrl.tx'],    'overridemaps': [[ 1, 0, 0, 1 ]] },
        {'zone': 'mouth',    'pose': 'right_narrow_smile',       'driver': 'R_mouthCorner_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': ['R_mouthCorner_ctrl.tx'],    'overridemaps': [[ 1, 0, 0, 1 ]] },
        {'zone': 'mouth',    'pose': 'right_wide_smile',         'driver': 'R_mouthCorner_ctrl.ty',    'mapping': [0, 1, 0, 1],    'overrides': ['R_mouthCorner_ctrl.tx'],    'overridemaps': [[ -1, 0, 0, 1 ]] },
        {'zone': 'mouth',    'pose': 'right_wide_frown',         'driver': 'R_mouthCorner_ctrl.ty',    'mapping': [0, -1, 0, 1],   'overrides': ['R_mouthCorner_ctrl.tx'],    'overridemaps': [[ -1, 0, 0, 1 ]] },

        {'zone': 'mouth',    'pose': 'left_mouth_sneer',          'driver': 'L_mouthCorner_ctrl.sneer',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] }, # mouth based sneer
        {'zone': 'mouth',    'pose': 'right_mouth_sneer',         'driver': 'R_mouthCorner_ctrl.sneer',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'left_grimace',              'driver': 'L_mouthCorner_ctrl.grimace',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] }, # mouth based grimace
        {'zone': 'mouth',    'pose': 'right_grimace',             'driver': 'R_mouthCorner_ctrl.grimace',    'mapping': [-10, 10, -1, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'left_mouth_curl_up',        'driver': 'L_mouthCorner_ctrl.mouth_curl',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'right_mouth_curl_up',       'driver': 'R_mouthCorner_ctrl.mouth_curl',    'mapping': [0, 10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'left_mouth_curl_down',      'driver': 'L_mouthCorner_ctrl.mouth_curl',    'mapping': [0, -10, 0, 1],    'overrides': [],    'overridemaps': [] },
        {'zone': 'mouth',    'pose': 'right_mouth_curl_down',     'driver': 'R_mouthCorner_ctrl.mouth_curl',    'mapping': [0, -10, 0, 1],    'overrides': [],    'overridemaps': [] },

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
