# Master SVG Schema & Convention Specification

This document defines the mandatory SVG XML structure, naming conventions, metadata placeholders, and CSS styling classes for generated water treatment plant visualizations. 

All Phase 1 SVG generation pipelines must strictly output XML conforming to this specification. Phase 2 data-binding logic relies on these exact attributes to bind real-time SCADA telemetry[cite: 1, 3].

---

## 1. Canvas & ViewBox Rules

1. **Standard Resolution:** The primary canvas coordinate space is fixed at `1400 × 940` pixels.
2. Fluid Responsiveness: The root <svg> tag MUST include a responsive viewBox attribute and MUST NOT hardcode pixel width or height attributes:
   <svg xmlns="http://www.w3.org/2000/svg" 
        viewBox="0 0 1400 940" 
        class="water-treatment-subsystem">
3. Mandatory Layer Render Order: To prevent visual overlap and ensure text readability, SVG nodes MUST be emitted in the following z-index sequence:
   1. Canvas defs and CSS <style> blocks (<defs>, <style>)
   2. Boundary nodes and background collector fills (.boundary-container)
   3. Process pipe paths (<path class="process-pipe ...">)
   4. Core equipment groups (<g class="equipment ...">)
   5. Opaque white-backed instrument elements and valves
   6. Telemetry text anchors (<text data-tag="...">)

---

## 2. Asset Identification & Grouping (<g>)

Every physical equipment item (Pumps, RO Vessels, Pressure Exchangers, Valves) MUST be enclosed in a single <g> element with explicit asset identification:

<g id="asset-{ASSET_ID}" 
   class="equipment {ASSET_TYPEE" 
   data-asset-type="{ASSET_TYPE}">
  <!-- Visual paths, shapes, and label tags -->
</g>

### Mandatory Identifier Rules:
- id: MUST start with asset- followed by the original SCADA asset tag (e.g., asset-10GDJ35AP001, asset-1ST-PASS, asset-PRESSURE-EXCHANGER).
- class: MUST include equipment plus the standardized asset class name matching docs/standards/equipment-catalog.md (e.g., pump, ro-rack, pressure-exchanger valve).

---

## 3. SCADA Telemetry Data Anchors (data-tag)

Dynamic operational data text nodes MUST use native <text> elements carrying the data-tag attribute bound to the backend SCADA tag identifier:

<g id="asset-{SCADA_TAG}" class="equipment telemetry-anchor">
  <!-- Telemetry Value Display Anchor -->
  <text id="tag-{SCADA_TAG}" 
        data-tag="{SCADA_TAG}" 
        data-unit="{UNIT}" 
        class="telemetry-value">
    {LIVE_VALUE} {UNIT}
  </text>
</g>

### Telemetry Text Node Rules:
1. Native Text Nodes Only: All telemetry values MUST be rendered as true <text> nodes, NEVER converted to graphics paths (<path>) or glyph references (<use>).
2. Direct Tag Mapping: The data-tag attribute MUST verbatim match the primary SCADA tag name from the input diagram (e.g., data-tag="10GDJ35CP006UIR").
3. Font Sizing: Telemetry value text MUST use a font size between 10px and 12px for clear readability on standard displays.

---

## 4. Status Styling Classes (Phase 2 Binding Contract)

Dynamic equipment state changes in Phase 2 are driven by toggling predefined CSS status classes on the asset <g> container:

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