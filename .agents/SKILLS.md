# Workspace electronics skills

The skills in `skills/` are vendored from
[aklofas/kicad-happy](https://github.com/aklofas/kicad-happy).

- Installed release: [v2.2.1](https://github.com/aklofas/kicad-happy/releases/tag/v2.2.1), published 2026-09-01.
- Pinned commit: `d5fd7da585fce7e59329b68fd065384216d4ff0a`.
- Checked and updated: 2026-09-12.
- Provenance and per-file hashes: [skills-lock.json](skills-lock.json).
- Upstream license: [kicad-happy.LICENSE](kicad-happy.LICENSE).
- Local modifications to upstream skill files: none.

## Update result

The previous 172 skill files matched upstream v2.1.0
(`f765dc0916e9752fe2639ca5bad4bda2d5161b8f`), allowing for CRLF/LF line endings.
There were no custom edits to merge.

| Skill(s) | Result |
| --- | --- |
| `kicad` | Updated: 21 changed files and two new files. |
| `emc` | Updated: one changed file. |
| `bom` | Updated: one reference document. |
| `spice` | Added the missing sibling skill used by the KiCad/EMC workflows. |
| `datasheets`, `digikey`, `element14`, `jlcpcb`, `lcsc`, `mouser`, `pcbway` | Already identical to v2.2.1; retained. |

All 187 installed files match the pinned upstream release after normalizing line
endings. The `jlcpcb/` ignore rule now exempts `.agents/skills/jlcpcb/` so the skill
can be tracked with the other workspace tools.

The originals of the three replaced skills are retained locally under
`.git/skill-maintenance/20260912T195148/previous/`. The comparison, upstream
checkout, staged copies of unchanged skills, and probe outputs are in the same
maintenance directory. These local backups are not part of a fresh clone;
the previous pinned release above remains the reproducible rollback source.

## Validation and limits

- All 11 `SKILL.md` files passed the skill creator's `quick_validate.py` check.
- Schematic, PCB (`--full` with schematic input), cross-analysis, and EMC
  analyzers produced JSON successfully from a copied local KiCad project.
  The schematic and PCB each contained 83 components/footprints.
- These were software integration checks. The resulting circuit findings were
  not reviewed or adopted as design conclusions.
- SPICE's CLI and imports loaded, but simulation reported that no supported
  simulator was found. Install/configure ngspice, LTspice, or Xyce before relying
  on simulation results; installing the skill does not install a simulator.
- Distributor credentials, live sourcing, and physical board validation were
  not exercised by this update.

## Future updates

1. Compare the pinned release with upstream's latest stable release and read
   the intervening release notes. Keep all related skills on a consistent pin.
2. Compare installed content with `skills-lock.json` to identify local edits.
   Preserve or merge those edits instead of overwriting them.
3. Use the skill installer helper with `--ref` set to the selected commit and
   `--dest` set to an empty staging directory. Retain sibling dependencies.
4. Run the relevant tools on copied project inputs before replacing changed
   skill directories. Keep backups outside skill discovery paths, then refresh
   the lock file, license, and this record. Leave unchanged skills in place.

Keep project-specific requirements in
[the V3 requirements brief](../motor_expansion_board_v3/REQUIREMENTS.md), so
updating vendor skills does not replace design decisions.
