from . import (
	objects,
	generators,
	viz,
)

modules = [
	objects,
	generators,
	viz,
]

def register():
	for mod in modules:
		mod.register()

def unregister():
	for mod in reversed(modules):
		mod.unregister()
