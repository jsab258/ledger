import bpy, sys
args = sys.argv[sys.argv.index("--")+1:]
clip, out = args[:2]
W, H = (int(args[2]), int(args[3])) if len(args) >= 4 else (480, 832)
sc = bpy.context.scene
sc.sequence_editor_create()
ed = sc.sequence_editor
s = (ed.strips if hasattr(ed, "strips") else ed.sequences).new_movie("m", clip, 1, 1)
sc.frame_start, sc.frame_end = 1, s.frame_final_duration
sc.render.fps, sc.render.fps_base = 24, 1.0
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = W, H, 100
sc.render.image_settings.media_type = "VIDEO" if hasattr(sc.render.image_settings, "media_type") else None
sc.render.image_settings.file_format = "FFMPEG"
sc.render.ffmpeg.format, sc.render.ffmpeg.codec = "MPEG4", "H264"
sc.render.ffmpeg.constant_rate_factor = "HIGH"
sc.render.filepath = out
bpy.ops.render.render(animation=True)
print("MP4DONE", s.frame_final_duration)
