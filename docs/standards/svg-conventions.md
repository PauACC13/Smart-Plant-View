# Master SVG Schema & Convention Specification

This document defines the mandatory SVG XML structure, naming conventions, metadata placeholders, and CSS styling classes for generated water treatment plant visualizations. 

All Phase 1 SVG generation pipelines must strictly output XML conforming to this specification. Phase 2 data-binding logic relies on these exact attributes to bind real-time SCADA telemetry[cite: 1, 3].

---

## 1. Canvas & ViewBox Rules

1. **Standard Resolution:** The primary canvas coordinate space is fixed at `1400 × 940` pixels.
2. **Scalability:** The SVG element MUST include a responsive `viewBox` attribute and NO hardcoded pixel width/height attributes on the top `<svg>` tag:
   ```xml
   <svg xmlns="[http://www.w3.org/2000/svg](http://www.w3.org/2000/svg)" 
        viewBox="0 0 1400 940" 
        class="water-treatment-pfd">what 