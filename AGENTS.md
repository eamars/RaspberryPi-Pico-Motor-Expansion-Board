# Project context

V3 is the work-in-progress board. For V3 planning or design changes, read
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

The copied OWMC design is reference material only. There is no pre-existing V3
schematic or PCB to continue. Before schematic implementation, complete the
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
