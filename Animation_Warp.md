# Animation Warp by Chris Lesage
http://rigmarolestudio.com

### Summary
A work-in-progress Maya Python script that sets up a path-constraint system which "warps" a straight animation (like a walk-cycle) bending it so that it follows a path with no feet sliding. The animation remains editable in the original straight space.

Example Files:
chrislesage_blank_scene_with_walk_cycle.ma - (This is a file with a cat referenced with a walk cycle. Use this file as a starting point if you want to run the tool to see it in action.)
chrislesage_sabreCat_walking_warped.ma - (This file shows the RESULTS of having run the warp script and modified the warp path.)

### How To Use This Tool

1. Create a new scene
2. Reference your rig and animate it
3. Run the script
4. A window will pop up. Select all the IK and world-space controls. Head, neck, all spine controls, IK feet, etc.
5. Click on "Step 3: Warp".
6. It will create two paths; red and yellow. Red must be placed along your existing walk cycle. Yellow can be bent and moved to create the path you want.
7. At the end, the IK controllers you selected in step 4 will have constraints on them. You can bake this if you want keyframe data.

### Notes, Problems and Limitations

- The character MUST be referenced, not imported. The script queries the reference and references a 2nd instance of the character. This is currently a limitation that I am testing solutions for.
- The two characters share animation. The IK controls from step 4 have constraints but otherwise, editing any keyframe on the other controllers will affect both characters.
