# Changelog — Mystical Realms Data-Pack

All notable changes to this project will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- **CI**: `PUBLIC_OPTIONAL` back to `"LICENSE NOTICE libs/"` in `.gitlab-ci.yml`, undoing the
  `ci: publish optional public wiki paths` commit. The previous allowlist added
  `wiki/ mkdocs.yml .github/`, which could publish the private wiki and the repository workflows
  in the public snapshot. The wiki is not built by CI: it lives in the GitLab and GitHub
  `.wiki.git` repositories.

## [1.0.0-beta.6] - 2026-09-05

Root cause of the "Butchery guidebook is partly in English" report: the book's
title and landing/welcome page are literal English strings hardcoded in
`book.json` (not translation keys), a single global file outside the
per-locale categories/entries tree that the es_es guidebook translation
(mystical-realms-translation-fixes 0.1.0-beta.4) never covered. Apotheosis's
own book does this correctly via `book.apotheosis.name`-style keys;
butchery and irons_spellbooks do not.

### Added
- **butchery** — `book.json` overridden: title -> "Guía de Carnicería Vol. I",
  landing text translated to Spanish.
- **irons_spellbooks** — same fix for its guidebook: title -> "Guía de Iron's
  Spellbooks", landing text translated (external wiki link preserved).

### Notes
- Apotheosis's own guidebook is unaffected by this bug (uses proper i18n
  keys) but its `apotheosis` lang namespace itself has no es_es file at all
  in this modpack's translation set — a separate, larger gap (hundreds of
  item/enchantment names), not fixed here.

## [1.0.0-beta.5] - 2026-09-04

Refreshed against the 2026-09-04 *Develop* instance run (log analysis).

### Added
- **reliquary** — disables 3 "uncrafting" recipes (`uncrafting/redstone`,
  `uncrafting/glowstone_dust`, `uncrafting/gunpowder_witch_hat`) that turn
  3× `reliquary:witch_hat` into 6× `minecraft:redstone` / `glowstone_dust` /
  `gunpowder`. `witch_hat` itself costs only 10 EMC (via its real crafting
  recipe: sugar + gold_ingot + glowstone_dust + redstone_dust + stick), so
  each of these flavor recipes is a net EMC generator (up to ×12.8 for
  glowstone_dust) once picked up by Equivalent Legacy's automatic EMC
  scanner — logged every boot as `EMC Exploit: ingredients (...) cost 30 but
  output value is 384` (and 192 / 64 for gunpowder / redstone). Confirmed by
  reading the actual recipe JSONs inside the reliquary jar; none of the 3
  reuse witch_hat's real ingredients, they're unrelated bonus conversions.
  Same `neoforge:false` stub pattern as the existing entries.

## [1.0.0-beta.4] - 2026-09-03

Refreshed against the 2026-09-03 *Develop* instance run.

### Added
- **illagerstructures** — empties `has_structure/monastery` biome tag. The mod
  ships a corrupt `structure/monastery.nbt` (`UTFDataFormatException: malformed
  input around byte 340`); every placement attempt threw mid-worldgen
  (`ChunkGenerator` → `JigsawPlacement` → `readStructure`). With no valid biome,
  `findValidGenerationPoint` bails before the template is read.

### Changed
- **IDAS biome tags** — the beta.2/beta.3 pack defined `byg_redwood_biomes` and
  `bygmohogany_biomes`, which match the (already-present) misspelled files inside
  the IDAS jar and so fixed nothing. Replaced with the three names the game
  actually reports as undefined: `bopmahogany_biomes`, `bygmahogany_biomes`,
  `bygredwood_biomes` (`Not all defined tags for registry ... worldgen/biome`).

### Notes
- Still shipped: cataclysm_spellbooks (26 recipes) + justenoughbreeding shiba
  disables, farmer_delight_pizza_lovers `cheese_rec`, IDAS loot tables +
  dread_citadel spawner. 40 files.
