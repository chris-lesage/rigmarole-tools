# Animation Warp by Chris Lesage
http://rigmarolestudio.com

(Last updated June 2018)

### SUMMARY:
A work-in-progress Maya Python script that sets up a path-constraint system which "warps" a straight animation (like a walk-cycle), bending it so that it follows a path with no feet sliding. The animation in the original straight walk-cycle remains editable.

### TO USE THIS TOOL:
1. Reference a rig. It won't work if the rig is imported in the scene. It must be referenced.
2. Run the script. A window will pop open.
3. In "STEP 1", select all the IK controls, and any controls which are in world-space, like the COG.
4. In "STEP 2", select ALL the controls in the character and hit the button. It is important to get all of the controls, even ones that are hidden.
5. Run the script by clicking "Step 3: Warp".
6. The tool will reference a 2nd character into the scene. It will create two paths; red and yellow. Red must be placed along your existing walk cycle. Yellow can be bent and moved to create the path you want.
7. Afterwards, all of the IK and mover controllers you selected in "STEP 1" will have constraints on them. You can bake this if you want keyframe data. All of the other controls are going to SHARE animation. So if you edit the curve in the graph editor, it is going to move both characters at the same time.

### NOTES, PROBLEMS AND LIMITATIONS:
* The character MUST be referenced, not imported. The script queries the reference and references a 2nd instance of the character. This is currently a limitation that I am testing solutions for.

* The two characters share animation. The IK controls from step 4 have constraints but otherwise, editing any keyframe on the other controllers will affect both characters.

* Another way to use this tool is to rotate the entire path without bending it. This is useful if you want to change the direction of your walk-cycle without changing the orientation of your master controller.

* In the future, there will be a button that lets you automatically bake the warped animation. Right now, you have to do it manually.
