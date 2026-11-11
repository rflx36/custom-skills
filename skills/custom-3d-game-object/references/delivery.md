# Export and previews

## Scale

Model **1 Blender unit = 1 Roblox stud**. Convert meters by multiplying by **25/7**. The arcade reference was unitless at scale 1; the shredder was Metric at scale 1. Labels alone do not establish the intended scale. Avoid double conversion.

Save an editable `.blend` with named collections and components. New static props default to a ground-center pivot; honor placement references and functional pivots for moving components.

Export FBX with only the requested asset, evaluated modifiers, and mesh copies of curves. Preserve names and relative placement. Exclude presentation geometry, cameras, lights, references, and unused variants. Start with **-Z forward / Y up**, global scale 1, disabled scene-unit scaling, and FBX_SCALE_NONE for stud-sized coordinates.

Verify the actual Studio pipeline with a 1-unit reference imported at 1 stud; record the working import unit and custom scale settings. An export preset alone is not proof. If Studio import is not requested or available, mark that verification as pending. Never convert geometry and then apply the same conversion again during import.

## Five preview views

Render **main three-quarter perspective, front, left, right, and top**; all except main use orthographic projection. Default front is Blender -Y, Z up. Honor a specified asset front. Use consistent neutral studio lighting and background, readable framing, and margins. Render the evaluated export copies and visually inspect every image before delivery.

Neutral object-color previews require no material assignment. The helper renders Glass-tagged geometry opaque: disclose this, or supply an additional labeled transparency review when needed without changing the material naming contract.

Report dimensions, mesh count, evaluated/exported triangle counts, prefixes, meaningful simplifications, and Studio scale-validation status. Count optional prize contents separately.

## Helper usage

Run with Blender, not ordinary Python:

```text
blender --background --python scripts/prepare_asset.py -- --source Asset.blend --collection Asset --output-dir export --name Asset
```

Options: `--no-render` for export checks, `--front +Y` (also +X or -X), `--triangle-limit N` for a user-established different budget, and `--allow-overwrite` to replace helper outputs deliberately. Default whole-collection ceiling is 3500.

The helper never saves over the source. Save the editable `.blend` after modeling separately. It prepares copies, performs 0.01-stud cleanup and angle smoothing, exports FBX, renders PNGs, and writes JSON. It rejects invalid names or over-budget geometry, reports legacy prefixes, and leaves Studio scale marked unverified. It cannot choose prize variants: use a dedicated collection containing only intended export objects. It does not implement materials or rename ambiguous surfaces.
