# Project Overview

## Project Name

AI-Generated Real-Time Plant Visualization & Digital Twin for Water Treatment Facilities

---

## Background

The goal of this project is to automatically transform existing water treatment plant diagrams (specifically subsystem and operational SCADA displays like Reverse Osmosis racks) into structured, interactive SVG visualizations connected to live operational data.

Currently, plant operational data exists and is accessible via SCADA systems and internal applications. However, data is primarily presented through tables, lists, and charts, lacking a process-oriented visual layer.

This project bridges that gap by creating an AI-driven workflow capable of generating visual process representations directly from existing subsystem diagrams.

---

## Vision

Transform plant subsystem diagrams into live process visualizations that serve as operational Digital Twin representations.

---

## Main Objectives

1. Automatically interpret existing plant subsystem diagrams (PFD / P&ID views).
2. Identify process equipment, connections, and flow paths (focusing on key 6–7 primary assets per subsystem display).
3. Generate standardized, editable, and machine-readable SVG files.
4. Prepare SVG assets for integration with operational data.
5. Connect SVG elements directly to SCADA tags (using original diagram tags and secondary backend identifiers).
6. Display live equipment states, telemetry measurements, and alarms.
7. Enable process-oriented Digital Twin visualization capabilities.

---

## Project Scope

### Input Formats

- Subsystem PDF diagrams (vector & raster)
- SCADA screen exports / image files
- Process flow schematics (e.g., RO Racks, Filter Units)

### Output

- Structured SVG (`viewBox="0 0 1400 940"`)
- Machine-readable asset identifiers
- Data-tag embedded telemetry placeholders (`data-tag="..."`).
- Interactive process visualization

---

# Phase 1: Diagram to Structured SVG

## Goal

Convert plant subsystem diagrams into standardized, validated SVG files.

## Key Activities

- Define core equipment catalog (scope of 6–7 priority assets per module)
- Define SVG standards and canvas rules (`docs/standards/svg-conventions.md`)
- Define naming and tag attribute conventions
- Adapt visual symbology from input source diagrams
- Detect equipment and process connections
- Generate structured SVGXML
- Validate output quality via automated schema scripts (`svg_validator.py`)

## Deliverable

Subsystem Diagram → Structured SVG

---

# Phase 2: Real-Time Visualization & Digital Twin

## Goal

Transform generated SVGs into real-time operational visualizations connected to telemetry.

## Key Activities

- Map SVG data anchors directly to SCADA tags (primary tag & secondary alias)
- Connect SVG elements to live SCADA feeds
- Display live telemetry values and units
- Display equipment status styling (`.status-running`, `.status-stopped`, `.status-alarm`)
- Add user interactions (hovering, trend popups, ECharts telemetry overlays)
- Establish operational 2D Digital Twin view

## Deliverable

Structured SVG → Live Process Visualization → Operational Digital Twin

---

# Research Areas

## 1. Existing Plant Standards

- Review real plant diagrams and SCADA displays (e.g., Acciona SWRO RO Racks)
- Review engineering and drawing conventions
- Identify diagram types (vector PDFs vs. raster image scans)

## 2. SCADA Research

- Review existing SCADA screens
- Identify commonly used equipment symbols and visual states
- Understand telemetry display conventions (pressure `bar`, flow `m³/h`, conductivity `µS/cm`)
- Understand alarm and status representations

## 3. Asset & Tag Model Definition

- Equipment classification (6–7 core asset types)
- Tag mapping strategy (direct attachment to backend tags)
- Telemetry attribute structure (`data-tag`, `data-unit`)

## 4. SVG Standards

- Layout rules and viewports
- Symbol catalog adaptation
- Label and telemetry positioning
- Machine-readable XML structure

---

# Key Principle

This project is not intended to replace existing SCADA systems, PLCs, or historians.

The goal is to automatically generate the process-oriented visualization layer that currently requires significant manual engineering effort, making plant diagrams easier to connect with operational data and Digital Twin applications.

---

# Expected End State

A user provides a subsystem plant diagram, and the system automatically generates an interactive SVG-based process visualization that connects to live SCADA tags and serves as an operational 2D Digital Twin.

---

# Reference Materials

A reference `SKILL.md` from Scott Duncan's Chemical Manufacturing Skills project is included for inspiration.

This document should be used as a reference for:

- Skill structure
- Workflow design
- Validation rules
- Documentation organization
- Reference file structure
- Quality control processes

The chemical engineering conventions, ISA standards, instrumentation rules, and PFD-specific requirements are not directly applicable to this project unless explicitly adopted.

The objective is to adapt the underlying methodology and architecture to the water treatment domain.

---

# Duncan's Repository Layout

```text
.
├── .claude-plugin/
│   └── marketplace.json         plugin catalog — one entry per skill
├── skills/
│   └── pfd-generator/
│       ├── SKILL.md              instructions Claude loads
│       ├── references/           detail loaded on demand, not up front
│       ├── scripts/              deterministic code the skill calls
│       └── examples/            sample output
└── templates/
    └── skill-template/          scaffold for a new skill
