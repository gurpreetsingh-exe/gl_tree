import bpy
import blf
import gpu
import bgl
from gpu_extras.batch import batch_for_shader
from bpy.types import Node

from gl_tree.data_structure import Mesh
from gl_tree.node_tree import gl_CustomTreeNode, update_node
from gl_tree.sockets import process_socket

import numpy as np

def tag_redraw_all_3dviews():
	for window in bpy.context.window_manager.windows:
		for area in window.screen.areas:
			if area.type == 'VIEW_3D':
				for region in area.regions:
					if region.type == 'WINDOW':
						region.tag_redraw()


def draw_callback_px(self, **args):
	data = self.node_dict[hash(self)]
	p_shader, p_batch = data['p_shader'], data['p_batch']
	e_shader, e_batch = data['e_shader'], data['e_batch']

	if p_shader and p_shader:
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

	vertex_shader: bpy.props.StringProperty(default="""uniform mat4 viewProjectionMatrix;
in vec2 position;
in vec2 uv;

out vec2 uvInterp;

void main()
{
	uvInterp = uv;
	gl_Position = viewProjectionMatrix * vec4(position, 0.0, 1.0);
}
""")

	fragment_shader: bpy.props.StringProperty(default="""uniform sampler2D image;

in vec2 uvInterp;
out vec4 FragColor;

void main()
{
	FragColor = texture(image, uvInterp);
}
""")

	face_color: bpy.props.FloatVectorProperty(default=(0.071, 0.508, 2.000, 0.500), size=4, precision=3, subtype='COLOR')
	edge_color: bpy.props.FloatVectorProperty(default=(0.000, 2.000, 0.683, 1.000), size=4, precision=3, subtype='COLOR')

	def gl_init(self, context):
		self.node_dict[hash(self)] = {}
		self.inputs.new(type="gl_SocketMesh", name="Mesh")

	def draw_buttons(self, context, layout):
		layout.prop(self, "face_color")
		layout.prop(self, "edge_color")

	def generate_props(self):
		props = lambda: None
		props.face_color = self.face_color
		props.edge_color = self.edge_color
		return props

	def create_batch(self, mesh):
		shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
		batch = batch_for_shader(shader, 'TRIS', {"pos": mesh.vertices}, indices=mesh.indices)
		return shader, batch

	def gl_update(self):
		data = self.node_dict[hash(self)]
		if not self.inputs or not self.inputs[0].is_linked:
			if data.get('handler'):
				bpy.types.SpaceView3D.draw_handler_remove(data.get('handler'), 'WINDOW')
				tag_redraw_all_3dviews()
				data.pop('handler')
				return
		else:
			mesh = self.inputs[0].links[0].from_socket.gl_get()
			if not mesh:
				return

			data['p_shader'], data['p_batch'] = self.create_batch(mesh)
			data['e_shader'] = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
			data['e_batch'] = batch_for_shader(data['e_shader'], 'LINES', {"pos": mesh.edges_flat})

			if not data.get('handler'):
				handler = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, ((self,)), 'WINDOW', 'POST_VIEW')
				tag_redraw_all_3dviews()
				data['handler'] = handler

	def free(self):
		data = self.node_dict[hash(self)]
		handler = data['handler']
		bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')
		data.pop('handler')

def register():
	bpy.utils.register_class(gl_NodeMeshViewer)

def unregister():
	bpy.utils.unregister_class(gl_NodeMeshViewer)
