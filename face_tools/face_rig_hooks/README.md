# face-rig-hooks
A semi-modular face rigging system

Author: Chris Lesage

Email: chris@chrislesage.com

### Overview

This is a WIP face rigging system that uses locators to generate pose deltas for a joint based rig.

It also supports blendshapes and passing arbitrary data through attributes stored on joints. These joints can be baked and their information can be used in a game engine.

### Outstanding Issues
* I wish jaw open and lips opening were a combo, so that I could override the lips opening. Move the jaw but seal the lips. Or do this with a special attribute.
* DONE Add lip moving control that slides lips across the teeth
* DONE Add a corrective for ooh + mouth open to avoid that weird keyhole effect.
* Fix the skinning on the mouth. I am not getting a perfect seal. I fixed sneer and broke other shapes.
* DONE "Cheeks" attributes should be mapped back onto the lower eyelid controls. Except "Cheek Puff" should be put on the corner lips. Cheeks is a useless control.
* I need a "lip press" row of joints for getting good MMM shapes. Or a blendshape.
* I need to solve the way the squint interacts with the blink blendshapes/skinning without collapsing the eye
* There is some weird jittering/interpolation in the pucker. I need a local pivot on each joint.
* Cheek puff needs better skinning
* Eyebrow skinning is a little dicey in some extremes. Might need 4 joints instead of only 3.

* MAPPING POSES:
	* Sometimes, I want to re-use a pose on multiple attributes. For example, mouth_wide gets driven by both the mouth control and the left and right corner controls. How shall I handle that? Instanced poses? Multiple drivers/hooks?
	* I have figured out a way to map overrides to controllers for things like small_mmm. But I had originally imagined the results of poses to override other poses. So if you did an override on a pose, all the poses that IT overrides would come back on. But everything is being driven by controls anyway. So I might as well map it all through controllers. The end result is the same. MMM and OOH are being blended off...
	* ALTERNATIVELY, I could say that a pose or -pose is the override, and then the script would automatically map it the same or reverse as the mapping for that pose. I could make it so that it can take either a list of numbers or a pose name as input. But for now I can set it up manually...

* ORIENTATION of joints and driven pivots. Can I just rotate the joints and derive orientation? OR, if I want to be game-friendly, maybe I should store NEUTRAL as a pose, and drive the joints directly. The NEUTRAL pose can also be driven by pose locators.
* Is there a way that I can dynamically move (and then save) the pivot position of any given joint? The other idea I had was that **underneath** each point is a pivot locator that can be moved relative to the joint. Then when I run the build, it flips the hierarchy and puts the joint underneath that pivot. If there is no pivot underneath the joint, then the joint's transform is used.
* Right now I am imagining having multiple pivot points, but this seems overly complex...
* How am I going to define all this information in an easy to edit way? Text files.
* I have **Macros, Overrides and Blendshapes**. It seems like there might be some conceptual overlap here...
* I originally imagined automatically handling symmetry. At least defining left poses and including right poses. But at most, having a way of setting one side and having the right follow automatically. At least, I think I'll add a keyword like "**symmetry_smile**" which will result in "**left_smile**" and "**right_smile**"

### The Conventions

The joints involved in opening the mouth are called "mouth". Not lips.
The area above and below the mouth are top_lip and bottom_lip.

### The Rig Structure

**zones, poses, poseAttributes, blendshapePoses, overrides, macros, joints, pivots, drivers, hooks**

**Zones** --- To put a joint in a Zone, put it into a set called [name]_zone. Eg. mouth_zone. A joint can belong to multiple Zones, but it is best to put it in as least amount of zones as possible. If you want the nose to move a bit in a mouth pose, use a Macro with a small positive value.

**Poses** --- drive all the joints in their zone. They also drive a portion of each custom attribute. Every pose must belong in a zone. If it doesn't, I'll automatically include a "misc" zone to capture all the orphans.

**poseAttributes** --- Arbitrary Attributes live on each pose. Each pose can contribute (or subtract) from attributes. You can thus use these as drivers for wrinkles, blendshapes, or any other custom behaviour. The attributes are clamped from 0.0 to 1.0 so they can drive normalized things like a wrinkle map from off to on. And so combinations of poses don't overdrive them.

