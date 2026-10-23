# Layout & Visual Geometry Rules

Layout geometry, corridor management, and QA checklist for water treatment subsystem displays (e.g., SWRO RO Racks).

---

### 1. Canvas and Coordinate Budget

Default canvas `1400 × 940` (16:10 widescreen ratio), border inset 15.

| Zone | Y Range | Contents |
|---|---|---|
| Header & Stamp | 40–95 | Subsystem title, operational status, project stamp |
| Upper Process Corridor | 110–290 | High-pressure feed lines, chemical dosing inlets, top transmitters |
| Core Equipment Rack | 300–640 | RO Membrane vessels, Pressure Exchangers, High-Pressure Pumps |
| Lower Process Corridor | 650–780 | Permeate collection lines, brine discharge routing |
| Telemetry & Legend | 800–900 | Subsystem legend, stream indicators, revision identifier |

Scale up proportionally for wider units. Keep at least 30 px of clear space around the sheet border.

---

### 2. Bands and Corridors

- **Elevation Bands:** Every horizontal pipe run gets its own Y band (minimum 30 px spacing between adjacent bands so labels fit).
- **Vertical Corridors:** Every vertical pipe drop gets its own X corridor (minimum 25 px spacing so parallel lines read as distinct paths).
- **Collinear Segments:** Two parallel process or signal runs sharing an axis must be offset by at least 20 px to prevent reading as a single intermittent line.

---

### 3. Eliminating Crossings

Resolve line crossings in strict priority order:

1. **Re-order elevations:** Assign Y-elevations based on nozzle connection heights on equipment. Most crossings disappear here.
2. **Move the source:** Route lines from top or opposite canvas boundaries.
3. **Relocate telemetry anchors:** Placing a sensor box on the same side as its impulse lead avoids crossing process lines.
4. **Line jump (`line_jump`):** Only when 1–3 all fail. Draw a semicircular hop:
   ```xml
   <path d="M {x-14},{y} A 14 14 0 0 1 {x+14},{y}" fill="none" stroke="{color}" stroke-width="2.4"/>