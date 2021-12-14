import bpy

def tag_redraw_all_3dviews():
	for window in bpy.context.window_manager.windows:
		for area in window.screen.areas:
			if area.type == 'VIEW_3D':
				for region in area.regions:
					if region.type == 'WINDOW':
						region.tag_redraw()
