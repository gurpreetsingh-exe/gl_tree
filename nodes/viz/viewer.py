import bpy
import blf
import gpu
from gpu_extras.batch import batch_for_shader
from bpy.types import Node

from gl_tree.node_tree import gl_CustomTreeNode, update_node
from gl_tree.sockets import process_socket
from mathutils import Vector

def draw_callback_px(self, **args):
	if self.viewer_type == '2D':
		positions = self.node_dict[hash(self)]['positions']
		x, y = self.location
		text_height = 20
		x += self.width
		r, g, b = (1, 1, 1)

		blf.size(1, int(text_height), 72)
		blf.color(1, r, g, b, 1.0)
		if positions == None:
			blf.position(1, x + 10, y - (text_height * 0.75), 0)
			blf.draw(1, "None")
			return

		tmp_y = 0
		for pos in positions:
			blf.position(1, x + 10, y - (text_height * 0.75) - tmp_y, 0)
			tmp_y += text_height
			blf.draw(1, str(pos))

	elif self.viewer_type == '3D':
		data = self.node_dict[hash(self)]
		shader = data['shader']
		batch = data['batch']
		if batch and shader:
			shader.bind()
			shader.uniform_float("color", (0, 0.6, 0.8, 1.0))
			batch.draw(shader)

class gl_NodeMeshViewer(Node, gl_CustomTreeNode):
	bl_idname = "gl_NodeMeshViewer"
	bl_label = "Mesh Viewer"

	node_dict = {}

	viewer_type: bpy.props.EnumProperty(items=(
		('2D', '2D', '', 0),
		('3D', '3D', '', 1),
	), default='3D', update=update_node)

	def create_batch(self):
		data = self.node_dict[hash(self)]
		coords = data['positions']
		if coords:
			coords = [tuple(co) for co in coords]
			shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
			indices = ([0, 1, 2], [2, 3, 1])
			batch = batch_for_shader(shader, 'TRIS', {"pos": coords}, indices=indices)
			data['batch'] = batch
			data['shader'] = shader

	def draw_buttons(self, context, layout):
		layout.prop(self, "viewer_type", text="Type")

	def gl_init(self, context):
		self.node_dict[hash(self)] = {}
		self.inputs.new(type="gl_SocketMesh", name="Mesh")

	def gl_update(self):
		if len(self.inputs) <= 0 and not self.inputs[0].is_linked:
			return
		if not self.inputs[0].is_linked:
			self.node_dict[hash(self)]['positions'] = None
			return
		else:
			data = self.inputs[0].links[0].from_socket.gl_get()
			cache = self.node_dict[hash(self)]
			cache['positions'] = data

			if self.viewer_type == '3D':
				self.create_batch()
				if not cache.get('handler3d'):
					handler3d = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, ((self,)), 'WINDOW', 'POST_VIEW')
					cache['handler3d'] = handler3d

			if self.viewer_type == '2D':
				if not cache.get('handler2d'):
					handler2d = bpy.types.SpaceNodeEditor.draw_handler_add(draw_callback_px, ((self,)), 'WINDOW', 'POST_VIEW')
					cache['handler2d'] = handler2d

	def free(self):
		handler2d = self.node_dict[hash(self)]['handler2d']
		handler3d = self.node_dict[hash(self)]['handler3d']

		bpy.types.SpaceNodeEditor.draw_handler_remove(handler2d, 'WINDOW')
		bpy.types.SpaceView3D.draw_handler_remove(handler3d, 'WINDOW')

def register():
	bpy.utils.register_class(gl_NodeMeshViewer)

def unregister():
	bpy.utils.unregister_class(gl_NodeMeshViewer)
