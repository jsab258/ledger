import bpy, sys
clip, out = sys.argv[sys.argv.index("--")+1:][:2]
sc = bpy.context.scene
sc.sequence_editor_create()
s = sc.sequence_editor.strips.new_movie("m", clip, 1, 1) if hasattr(sc.sequence_editor, "strips") else sc.sequence_editor.sequences.new_movie("m", clip, 1, 1)
n = s.frame_final_duration
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 480, 832, 100
sc.render.image_settings.file_format = "PNG"
print("FRAMES", n)
for f in [1, 11, 21, 31, 41, 51, 61, 71, n]:
    sc.frame_set(f); sc.render.filepath = out + "/f%02d.png" % f
    bpy.ops.render.render(write_still=True)
