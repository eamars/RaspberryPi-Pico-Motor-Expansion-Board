# Component source cache

[manifest.json](manifest.json) lists the retained PDFs, source URLs, retrieval
dates and SHA-256 hashes. These sources support the current B1 circuit. The
2N7002K PDF is retained only as evidence for replacing Q2 with BSS138LT1G; it is
not a fitted component. [capture-sources.json](capture-sources.json) preserves
the capture-stage download results, including failures.

The cache is partial. Direct downloads of BSS138LT1G, CAT24C256, USBLC6-2,
TMC2209 and MAX3232 failed. Primary web sources and useful pinned reference
designs supplement it; the independent review states its evidence and limits.
Neither a failed download nor a populated MPN establishes lifecycle or stock.

Eighteen PDFs for removed draft components were moved to hash-checked local
rollback storage; see [cleanup evidence](../research/unused-datasheets-cleanup.json).
They are no longer active project resources. Necessary external-display and
Fly/reference evidence remains under `../references/`.
