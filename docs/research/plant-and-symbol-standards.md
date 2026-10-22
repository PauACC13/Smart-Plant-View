# Research Notes: Plant Diagrams & Symbol Standards

**Author:** Pau  
**Project:** Bachelor's Thesis (TFG) - Acciona Water Treatment Visualization    

---

## 1. Input Diagram Formats & Classification

Based on industrial OT standards and typical water treatment plant documentation, the ingestion pipeline will target two primary diagram types:

### A. Process Flow Diagrams (PFD)
* **Scope:** High-level operational view showing major process units (e.g., Raw Water Intake, Pre-treatment, RO Membrane Racks, Permeate Storage) and main fluid streams.
* **Primary Use Case:** Top-level executive dashboards and plant overview screens.
* **Ingestion Characteristics:** Clean layouts with low line density; fewer individual instrument balloons.

### B. Piping & Instrumentation Diagrams (P&ID)
* **Scope:** Detailed engineering schematics showing every physical vessel, pump, valve, and instrument balloon tied to a SCADA tag.
* **Primary Use Case:** Sub-system diagnostic views and detailed real-time SCADA binding.
* **Ingestion Characteristics:** High line density, nested control loops, and explicit instrument tag codes.

### Expected Source Formats:
1. **Vector PDFs / AutoCAD CAD Exports (~80%):** Text layers are embedded as native vector fonts.
2. **Scanned Image PDFs / Raster Images (~20%):** Scanned physical site drawings requiring full computer vision line and symbol extraction.

---

## 2. Symbology Baseline & ISA-5.1 Comparison

Industrial water treatment facilities rely heavily on **ISA-5.1 (Instrumentation Symbols and Identification)**, adapted for specific water process units:

### Instrument Balloon Conventions (ISA-5.1)
* **Plain Circle:** Field-mounted instrument (e.g., local pressure gauge).
* **Circle Inside a Square:** Shared display / DCS / SCADA instrument (the primary target for Phase 2 dynamic data binding).

The company has not an specific standard. We will set the simbology based on the input's diagram.

---
