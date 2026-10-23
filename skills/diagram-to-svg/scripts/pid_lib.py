"""
pid_lib - primitives for hand-authored P&ID SVGs.

Example Usage:
    from pid_lib import PID
    d = PID(1400, 940)
    d.title("SP1 RO RACK6", "Subsystem Display | SWRO Desalination")
    d.ro_rack(400, 300, 300, 120, tag="1ST PASS", pass_type="1st")
    d.pump(150, 300, tag="10GDJ35AP001")
    d.telemetry_anchor(250, 280, tag="10GDJ35CP006UIR", value="73.4", unit="bar")
    d.save("out.svg")
"""

# Standard color palette
BLUE = "#1d4e89"      # Raw water / High-pressure feed
CYAN = "#2ec4b6"      # Permeate / Treated water (Running State)
RUST = "#a34a28"      # Brine / Concentrate rejection
GREEN = "#3f7a4d"     # Chemical dosing
SIG = "#50565f"       # Instrument signal / DCS
EQ = "#343a46"        # Equipment body contours
INK = "#111418"       # Primary text
SUB = "#5a6472"       # Subtitles & secondary tags
HAIR = "#b8bec7"      # Border lines
SHELL = "#f7f8fa"     # Vessel hull fill
RED = "#e63946"       # Alarm state / Notice stamps
FONTS = "'Helvetica Neue', Helvetica, Arial, sans-serif"

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

