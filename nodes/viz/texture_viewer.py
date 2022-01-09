import bpy
import blf
import gpu
import bgl
from gpu_extras.batch import batch_for_shader
from bpy.types import Node

from gl_tree.data_structure import Mesh
from gl_tree.node_tree import gl_CustomTreeNode, update_node
from gl_tree.sockets import process_socket
from gl_tree.utils import tag_redraw_all_3dviews

def draw_callback_px(self, **args):
	data = self.node_dict[hash(self)]
	color = data['color'].texture_color
	shader = data['shader']
	batch = data['batch']
	if batch and shader:
		shader.bind()
		shader.uniform_float("viewProjectionMatrix", bpy.context.region_data.perspective_matrix)
		shader.uniform_sampler("image", color)
		# bgl.glEnable(bgl.GL_DEPTH_TEST)
		# bgl.glEnable(bgl.GL_BLEND)
		batch.draw(shader)
		# bgl.glDisable(bgl.GL_BLEND)
		# bgl.glDisable(bgl.GL_DEPTH_TEST)

class gl_NodeTextureViewer(Node, gl_CustomTreeNode):
	bl_idname = "gl_NodeTextureViewer"
	bl_label = "Texture Viewer"

	node_dict = {}

	vertex_shader: bpy.props.StringProperty(default="""uniform mat4 viewProjectionMatrix;
in vec3 position;
in vec2 uv;

out vec2 texCoord;

void main()
{
	texCoord = uv;
	gl_Position = viewProjectionMatrix * vec4(position, 1.0);
}
""")

	fragment_shader: bpy.props.StringProperty(default="""uniform sampler2D image;
in vec2 texCoord;

out vec4 FragColor;

void main()
{
	FragColor = texture(image, texCoord);
}
""")

	def gl_init(self, context):
		self.node_dict[hash(self)] = {}
		self.inputs.new(type="gl_SocketColor", name="Color")

	def create_batch(self, mesh):
		data = self.node_dict[hash(self)]
		shader = gpu.types.GPUShader(self.vertex_shader, self.fragment_shader)
		batch = batch_for_shader(shader, 'TRIS', {
			"position": mesh.vertices,
			"uv": mesh.uv,
		}, indices=mesh.indices)
		self.node_dict[hash(self)]['batch'] = batch
		data['batch'] = batch
		data['shader'] = shader

	def gl_update(self):
		data = self.node_dict[hash(self)]
		if not self.inputs[0].is_linked:
			self.free()
			return

		mesh = self.id_data.mesh
		self.create_batch(mesh)
		data['color'] = self.inputs[0].links[0].from_socket.gl_get()
		tag_redraw_all_3dviews()

		if not data.get('handler'):
			data['handler'] = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, ((self,)), 'WINDOW', 'POST_VIEW')
			tag_redraw_all_3dviews()

	def free(self):
		data = self.node_dict[hash(self)]
		handler = data.get('handler')
		if handler:
			bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')
			tag_redraw_all_3dviews()
			data.pop('handler')


def register():
	bpy.utils.register_class(gl_NodeTextureViewer)

def unregister():
	bpy.utils.unregister_class(gl_NodeTextureViewer)
