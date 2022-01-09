import bpy
import gpu
import bgl
from bpy.types import Node, Operator
from gpu_extras.batch import batch_for_shader

from gl_tree.node_tree import gl_CustomTreeNode, update_node

class GL_OT_update_shader(Operator):
	bl_idname = "gl.update_shader"
	bl_label = "Update Shader"

	node_name: bpy.props.StringProperty(default="")
	tree_name: bpy.props.StringProperty(default="")

	def execute(self, context):
		node = bpy.data.node_groups[self.tree_name].nodes[self.node_name]
		node.gl_update()
		return {'FINISHED'}

class gl_NodeGlslScript(Node, gl_CustomTreeNode):
	bl_idname = "gl_NodeGlslScript"
	bl_label = "GLSL Script"

	node_dict = {}

	vert: bpy.props.StringProperty(name="Vertex Shader", default="""in vec3 a_position;
in vec2 uv;

out vec2 texCoord;

void main() {
	gl_Position = vec4(a_position, 1.0);
	texCoord = uv;
}""")

	frag: bpy.props.PointerProperty(type=bpy.types.Text, name="Shader", update=update_node)

	def gl_init(self, context):
		self.node_dict[hash(self)] = {}
		self.outputs.new(type="gl_SocketColor", name="Color")

	def draw_buttons(self, context, layout):
		layout.prop(self, "frag")
		self.draw_operator(layout, "gl.update_shader")

	def gl_update(self):
		if not self.frag:
			return

		mesh = self.id_data.mesh

		width = height = self.id_data.custom_resolution if self.id_data.resolution == "CUSTOM" else int(self.id_data.resolution)
		offscreen = gpu.types.GPUOffScreen(width, height)
		with offscreen.bind():
			shader = gpu.types.GPUShader(self.vert, self.frag.as_string())
			batch = batch_for_shader(shader, 'TRIS', {
				"a_position": mesh.vertices,
				"uv": mesh.uv,
			}, indices=mesh.indices)
			# bgl.glEnable(bgl.GL_BLEND)
			batch.draw(shader)
			# bgl.glDisable(bgl.GL_BLEND)

		self.outputs[0].gl_set(offscreen)
		self.linked_update()


def register():
	bpy.utils.register_class(GL_OT_update_shader)
	bpy.utils.register_class(gl_NodeGlslScript)

def unregister():
	bpy.utils.unregister_class(GL_OT_update_shader)
	bpy.utils.unregister_class(gl_NodeGlslScript)
