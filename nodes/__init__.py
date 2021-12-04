from . import (
	objects,
	generators
)

modules = [
	objects,
	generators,
]

def register():
	for mod in modules:
		mod.register()

def unregister():
	for mod in reversed(modules):
		mod.unregister()
