import bpy
import gpu
import bgl
from gpu_extras.batch import batch_for_shader
from bpy.types import Node

from gl_tree.node_tree import gl_CustomTreeNode, update_node

class gl_NodeDefaultShader(Node, gl_CustomTreeNode):
	bl_idname = "gl_NodeDefaultShader"
	bl_label = "Default Shader"

	vert: bpy.props.StringProperty(name="Vertex Shader", default="""in vec3 a_position;
in vec2 uv;

out vec2 texCoord;

void main() {
	gl_Position = vec4(a_position, 1.0);
	texCoord = uv;
}""")

	frag: bpy.props.StringProperty(name="Fragment Shader", default="""in vec2 texCoord;

out vec4 FragColor;

void main() {
	FragColor = vec4(texCoord, 0.0f, 1.0);
}""")

	def gl_init(self, context):
		self.outputs.new(type="gl_SocketColor", name="Color")

	def gl_update(self):
		mesh = self.id_data.mesh

		width = height = self.id_data.custom_resolution if self.id_data.resolution == "CUSTOM" else int(self.id_data.resolution)
		offscreen = gpu.types.GPUOffScreen(width, height)
		with offscreen.bind():
			shader = gpu.types.GPUShader(self.vert, self.frag)
			batch = batch_for_shader(shader, 'TRIS', {
				"a_position": mesh.vertices,
				"uv": mesh.uv,
			}, indices=mesh.indices)
			batch.draw(shader)

		self.outputs[0].gl_set(offscreen)

def register():
	bpy.utils.register_class(gl_NodeDefaultShader)

def unregister():
	bpy.utils.unregister_class(gl_NodeDefaultShader)
