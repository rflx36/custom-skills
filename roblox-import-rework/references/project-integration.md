# Project integration

Read the live project's scripts before editing; these are established conventions, not permission to modify an unrelated place.

## Library and materials

- Structure folders: `ServerStorage.Structures.<StructureName>`.
- Each folder: `Prefab` Model and editable `Constants` ModuleScript.
- Main placement system: `ServerStorage.Structures.StructureSpawner`, called by `ServerScriptService.WastelandGenerator`.
- Gallery: `ServerStorage.Structures.StructureShowcase`, called by `ServerScriptService.ScrapTestArea`.
- Scrap contents: `ServerStorage.Structures.StructureContents.populate(model, config, rng, anchored, scale)`.
- Actual scrap material provider in this project: `ServerStorage.Scraps.ScrapMaterials`. Although the user calls this ScrapKit material assignment, inspect `ServerStorage.ScrapKit` and the material module rather than assuming ScrapKit itself exposes `apply`.

The material module currently provides `Looks`, `apply(model, rng)`, `applyLooks(model, chosenLooks, rng)`, and `ensureVariants()`. It consumes each part's `ScrapRole` attribute. Reuse its weighted MaterialVariants and palettes.

## Runtime hook

This project opts architecture into randomization with:

```lua
-- In the structure's Constants:
RandomizeStructureMaterials = true,
UseAllScraps = true,
PreferredScrapMultiplier = 2.5,
```

`StructureContents.populate` originally called `Materials.apply(model, rng)` when `config.RandomizeStructureMaterials` is true. That call groups by base role and would collapse Metal2/Metal3 into Metal. For this updated workflow, install the bundled helper as `ServerStorage.Structures.ImportedStructureRework` and replace only that architecture opt-in call with:

```lua
if c.RandomizeStructureMaterials then
 require(Storage.Structures.ImportedStructureRework).applyGroupedMaterials(m, Materials, rng)
end
```

Both the spawner and gallery use this shared function. Verify the call is present and the helper version is current. Keep the ordinary scrap-content material logic unchanged. Existing parts without numbered groups retain their base-role group behavior.

Apply name-based role tagging to the staged prefab and again to clones if the project permits live renaming. Do not infer roles for every untagged Plastic import. Prefix assignment and original-part matching are authoritative.

Numbered prefixes retain two attributes: `ScrapRole = "Metal"` selects `Materials.Looks.Metal`; `ScrapMaterialGroup = "Metal2"` separates the random draw. Each of Rust, Metal, Plastic and Wood supports an unnumbered group plus groups 2, 3, 4 and 5. Both `_` and `.` terminate the prefix, whichever occurs first: `Metal2_`, `Metal2.001`, and `metal2_Beam.003` share Metal2; `Wood.` uses the unnumbered Wood group. Numbers after a separator are duplicate/descriptive identifiers, not material groups. Never add numbered palettes to the provider: reuse the base role's weighted variants. Sort group keys for reproducible seeded generation. Store chosen look names as `Look_Metal`, `Look_Metal2` through `Look_Metal5`, etc. All parts sharing a group must share the same Material/MaterialVariant, while palette colors may vary per part.

`ScrapMarkers` is a Folder of invisible BaseParts inside each prefab. Preserve `PlacementRadius` attributes. These markers are not visible architecture and do not receive role tags. Contents are randomized independently by the existing content system.

The preview uses a fresh random seed per build unless `StructurePreviewSeed` is set. Do not reintroduce a fixed preview seed and then claim rerolls are changing.

## Geometry and source handling

The established RuinedWaterTower import had a 2048-stud foundation corresponding to a 48-stud source footprint. Its correction was 48/2048 = 0.0234375. This is an example of measured unit inflation, **not a default conversion for all imports**.

For source reference CFrame S, target reference CFrame T, and factor k:

```lua
local relative = S:ToObjectSpace(sourcePart.CFrame)
newPart.Size = sourcePart.Size * k
newPart.CFrame = T * (CFrame.new(relative.Position * k) * relative.Rotation)
```

Keep MeshIds from the actual edited import. Inspect scale and orientation against the foundation and visible edited features. Ensure hollow/open meshes render correctly; preserve intended sidedness.

Use ScriptEditorService:GetEditorSource/UpdateSourceAsync for existing open scripts; writing Source alone can leave the editor buffer stale. Source changes do not invalidate an already required ModuleScript in Edit mode. A fresh preview module/dependency instance or a new Play session may be required. Avoid retaining competing library modules with identical names.

After success, retain a backup in ServerStorage outside the live Structures library, then remove the exact processed Workspace reference. A reference sharing the same Name is not necessarily the same instance.

