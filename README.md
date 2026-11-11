# Custom Skills

Personal Codex skills maintained by RFLX36.

| Skill | Purpose |
| --- | --- |
| [custom-3d-game-object](skills/custom-3d-game-object/SKILL.md) | Optimized Blender game objects for Roblox, name-based material groups, FBX export, and five preview views. |
| [roblox-import-rework](skills/roblox-import-rework/SKILL.md) | Rework imported structures into generator-ready Roblox prefabs using the existing project's scrap materials. |

Copy an individual folder from `skills/` into your Codex personal skills directory (normally `~/.codex/skills/`). Invoke `$custom-3d-game-object` or `$roblox-import-rework`.

The 3D skill requires Blender with Python and FBX support. Helpers run inside Blender. A Blender installation or live connection is not bundled.

The existing import-rework skill is project-specific. Its parser supports Rust/Metal/Plastic/Wood and legacy groups 2–5; it does **not** support the 3D skill's full vocabulary, explicit group 1, or arbitrary group numbers. Check compatibility before using that importer with new assets. This repository does not automatically change project runtime code.

Personal Blender references, credentials, generated models, and renders are not included. No license for third-party models is granted by this repository.
