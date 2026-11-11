---
name: roblox-import-rework
description: Rework a Blender-imported Roblox structure into a generator-ready prefab, assign existing scrap material variants from Rust/Metal/Plastic/Wood name prefixes, validate the result, and remove the processed imported reference.
---

# Roblox import rework

Use for an imported structure already in Roblox Studio, or guide the user through importing its saved Blender export first. This workflow creates a usable prefab; exporting a file alone is not completion.

If the user requests guidance only, explain the workflow without changing Studio or deleting any reference.

## Select the source and destination

Use connected Studio tools to inspect the current mode, selection, source geometry and structure library. Resolve the selected model by instance identity, including selections of its descendants. Duplicate names are common: never choose or delete all models matching a name.

Honor an explicit destination. Otherwise create a new folder named after the original structure plus `v2` under the existing structure library; keep the previous version. If the destination exists, inspect it and follow the user's update intent instead of silently replacing it.

Confirm the imported geometry has persistent mesh assets. EditableMesh object content and opaque session content are not permanent mesh imports. When the standard importer is needed, use available computer-use tooling; if that fails, provide the prepared FBX/OBJ and resume after manual import. Never approximate edited meshes with their old primitive shapes.

## Rework the imported geometry

Read [references/project-integration.md](references/project-integration.md) for this user's wasteland conventions and integration points. The helper [assets/imported-structure-rework.luau](assets/imported-structure-rework.luau) provides the reusable name parser, prefab staging, validation, and precise reference cleanup.

Preserve edited geometry, uploaded MeshIds, relative transforms, material-bearing surfaces and the user's foundation choice. Create a fresh anchored Model named `Prefab`, so imported Model scaling caches do not affect later `ScaleTo` calls.

Measure import scale against a known reference such as the original foundation's footprint. Normalize uniform importer inflation while retaining the Blender edits. Derive the pivot from the corresponding reference part, so the prefab's ground plane matches the generator. Do not force every import to a hardcoded size or multiply the normalization factor twice.

## Material assignment

For every visible BasePart or MeshPart:
- Parse `<material><group><duplicateIdentifier>` case-insensitively. Material is `Rust`, `Metal`, `Plastic`, or `Wood`; group is absent or one of `2`, `3`, `4`, `5`; duplicateIdentifier is `_` or `.`. Read only the text before the first occurrence of either separator, trim surrounding whitespace, and ignore the remainder for material/group detection. Accept canonical bare tokens as well for existing attributes and backward compatibility.
- Keep the base palette in `ScrapRole`, and the full canonical prefix in `ScrapMaterialGroup`. For `metal2_Beam`, use `ScrapRole = "Metal"` and `ScrapMaterialGroup = "Metal2"`. The name prefix takes precedence over inherited roles/groups.
- Use the project's existing scrap material provider and weighted variants; do not invent replacement palettes or flatten every mesh to one material.
- For an unrecognized prefix, retain a valid existing role or restore a matched original part's material and role. Otherwise preserve its material, leave it untagged, and report it. Concrete, glass, and unrelated names must not become plastic merely because the importer supplied Plastic.
- Keep names useful for later edits. Parsing the prefix does not require deleting the descriptive remainder.

Examples: `Metal2_` → Metal/Metal2; `Wood.` → Wood/Wood; `metal2.001` → Metal/Metal2; `Metal4_Pipe.002` → Metal/Metal4; `Rust5.Panel_001` → Rust/Rust5; `Plastic3_Cap` → Plastic/Plastic3. `Metal_2_Pipe` and `Metal.2_Pipe` belong to the ordinary Metal group because only the segment before the first separator is examined. Group 1, 0, 6, or multi-digit groups are not supported. `RustyTank_001` and `MetalSheet.001` are not exact role prefixes.

Apply compatible randomized looks to tagged architecture when spawned and when displayed in the test gallery. Use the helper's `applyGroupedMaterials(model, provider, rng)`: every material group draws once from its base role's existing weighted palette, and every part in that group shares the chosen look. Metal, Metal2, Metal3, Metal4, and Metal5 make independent draws; the same applies to all four roles. Both separators map to the same canonical group: `Metal2_Pipe` and `Metal2.001` share Metal2. Independent draws can coincide. Palette colors may still vary per part within the chosen look. Keep ordinary scrap-content randomization active as well.

## Integrate, verify, clean up

Copy or adapt the original editable Constants and scrap markers to the new folder. Preserve its scrap pool/preferences, count limits, spacing and scale controls. Check marker positions against the edited geometry. Register through the existing discovery system and include the result in the existing test area, without adding display labels unless requested.

Before cleanup, verify:
- Expected visible geometry count, mesh asset persistence, corrected size/pivot and anchored structural parts.
- Role/group-prefix assignment, one draw per group, consistent looks inside each group, and independent group draws. Also check that different seeds produce different looks.
- Scrap spawning still works, stays supported, and avoids geometry.
- The generator and gallery use the new prefab. Refresh cached ModuleScripts when needed and verify source changes through ScriptEditorService.
- The previous version remains available when creating v2.

Then back up and delete **only the exact imported reference model that was processed**, using its retained instance reference through Studio APIs. This cleanup is part of the requested workflow; do not delete sibling imports, other versions, staging backups, source Blender files, or unrelated models. If validation fails, retain the source and explain the unfinished step. If the user explicitly excludes cleanup, honor that instruction.

Report the created/updated folder, material roles, validation result, and whether the processed reference was removed.

