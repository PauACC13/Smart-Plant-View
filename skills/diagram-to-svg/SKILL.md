---
name: diagram-to-svg
description: Converts static water treatment subsystem process diagrams (PDFs/P&DIs or image exports) into standardized, machine-readable SVG graphics. Use when processing RO Rack or subsystem SCADA screens to establish interactive 2D Operational Digital Twin screens. Not a substitute for issued-for-design CAD P&ID engineering models or physical plant CAD files.
---

# Diagram to Structured SVG Converter

Produces a standardized, machine-readable SVG graphic of a water treatment subsystem screen (e.g., Reverse Osmosis Racks that a process control or SCADA engineer would accept: accurate equipment geometries, non-overlapping pipe paths, correct flow directionality, and strict adherence to DOM grouping standards (`<g id="asset-...">`) and SCADA telemetry anchors (`data-tag="..."`).

The output is judged by a SCADA automation engineer who will spot a misplaced flow arrow, a missing nozzle connection, or a misaligned telemetry text box.

---

## Non-negotiable output rules

1. **Root Canvas Attributes:** Root element MUST use `viewBox="0 0 1400 940"` and MUST NOT hardcode fixed pixel `width` or `height` attributes.
2. **Asset ID Grouping:** Every core equipment item MUST be enclosed inside `<g id="asset-{ASSET_ID}" class="equipment {ASSET_TYPE}" data-asset-type="{ASSET_TYPE}">`.
3. **Telemetry Anchors:** Telemetry text nodes MUST use native `<text id="tag-{SCADA_TAG}" data-tag="{SCADA_TAG}" data-unit="{UNIT}" class="telemetry-value">` carrying exact SCADA tag identifiers from the original screen.
4. **Editable Native Text:** Text MUST be rendered using true `<text>` elements—NEVER converted to graphics paths (`<path>`) or glyph references (`<use>`).
5. **Equipment Catalog Fidelity:** Equipment shapes MUST strictly conform to `docs/standards/equipment-catalog.md` (e.g., pumps with internal direction arrows, RO racks with stage divider geometries, pressure exchangers with opposing flow arrows).
---

## Workflow

### 1. Read the request and fill the gaps

What is almost always underspecified? List the questions worth asking, and cap them (e.g. "ask at most 2–3, and only for things that change the answer"). For everything else, make a defensible assumption and state it afterward.

Subsystem diagram inputs often contain minor visual defects or cropped boundaries. Before generating the script, resolve:
* What is the primary operational subsystem (e.g., 1st Pass, 2nd Pass, ERD Loop)?
* What are the boundary inlet/outlet node labels (e.g., `BRINE DISCHARGE`, `1ST PASS PRMT`)?
* Are there any unrecognized non-catalog assets that require generic fallback box handling?
* Ask at most 2–3 questions, and only for critical ambiguities. For anything minor, make a defensible engineering assumption based on `docs/standards/plant-standards.md` and state it afterward.*

### 2. Plan before producing

Identify and map the 6–7 primary equipment assets on the $1400 \times 940$ coordinate grid:
1. Assign $X, Y$ positions to core assets (Pumps, RO Racks, ERDs, Valves).
2. Determine main process pipe corridors (Feed line, Permeate collector, Brine discharge).
3. Identify telemetry anchor coordinates adjacent to their corresponding nozzles or pipes.

### 3. Produce

> `scripts/pid_lib.py` provides the drawing primitives. Read it before writing the generation script and use its helper functions rather than hand-crafting raw SVG bezier curves. Read `references/svg-schema.md` for coordinate conventions and `references/symbol-catalog.md` for geometry rules.

Generate the Python script (`build_subsystem_svg.py`) that imports `pid_lib.py` and emits the final SVG in the mandatory layer render order[cite: 1, 2, 6]:
1. Defs & CSS Style blocks (`<defs>`, `<style>`)[cite: 1, 2]
2. Boundary nodes (`.boundary-container`)[cite: 1]
3. Process pipe paths (`<path class="process-pipe ...">`)[cite: 1, 2]
4. Core equipment groups (`<g class="equipment ...">`)[cite: 1, 2]
5. Valves and opaque white-backed instrument nodes[cite: 1, 2]
6. Telemetry text anchors (`<text data-tag="...">`)[cite: 1, 2]

### 4. Check the output and fix it

**The step that separates a passable result from a professional one.** Render it, run it, or validate it — then actually look at the result and iterate. Say how many rounds to expect and list the defects that are only visible on inspection.

### 5. Deliver

Where the output goes, and what to state alongside it: assumptions made, anything that couldn't be done and why, and any concern noticed along the way. Flagging concerns is usually a large part of the value.

## What this skill does not do

State the limits plainly, and say so to the user if their framing suggests they expect more. Everything in this repo is conceptual, engineering-support output — not issued-for-design work, not hazard analysis, not equipment sizing.
