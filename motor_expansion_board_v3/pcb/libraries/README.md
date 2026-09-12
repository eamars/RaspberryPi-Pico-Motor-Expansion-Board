# V3 production library conventions

No imported symbols, footprints or models have been approved for V3 yet.
[manifest.json](manifest.json) records adopted assets as they are qualified;
work status belongs only in [PROGRESS.md](../../PROGRESS.md).

Use this structure as assets are adopted:

| Resource | Local location / convention |
| --- | --- |
| Symbols | `symbols/OpenTricklerV3.kicad_sym`; stable `OpenTricklerV3` nickname |
| Footprints | `footprints/OpenTricklerV3.pretty/`; stable `OpenTricklerV3` nickname |
| Models | `models/`; exact-part names and units/origin/orientation checked |
| Library tables | `../sym-lib-table` and `../fp-lib-table`, with `${KIPRJMOD}/libraries/...` paths |
| Source evidence | Local manifest with upstream URL/revision/hash/license, source name, adopted local name, reason, modifications and validation references |

Copy only assets actually needed by the design. Check each selected component's
symbol pin numbers/functions, footprint pad numbering/pitch, land pattern and
3D alignment against its manufacturer drawing. Resolve symbol footprint defaults
to the local nickname. Record original authorship/license and modifications;
do not silently relabel a downloaded asset as original work.

Vendor every nonstandard production dependency. For standard KiCad assets, pin
the supported KiCad/library version and either vendor the used asset with its
license or document the installed standard dependency and verify it on a fresh
checkout. No personal or other-project library resolution is permitted. Production
models should resolve locally; an unavailable model must be an explicit review
gap rather than a broken path presented as complete 3D verification.

Library organization is ready for adoption, but part-level validation and the
fresh-checkout resolution test remain future acceptance work. File presence or
an empty library table does not establish library correctness.
