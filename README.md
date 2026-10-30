# Mystical Realms Data-Pack

Server-side datapack for Minecraft **1.21.1** (NeoForge 21.1+, pack format 48)
that patches broken content shipped by third-party mods — content that errors
because an optional dependency is missing (Ice and Fire, BYG) or because the
mod's own data is malformed. It never touches, and never requires, any of our
mods.

Built from the errors observed in the *Develop Mystical Realms* instance run of
2026-09-01 (`logs/latest.log` + `logs/debug.log`).

## Fixes included

| Mod | What was wrong | Fix |
|-----|----------------|-----|
| **cataclysm_spellbooks** | 26 recipes reference items the mod never registers (`engineer_*`, `excel_upgrade_*`, `technomancy_*`, `murasama`, `the_*_upgrade`, `smithing/excelsius_*`) → `Unknown registry key` + ~660 cascading JEI "broken recipe" errors via Iron's Spellbooks | Each recipe replaced by a `neoforge:false`-conditioned stub, discarded before its body is parsed |
| **justenoughbreeding** | `breeding/quark/shiba` is malformed (`No key tag in MapLike[{"meat":"true"}]`) | Same `neoforge:false` stub |
| **farmer_delight_pizza_lovers** | `advancement/recipes/cheese_rec` contains a *recipe* json, not an advancement (`No key criteria`) | Rebuilt as a standard hidden recipe-unlock advancement |
| **IDAS** (→ Ice and Fire) | 5 chest loot tables reference `iceandfire:*` items → whole table rejected, chests spawn empty | Tables curated from the IDAS jar: only `iceandfire:` entries dropped, all other loot kept |
| **IDAS** | structures point at `has_structure/bopmahogany_biomes` / `bygmahogany_biomes` / `bygredwood_biomes`, but the jar only ships misspelled files (`bopmohogany_biomes`…) → `Not all defined tags for registry … worldgen/biome` | The three correctly-spelled tags added, empty |
| **IDAS** (→ Ice and Fire) | `integrated_structure_spawners/dread_citadel` lists only `iceandfire:` mobs → `integrated_api`: *dread_lich is not a valid entity ID* | Swapped to vanilla wither_skeleton / skeleton / zombie / vex |
| **illagerstructures** | `structure/monastery.nbt` is corrupt (`UTFDataFormatException`) → every placement throws mid-worldgen | `has_structure/monastery` biome tag emptied so the template is never read |
| **butchery** / **irons_spellbooks** | Both mods hardcode their Patchouli guidebook title + landing-page text as literal English strings directly in `book.json` (not translation keys, unlike apotheosis's `book.apotheosis.name` style) — a single global file, not sharded per locale like the categories/entries tree, so the existing es_es guidebook translation (mystical-realms-translation-fixes) never covered it. This is the "part of the book still in English" (the cover/welcome page) | `book.json` overridden with the Spanish title + landing text for both books |
| **reliquary** | 3 "uncrafting" recipes let 3× `witch_hat` (10 EMC each via its real craft) be turned into 6× `redstone`/`glowstone_dust`/`gunpowder` — flavor recipes unrelated to witch_hat's actual ingredients, picked up by Equivalent Legacy's EMC scanner as real conversions (net gain up to ×12.8, logged as `EMC Exploit` on every boot) | The 3 recipes (`uncrafting/redstone`, `uncrafting/glowstone_dust`, `uncrafting/gunpowder_witch_hat`) disabled with a `neoforge:false` stub, same pattern as the other entries above |

## Not fixable from a datapack

- **`runes:*_altar`** recipe-book category NPE — bug inside `runes`.
- **`supplementaries:sign_post_jungle` / `hanging_sign_jungle`** "invalid item"
  — stale block-entity data in already-generated chunks; heals on re-save.
- **`spell_engine:handheld`** tag missing references — overriding a mod's own
  functional item tag is unsafe; left as-is.
- Cosmetic third-party model / texture / sound gaps.

## Requirements

- Minecraft **1.21.1** (pack format 48), NeoForge **21.1+**
- No mod dependencies.

## Installation

1. Build (or download `build/Mystical_Realms_Data_Pack-<version>.zip`).
2. Drop the zip in `world/datapacks/` (or `saves/<world>/datapacks/`).
3. Load the world — or `/reload` — and the fixes apply.

## Build

```bash
python generate_fixes.py      # regenerate datapack/data/ from the fix list
python build_fix_pack.py      # -> build/Mystical_Realms_Data_Pack-<version>.zip
```

`generate_fixes.py` auto-finds the IDAS jar in the Develop instance to curate
the loot tables; pass `--idas-jar PATH` to point it elsewhere, or it falls back
to empty (but valid) tables. Version is read from `version.txt`.

## License

All Rights Reserved.
