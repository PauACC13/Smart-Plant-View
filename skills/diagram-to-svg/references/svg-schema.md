# Master SVG Schema & Convention Reference (AI Runtime Context)

This reference document defines the mandatory XML structure, layer hierarchy, metadata attributes, and CSS styling classes for generated water treatment subsystem SVGs (e.g., SWRO RO Racks).

---

## 1. Canvas & ViewBox Rules

1. **Grid Resolution:** Coordinate space is fixed at `1400 × 940` units (16:10 widescreen aspect ratio).
2. **Fluid Responsiveness:** The root `<svg>` element MUST include a responsive `viewBox="0 0 1400 940"` and MUST NOT hardcode pixel `width` or `height` attributes:
   ```xml
   <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 940" class="water-treatment-subsystem">
   ```
3. **Mandatory Z-Index Layer Order:** To prevent line bleed-through and ensure visual readability, SVG nodes MUST be emitted in this exact sequence:
   1. Canvas defs and CSS `<style>` blocks (`<defs>`, `<style>`)
   2. Boundary nodes and background collector fills (`.boundary-container`)
   3. Process pipe paths (`<path class="process-pipe ...">`)
   4. Core equipment groups (`<g class="equipment ...">`)
   5. Opaque white-backed instrument elements and valves (`fill="#ffffff"`)
   6. Telemetry text anchors (`<text data-tag="...">`)

---

## 2. Asset Identification & Grouping (`<g>`)

Every physical equipment item (Pumps, RO Vessels, Pressure Exchangers, Valves) MUST be enclosed in a single `<g>` element with explicit asset identification:

```xml
<g id="asset-{ASSET_ID}" 
   class="equipment {ASSET_TYPE}" 
   data-asset-type="{ASSET_TYPE}">
  <!-- Visual shapes, internal paths, and label tags -->
</g>
```

### Identifier Constraints:
* `id`: MUST start with `asset-` followed verbatim by the original SCADA tag (e.g., `asset-10GDJ35AP001`, `asset-1ST-PASS`, `asset-PRESSURE-EXCHANGER`).
* `class`: MUST include `equipment` plus the standardized asset class name matching `docs/standards/equipment-catalog.md` (`pump`, `ro-rack`, `erd-exchanger`, `valve`).

---

## 3. SCADA Telemetry Data Anchors (`data-tag`)

Dynamic operational data text nodes MUST use native `<text>` elements carrying the `data-tag` attribute bound to the backend SCADA tag identifier:

```xml
<g id="asset-{SCADA_TAG}" class="equipment telemetry-anchor">
  <!-- Telemetry Value Display Anchor -->
  <text id="tag-{SCADA_TAG}" 
        data-tag="{SCADA_TAG}" 
        data-unit="{UNIT}" 
        class="telemetry-value">
    {LIVE_VALUE} {UNIT}
  </text>
</g>
```

### Telemetry Text Constraints:
1. **Native Text Nodes Only:** Render as true `<text>` elements—NEVER convert to path glyphs (`<path>`) or `<use>` references.
2. **Direct Tag Mapping:** `data-tag` MUST verbatim match the primary SCADA tag name from the input diagram (e.g., `data-tag="10GDJ35CP006UIR"`).
3. **Font Size:** Telemetry value text MUST use a font size between 10px and 12px for clear readability.

---

## 4. CSS Status Classes (Phase 2 Binding Contract)

Dynamic equipment state changes in Phase 2 are driven by toggling predefined CSS status classes on the asset `<g>` container:

```css
/* Equipment State Classes */
.equipment.status-running .equipment-body {
  fill: #2ec4b6; /* Green running state */
}

.equipment.status-stopped .equipment-body {
  fill: #8d99ae; /* Neutral gray stopped state */
}

.equipment.status-alarm .equipment-body {
  fill: #e63946; /* Red alarm state */
  animation: blink 1s infinite;
}
```

---

## 5. Fallback Rule for Unrecognized Symbols

If an input diagram contains an asset outside the core V1 equipment catalog:
1. Render a generic labeled box (`<rect class="equipment generic-asset">`).
2. Assign `id="asset-GENERIC-{INDEX}"`.
3. Add attribute `data-unrecognized-symbol="true"` for human review.