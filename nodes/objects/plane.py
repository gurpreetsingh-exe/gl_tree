import bpy
from bpy.types import Node

from gl_tree.node_tree import gl_CustomTreeNode, update_node
from mathutils import Vector

class gl_NodeObjectPlane(Node, gl_CustomTreeNode):
	bl_idname = "gl_NodeObjectPlane"
	bl_label = "Plane"
	bl_icon = 'MESH_PLANE'

	def gl_init(self, context):
		self.inputs.new(type="gl_SocketVector", name="Location")
		self.inputs.new(type="gl_SocketFloat", name="Scale")
		self.outputs.new(type="gl_SocketMesh", name="Mesh")

	def gl_update(self):
		if not self.inputs:
			return

		pos = Vector(self.inputs[0].value)
		scale = self.inputs[1].value
		data = (
			pos + Vector([-scale, -scale, 0]),
			pos + Vector([-scale,  scale, 0]),
			pos + Vector([ scale, -scale, 0]),
			pos + Vector([ scale,  scale, 0]))

		self.outputs[0].gl_set(data)
		self.linked_update()

def register():
	bpy.utils.register_class(gl_NodeObjectPlane)

def unregister():
	bpy.utils.unregister_class(gl_NodeObjectPlane)
