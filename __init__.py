bl_info = {
	"name": "gl_tree",
	"description": "Node-based texturing & procedural shaders",
	"version": (0, 0, 1),
	"blender": (2, 93, 0),
	"author": "Gurpreet Singh",
	"location": "Node Editor",
	"category": "Node",
}

import bpy

from . import node_tree
from . import nodes

modules = [
	nodes,
	node_tree,
]

def register():
	for mod in modules:
		mod.register()

def unregister():
	for mod in reversed(modules):
		mod.unregister()
