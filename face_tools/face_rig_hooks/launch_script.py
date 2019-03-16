#TODO: Deploy this properly in Maya scripts environment.
import sys
sys.path.append('/Users/sage/Projects/face-rig-hooks/')
import generate_poses_face_rig as FACE
reload(FACE)

FACE.do_the_thing()

import saved_poses
reload(saved_poses)

