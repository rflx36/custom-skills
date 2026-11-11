"""Run inside Blender: prepare one collection for FBX and five previews.

Source files are read only. Outputs are written only to --output-dir.
"""
import argparse
import json
import math
import re
import sys
from pathlib import Path

import bpy
import bmesh
from mathutils import Matrix, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from naming import parse_name


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--collection', required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--front', choices=('-Y', '+Y', '-X', '+X'), default='-Y')
    parser.add_argument('--triangle-limit', type=int, default=3500)
    parser.add_argument('--no-render', action='store_true')
    parser.add_argument('--allow-overwrite', action='store_true')
    return parser.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])


def smooth_and_clean(mesh):
    bm = bmesh.new()
    try:
        bm.from_mesh(mesh)
        before = len(bm.verts)
        bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=0.01)
        bm.normal_update()
        for face in bm.faces:
            face.smooth = True
        for edge in bm.edges:
            if len(edge.link_faces) != 2 or edge.calc_face_angle(0) > math.radians(30):
                edge.smooth = False
        # Triangulate after setting angle sharpness so coplanar diagonals stay smooth.
        bmesh.ops.triangulate(bm, faces=list(bm.faces))
        if not bm.faces or any(f.calc_area() <= 1e-12 for f in bm.faces):
            raise ValueError('Empty or degenerate faces after 0.01-stud cleanup')
        loose = sum(not v.link_faces for v in bm.verts)
        if loose:
            raise ValueError(f'{loose} vertices do not belong to any face')
        bm.to_mesh(mesh)
        mesh.update()
        return before - len(bm.verts)
    finally:
        bm.free()


def preview(scene, objects, bounds, output, stem, front):
    lo, hi = bounds
    center = (lo + hi) * 0.5
    radius = max((hi - lo).length * 0.5, 0.1)
    directions = {'-Y': Vector((0, -1, 0)), '+Y': Vector((0, 1, 0)),
                  '-X': Vector((-1, 0, 0)), '+X': Vector((1, 0, 0))}
    forward = directions[front]
    right = Vector((-forward.y, forward.x, 0))
    views = [('main', (forward + right * 0.8 + Vector((0, 0, .65))).normalized(), 'PERSP'),
             ('front', forward, 'ORTHO'), ('left', -right, 'ORTHO'),
             ('right', right, 'ORTHO'), ('top', Vector((0, 0, 1)), 'ORTHO')]
    scene.render.engine = 'BLENDER_WORKBENCH'
    scene.render.resolution_x = scene.render.resolution_y = 1000
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.film_transparent = False
    shading = scene.display.shading
    shading.light = 'STUDIO'
    shading.color_type = 'SINGLE'
    shading.single_color = (.62, .65, .68)
    shading.background_type = 'WORLD'
    shading.background_color = (.055, .055, .055)
    scene.world = bpy.data.worlds.new('ExportPreviewWorld')
    scene.world.color = (.055, .055, .055)
    shading.show_shadows = True
    shading.show_cavity = False
    camera_data = bpy.data.cameras.new('ExportPreviewCamera')
    camera = bpy.data.objects.new('ExportPreviewCamera', camera_data)
    scene.collection.objects.link(camera)
    scene.camera = camera
    camera_data.lens = 50
    camera_data.clip_start = max(radius / 10000, .001)
    camera_data.clip_end = radius * 30 + 100
    results = []
    for name, direction, projection in views:
        camera_data.type = projection
        camera_data.ortho_scale = radius * 2.35
        camera.location = center + direction * radius * 4
        camera.rotation_euler = (center - camera.location).to_track_quat('-Z', 'Y').to_euler()
        destination = output / f'{stem}_{name}.png'
        scene.render.filepath = str(destination)
        bpy.context.view_layer.update()
        bpy.ops.render.render(write_still=True)
        results.append(destination.name)
    return results


