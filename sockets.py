import bpy
from bpy.types import NodeSocket

socket_data_cache = {}

class gl_SocketCommon():
	@property
	def socket_id(self):
		return str(hash(self.node.node_id) + hash(self))

	def draw(self, context, layout, node, text):
		layout.label(text=self.bl_label)

	def draw_color(self, context, node):
		return self.color

	def gl_get(self):
		global socket_data_cache

		s_id = self.socket_id
		s_ng = self.id_data.tree_id
		out = socket_data_cache[s_ng][s_id]
		if out:
			return out

	def gl_set(self, data):
		global socket_data_cache

		s_id = self.socket_id
		s_ng = self.id_data.tree_id
		try:
			socket_data_cache[s_ng][s_id] = data
		except:
			socket_data_cache[s_ng] = {}
			socket_data_cache[s_ng][s_id] = data

def process_socket(self, context):
	self.node.gl_update()

class gl_SocketMesh(NodeSocket, gl_SocketCommon):
	bl_idname = "gl_SocketMesh"
	bl_label = "Mesh"
	color = (0.2, 0.9, 0.2, 1.0)

class gl_SocketFloat(NodeSocket, gl_SocketCommon):
	bl_idname = "gl_SocketFloat"
	bl_label = "Float"
	color = (1.0, 1.0, 1.0, 1.0)

	value: bpy.props.FloatProperty(default=1.0, update=process_socket, precision=3)

	def draw(self, context, layout, label, text):
		if self.is_linked:
			layout.label(text=self.name)
		else:
			layout.prop(self, "value", text=self.name)

classes = (
	gl_SocketMesh,
	gl_SocketFloat,
)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
