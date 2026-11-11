---
name: custom-3d-game-object
description: Create or revise Blender game props, machinery, and architectural objects for Roblox with realistic shapes, economical geometry, name-based material groups, FBX export, and multiple preview angles. Use for modeling from descriptions or reference images; Roblox prefab integration is a separate workflow.
---

# Custom 3D Game Object

## Ask the style first

Before modeling, ask: **"Should this use Realistic Style or Stud Style?"** If already specified for the current asset, use that answer without asking again.

For **Stud Style**, reply: **"Stud style is currently in development and needs to be updated by you."** Stop without modeling or exporting.

For **Realistic Style**, follow the workflow below. The target is believable construction and proportions with economical geometry, not deliberately faceted low-poly art or a photorealistic texture requirement.

## Model the object

Read [references/modeling.md](references/modeling.md) for construction, curves, smoothing, reference fidelity, and budgets. Read [references/material-names.md](references/material-names.md) before naming components.

Use **1 Blender unit = 1 Roblox stud**. Convert meter dimensions using **1 meter = 25/7 studs**. Inspect existing geometry and intended dimensions before conversion: a Metric unit label alone does not establish actual modeling scale.

Match reference images' silhouette, proportions, structure, architecture, major openings, and component placement. Preserve distinctive features. Simplify costly small details and permanently hidden faces first. Use conservative functional construction for unseen sides and disclose significant assumptions or omissions.

For objects roughly **8–10 studs in overall size**, aim for **2,000 evaluated triangles**, with a **3,500 ceiling**. Count the complete export, including converted curves and evaluated modifiers. Report optional claw-machine prizes separately; do not include alternate prize layouts in the machine export. Do not give every small component this whole budget or scale budgets linearly for other sizes. Resolve a suitable budget when a substantially different scale makes this target unsuitable.

Represent material intent by renaming objects, not assigning materials or textures. Keep different material groups and moving parts separate. Do not create Blender material slots, shaders, textures, or baked maps to implement the naming contract. Preserve existing user materials when editing unless asked otherwise; names govern material intent.

## Deliver and verify

Read [references/delivery.md](references/delivery.md) for FBX settings, scale calibration, pivots, previews, and helper usage.

Save an editable `.blend` and an `.fbx` by default. Render a main three-quarter perspective plus **front, left, right, and top orthographic views** with neutral lighting, background, and complete framing. Use the evaluated export geometry and visually inspect all images before delivery.

Report dimensions in studs, evaluated/exported triangle and mesh counts, material prefixes, significant simplifications, and scale-validation status. Do not claim a verified Roblox import from FBX creation alone. Uploading assets, changing gameplay, and project-specific prefab integration require a corresponding user request.

Optional [scripts/prepare_asset.py](scripts/prepare_asset.py) evaluates an explicit collection, creates export copies, merges at 0.01 stud, applies 30-degree angle smoothing while preserving sharp edges, exports FBX, renders five views, and writes a report. [scripts/naming.py](scripts/naming.py) parses material groups. Helpers support modeling and visual review; they do not design the object.
