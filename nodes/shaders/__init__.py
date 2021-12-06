from . import default_shader

from gl_tree.node_tree import gl_NodeCategory, NodeItem, register_node_categories, unregister_node_categories

node_categories = [
	gl_NodeCategory('GL_SHADERS', "Shaders", items=[
		NodeItem("gl_NodeDefaultShader"),
	])
]

def register():
	default_shader.register()
	register_node_categories('GL_SHADERS', node_categories)

def unregister():
	unregister_node_categories('GL_SHADERS')
	default_shader.unregister()
