# Selected reference evidence

These are references, not V3 production CAD. Retain a file only when it explains
a design decision or supports a required check. Origins, hashes, purpose and
limits are recorded in [manifest.json](manifest.json); work status is maintained
only in [PROGRESS.md](../PROGRESS.md).

| Retained reference | Why it is needed |
| --- | --- |
| [OWMC root schematic](owmc/owmc.kicad_sch) and [power child](owmc/power_supplies.kicad_sch) | Exact inspected source for the ESP32 core and its cross-sheet RF, reset and USB supply dependencies |
| [OWMC reference PCB](owmc/owmc.kicad_pcb) | Embedded 2D placement and footprints for MCU/RF layout evidence; never the V3 starting layout |
| [TDO B1617A specification](vendor/TDO-TS040WVS02CP-B1617A-v1.0.pdf) | Selected QSPI candidate qualification; unresolved drawing, protocol and power details are documented in the research report |
| [Fly-2209 schematic revision 1.0](vendor/Fly-2209-Schematic-v1.0.pdf) | User-requested StepStick support-circuit reference; capacitor ratings and current-production identity remain to be checked |

The OWMC schematic pair is copied from the actual inspected source, not the
modified imported placeholders. Its power sheet was uncommitted at the recorded
source revision; the exact reviewed bytes are preserved here. Embedded symbol
definitions and PCB footprints make the selected snapshot useful for 2D viewing.
It intentionally omits project check/export settings and application-specific
libraries/models, so complete 3D reconstruction and original configured ERC/DRC
are not promised. Do not use those unresolved historical model names as V3
production dependencies.

The original imported tree is preserved locally at
`.git/v3-development-research-20260912/imported-owmc-before-cleanup/`, relative to
the repository root. All 203 files were checked after moving. This rollback is
not distributed with a fresh clone; its inventory and hashes are preserved in
[the cleanup record](../research/asset-cleanup.json).

The V2.1 mechanical/interface baseline remains untouched in the repository's
[archive](../../archive/motor_expansion_board_v2/pcb/). Production adoption must
copy and validate only the needed assets into V3's own libraries. Firmware and
application references use pinned source citations rather than requiring those
other workspaces to exist.
