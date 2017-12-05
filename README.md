# Rigmarole Blendshape Tools (alpha)

*Beware. This tool is very early in development. It contains several bugs and no undo support. But the core functionality does work. Save yer scene...*

author: Chris Lesage (Rigmarole Studio)

date: December 2017

A collection of utilities for working in Autodesk Maya (Tested in Maya 2016 and 2017.)
with blendshapes and character rigging workflows.

The [source for Rigmarole Blendshape Tools](https://github.com/chris-lesage/rigmarole-tools) is available on
GitHub.

I wrote this because Maya's "Flip Blendshape" silently corrupted my geometry
and I realized I needed some scripts I could trust and fix.

1. Split Blendshapes - I had never found a blendshape splitting tool where
you could control the falloff. Linear falloff usually causes visible seams at the
edge of the falloff. Especially on dense geometry.

Other split tools I've seen would use a percentage of the geometry's width. This
tool uses split helpers to read split positions, so you can get consistent splits
between geometry of different widths. For example, head vs. eyebrow geometry.

2. Vertex Smash - This simply sets the positions of the vertices to match
a target geo. It is especially useful when you are working in the Shape
Editor and have "Edit" enabled on a shape. It's a fast convenient way
to load a modelled shape into a blendshape which already exists without
having to delete the existing target and reload it. Tools like this already
exist in Maya and the Shape Editor, but I'll integrate it into the BS Tools.

3. Split by Soft Selection - This takes a selection and splits between what is
selected and what isn't. This is very useful for isolating the upper eyelid
from a total blink shape, for example. Or for splitting a custom seam that a
world axis couldn't give you.

4. Split by weight map - Coming later.

More to come, including:
[x] Split by soft selection support
* multiple splits (not just left/right)
* Vertex smash to support soft selection
* splitting on a custom axis
* undo support!
* working with weight maps
* Basic API to run the commands in a script.