- Left to the `utility_nexus_fixes` benign-log filter (not this pack):
  `totw_modded:has_structure/*` dangling refs for absent dimension mods,
  `integrated_villages` empty jigsaw pools, `spell_engine:handheld` /
  `#c:tools/ranged_weapons` (overriding a mod's functional tag is unsafe).

## [1.0.0-beta.3] - 2026-09-01

### Removed
- **irons_spellbooks `spell_book_equip` advancement override** — no longer needed.
  `regalia_slots_api` >= 0.0.0-beta.9 registers the `curios:equip_curio` trigger natively
  (and beta.10 wires the `curios:slot` filter), so the advancement and its 13 children load
  on their own. The datapack was masking a mod bug that is now fixed at the source.

### Notes
- Still shipped: cataclysm_spellbooks (26 recipes) + justenoughbreeding shiba disables,
  farmer_delight_pizza_lovers `cheese_rec`, IDAS loot tables + BYG biome tags + dread_citadel
  spawner. 38 files.

## [1.0.0-beta.2] - 2026-09-01

Full rebuild of the data tree against the actual errors seen in the *Develop*
instance run (2026-09-01), and migration to the 1.21 singular directory layout
(`recipe/`, `advancement/`, `loot_table/`, `tags/worldgen/biome/...`). The
beta.1 tree used the pre-1.21 plural layout and targeted identifiers that did
not match any real error, so none of it applied.

### Added
- `generate_fixes.py` — deterministically regenerates `datapack/data/` from the
  known broken-content list; curates IDAS loot tables straight from the IDAS jar
  when it is present.

### Changed
- **cataclysm_spellbooks** — now disables the **26** recipes that actually fail
  to parse (`Unknown registry key: cataclysm_spellbooks:*`), via
  `neoforge:conditions` + `neoforge:false` (the recipe body is discarded before
  decode, so the parse error never fires). Was: 17 recipes via an invalid
  `minecraft:reference` condition.
- **irons_spellbooks** — rebuilds `irons_spellbooks/spell_book_equip` with a
  `minecraft:inventory_changed` trigger instead of the non-existent
  `curios:equip_curio`. This unblocks its 13 child advancements
  (`spell_book_iron`, `_diamond`, …) that were dropped with it. Was: an
  unrelated `root.json` override.
- **farmer_delight_pizza_lovers** — fixes `advancement/recipes/cheese_rec`
  (the mod ships a recipe json there instead of an advancement → *No key
  criteria*). Was: an unrelated `pizza_lover` override.
- **IDAS loot tables** — curates the 5 chest tables that actually error
  (`chests/dread_citadel/*`, `chests/haunted_manor/if_haunted_manor`,
  `chests/labyrinth/if_labyrinth_tomb`): only the `iceandfire:` entries are
  removed, all vanilla/Create/Quark/Supplementaries loot is kept. Was: 7 empty
  `entities/iceandfire_*` tables that matched no error.
- **IDAS biome tags** — empties the 2 tags that actually fail
  (`has_structure/byg_redwood_biomes`, `has_structure/bygmohogany_biomes`).
  Was: 19 `has_structure_*` tags for vanilla structures that never errored.

### Added (new fixes)
- **justenoughbreeding** — disables the malformed `breeding/quark/shiba`
  recipe (`No key tag in MapLike[{"meat":"true"}]`).
- **IDAS** — `integrated_structure_spawners/dread_citadel` swapped from
  iceandfire-only mobs (→ *iceandfire:dread_lich is not a valid entity ID*) to
  vanilla wither_skeleton / skeleton / zombie / vex.

### Removed
- `mystical_realms_pack:always_false` predicate (`minecraft:always_false` is not
  a valid predicate condition; unused).
- Fabricated `minecraft:missing_biomes` / `minecraft:missing_entities` reference
  tags (no consumer, ~150 speculative ids).

### Not fixable via datapack (documented, no change here)
- `illagerstructures:monastery` — corrupt `.nbt` inside the mod jar
  (`ReportedNbtException`). Needs a mod update or a hand-built replacement nbt.
- `runes:*_altar` recipe-book category NPE — bug inside the `runes` mod.
- `supplementaries:sign_post_jungle` / `hanging_sign_jungle` "invalid item" —
  stale block-entity data in already-generated chunks; self-heals on re-save.
- `spell_engine:handheld` tag missing references — left to `spell_engine`,
  overriding a mod's own functional item tag is unsafe.
- Cosmetic third-party model/texture/sound gaps (ars_nouveau, ars_additions,
  aces_spell_utils, cataclysm sounds, aquamirae sounds, …).

## [1.0.0-beta.1] - 2026-09-01

### Added
- Initial release for Minecraft 1.21.1 (NeoForge 21.1+, pack format 48).
- **Predicate** `mystical_realms_pack:always_false` — reusable condition to disable recipes/advancements.
- **Biome tag** `minecraft:missing_biomes` — identifiers from Biomes You Go, Biomes O' Plenty and other absent mods.
- **Entity tag** `minecraft:missing_entities` — identifiers from Ice and Fire and Alex's Mobs.
- **IDAS** — 19 empty `has_structure_*` biome tags to silence "Unknown biome" errors.
- **IDAS loot tables** — 7 empty `iceandfire_*` entity loot tables (dread_knight, dragons).
- **cataclysm_spellbooks** — 17 recipes disabled (excel upgrades, technomancy rune, weapon parts).
- **irons_spellbooks** — root advancement without the `equip_curio` criterion.
- **farmer_delight_pizza_lovers** — `pizza_lover` advancement with valid `consume_item` criterion.
- Build system: `build_fix_pack.py` with JSON validation, `version.txt`, `.gitlab-ci.yml`, CurseForge upload script.

### Fixed
- Log spam: `Unknown biome: <byg|biomesoplenty|iceandfire>:...`
- Log spam: `Invalid entity type: <iceandfire|alexsmobs>:...`
- Log spam: `Could not parse recipe: cataclysm_spellbooks:...`
- Log spam: `Could not load loot table: idas:entities/iceandfire_...`
- Advancement errors: `Criterion 'equip_curio' not found`

### Workarounds (config required, not datapack)
- **Quark** mob categories: disable `stoneling`, `toretoise`, `foxhound` in `config/quark-common.toml`.

### Compatibility
- Tested with: IDAS, Cataclysm Spellbooks, Iron's Spellbooks, Quark, Farmer's Delight Pizza Lovers, Regalia Slots API.
- Does NOT require: Ice and Fire, Alex's Mobs, Biomes You Go, Biomes O' Plenty, Curios API.