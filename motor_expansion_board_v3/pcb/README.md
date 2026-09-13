# Motor Expansion Board V3 CAD

Open [motor_expansion_board_v3.kicad_pro](motor_expansion_board_v3.kicad_pro)
with KiCad 10 and its standard libraries. The populated
[root schematic](motor_expansion_board_v3.kicad_sch) contains four child sheets:
[power](power.kicad_sch), [motors](motors.kicad_sch),
[serial/outputs](interfaces.kicad_sch) and
[external display connections](display_connector.kicad_sch).

The [B1 review package](../review/README.md),
[review PDF](../review/motor_expansion_board_v3.pdf),
[native ERC](../review/erc.json) and
[connection reconciliation](../review/connectivity-check.json) accompany the
editable sources. Use [PROGRESS.md](../PROGRESS.md) for status and the mandatory
independent review / owner approval gate. No V3 PCB has been created yet.

All current symbol and footprint IDs refer to shipped KiCad assets. The normal
embedded symbol cache is part of each schematic; it is not a duplicate custom
library. See the [resource audit](../design/library-audit.json) and
[library conventions](libraries/README.md). No personal/other-project library
paths or imported OWMC design rules are needed.

The intended netlist, numeric clearances and hierarchy were specified before
capture under [design](../design/). Review outputs live under [review](../review/).
The rejected 15-sheet draft and its generators/libraries were removed reversibly;
[cleanup evidence](../research/rejected-draft-cleanup.json) records the rollback.

Native KiCad edits are supported. The capture tool checks prior generated hashes
and refuses to overwrite subsequent manual CAD edits. Treat CAD edits as work to
preserve; reconcile the contract, exports and review before regenerating.
