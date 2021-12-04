import bpy
import gpu
from bpy.types import Node

from gl_tree.node_tree import gl_CustomTreeNode, update_node

class gl_NodeObjectPlane(Node, gl_CustomTreeNode):
	bl_idname = "gl_NodeObjectPlane"
	bl_label = "Plane"
	bl_icon = 'MESH_PLANE'

	scale: bpy.props.FloatProperty(default=1.0, update=update_node)

	def init(self, context):
		self.outputs.new(type="NodeSocketObject", name="Object")

	def gl_update(self):
		print(self.n_id)

def register():
	bpy.utils.register_class(gl_NodeObjectPlane)

def unregister():
	bpy.utils.unregister_class(gl_NodeObjectPlane)
