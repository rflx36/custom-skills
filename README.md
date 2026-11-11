# Custom Skills

Personal Codex skills maintained by RFLX36.

| Skill | Purpose |
| --- | --- |
| [custom-3d-game-object](custom-3d-game-object/SKILL.md) | Optimized Blender game objects for Roblox, name-based material groups, FBX export, and five preview views. |
| [roblox-import-rework](roblox-import-rework/SKILL.md) | Rework imported structures into generator-ready Roblox prefabs using the existing project's scrap materials. |

Copy either skill folder from this repository root into your Codex personal skills directory (normally `~/.codex/skills/`). Include its subfolders. Invoke `$custom-3d-game-object` or `$roblox-import-rework`.

The 3D skill requires Blender with Python and FBX support. Helpers run inside Blender. A Blender installation or live connection is not bundled.

The existing import-rework skill is project-specific. Its parser supports Rust/Metal/Plastic/Wood and legacy groups 2–5; it does **not** support the 3D skill's full vocabulary, explicit group 1, or arbitrary group numbers. Check compatibility before using that importer with new assets. This repository does not automatically change project runtime code.

Two Blender study references are included in [custom-3d-game-object/assets/reference-models](custom-3d-game-object/assets/reference-models/):

- [Junkyard_Arcade_Library_Gantry_Reworked.blend](custom-3d-game-object/assets/reference-models/Junkyard_Arcade_Library_Gantry_Reworked.blend): study the `Arcade 1` (broken), `Arcade 2`, and `Gantry Claw` collections. Other collections and alternative prize layouts are not the primary benchmark.
- [shredderrework.blend](custom-3d-game-object/assets/reference-models/shredderrework.blend): study economical machinery geometry and clean structural detail.

These are copies of the owner's reference files; editing the repository copies does not modify the originals. Credentials, generated exports, and preview renders are not included. No license for third-party models is granted by this repository.
