# Equipment & Symbol Catalog Standard (Version 1)

This document establishes the canonical asset catalog, SVG visual shapes, and tag naming rules for Version 1 of the water treatment process visualization pipeline. 

For Phase 1, the catalog is strictly scoped to **6 to 7 primary equipment assets** per subsystem/rack screen..

---

## 1. Core Asset Inventory (V1 Scope)

| Asset Class Name | Tag Code Prefix | Visual Representation & SVG Shapes |
| :--- | :--- | :--- | :--- |
| `pump` | `10GDJ35AP` | Circle (`<circle>`) with tangential discharge line and **internal flow direction triangle** (`<path d="M...Z">`). Green fill when running (`#2ec4b6` / `.status-running`) |
| `ro-rack` | `1ST PASS`, `2ND PASS` | Rectangular vessel body (`<rect>`) with internal stage geometry (`<path d="...">`). Geometry internal variants include **3 flow triangles** (1st Pass) or **diagonal stage divider lines connecting opposite corners** (2nd Pass). |
| `pressure-exchanger` | `PRESSURE EXCHANGER` | Vertical cylindrical vessel (`<rect rx="12">`) with **two internal curved opposing flow arrows** (`<path d="...">` with `<marker>` arrowheads) representing isobaric energy exchange. |
| `valve` / `control-valve` | `10GDJ35AA` | Opposing bowtie triangles (`<path d="M...Z">`) with top actuator stem |
| `telemetry-anchor` | `10GDJ35CF`, `10GDJ35CP`, `10GDJ35CQ` | Rectangular telemetry display box containing live SCADA value and unit. |
| `temperature-transmitter` | `10GDJ35CT` | Small horizontal ribbed cylinder (`<rect>` or `<path>`) attached to pipe with adjacent value box (`DEGC`). |
| `pipe` | N/A | Process connection line represented by a continuous SVG path (<path>) or straight line segment (<line>). May include directional flow markers, elbows, tees, and branch connections. Colour is process-dependent (e.g. feed water, permeate, brine, CIP).|

---