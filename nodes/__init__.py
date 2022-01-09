from . import (
	objects,
	generators,
	viz,
	shaders,
	util_nodes,
)

modules = [
	objects,
	generators,
	viz,
	shaders,
	util_nodes,
]

def register():
	for mod in modules:
		mod.register()

def unregister():
	for mod in reversed(modules):
		mod.unregister()
