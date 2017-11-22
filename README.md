# Rigmarole Blendshape Tools

author: Chris Lesage (Rigmarole Studio)

date: November 2017

A collection of utilities for working in Autodesk Maya
with blendshapes and character rigging workflows.

The [source for Rigmarole Blendshape Tools](https://github.com/chris-lesage/rigmarole-tools) is available on
GitHub.

I wrote this because Maya's "Flip Blendshape" silently corrupted my geometry
and I realized I needed some scripts I could trust and fix.

1. Split Blendshapes - I had never found a blendshape splitting tool where
you could control the falloff. Linear falloff usually causes visible seams.

2. Vertex Smash - This just sets the positions of the vertices to match
a target geo. It is especially useful when you are working in the Shape
Editor and have "Edit" enabled on a shape. It's a fast convenient way
to load a modelled shape into a blendshape which already exists without
having to delete the existing target and reload it.

More to come, including:
* working with weight maps
* soft selection falloff support
* multiple splits (not just left/right)
* splitting on a custom axis
* undo support
