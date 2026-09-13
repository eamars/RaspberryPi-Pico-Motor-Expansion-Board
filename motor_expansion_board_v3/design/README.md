# Pre-capture design specification

The initial [G-01 record](pre-capture-gate-initial.json) predates corrected CAD.
[The current record](pre-capture-gate.json) includes the later L4 part/value
and Q2 MOSFET amendments made before regenerating the affected schematics. These are evidence
records; [PROGRESS.md](../PROGRESS.md) is the only work tracker.

- [net-intent.json](net-intent.json): every component, numbered terminal, intended
  net, explicit NC, footprint, rating and candidate source property.
- [net-endpoints.json](net-endpoints.json): 116 named nets with their physical
  endpoints, grouped independently of schematic drawing coordinates.
- [hierarchy.json](hierarchy.json): five pages, responsibilities and exact named
  child-sheet interfaces/directions.
- [net-classes.json](net-classes.json): numeric clearance/width/via rules and the
  explicit stackup assumptions. The .kicad_pro applies these constraints.
- [library-audit.json](library-audit.json): all installed footprint resources,
  source hashes and references; zero custom libraries.
- [generated-schematic-hashes.json](generated-schematic-hashes.json): last native
  generated revision; protects later manual CAD edits from accidental overwrite.

The circuit preserves V2.1 external pin mappings. The primary source is the
archived CAD; inherited ambiguous component names were resolved against the
manufacturer/stock asset where possible. Remaining package/source or physical
test qualifications are explicit in the review and master tracker.
