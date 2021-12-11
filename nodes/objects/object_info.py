import bpy
from bpy.types import Node, Operator

from gl_tree.data_structure import Mesh
from gl_tree.node_tree import gl_CustomTreeNode, update_node
from mathutils import Vector
import numpy as np

selection = None

class GL_OT_get_selection(Operator):
	bl_idname = "gl.get_selection"
	bl_label = "Get Selection"

	node_name: bpy.props.StringProperty(default='')
	tree_name: bpy.props.StringProperty(default='')

	@classmethod
	def poll(cls, context):
		return context.object and context.object.type in {'MESH'}

	def execute(self, context):
		me = context.object.data
		me.calc_loop_triangles()

		vertices = np.empty((len(me.vertices), 3), 'f')
		edges = np.empty((len(me.edges), 2), 'i')
		indices = np.empty((len(me.loop_triangles), 3), 'i')

		me.vertices.foreach_get("co", np.reshape(vertices, len(me.vertices) * 3))
		me.edges.foreach_get("vertices", np.reshape(edges, len(me.edges) * 2))
		me.loop_triangles.foreach_get("vertices", np.reshape(indices, len(me.loop_triangles) * 3))

		node = bpy.data.node_groups[self.tree_name].nodes[self.node_name]
		global selection

		selection = Mesh(vertices, edges, indices)
		node.gl_update()

		return {'FINISHED'}

class gl_NodeObjectInfo(Node, gl_CustomTreeNode):
	bl_idname = "gl_NodeObjectInfo"
	bl_label = "Object Info"

	def gl_init(self, context):
		self.outputs.new(type="gl_SocketMesh", name="Mesh")

	def draw_buttons(self, context, layout):
		op = layout.operator("gl.get_selection")
		op.node_name = self.name
		op.tree_name = self.id_data.name

	def gl_update(self):
		global selection
		if selection:
			self.outputs[0].gl_set(selection)
		self.linked_update()


def register():
	bpy.utils.register_class(gl_NodeObjectInfo)
	bpy.utils.register_class(GL_OT_get_selection)

def unregister():
	bpy.utils.unregister_class(GL_OT_get_selection)
	bpy.utils.unregister_class(gl_NodeObjectInfo)
