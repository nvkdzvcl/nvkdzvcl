"""Generate assets/christmas.svg — animated Christmas banner (tree, Santa's sleigh, reindeer, snow).

Usage: python scripts/build_christmas_banner.py .
"""
import math
import random
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
W, H = 1200, 360
SANS = 'Segoe UI,Ubuntu,Helvetica,Arial,sans-serif'
rnd = random.Random(2512)
out = []
add = out.append


def star_points(cx, cy, r1, r2, n=5):
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        a = -math.pi / 2 + i * math.pi / n
        pts.append(f'{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}')
    return ' '.join(pts)


add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">')
add('<title id="t">Merry Christmas from Catouis</title>')
add('<desc id="d">Snow falls on a night sky while Santa’s sleigh, pulled by reindeer, flies past the moon. '
    'A glowing Christmas tree, gifts, a pixel cat in a Santa hat and a waving snowman stand in the snow.</desc>')
add('''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#0b0b17"/><stop offset=".55" stop-color="#1e1e2e"/><stop offset="1" stop-color="#313244"/></linearGradient>
<radialGradient id="moonglow"><stop offset=".45" stop-color="#f9e2af" stop-opacity=".35"/><stop offset="1" stop-color="#f9e2af" stop-opacity="0"/></radialGradient>
<radialGradient id="treeglow"><stop stop-color="#f9e2af" stop-opacity=".22"/><stop offset="1" stop-color="#f9e2af" stop-opacity="0"/></radialGradient>
<linearGradient id="xmas" x1="0" x2="1" spreadMethod="reflect">
  <stop offset="0" stop-color="#f38ba8"/><stop offset=".3" stop-color="#f9e2af"/><stop offset=".6" stop-color="#a6e3a1"/><stop offset="1" stop-color="#f38ba8"/>
  <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="5s" repeatCount="indefinite"/>
</linearGradient>
<linearGradient id="tree" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#40a02b"/><stop offset="1" stop-color="#1f6f3a"/></linearGradient>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="softglow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="frame"><rect width="1200" height="360" rx="22"/></clipPath>
</defs>
<style>@media (prefers-reduced-motion: reduce){*{animation:none!important}}</style>''')
add('<g clip-path="url(#frame)">')
add(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')

# twinkling stars
for _ in range(45):
    x, y, r = rnd.uniform(10, W - 10), rnd.uniform(50, 200), rnd.uniform(.6, 1.6)
    d = rnd.uniform(1.5, 4)
    add(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#cdd6f4"><animate attributeName="opacity" values="1;.15;1" dur="{d:.1f}s" begin="-{rnd.uniform(0, d):.1f}s" repeatCount="indefinite"/></circle>')

# moon
add('<circle cx="1085" cy="95" r="95" fill="url(#moonglow)"/>')
add('<circle cx="1085" cy="95" r="42" fill="#f9e2af"/><circle cx="1070" cy="85" r="7" fill="#f2cd8f" opacity=".7"/>'
    '<circle cx="1098" cy="108" r="5" fill="#f2cd8f" opacity=".7"/><circle cx="1096" cy="78" r="3.5" fill="#f2cd8f" opacity=".7"/>')

# string lights across the top
wire = 'M0 14' + ''.join(f' Q{x0 + 100} 50 {x0 + 200} 14' for x0 in range(0, W, 200))
add(f'<path d="{wire}" fill="none" stroke="#45475a" stroke-width="2"/>')
bulb_colors = ['#f38ba8', '#f9e2af', '#a6e3a1', '#89b4fa', '#cba6f7', '#fab387']
k = 0
for x0 in range(0, W, 200):
    for t in (.17, .38, .62, .83):
        x, y = x0 + 200 * t, 14 + 72 * t * (1 - t)
        c = bulb_colors[k % len(bulb_colors)]
        add(f'<g filter="url(#glow)"><rect x="{x - 2.5:.1f}" y="{y - 2:.1f}" width="5" height="5" fill="#585b70"/>'
            f'<ellipse cx="{x:.1f}" cy="{y + 9:.1f}" rx="4.5" ry="7" fill="{c}">'
            f'<animate attributeName="opacity" values="1;.25;1" dur="1.6s" begin="{(k % 3) * .53:.2f}s" repeatCount="indefinite"/></ellipse></g>')
        k += 1

# ---------- Santa's sleigh + reindeer (flies across) ----------
def reindeer(x, red_nose, phase):
    legs = []
    for lx, delay in ((-14, 0), (-8, .15), (10, .3), (16, .45)):
        legs.append(f'<line x1="{lx}" y1="6" x2="{lx}" y2="22" stroke="#7a4f2e" stroke-width="3.5" stroke-linecap="round">'
                    f'<animateTransform attributeName="transform" type="rotate" values="-28 {lx} 6;28 {lx} 6;-28 {lx} 6" dur=".6s" begin="{phase + delay:.2f}s" repeatCount="indefinite"/></line>')
    nose_color = '#f38ba8' if red_nose else '#3a2a20'
    nose = (f'<circle cx="42" cy="-19" r="{4 if red_nose else 2.5}" fill="{nose_color}"' +
            (' filter="url(#glow)"><animate attributeName="opacity" values="1;.45;1" dur=".9s" repeatCount="indefinite"/></circle>' if red_nose else '/>'))
    return (f'<g transform="translate({x} 0)">{"".join(legs)}'
            '<ellipse cx="0" cy="0" rx="23" ry="11" fill="#a0683f"/>'
            '<ellipse cx="2" cy="4" rx="15" ry="5" fill="#d9b38c" opacity=".55"/>'
            '<ellipse cx="-23" cy="-5" rx="5" ry="4" fill="#f5e0c8"/>'
            '<path d="M14 -6 L24 -22 L32 -16 L22 2 Z" fill="#a0683f"/>'
            '<ellipse cx="33" cy="-20" rx="10" ry="6.5" fill="#a0683f"/>'
            '<ellipse cx="25" cy="-26" rx="4" ry="2" fill="#7a4f2e" transform="rotate(-30 25 -26)"/>'
            '<path d="M28 -25 l-5 -12 M25.5 -31 l-7 -3 M32 -25 l3 -13 M33.5 -32 l7 -3" stroke="#e6c9a8" stroke-width="2.5" stroke-linecap="round" fill="none"/>'
            '<circle cx="35" cy="-22" r="1.6" fill="#11111b"/>'
            f'{nose}'
            '<path d="M-10 -9 Q0 -4 14 -6" stroke="#f38ba8" stroke-width="3" fill="none"/>'
            '<circle cx="2" cy="-6" r="2.4" fill="#f9e2af"/>'
            '</g>')


sleigh = (
    # sparkle trail
    ''.join(f'<circle cx="{-20 - i * 18}" cy="{-4 + (i % 2) * 8}" r="{2.6 - i * .35:.1f}" fill="#f9e2af" filter="url(#glow)">'
            f'<animate attributeName="opacity" values="1;0;1" dur=".8s" begin="{i * .13:.2f}s" repeatCount="indefinite"/></circle>' for i in range(6)) +
    # gift sack
    '<path d="M2 -26 Q-6 -52 12 -58 Q30 -52 22 -26 Z" fill="#8b5e3c"/><path d="M8 -55 l4 -6 l4 6" stroke="#f9e2af" stroke-width="2" fill="none"/>'
    '<rect x="16" y="-44" width="12" height="12" fill="#89b4fa"/><rect x="21" y="-44" width="2.5" height="12" fill="#f9e2af"/>'
    # Santa
    '<circle cx="44" cy="-34" r="15" fill="#e64553"/><rect x="31" y="-31" width="27" height="5" fill="#11111b"/><rect x="41" y="-32" width="7" height="7" fill="#f9e2af"/>'
    '<circle cx="47" cy="-55" r="9" fill="#f5d0b5"/>'
    '<path d="M38 -52 Q47 -36 56 -52 Q52 -45 47 -46 Q42 -45 38 -52 Z" fill="#ffffff"/>'
    '<circle cx="50" cy="-57" r="1.4" fill="#11111b"/><circle cx="54" cy="-53" r="2" fill="#f2a7a7"/>'
    '<path d="M38 -59 Q44 -78 30 -80 Q48 -84 56 -60 Z" fill="#e64553"/><rect x="37" y="-62" width="20" height="5" rx="2.5" fill="#ffffff"/>'
    '<circle cx="30" cy="-80" r="4" fill="#ffffff"/>'
    '<g><line x1="54" y1="-38" x2="66" y2="-54" stroke="#e64553" stroke-width="6" stroke-linecap="round"/><circle cx="67" cy="-56" r="4.5" fill="#40a02b"/>'
    '<animateTransform attributeName="transform" type="rotate" values="0 54 -38;-25 54 -38;0 54 -38" dur=".8s" repeatCount="indefinite"/></g>'
    # sleigh body + runner
    '<path d="M-6 -30 Q-12 -30 -10 -20 L-2 0 H62 Q78 0 80 -16 L82 -28 H72 L70 -18 Q68 -12 60 -12 H6 L4 -30 Z" fill="#d20f39" stroke="#f9e2af" stroke-width="2.5" stroke-linejoin="round"/>'
    '<path d="M6 -6 H58" stroke="#f9e2af" stroke-width="1.5" stroke-dasharray="3 4"/>'
    '<path d="M6 0 v10 M56 0 v10" stroke="#f9e2af" stroke-width="2.5"/>'
    '<path d="M-14 12 H72 Q90 12 90 -2" fill="none" stroke="#f9e2af" stroke-width="3.5" stroke-linecap="round"/>'
    # harness
    '<path d="M80 -20 Q120 -6 150 -8 M150 -8 Q190 -4 216 -8" fill="none" stroke="#f9e2af" stroke-width="1.8"/>'
    + reindeer(150, False, 0) + reindeer(222, True, .3)
)
add('<g>')
add(f'<g><g>{sleigh}<animateTransform attributeName="transform" type="translate" values="0 0;0 -7;0 0" dur="1.2s" repeatCount="indefinite"/></g>'
    '<animateMotion dur="14s" repeatCount="indefinite" path="M-320 150 C 150 70, 420 170, 760 105 S 1250 90, 1560 60"/></g>')
add('</g>')

# ---------- snowy ground ----------
add('<path d="M0 300 Q150 270 320 292 T640 288 T960 284 T1200 290 V360 H0 Z" fill="#bac2de" opacity=".55"/>')
add('<path d="M0 318 Q200 296 420 314 T820 308 T1200 312 V360 H0 Z" fill="#eff1f5"/>')

# ---------- Christmas tree ----------
TX = 150
add(f'<ellipse cx="{TX}" cy="200" rx="150" ry="140" fill="url(#treeglow)"/>')
add(f'<rect x="{TX - 12}" y="285" width="24" height="30" fill="#7a4f2e"/>')
tiers = [(110, 175, 70), (150, 225, 92), (192, 285, 116)]  # top_y, bottom_y, half_width
for top, bottom, hw in tiers:
    step = hw / 3  # six scallops along the bottom edge, drawn left → right
    scallop = ''.join(f' Q{TX - hw + (i + .5) * step:.0f} {bottom + 9} {TX - hw + (i + 1) * step:.0f} {bottom}' for i in range(6))
    add(f'<path d="M{TX} {top - 45} L{TX - hw} {bottom}{scallop} Z" fill="url(#tree)"/>')
# tinsel garlands
for (y1, x1), (y2, x2) in [((118, TX - 38), (160, TX + 52)), ((170, TX - 62), (215, TX + 74)), ((222, TX - 86), (268, TX + 96))]:
    add(f'<path d="M{x1} {y1} Q{TX} {(y1 + y2) / 2 + 26:.0f} {x2} {y2}" fill="none" stroke="#f9e2af" stroke-width="3" stroke-dasharray="6 5" stroke-linecap="round">'
        '<animate attributeName="stroke-dashoffset" values="0;22" dur="1s" repeatCount="indefinite"/></path>')
# ornaments
orn = [(TX - 20, 125), (TX + 25, 140), (TX - 45, 182), (TX + 5, 195), (TX + 55, 200), (TX - 70, 240),
       (TX - 25, 255), (TX + 30, 245), (TX + 80, 262), (TX - 5, 160), (TX - 90, 275), (TX + 60, 280)]
for i, (x, y) in enumerate(orn):
    c = bulb_colors[i % len(bulb_colors)]
    add(f'<circle cx="{x}" cy="{y}" r="6" fill="{c}" filter="url(#glow)"><animate attributeName="opacity" values="1;.35;1" dur="{1.2 + (i % 4) * .35:.2f}s" begin="{i * .17:.2f}s" repeatCount="indefinite"/></circle>'
        f'<circle cx="{x - 2}" cy="{y - 2}" r="1.6" fill="#ffffff" opacity=".8"/>')
# star on top
add(f'<g filter="url(#softglow)"><polygon points="{star_points(TX, 62, 20, 8.5)}" fill="#f9e2af">'
    f'<animateTransform attributeName="transform" type="rotate" values="-8 {TX} 62;8 {TX} 62;-8 {TX} 62" dur="3s" repeatCount="indefinite"/>'
    '<animate attributeName="fill" values="#f9e2af;#fab387;#f9e2af" dur="1.5s" repeatCount="indefinite"/></polygon></g>')
# gifts
for x, w, h, c, rb in [(TX - 112, 34, 28, '#f38ba8', '#f9e2af'), (TX + 62, 40, 34, '#89b4fa', '#f5c2e7'), (TX + 26, 26, 22, '#a6e3a1', '#f38ba8')]:
    y = 318 - h
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{c}"/><rect x="{x + w / 2 - 3}" y="{y}" width="6" height="{h}" fill="{rb}"/>'
        f'<rect x="{x}" y="{y + h / 2 - 3}" width="{w}" height="6" fill="{rb}" opacity=".85"/>'
        f'<path d="M{x + w / 2} {y} q-10 -12 -14 -2 q4 6 14 2 q10 -12 14 -2 q-4 6 -14 2" fill="none" stroke="{rb}" stroke-width="2.5"/>')

# ---------- pixel cat in a Santa hat ----------
CAT = ['.....rw.', '....rrr.', '...rrrr.', '..rrrrr.', 'mwwwwwwm', 'mmmmmmmm', 'mEmmmmEm', 'mmmmmmmm', 'mmmppmmm', '.mmmmmm.', 'mmmmmmmm', 'mm.mm.mm']
PAL = {'m': '#cba6f7', 'r': '#e64553', 'w': '#ffffff', 'p': '#f38ba8', 'E': '#11111b'}
s = 6
cx0, cy0 = 300, 318 - len(CAT) * s
cells, eyes = [], []
for r, row in enumerate(CAT):
    for c, ch in enumerate(row):
        if ch == '.':
            continue
        rect = f'<rect x="{cx0 + c * s}" y="{cy0 + r * s}" width="{s}" height="{s}" fill="{PAL[ch]}"/>'
        (eyes if ch == 'E' else cells).append(rect)
add(f'<g shape-rendering="crispEdges">{"".join(cells)}'
    f'<g>{"".join(eyes)}<animate attributeName="opacity" values="1;1;0;1" keyTimes="0;.9;.95;1" dur="4s" repeatCount="indefinite"/></g>'
    f'<path d="M{cx0 + 48} {cy0 + 60} h6 v-18 h6 v-6" fill="none" stroke="#cba6f7" stroke-width="6">'
    f'<animateTransform attributeName="transform" type="rotate" values="0 {cx0 + 48} {cy0 + 60};-12 {cx0 + 48} {cy0 + 60};0 {cx0 + 48} {cy0 + 60}" dur="1.4s" repeatCount="indefinite"/></path>'
    f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="1.8s" repeatCount="indefinite"/></g>')

# ---------- snowman ----------
SX = 1060
add(f'<ellipse cx="{SX}" cy="318" rx="46" ry="6" fill="#bac2de" opacity=".6"/>')
add(f'<circle cx="{SX}" cy="285" r="34" fill="#ffffff"/><circle cx="{SX}" cy="232" r="25" fill="#ffffff"/><circle cx="{SX}" cy="192" r="19" fill="#ffffff"/>')
add(f'<circle cx="{SX + 10}" cy="282" r="30" fill="#dce0e8" opacity=".5"/>')
for y in (222, 236, 250):
    add(f'<circle cx="{SX}" cy="{y}" r="3" fill="#313244"/>')
add(f'<circle cx="{SX - 7}" cy="188" r="2.6" fill="#11111b"/><circle cx="{SX + 7}" cy="188" r="2.6" fill="#11111b"/>'
    f'<path d="M{SX} 194 L{SX + 20} 198 L{SX} 199 Z" fill="#fab387"/>'
    f'<path d="M{SX - 8} 202 Q{SX} 208 {SX + 8} 202" fill="none" stroke="#11111b" stroke-width="2" stroke-dasharray="1.5 3" stroke-linecap="round"/>')
add(f'<rect x="{SX - 22}" y="170" width="44" height="6" rx="2" fill="#313244"/><rect x="{SX - 14}" y="146" width="28" height="26" rx="2" fill="#313244"/>'
    f'<rect x="{SX - 14}" y="162" width="28" height="5" fill="#e64553"/>')
add(f'<path d="M{SX - 20} 210 Q{SX} 220 {SX + 20} 210 L{SX + 20} 216 Q{SX} 226 {SX - 20} 216 Z" fill="#e64553"/>'
    f'<path d="M{SX + 10} 214 l6 28 l8 -2 l-6 -26 Z" fill="#e64553"><animateTransform attributeName="transform" type="rotate" values="0 {SX + 12} 214;10 {SX + 12} 214;0 {SX + 12} 214" dur="2s" repeatCount="indefinite"/></path>')
add(f'<path d="M{SX - 24} 235 L{SX - 60} 215 M{SX - 46} 223 l-6 -10" stroke="#7a4f2e" stroke-width="3.5" stroke-linecap="round" fill="none"/>')
add(f'<g><path d="M{SX + 24} 235 L{SX + 58} 212 M{SX + 48} 219 l4 -11" stroke="#7a4f2e" stroke-width="3.5" stroke-linecap="round" fill="none"/>'
    f'<animateTransform attributeName="transform" type="rotate" values="0 {SX + 24} 235;-18 {SX + 24} 235;0 {SX + 24} 235" dur="1s" repeatCount="indefinite"/></g>')

# ---------- greeting ----------
add('<text x="660" y="232" text-anchor="middle" font-family="' + SANS + '" font-size="62" font-weight="900" letter-spacing="1" '
    'fill="url(#xmas)" filter="url(#softglow)">Merry Christmas!</text>')
add('<text x="660" y="272" text-anchor="middle" font-family="' + SANS + '" font-size="22" font-weight="600" fill="#cdd6f4">'
    'Hi, I’m <tspan fill="#f5c2e7" font-weight="800">Catouis</tspan> — ho ho ho, happy shipping</text>')

# ---------- falling snow (on top) ----------
for _ in range(90):
    x, r = rnd.uniform(0, W), rnd.uniform(1.2, 3.4)
    dur = rnd.uniform(7, 15) * (2.4 / (r + 1))
    drift = rnd.uniform(-40, 40)
    add(f'<circle cx="{x:.0f}" cy="-10" r="{r:.1f}" fill="#ffffff" opacity="{rnd.uniform(.55, .95):.2f}">'
        f'<animateTransform attributeName="transform" type="translate" values="0 0;{drift / 2:.0f} 190;{drift:.0f} 380" '
        f'dur="{dur:.1f}s" begin="-{rnd.uniform(0, dur):.1f}s" repeatCount="indefinite"/></circle>')

add('</g>')
add(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="22" fill="none" stroke="#45475a" stroke-width="2"/>')
add('</svg>')

dest = ROOT / 'assets' / 'christmas.svg'
dest.write_text('\n'.join(out) + '\n', encoding='utf-8')
print(f'wrote {dest} ({dest.stat().st_size // 1024} KB)')
