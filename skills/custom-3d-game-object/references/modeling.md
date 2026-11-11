# Realistic modeling

## Visual target and reference images

The owner's arcades, gantry claw, and shredder are primary design benchmarks: compact clean housings, recognizable silhouettes, separate controls and trim, useful mechanical detail, sharp edges, and sparse geometry. External high-budget hero props are not the default standard. Reference files are private, optional study inputs, not dependencies of this skill.

The inspected shredder has five meshes and approximately 1,492 base triangles; this is an observation, not an evaluated export budget. The gantry contains alternate reward layouts: do not count or export them all as one machine.

Replicate a supplied image's silhouette, width/height/depth proportions, main angles, negative spaces, architecture, openings, supports, and component alignment before adding small detail. Preserve visible asymmetry and damage. Make conservative assumptions for unseen sides. Describe substantial simplifications alongside previews.

Favor geometry for silhouettes, deep recesses, openings, meaningful shadows, or movement. Rails, brackets, panels, handles, controls, and exposed mechanisms communicate construction. Simplify tiny fasteners, shallow grooves, repeated minor elements, and concealed surfaces first. Do not introduce texture baking as a requirement.

## Thickness and circular parts

- Machine supports/outlines normally measure **0.25–0.5 stud** thick; allow **0.1–1 stud** when the component warrants it. This is not a universal minimum detail thickness.
- Small circles: **6 sides**. Ordinary circles: **12–16 sides**. Large circles: **24 sides**. Check intended viewing distance before adding segments.
- Use restrained geometric bevels where silhouette or highlights improve readability. Avoid blanket subdivision and dense support loops.

## Curved pipes, cables, and hoses

Use **Curve → Bézier**, then **Data → Geometry → Bevel**. Bevel depth controls radius; diameter is twice depth. Use bevel resolution **0 for small sizes**, increasing only as needed to **4 for large sizes**. Path resolution is separate; keep it economical too. Check evaluated triangles after either setting changes. Cap only ends that need it. Keep source curves editable; convert copies for FBX.

## Cleanup and shading

Apply **Merge by Distance at 0.01 stud to every mesh**, within each object, accounting for object scale. Do not weld different objects or moving assemblies together. If it damages a feature, revise the geometry or disclose the conflict rather than silently changing the threshold. Check for collapsed faces, lost openings, and degenerate edges afterward.

Favor **Auto Smooth / Smooth by Angle at 30°** on every mesh, preserving manually sharp edges. Use the installed Blender version's supported equivalent rather than removed properties. When ngons shade poorly, mark appropriate edges sharp. Repair nonplanar or malformed geometry and inspect its triangulation too: sharpness alone does not repair topology.

Omit only permanently concealed faces. Preserve surfaces that become visible through movement, normal gameplay, or damage. Broken variants need visible interiors. Intentional open meshes need not be made watertight.

Inspect evaluated triangles, normals, duplicate faces, z-fighting, gaps, and silhouette from every preview angle. Low object count is not proof of low triangle count.
