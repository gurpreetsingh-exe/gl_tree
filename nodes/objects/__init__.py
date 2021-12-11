from . import plane, object_info

from gl_tree.node_tree import gl_NodeCategory, NodeItem, register_node_categories, unregister_node_categories

node_categories = [
	gl_NodeCategory('GL_OBJECTS', "Objects", items=[
		NodeItem("gl_NodeObjectPlane"),
		NodeItem("gl_NodeObjectInfo"),
	])
]

modules = (
	plane,
	object_info,
)

def register():
	for mod in modules:
		mod.register()
	register_node_categories('GL_OBJECTS', node_categories)

def unregister():
	unregister_node_categories('GL_OBJECTS')
	for mod in modules:
		mod.unregister()
