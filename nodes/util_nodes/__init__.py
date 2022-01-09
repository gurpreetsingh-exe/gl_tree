from . import glsl_script

from gl_tree.node_tree import gl_NodeCategory, NodeItem, register_node_categories, unregister_node_categories

node_categories = [
	gl_NodeCategory('GL_UTILS', "Utilities", items=[
		NodeItem("gl_NodeGlslScript"),
	])
]

def register():
	glsl_script.register()
	register_node_categories('GL_UTILS', node_categories)

def unregister():
	unregister_node_categories('GL_UTILS')
	glsl_script.unregister()
