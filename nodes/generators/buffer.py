import bpy
import gpu
import bgl
from gpu_extras.batch import batch_for_shader
from bpy.types import Node

from gl_tree.node_tree import gl_CustomTreeNode, update_node

class gl_NodeBuffer(Node, gl_CustomTreeNode):
	bl_idname = "gl_NodeBuffer"
	bl_label = "Buffer"
	bl_icon = 'SHADERFX'

	size: bpy.props.IntProperty(default=256, update=update_node)

	def gl_init(self, context):
		self.node_cache[self.node_id] = {}
		self.outputs.new(type="gl_SocketBuffer", name="Buffer")

		data = bgl.Buffer(bgl.GL_BYTE, [self.size] * 2)
		self.outputs[0].gl_set(data)

	def gl_update(self):
		data = bgl.Buffer(bgl.GL_BYTE, [self.size] * 2)
		self.outputs[0].gl_set(data)

	def draw_buttons(self, context, layout):
		layout.prop(self, "size")

def register():
	bpy.utils.register_class(gl_NodeBuffer)

def unregister():
	bpy.utils.unregister_class(gl_NodeBuffer)
