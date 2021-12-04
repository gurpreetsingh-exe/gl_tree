from . import buffer

from gl_tree.node_tree import gl_NodeCategory, NodeItem, register_node_categories, unregister_node_categories

node_categories = [
	gl_NodeCategory('GL_GENERATORS', "Generators", items=[
		NodeItem("gl_NodeBuffer"),
	])
]

def register():
	buffer.register()
	register_node_categories('GL_GENERATORS', node_categories)

def unregister():
	unregister_node_categories('GL_GENERATORS')
	buffer.unregister()
