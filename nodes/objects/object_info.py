import bpy
from bpy.types import Node, Operator

from gl_tree.node_tree import gl_CustomTreeNode, update_node
from mathutils import Vector
import numpy as np

selection = {}

class GL_OT_get_selection(Operator):
	bl_idname = "gl.get_selection"
	bl_label = "Get Selection"

	@classmethod
	def poll(cls, context):
		return context.object in {'MESH'}

	def execute(self, context):
		me = self.object.data
		me.calc_loop_triangles()

		vertices = np.empty((len(me.vertices), 3), 'f')
		indices = np.empty((len(me.loop_triangles), 3), 'i')

		me.vertices.foreach_get("co", np.reshape(vertices, len(me.vertices) * 3))
		me.vertices.foreach_get("vertices", np.reshape(indices, len(me.loop_triangles) * 3))

		selection['vertices'] = vertices
		selection['indices'] = indices

		return {'FINISHED'}

class gl_NodeObjectInfo(Node, gl_CustomTreeNode):
	bl_idname = "gl_NodeObjectInfo"
	bl_label = "Object Info"

	def gl_init(self, context):
		self.outputs.new(type="gl_SocketMesh", name="Mesh")

	def draw_buttons(self, context, layout):
		layout.operator("gl.get_selection")

	def gl_update(self):
		self.outputs.gl_set(dict(selection))


def register():
	bpy.utils.register_class(gl_NodeObjectInfo)
	bpy.utils.register_class(GL_OT_get_selection)

def unregister():
	bpy.utils.unregister_class(GL_OT_get_selection)
	bpy.utils.unregister_class(gl_NodeObjectInfo)
