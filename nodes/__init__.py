from . import (
	objects,
	generators,
	viz,
	shaders,
)

modules = [
	objects,
	generators,
	viz,
	shaders,
]

def register():
	for mod in modules:
		mod.register()

def unregister():
	for mod in reversed(modules):
		mod.unregister()
