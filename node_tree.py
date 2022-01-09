import bpy
from bpy.types import Node, NodeTree, PropertyGroup
from bpy.props import EnumProperty, IntProperty, PointerProperty

from gl_tree.data_structure import Mesh

class gl_NodeTreeCommon:
	t_id: bpy.props.StringProperty(default="")

	@property
	def tree_id(self):
		if not self.t_id:
			self.t_id = str(hash(self))
		return self.t_id

	def update_nodes(self, context):
		for node in self.nodes:
			node.gl_update()

	resolution: EnumProperty(name="Resolution", items=(
		(   '128',    '128', '', 0),
		(   '256',    '256', '', 1),
		(   '512',    '512', '', 2),
		(  '1024',   '1024', '', 3),
		(  '2048',   '2048', '', 4),
		('CUSTOM', 'Custom', '', 5)
	), default='1024', update=update_nodes)

	custom_resolution: IntProperty(name="Custom", default=1024, update=update_nodes)

	mesh = Mesh(vertices=(
		(-1, -1,  0),
		(-1,  1,  0),
		( 1, -1,  0),
		( 1,  1,  0)),
	indices=((0, 1, 2), (2, 3, 1)),
	uv=((0, 0), (0, 1), (1, 0), (1, 1)))


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
	def is_output_linked(self):
		return bool([sock for sock in self.outputs if sock.is_linked])

	@property
	def is_input_linked(self):
		return bool([sock for sock in self.inputs if sock.is_linked])

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
		if self.is_output_linked:
			nodes = self.get_linked_nodes()
			for node in nodes:
				node.gl_update()

	def draw_operator(self, layout, bl_idname):
		op = layout.operator(bl_idname)
		op.node_name = self.name
		op.tree_name = self.id_data.name

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
	def poll(cls, context):
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

