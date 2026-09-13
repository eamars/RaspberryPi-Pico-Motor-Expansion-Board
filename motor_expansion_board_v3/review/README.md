# B1 schematic review package

This package is the corrected **Motor Expansion Board V3** schematic for the
owner's G-02 review. It replaces the rejected draft. The three core changes are
the directly fitted ESP32-S3R8, two onboard TMC2209s and an external display
connector, with the archived V2.1 interfaces retained.

Open the [five-page schematic PDF](motor_expansion_board_v3.pdf) or the editable
[KiCad 10 project](../pcb/motor_expansion_board_v3.kicad_pro).
The [independent review](INDEPENDENT_SCHEMATIC_REVIEW.md) gives the electrical
assessment, source evidence, qualifications and exact schematic hashes.
[package-manifest.json](package-manifest.json) identifies all package artifacts.
Live status and dispositions remain in the one [master tracker](../PROGRESS.md).

## Drawing and connection checks

- One populated parent and four child sheets, grouped by function; both motor
  channels share a page. Named hierarchical ports connect the sheets. There are
  no global signal labels.
- All symbols and footprints use installed KiCad assets. Ordinary passives use
  the V2 0805 hand-solder footprint style; RF/clock, shunts and IC packages are
  explicit exceptions. No custom library copies are required.
- [Native KiCad ERC](erc.json): **0 errors / 0 warnings**. Ignored check categories
  and analyzer limitations are disclosed in the independent report.
- [Native netlist](netlist.xml) and [reconciliation](connectivity-check.json):
  **116 connected nets, 551 connected physical endpoints and 37 explicit NCs**
  across 166 component instances. The reviewer also reconstructed connections
  independently from the native drawings.
- [Pin-capability check](../research/PIN_CAPABILITY_CHECK.md): MCU physical pins,
  R8 memory reservations, signal capabilities, levels and boot restrictions.
  Firmware rework and application-port analysis are outside scope (DEC-022).
- [BOM analysis](bom-analysis.json) exposes sourcing gaps in the captured symbol
  properties. This is component-inventory evidence for schematic review; the
  preliminary BOM handoff remains part of the later completed-PCB delivery.

The [initial pre-capture gate](../design/pre-capture-gate-initial.json) records
the numbered connection contract and numeric clearances before CAD capture.
[Current constraints](../design/net-classes.json) remain inputs to PCB work;
they do not establish routed impedance or current capacity by themselves.

## What approval covers

G-02 approves the reviewed schematic as the basis for PCB implementation. Under
the owner's REQ-PROC-007 instruction, an independent review and explicit owner
approval are required before that work starts. Approval has not been inferred
from the earlier instruction to begin schematic design.

The remaining bounded qualifications are C8 output-capacitor ESR/filter evidence,
the supplied display/cable and Mini KILL-link details, exact preliminary-BOM
parts and prototype measurements. Their IDs, ownership and stages are recorded
under ISR-02 through ISR-06 in the master tracker. They are not hidden passes.
Any material electrical or connector change requires the affected review and
approval to be renewed.

Main PD power is required for service; the PC connection cannot supply board or
motor power. Only one display assembly is connected, with power off for cable
changes. The board contains the external display interface, not a display module.

No V3 PCB has yet been created. Board geometry/placement/routing, DRC and the
first preliminary BOM follow approval. Production and initial physical testing
belong to the owner/Mellow; this package is not a fabrication release.
