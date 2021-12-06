import bpy
import blf
import gpu
import bgl
from gpu_extras.batch import batch_for_shader
from bpy.types import Node

from gl_tree.node_tree import gl_CustomTreeNode, update_node
from gl_tree.sockets import process_socket

import numpy as np

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
		p_shader, p_batch = data['p_shader'], data['p_batch']
		e_shader, e_batch = data['e_shader'], data['e_batch']

		if e_batch and p_shader:
			props = self.generate_props()
			bgl.glEnable(bgl.GL_BLEND)
			p_shader.bind()
			p_shader.uniform_float("color", props.face_color)
			p_batch.draw(p_shader)
			e_shader.bind()
			e_shader.uniform_float("color", props.edge_color)
			e_batch.draw(e_shader)
			bgl.glDisable(bgl.GL_BLEND)

# Edge color [0.000000, 1.000000, 0.341914, 1.000000]
# Vertex color [0.000000, 0.147027, 1.000000, 1.000000]

class gl_NodeMeshViewer(Node, gl_CustomTreeNode):
	bl_idname = "gl_NodeMeshViewer"
	bl_label = "Mesh Viewer"

	node_dict = {}

	viewer_type: bpy.props.EnumProperty(items=(
		('2D', '2D', '', 0),
		('3D', '3D', '', 1),
	), default='3D', update=update_node)

	def create_shader(self, draw_type, coords, indices=None):
		shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
		batch = None
		if indices:
			batch = batch_for_shader(shader, draw_type, {"pos": coords}, indices=indices)
		else:
			batch = batch_for_shader(shader, draw_type, {"pos": coords})

		return shader, batch

	def generate_props(self):
		props = lambda: None
		props.face_color = (0.071, 0.508, 2.0, 0.5)
		props.edge_color = (0.0, 2.0, 0.683, 1.0)
		return props

	def create_batch(self):
		data = self.node_dict[hash(self)]
		coords = data['positions']
		if coords:
			indices = ([0, 1, 2], [2, 3, 1])
			edge_coords = list(coords)
			edge_coords[2], edge_coords[3] = edge_coords[3], edge_coords[2]
			edge_coords = list(np.roll(np.array(edge_coords), -3))

			shift_pos = list(np.roll(np.array(edge_coords), -3))
			edges = np.array([(p0, p1) for p0, p1 in zip(edge_coords, shift_pos)]).flatten()
			edges = list(edges.reshape(-1, 3))

			data['p_shader'], data['p_batch'] = self.create_shader('TRIS', coords, indices)
			data['e_shader'], data['e_batch'] = self.create_shader('LINES', edges)

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