**BlendshapePose** --- This is a special zone that contains no joints. Poses would still run through the Hook and Attribute system and could have Overrides, just like poses. Note that this is different than PoseAttributes. PoseAttributes are driven in part by every single pose. Note that if I was running a blendshape as a wrinkle shape, I would want it to be driven by a PoseAttribute. A BlendshapePose would only have one driver.

**Overrides** --- Each pose can override a list of other poses. eg. "special wide smile" could override "wide" and "smile", as a corrective shape. When it is turned to 1.0, the other poses are cancelled out. Or "closed_lips" could prevent the lips opening to seal the lips and get chewing effects.

**Macros** --- Macros are like positive Overrides. An Override multiplies a pose down to 0.0. But a Macro will follow the pose at a multiplied amount. If you had a Macro at -1.0 it would act like an override, but it wouldn't clamp. If the pose went to -2.0, the macro would also go to -2.0. But usually a Macro would be a tiny amount like 0.1 so that you could have some small amounts of other poses driven by other poses.

**Joints** --- **_jnt** joints get included in the skeleton but not in poses. **_hub** joints are just for organizing joints to keep the visible hierarchy cleaner. They don't get skinned. **_skin** joints are used in the skinning, and they are driven by poses. A _skin joint can be a group too. A lot of joints get parented under the jaw and muzzle. But those are skin joints. "_hub" says to not include it in the final skeleton.

**Pivots** --- The _skin joints define the skinning skeleton. But any joint can have multiple pivots. The driving pose values exist on Pivots and drive the joints. This way, multiple joints can have the same pivot point, but the skin joints won't all be in the same position. And by having multiple pivot points, you can define arcing motion that wouldn't be possible with simple linear drivers. This also keeps the base skeleton simple, and a layer of complexity is kept on the rig.

**Drivers** --- Every control rig attribute can be a driver. It has a mapping to the Hooks.

**Hooks** --- The Hooks drive the poses. It is a list of attributes that get driven by the Drivers. But if you didn't drive these attributes by any controllers, you could drive the entire face rig directly from the Hooks. When the smile Hook is set to 1.0, the smile pose is fully on. When it is 2.0, it is driven doubly. The hooks have no negative or positive limits. It relies on the mapping you define in the rig.

### The Definitions

[Describe how to define poses, overrides, macros and driver relationships. These will likely be text files of some sort.]


### Notes

> I want to add arbitrary attributes to the rig. Right now, each special attribute is driven by each pose. But what if I wanted to only have 5 joint poses, and then 20 blendshape attribute poses. Is this a 3rd thing? For each blendShape pose, the arbitrary attributes would get driven too.

> * A pose can drive all joints
* Each pose drives some amount of each arbitrary attribute
* A pose can drive a blendShape, if it is the only one driving some attribute (it would also drive all joints)
* When I build the final rig, I can delete all connections that have an empty delta for optimization
* I could add a flag to each pose that would say whether it drives joints or blendshapes (or both)
* I am thinking of this rig to be game OR film compatible, so blendshapes would be less common. (Think Coq)
* If I had 20 blendshapes, each pose would need 20 attributes and most would do nothing... (again weed empty deltas later.)
* I could keep associations of joints to poses, so a pose would only affect certain joints. Otherwise every pose will include every single locator, which will be cumbersome to edit, won't it? Or is it better to overshoot, and then prune-optimize later?
* Instead, I could have a Zone called "Blendshapes". This zone doesn't drive any joints. I could store any number of poses in this Zone and drive a 100% Blendshape rig using this. And then if I added one pose in "Muzzle" I could have a single mouth open pose, but all others are blendshapes. The blendshapes would be driven by a Hook system that could have Overrides and Attributes too.
* **The poses could be split into zones**, and each pose would only affect the joints which are in that zone. Any joint can be in multiple zones. But usually it will just be one. Instead of managing giant lists of joints, I'd only have to pick between zones: "head", "brow", "eye", "cheek", "nose", "muzzle", "jaw" (The muzzle zone will have 14 joints instead of all 80. For 42 poses, this is already 2240 less pose locators and connections. Some zones will have less joints. This is a good move.)
* Each zone will have a "hub" joint. But muzzle, jaw and nose should be together. If I combine those, I think those are the only zones which will interact with each other very much. All other zones will likely be quite separated.
