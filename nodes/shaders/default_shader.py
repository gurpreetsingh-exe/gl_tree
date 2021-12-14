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
void main() {
	gl_FragColor = vec4(texCoord, 0.0f, 1.0);
}""")

	def gl_init(self, context):
		self.inputs.new(type="gl_SocketMesh", name="Mesh")
		self.outputs.new(type="gl_SocketColor", name="Color")

	def gl_update(self):
		if not self.inputs[0].links:
			return

		mesh = self.inputs[0].links[0].from_socket.gl_get()

		width = height = 512
		offscreen = gpu.types.GPUOffScreen(width, height)
		with offscreen.bind():
			shader = gpu.types.GPUShader(self.vert, self.frag)
			batch = batch_for_shader(shader, 'TRIS', {
				"a_position": ((-1, -1, 0), (-1, 1, 0), (1, -1, 0), (1, 1, 0)),
				"uv": mesh.uv,
			}, indices=mesh.indices)
			batch.draw(shader)

		self.outputs[0].gl_set(offscreen)

def register():
	bpy.utils.register_class(gl_NodeDefaultShader)

def unregister():
	bpy.utils.unregister_class(gl_NodeDefaultShader)
