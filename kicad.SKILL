# KiCad ECAD File Reading and Modification Skill

This skill defines the procedures and rules for AI agents to parse, understand, and modify KiCad EDA files (v6/v7/v8+). KiCad files are highly structured, often exceptionally large, and require targeted searching rather than full-file reading.

## 1. File Formats Overview
KiCad uses human-readable text formats for its core files:
*   **`.kicad_pro` (Project File):** A JSON file containing project-wide settings, NetClasses, Design Rule Checks (DRC), and active libraries.
*   **`.kicad_sch` (Schematic File):** An S-expression (LISP-like) file detailing the logical connections, components, and hierarchical structure.
*   **`.kicad_pcb` (Board Layout File):** An S-expression file detailing the physical board, footprints, traces (segments), vias, and copper zones.

## 2. General Principles for AI Agents
*   **NEVER read `.kicad_sch` or `.kicad_pcb` in their entirety.** They regularly exceed 10,000+ lines and will exhaust context limits.
*   **Always use `grep_search`** with `FixedStrings: true` (or targeted Regex) to extract specific blocks, followed by `read_file` with `offset` and `limit` to read the surrounding context of a match.
*   **S-Expressions are strict.** Parenthesis `()` balancing is critical. If making modifications, you must preserve the exact indentation and parenthesis structure.

## 3. How to Understand the Electrical Construction and Flow

To provide the user with a high-level understanding of a board, follow this sequence:

### Step 1: Identify Core Components (BOM Extraction)
Search the `.kicad_sch` file to find the main ICs, connectors, and passive blocks.
*   **Target:** `(property "Reference" "U"` (for ICs), `"J"` (for Connectors), `"Q"` (for Transistors), `"D"` (for Diodes).
*   **Target:** `(property "Value"`
*   *Action:* Grep for `(property "Reference" "U` to find all ICs. Then read the surrounding lines to find their corresponding `(property "Value"`. This tells you *what* the board does (e.g., identifying Microcontrollers, Motor Drivers, Regulators).

### Step 2: Understand Connectivity and Data Flow
Do not try to trace individual `(wire)` elements. Instead, track named nets and labels.
*   **Target:** `(global_label` or `(hierarchical_label`
*   *Action:* Grep the `.kicad_sch` for these labels. Named nets like `SPI_SDA`, `I2C_SCL`, `MOTOR_STEP`, or `+5V` instantly reveal the board's communication protocols and logical subsystems.

### Step 3: Analyze Power Architecture
*   **Target:** `(symbol "power:` or `(property "Value" "+` (e.g., +3V3, +5V, GND) in the `.kicad_sch`.
*   *Action:* Identify the power rails.
*   **Target:** `(zone` in the `.kicad_pcb`.
*   *Action:* Grep for copper pours to understand how power and ground are physically distributed across the layers (e.g., finding a dedicated GND plane on an inner layer).

### Step 4: Examine the Physical PCB Stackup and Constraints
*   *Action:* Read the `.kicad_pro` (JSON) to find the `board` object, which contains `design_settings`, `rules`, and `layers`. This tells you if it's a 2-layer or 4-layer board, and what the minimum trace widths/clearances are.
*   *Action:* Grep `.kicad_pcb` for `(layer "F.Cu")`, `(layer "In1.Cu")`, etc., to confirm the stackup.

## 4. How to Make Modifications

When asked to modify a KiCad project, exercise extreme caution. Structural routing modifications (moving traces/components) should generally be avoided via text editing, but logical modifications (changing values, renaming labels, altering properties) are highly effective.

### Safe Modifications
1.  **Changing Component Values:**
    *   *Scenario:* Changing a resistor from 10k to 4.7k.
    *   *Action:* Use `grep_search` to find the specific `(property "Reference" "R12")` block in both `.kicad_sch` and `.kicad_pcb`. Use `multi_edit` to replace the associated `(property "Value" "10k"` with `(property "Value" "4.7k"`. Both files must be updated to keep the schematic and PCB synchronized.
2.  **Updating Silkscreen Text:**
    *   *Scenario:* Changing a board revision number or label.
    *   *Action:* Grep `.kicad_pcb` for `(gr_text`. Locate the target string and use `edit` to update the text within the quotes.
3.  **Renaming Nets/Labels:**
    *   *Scenario:* Renaming `UART_TX` to `ESP_TX`.
    *   *Action:* Grep `.kicad_sch` for `(global_label "UART_TX"`. Use `replace_all` within the relevant blocks to update the label.

### Risky Modifications (Requires Extreme Precision)
1.  **Deleting Components:**
    *   You must delete the entire `(symbol ...)` block in `.kicad_sch` and the corresponding `(footprint ...)` block in `.kicad_pcb`, ensuring parenthetical balance is perfectly maintained.
2.  **Routing/Wire Changes:**
    *   Modifying `(wire ...)` in the schematic or `(segment ...)` in the PCB is not recommended for AI agents unless fixing a very specific, isolated coordinate error.

## 5. Standard Operating Procedure (SOP) for KiCad Queries
1.  User asks a question about the board design.
2.  Agent runs `grep_search` for `Reference` and `Value` to identify major components.
3.  Agent runs `grep_search` for `label` to map buses and power rails.
4.  Agent synthesizes the findings into a high-level architectural summary (Power, Compute, IO, Interfaces).
5.  If a modification is requested, Agent pinpoints the exact line numbers using `grep_search` with `MatchPerLine: true`, then utilizes the `read_file` tool to extract the exact S-expression block, and finally uses `edit` to inject the precise replacement.
