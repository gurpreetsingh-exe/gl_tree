import bpy
from bpy.types import PropertyGroup
from bpy.props import EnumProperty, IntProperty, PointerProperty

from gl_tree.node_tree import update_node

def draw_header(self, context):
	if context.space_data.tree_type == "gl_NodeTree" and context.space_data.node_tree != None:
		layout = self.layout
		gl_tree = context.space_data.node_tree
		layout.prop(gl_tree, "resolution", text="")
		if gl_tree.resolution == "CUSTOM":
			layout.prop(gl_tree, "custom_resolution")

def register():
	bpy.types.NODE_HT_header.append(draw_header)

def unregister():
	bpy.types.NODE_HT_header.remove(draw_header)