class PID:
    BLUE, CYAN, RUST, GREEN, SIG, EQ = BLUE, CYAN, RUST, GREEN, SIG, EQ
    INK, SUB, SHELL, RED = INK, SUB, SHELL, RED

    def __init__(self, w=1400, h=940, border=True):
        self.w = w
        self.h = h
        self.o = []

        self.o.append(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'font-family="{FONTS}" class="water-treatment-subsystem">'
        )

        # 2. Defs, Markers, and CSS State Animation
        self.o.append('<defs>')
        for name, col in (("aBlue", BLUE), ("aRust", RUST), ("aSig", SIG), ("aCyan", CYAN), ("aGreen", GREEN)):
            self.o.append(
                f'<marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" '
                f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M 0,0 L 10,5 L 0,10 z" fill="{col}"/></marker>'
            )
        # Embedded CSS rules for Phase 2 dynamic styling & status blinking
        self.o.append(
            '<style>\n'
            '  .equipment-body { fill: #ffffff; stroke: #343a46; stroke-width: 1.8px; }\n'
            '  .process-pipe { fill: none; stroke-linecap: round; stroke-linejoin: round; }\n'
            '  .label-tag { font-size: 11px; font-weight: bold; fill: #343a46; text-anchor: middle; }\n'
            '  .telemetry-value { font-size: 11px; font-weight: bold; fill: #111418; font-family: monospace; }\n'
            '  .telemetry-box { fill: #ffffff; stroke: #b8bec7; stroke-width: 1px; rx: 3px; }\n'
            '  .equipment.status-running .status-indicator { fill: #2ec4b6; }\n'
            '  .equipment.status-stopped .status-indicator { fill: #8d99ae; }\n'
            '  .equipment.status-alarm .status-indicator { fill: #e63946; animation: blink 1s infinite; }\n'
            '  @keyframes blink { 50% { opacity: 0.4; } }\n'
            '</style>'
        )
        self.o.append('</defs>')
        self.o.append(f'<rect width="{w}" height="{h}" fill="#ffffff"/>')
        if border:
            self.o.append(f'<rect x="15" y="15" width="{w-30}" height="{h-30}" '
                          f'fill="none" stroke="{HAIR}" stroke-width="1"/>')

    def add(self, s):
        self.o.append(s)

    def txt(self, x, y, s, size=10, fill=INK, weight="normal", anchor="start", ls=0):
        extra = f' letter-spacing="{ls}"' if ls else ""
        self.add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
                 f'fill="{fill}" text-anchor="{anchor}"{extra}>{esc(s)}</text>')

    def title(self, main, subtitle=None, stamp=True):
            self.txt(45, 60, main, size=21, weight="bold")
            if subtitle:
                self.txt(45, 82, subtitle, size=11.5, fill=SUB)
            if stamp:
                x = self.w - 222
                self.add(f'<rect x="{x}" y="42" width="177" height="24" fill="none" '
                         f'stroke="{RED}" stroke-width="1.4"/>')
                self.txt(x + 88, 59, "ACCIONA DIGITAL TWIN", size=11, weight="bold",
                         fill=RED, anchor="middle", ls=0.4)

    # ---------------------------------------------------------------- Piping
    def pipe(self, d, color=BLUE, arrow=False, width=2.4):
        key = {BLUE: "aBlue", RUST: "aRust", CYAN: "aCyan", GREEN: "aGreen"}.get(color, "aBlue")
        m = f' marker-end="url(#{key})"' if arrow else ''
        self.add(f'<path d="{d}" class="process-pipe" stroke="{color}" stroke-width="{width}"{m}/>')

    def sig(self, d, arrow=True):
        """Instrument / DCS signal line (dashed). Arrow points into receiving device."""
        m = ' marker-end="url(#aSig)"' if arrow else ''
        self.add(f'<path d="{d}" class="process-pipe signal-dcs" stroke="{SIG}" stroke-width="1.35" '
                 f'stroke-dasharray="7,5.5"{m}/>')

    def lead(self, x1, y1, x2, y2):
        """Thin solid impulse/sensing connection from pipe/vessel wall to sensor or telemetry box."""
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                 f'stroke="{EQ}" stroke-width="1.2"/>')

    def line_jump(self, x, y, color=BLUE, r=14):
        """Semicircular hop/bridge across intersecting pipe path at (x, y)."""
        self.add(f'<path d="M {x-r},{y} A {r} {r} 0 0 1 {x+r},{y}" fill="none" '
                 f'stroke="{color}" stroke-width="2.4"/>')

    # ---------------------------------------------------------------- Equipment Catalog (V1)

    # 1. Pump / High-Pressure Pump (pump)
    def pump(self, cx, cy, tag, status="running", r=20):
        self.add(f'<g id="asset-{tag}" class="equipment pump status-{status}" data-asset-type="pump">')
        self.add(f'  <circle cx="{cx}" cy="{cy}" r="{r}" class="equipment-body status-indicator" />')
        # Internal flow direction triangle
        self.add(f'  <path d="M {cx-12},{cy+10} L {cx-12},{cy-10} L {cx+8},{cy} Z" fill="{EQ}" />')
        # Tangential discharge nozzle
        self.add(f'  <line x1="{cx}" y1="{cy-r}" x2="{cx}" y2="{cy-r-12}" stroke="{EQ}" stroke-width="2" />')
        self.txt(cx, cy + r + 18, tag, size=11, weight="bold", anchor="middle")
        self.add('</g>')

    # 2. Reverse Osmosis Membrane Rack (ro-rack)
    def ro_rack(self, x, y, w, h, tag, pass_type="1st"):
        self.add(f'<g id="asset-{tag}" class="equipment ro-rack" data-asset-type="ro-rack">')
        self.add(f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{SHELL}" stroke="{EQ}" stroke-width="2"/>')
        
        # Internal pass geometry
        if pass_type == "1st":
            # 3 internal flow triangles
            for dx in (w*0.25, w*0.5, w*0.75):
                self.add(f'  <path d="M {x+dx-10},{y+h/2+10} L {x+dx-10},{y+h/2-10} L {x+dx+10},{y+h/2} Z" fill="{SUB}" opacity="0.5"/>')
        else:
            # Diagonal stage divider lines
            self.add(f'  <line x1="{x}" y1="{y}" x2="{x+w}" y2="{y+h}" stroke="{SUB}" stroke-width="1.5" stroke-dasharray="4,4"/>')

        self.txt(x + w/2, y + h/2 + 4, tag, size=12, weight="bold", anchor="middle")
        self.add('</g>')

    # 3. Isobaric Pressure Exchanger (erd-exchanger)
    def erd_exchanger(self, x, y, w, h, tag="PRESSURE EXCHANGER"):
        self.add(f'<g id="asset-{tag.replace(" ", "-")}" class="equipment erd-exchanger" data-asset-type="erd-exchanger">')
        self.add(f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{SHELL}" stroke="{EQ}" stroke-width="2"/>')
        # Two internal curved opposing flow arrows
        self.add(f'  <path d="M {x+w*0.3},{y+h*0.3} Q {x+w*0.7},{y+h*0.3} {x+w*0.7},{y+h*0.7}" fill="none" stroke="{EQ}" stroke-width="2" marker-end="url(#aBlue)"/>')
        self.add(f'  <path d="M {x+w*0.7},{y+h*0.7} Q {x+w*0.3},{y+h*0.7} {x+w*0.3},{y+h*0.3}" fill="none" stroke="{EQ}" stroke-width="2" marker-end="url(#aRust)"/>')
        self.txt(x + w/2, y + h + 18, tag, size=10.5, weight="bold", anchor="middle")
        self.add('</g>')

    # 4. Inline Static Mixer (static-mixer)
    def static_mixer(self, x, y, w=50, h=26, tag="STATIC MIXER"):
        self.add(f'<g id="asset-{tag.replace(" ", "-")}" class="equipment static-mixer" data-asset-type="inline-process">')
        self.add(f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="#ffffff" stroke="{EQ}" stroke-width="1.8"/>')
        # Criss-cross internal baffle lines
        self.add(f'  <path d="M {x+5},{y+5} L {x+w-5},{y+h-5} M {x+5},{y+h-5} L {x+w-5},{y+5}" stroke="{SUB}" stroke-width="1.2"/>')
        self.txt(x + w/2, y + h + 15, tag, size=9, weight="bold", anchor="middle")
        self.add('</g>')

    # 5. Control / Motorized Valve (valve)
    def valve(self, cx, cy, tag, actuator=True):
        self.add(f'<g id="asset-{tag}" class="equipment valve" data-asset-type="valve">')
        # Bowtie shapes
        self.add(f'  <path d="M {cx-14},{cy-10} L {cx-14},{cy+10} L {cx},{cy} Z" fill="#ffffff" stroke="{EQ}" stroke-width="1.5"/>')
        self.add(f'  <path d="M {cx+14},{cy-10} L {cx+14},{cy+10} L {cx},{cy} Z" fill="#ffffff" stroke="{EQ}" stroke-width="1.5"/>')
        if actuator:
            self.add(f'  <line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy-16}" stroke="{EQ}" stroke-width="1.4"/>')
            self.add(f'  <rect x="{cx-10}" y="{cy-24}" width="20" height="8" rx="2" fill="#ffffff" stroke="{EQ}" stroke-width="1.4"/>')
        self.txt(cx, cy + 22, tag, size=9.5, weight="bold", anchor="middle")
        self.add('</g>')

    # 6. SCADA Telemetry Anchor (telemetry-anchor)
    def telemetry_anchor(self, x, y, tag, value, unit, w=100, h=24):
        self.add(f'<g id="asset-{tag}" class="equipment telemetry-anchor">')
        self.add(f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" class="telemetry-box"/>')
        self.add(
            f'  <text x="{x + w/2}" y="{y + 16}" id="tag-{tag}" data-tag="{tag}" '
            f'data-unit="{unit}" class="telemetry-value" text-anchor="middle">'
            f'{esc(value)} {esc(unit)}</text>'
        )
        self.add('</g>')

    # Boundary Container / Stream Collector
    def boundary_node(self, x, y, w, h, label):
        self.add(f'<g class="boundary-container">')
        self.add(f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{SHELL}" stroke="{HAIR}" stroke-width="1.2" stroke-dasharray="4,3"/>')
        self.txt(x + w/2, y + h/2 + 4, label, size=10, fill=SUB, weight="bold", anchor="middle")
        self.add('</g>')

    # ---------------------------------------------------------------- Output
    def save(self, path):
        out = "\n".join(self.o + ["</svg>"])
        with open(path, "w", encoding="utf-8") as f:
            f.write(out)
        return path