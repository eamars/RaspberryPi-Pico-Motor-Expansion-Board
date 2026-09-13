# Project library conventions

The corrected schematic currently uses **zero custom symbols and zero custom
footprints**. Original KiCad library IDs resolve against the installed KiCad 10
libraries. [The resource audit](../../design/library-audit.json) records exact
footprint IDs, hashes and references. V2's 0805 hand-solder pad style is retained
where suitable; QFN and RF/clock package exceptions are explicit.

Do not clone shipped assets into this directory. Only a necessary nonstandard
asset belongs here, with its upstream source, license, reason for adoption,
modifications and pin/pad validation recorded. Use `MotorExpansionBoardV3` as
its library nickname and project-relative `${KIPRJMOD}` paths if one is needed.

Known model qualifications are distinct from land patterns: the V2-compatible
reset-switch stock land uses a different-height standard 3D model, and the
installed TPS5450 footprint references a model absent from this KiCad install.
Correct these during PCB/3D work; neither is evidence of a qualified 3D fit.
The old custom Sunlord inductor pattern and bulk library duplicates are no
longer active resources. The project does not depend on other checkouts.
