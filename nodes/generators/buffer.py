import bpy
import gpu
from bpy.types import Node

from gl_tree.node_tree import gl_CustomTreeNode

class gl_NodeBuffer(Node, gl_CustomTreeNode):
	bl_idname = "gl_NodeBuffer"
	bl_label = "Buffer"
	bl_icon = 'SHADERFX'

	vert: bpy.props.StringProperty(name="Vertex Shader", default="""in vec2 a_position;
out vec2 texCoord;

void main() {
	gl_Position = vec4(a_position, 0.0, 1.0);
	texCoord = a_position;
}""")

	frag: bpy.props.StringProperty(name="Fragment Shader", default="""uniform vec2 u_resolution;
void main() {
	vec3 color = vec3(0.0);
	vec2 st = gl_FragCoord.xy;
	color.rg = st;
	gl_FragColor = vec4(color, 1.0);
}""")

	def init(self, context):
		self.node_cache[self.node_id] = {}
		self.inputs.new(type="NodeSocketFloat", name="Value")
		self.outputs.new(type="NodeSocketFloat", name="Value")


def register():
	bpy.utils.register_class(gl_NodeBuffer)

def unregister():
	bpy.utils.unregister_class(gl_NodeBuffer)
