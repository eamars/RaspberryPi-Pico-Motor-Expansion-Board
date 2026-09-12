# V3 active CAD

No V3 schematic or PCB exists yet. The imported OWMC project and old placeholders
were removed from this directory under DEC-018; see the
[cleanup evidence](../research/asset-cleanup.json). Necessary reference material
is separated under [references](../references/README.md).

Use [PROGRESS.md](../PROGRESS.md) as the only work tracker. Gate G-01 requires
cleanup/resource preparation, intended net/endpoint and pin allocation, numeric
clearance/net-class rules and schematic hierarchy conventions before drawing.
The implementation netlist must later reconcile with that specification.

Future production files belong here under a V3-specific basename, proposed as
`opentrickler_v3`. Parent and child sheets belong to this project and use relative
sheet paths. The top sheet should describe functional connections; children
should own coherent MCU, power/service, motor, display and retained-interface
circuits with explicit ports. Final sheet boundaries are specified under A-07.

The independent schematic review must assess both connectivity and rendered
readability against all requirements. Owner approval of its exact reviewed
revision is mandatory under G-02 before PCB implementation. The archived V2.1
geometry defines the board, mounting and retained connectors; OWMC is not a
starting PCB.

Custom production assets belong under [libraries](libraries/README.md), with local
tables in this directory. Do not point active CAD into references, archives,
another checkout, personal libraries or the rollback backup. Select a real
fabrication stack-up and write new rules; no imported `.kicad_pro` or `.kicad_dru`
has been adopted.

Keep generated review/export artifacts under the future `../outputs/` tree,
separated by reviewed revision and purpose. Keep manufacturing releases separate
from scratch exports. Update documentation and links as each artifact is created.
