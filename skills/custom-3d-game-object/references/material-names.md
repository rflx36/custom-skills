# Material names

Rename Blender **objects** as `<MaterialName><MaterialGroupNumber>_<ObjectName>`.

Allowed names: **Concrete, Ground, Leather, Metal, Pavement, Plastic, Rock, Rubber, Rust, Stone, Wood, Glass, Color**.

These are custom categories. Do not substitute Roblox enum names, merge Stone with Rock, or add Ceramic or other categories without a user update. Glass is explicitly allowed. Color is a semantic tag, not a Roblox material.

Use any positive integer group number, no upper bound, and no leading zeros. Generate explicit group **1** for the first group. Matching material and group identify one intended shared appearance; different groups are independent choices that may coincide. The skill labels this intent; downstream systems implement it.

Examples: `Rust2_OutlineMetal`, `Metal1_Support`, `Metal12_Hinge`, `Glass1_Window`, `Color2_Button`.

Use Color **only when randomized color is acceptable**. Do not use it for glass, fixed-color warnings, or a functional display merely because its material is unclear. Matching Color groups indicate shared random color. Ask about genuinely ambiguous special surfaces instead of expanding the vocabulary silently.

Separate different groups and moving components. Compatible static components of one group may be combined. Make repeats unique in their description, e.g. `Metal1_Bolt_01`.

Read legacy unnumbered prefixes as group 1; accept known prefixes case-insensitively when inspecting existing assets. Report legacy names and generate canonical explicit-number names for new work. Blender `.001` suffixes belong to the description. `Metal_2_Panel` is legacy Metal group 1, not Metal2. Bare names such as Glass, DisplaySurface, or Scrap_Hopper in references are not canonical output names.

Do not assign Blender materials, shaders, textures, or baked maps to implement these labels. Preserve existing user materials on edits unless asked otherwise.

The separate roblox-import-rework skill's narrower parser is unchanged. This naming contract does not imply importer compatibility.
