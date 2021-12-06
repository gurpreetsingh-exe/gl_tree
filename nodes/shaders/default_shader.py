import bpy
import gpu
import bgl
from gpu_extras.batch import batch_for_shader
from bpy.types import Node

from gl_tree.node_tree import gl_CustomTreeNode, update_node

class gl_NodeDefaultShader(Node, gl_CustomTreeNode):
	bl_idname = "gl_NodeDefaultShader"
	bl_label = "Default Shader"

	vert: bpy.props.StringProperty(name="Vertex Shader", default="""in vec2 a_position;
in vec2 uv_coord;
out vec2 texCoord;

void main() {
	gl_Position = vec4(a_position, 0.0, 1.0);
	texCoord = uv_coord;
}""")

	frag: bpy.props.StringProperty(name="Fragment Shader", default="""in vec2 texCoord;
void main() {
	vec3 color = vec3(texCoord, 0.0);
	gl_FragColor = vec4(color, 1.0);
}""")

	def gl_init(self, context):
		self.outputs.new(type="gl_SocketShader", name="Shader")

	def gl_update(self):
		if not self.outputs:
			return

		offscreen = gpu.types.GPUOffScreen(256, 256)
		with offscreen.bind():
			shader = gpu.types.GPUShader(self.vert, self.frag)
			batch = batch_for_shader(shader, 'TRI_FAN', {
				"a_position": ((-1, -1), (1, -1), (1, 1), (-1, 1)),
				"uv_coord": ((0, 0), (1, 0), (1, 1), (0, 1))
			})
			batch.draw(shader)
		self.outputs[0].gl_set(offscreen)

def register():
	bpy.utils.register_class(gl_NodeDefaultShader)

def unregister():
	bpy.utils.unregister_class(gl_NodeDefaultShader)

