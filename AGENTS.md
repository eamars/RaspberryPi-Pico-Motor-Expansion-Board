# Project context

V3 means the Motor Expansion Board V3 PCB, retaining V2.1 functions and external
compatibility with three core changes: one ESP32-S3R8 in place of the Pico,
two onboard TMC2209s in place of StepSticks, and an external display connector.
OpenTrickler is application context. Do not expand this into a product or display
module design. For V3 planning or design changes, read
[motor_expansion_board_v3/REQUIREMENTS.md](motor_expansion_board_v3/REQUIREMENTS.md)
first. Maintain it as requirements and design objectives are agreed in
conversation. Keep user-confirmed requirements, proposed choices, open questions,
and verification evidence distinct; use the existing stable IDs when recording
decisions or design changes. Preserve unresolved values as TBD.

Use [motor_expansion_board_v3/PROGRESS.md](motor_expansion_board_v3/PROGRESS.md)
as the ONE master implementation progress tracker. Read it before V3 execution
work and update it as tasks, dependencies, findings and acceptance evidence
change. Do not create parallel task/status trackers. Requirements describe the
agreed specification; research reports hold evidence; PROGRESS.md holds work
status across research, schematic, placement, routing, BOM, checks and bring-up.

DEC-019 limits assistant delivery to the completed schematic, PCB layout and
first preliminary BOM, including pin-capability verification and design-review evidence. DEC-022
excludes firmware rework and application-port analysis: confirm only that the
selected pins can serve their intended purposes.
The owner manages production; Mellow manufactures and performs initial functional
testing. Track downstream acceptance separately by owner in the same tracker;
do not execute production management, purchasing or physical bring-up as assistant
scope. Use per-board BOM quantities without asking for production batch size or
schedule. Servo baseline is the MG90S identified in OpenTrickler's sourcing guide,
with its full-metal 180-degree recommendation and AliExpress item 1005004550692203.

The owner stopped the expanded 15-sheet draft, then explicitly authorized the
V2-based reset with "Proceed" on 2026-09-13. Cleanup, corrected specification
and schematic capture/review may proceed. The rejected draft is not a baseline.
Read [the V2 and OWMC study](motor_expansion_board_v3/research/V2_DESIGN_STUDY.md).
Use V2.1 for circuits, mechanical compatibility and assembly intent. Use the
owner's OWMC parent/child-sheet style: coherent grouped circuits, at most five
sheets total, explicit hierarchical sheet pins/labels between sheets and local
labels within pages. Prefer installed KiCad symbols/footprints; do not duplicate
stock assets. Retain V2's larger hand-solder pads where suitable and justify
exceptions. Keep only needed custom assets and reference evidence locally.

The copied OWMC design is reference material only. No V3 schematic or PCB existed
when this project began. Before resumed schematic implementation, complete the
cleanup, self-contained resource audit, intended net/endpoint specification,
numeric clearance/net-class rules and hierarchy conventions in the master
tracker's pre-schematic gate. Do not inherit the reference project's libraries
or design rules without explicit review. Keep adopted custom assets inside the
project with project-relative paths and provenance; retain only useful reference
snapshots. Update READMEs and evidence as artifacts move or change.

An independent agent must review the completed schematic against the confirmed
requirements. Resolve/disposition its findings, then obtain the owner's explicit
approval of the exact review package before PCB implementation. Do not request
that approval until the schematic and review evidence are concrete and ready.
Material changes invalidate the affected review/approval and require renewal.

For power, USB, or pin-allocation work, also read V3's
`POWER_ARCHITECTURE.md` and `USE_CASE_RESEARCH.md`. They capture the practical
OpenTrickler hardware/firmware context and distinguish proposals from agreed
requirements; source revisions and hashes are recorded under V3's `research/`.

Workspace electronics skills are vendored from a pinned upstream release.
Their source, validation record, and update procedure are in
[.agents/SKILLS.md](.agents/SKILLS.md), with file hashes in
[.agents/skills-lock.json](.agents/skills-lock.json).
