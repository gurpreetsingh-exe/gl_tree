import bpy
from bpy.types import Node, NodeTree

class gl_NodeTreeCommon:
	t_id: bpy.props.StringProperty(default="")

	@property
	def tree_id(self):
		if not self.t_id:
			self.t_id = str(hash(self))
		return self.t_id

	def update_nodes(self, context):
		pass
		# for node in self.node_tree.nodes:
		# 	node.gl_update()

class gl_NodeTree(NodeTree, gl_NodeTreeCommon):
	bl_idname = "gl_NodeTree"
	bl_label = "glTree"
	bl_icon = 'SHADERFX'

class gl_BaseNode:
	n_id: bpy.props.StringProperty(options={'SKIP_SAVE'})
	init_node: bpy.props.BoolProperty(default=False)

	@property
	def node_id(self):
		if not self.n_id:
			self.n_id = str(hash(self))
		return self.n_id

	@property
	def is_linked(self):
		return bool([sock for sock in self.outputs if sock.is_linked])
		'''
		for sock in self.outputs:
			if sock.is_linked:
				return True
		return False'''

	def init(self, context):
		self.gl_init(context)
		self.init_node = True

	def free(self):
		pass

	def copy(self, node):
		pass

	def update(self):
		if self.init_node:
			self.gl_update()

	def get_linked_nodes(self):
		nodes = []
		for sock in self.outputs:
			for link in sock.links:
				nodes.append(link.to_node)
		return nodes

	def linked_update(self):
		if self.outputs and self.is_linked:
			nodes = self.get_linked_nodes()
			for node in nodes:
				node.gl_update()

	# Override these methods
	def gl_init(self, context):
		pass

	def gl_update(self):
		pass

def update_node(self, context):
	self.id_data.update_nodes(context)

class gl_CustomTreeNode(gl_BaseNode):
	node_cache = {}

	@classmethod
	def poll(cls, ntree):
		return ntree.bl_idname == "gl_NodeTree"

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem, register_node_categories, unregister_node_categories

class gl_NodeCategory(NodeCategory):
	@classmethod
	def polll(cls, context):
		return context.space_data.tree_type == "gl_NodeTree"

classes = [
	gl_NodeTree,
]

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)

