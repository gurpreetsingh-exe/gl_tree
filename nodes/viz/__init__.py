from . import (mesh_viewer, texture_viewer)

from gl_tree.node_tree import gl_NodeCategory, NodeItem, register_node_categories, unregister_node_categories

node_categories = [
	gl_NodeCategory('GL_VIZ', "Viz", items=[
		NodeItem("gl_NodeMeshViewer"),
		NodeItem("gl_NodeTextureViewer"),
	])
]

modules = (
	mesh_viewer,
	texture_viewer,
)

def register():
	for mod in modules:
		mod.register()
	register_node_categories('GL_VIZ', node_categories)

def unregister():
	unregister_node_categories('GL_VIZ')
	for mod in reversed(modules):
		mod.unregister()
