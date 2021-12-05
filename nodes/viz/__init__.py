from . import viewer

from gl_tree.node_tree import gl_NodeCategory, NodeItem, register_node_categories, unregister_node_categories

node_categories = [
	gl_NodeCategory('GL_VIZ', "Viz", items=[
		NodeItem("gl_NodeMeshViewer"),
	])
]

def register():
	viewer.register()
	register_node_categories('GL_VIZ', node_categories)

def unregister():
	unregister_node_categories('GL_VIZ')
	viewer.unregister()