def run(args):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', args.name):
        raise ValueError('--name must be a simple filename stem')
    if args.triangle_limit <= 0:
        raise ValueError('--triangle-limit must be positive')
    source = args.source.resolve(strict=True)
    output = args.output_dir.resolve()
    filenames = [args.name + '.fbx', args.name + '_report.json']
    if not args.no_render:
        filenames += [f'{args.name}_{view}.png' for view in ('main', 'front', 'left', 'right', 'top')]
    if not args.allow_overwrite:
        for filename in filenames:
            if (output / filename).exists():
                raise FileExistsError(output / filename)
    bpy.ops.wm.open_mainfile(filepath=str(source))
    original_scene = bpy.context.scene
    root = bpy.data.collections.get(args.collection)
    if root is None:
        raise ValueError(f'Collection not found: {args.collection}')
    originals = sorted([o for o in root.all_objects if o.type in {'MESH', 'CURVE', 'SURFACE', 'FONT'}], key=lambda o: o.name)
    if not originals:
        raise ValueError('No supported geometry in the chosen collection')
    parsed = {o.name: parse_name(o.name) for o in originals}
    depsgraph = bpy.context.evaluated_depsgraph_get()
    export_scene = bpy.data.scenes.new('PreparedAssetExport')
    export_scene.unit_settings.system = 'NONE'
    export_scene.unit_settings.scale_length = 1
    copies, rows, warnings = [], [], []
    for original in originals:
        name = original.name
        evaluated = original.evaluated_get(depsgraph)
        mesh = bpy.data.meshes.new_from_object(evaluated, preserve_all_data_layers=True, depsgraph=depsgraph)
        if not mesh.vertices:
            raise ValueError(f'No evaluated geometry: {name}')
        initial_triangles = sum(len(p.vertices) - 2 for p in mesh.polygons)
        # Bake scale/rotation/shear into geometry, retaining each functional origin.
        origin = original.matrix_world.translation.copy()
        transform = Matrix.Translation(-origin) @ original.matrix_world
        mesh.transform(transform)
        if transform.to_3x3().determinant() < 0:
            mesh.flip_normals()
        if any(not math.isfinite(c) for v in mesh.vertices for c in v.co):
            raise ValueError(f'Nonfinite coordinates: {name}')
        removed = smooth_and_clean(mesh)
        # Release names in memory only; the source file is never saved.
        original.name = '__SOURCE__' + name
        copy = bpy.data.objects.new(name, mesh)
        copy.location = origin
        export_scene.collection.objects.link(copy)
        copies.append(copy)
        if parsed[name]['legacy']:
            warnings.append(f'Legacy name: {name}; canonical form: {parsed[name]["canonical"]}')
        if removed:
            warnings.append(f'{name}: merged {removed} vertices at 0.01 stud; visually inspect')
        rows.append(dict(name=name, source_type=original.type, source_evaluated_triangles=initial_triangles,
                         export_triangles=len(mesh.polygons), merged_vertices=removed, **parsed[name]))
    bpy.context.window.scene = export_scene
    bpy.context.view_layer.update()
    points = [o.matrix_world @ v.co for o in copies for v in o.data.vertices]
    lo = Vector(tuple(min(p[a] for p in points) for a in range(3)))
    hi = Vector(tuple(max(p[a] for p in points) for a in range(3)))
    total = sum(row['export_triangles'] for row in rows)
    if total > args.triangle_limit:
        raise ValueError(f'Over triangle ceiling: {total} > {args.triangle_limit}; simplify before export')
    for obj in copies:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = copies[0]
    output.mkdir(parents=True, exist_ok=True)
    bpy.ops.export_scene.fbx(filepath=str(output / (args.name + '.fbx')),
        use_selection=True, object_types={'MESH'}, global_scale=1,
        apply_unit_scale=False, apply_scale_options='FBX_SCALE_NONE',
        axis_forward='-Z', axis_up='Y', use_mesh_modifiers=False,
        mesh_smooth_type='EDGE', add_leaf_bones=False, bake_anim=False,
        path_mode='STRIP', embed_textures=False, use_custom_props=False)
    previews = [] if args.no_render else preview(export_scene, copies, (lo, hi), output, args.name, args.front)
    report = dict(asset=args.name, units='1 Blender unit = 1 Roblox stud',
                  dimensions_blender_xyz_studs=list(hi - lo),
                  dimensions_roblox_xyz_studs=[hi.x-lo.x, hi.z-lo.z, hi.y-lo.y],
                  source_evaluated_triangles=sum(r['source_evaluated_triangles'] for r in rows),
                  export_triangles=total, triangle_limit=args.triangle_limit,
                  mesh_count=len(copies), merge_distance_studs=.01, smoothing_angle_degrees=30,
                  studio_scale_verified=False, previews=previews, warnings=warnings, objects=rows)
    (output / (args.name + '_report.json')).write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('ASSET_PREPARED', json.dumps({k: report[k] for k in ('asset', 'mesh_count', 'export_triangles', 'previews')}))


if __name__ == '__main__':
    try:
        run(arguments())
    except Exception as exc:
        print(f'ASSET_PREPARATION_FAILED: {exc}', file=sys.stderr)
        raise SystemExit(1)
