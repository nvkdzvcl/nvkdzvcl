"""Regenerate the static profile SVGs: python scripts/build_static_assets.py . (header, section headers, about card, AI tools)."""
import html
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
A = ROOT / 'assets'
(A / 'headers').mkdir(parents=True, exist_ok=True)

C = dict(base='#181825', crust='#11111b', surface='#313244', text='#cdd6f4', sub='#a6adc8', dim='#6c7086',
         mauve='#cba6f7', pink='#f5c2e7', red='#f38ba8', peach='#fab387', yellow='#f9e2af', green='#a6e3a1',
         teal='#94e2d5', sky='#89dceb', blue='#89b4fa', lav='#b4befe')
SANS = 'Segoe UI,Ubuntu,Helvetica,Arial,sans-serif'
MONO = 'Cascadia Code,Fira Code,Consolas,Menlo,monospace'
RAINBOW = '''<linearGradient id="rb" x1="0" x2="1">
  <stop offset="0" stop-color="#f38ba8"/><stop offset=".25" stop-color="#fab387"/><stop offset=".5" stop-color="#cba6f7"/>
  <stop offset=".75" stop-color="#89b4fa"/><stop offset="1" stop-color="#94e2d5"/>
  <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="6s" repeatCount="indefinite"/>
</linearGradient>'''
REDUCED = '<style>@media (prefers-reduced-motion: reduce){*{animation:none!important}}</style>'


def write(name, body):
    (A / name).write_text(body.strip() + '\n', encoding='utf-8')


# ---------- top banner ----------
write('header.svg', f'''
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="150" viewBox="0 0 1200 150" role="img" aria-label="Hi, I'm Catouis">
<defs>{RAINBOW.replace('id="rb"', 'id="rb" spreadMethod="reflect"')}
<linearGradient id="w"><stop stop-color="#cba6f7"/><stop offset=".5" stop-color="#f38ba8"/><stop offset="1" stop-color="#89b4fa"/></linearGradient></defs>
{REDUCED}
<path fill="url(#w)" opacity=".18" d="M0 0H1200V70Q900 130 600 70T0 70Z"><animate attributeName="d" dur="9s" repeatCount="indefinite"
 values="M0 0H1200V70Q900 130 600 70T0 70Z;M0 0H1200V95Q900 35 600 95T0 95Z;M0 0H1200V70Q900 130 600 70T0 70Z"/></path>
<path fill="url(#w)" opacity=".35" d="M0 0H1200V45Q900 95 600 45T0 45Z"><animate attributeName="d" dur="7s" repeatCount="indefinite"
 values="M0 0H1200V45Q900 95 600 45T0 45Z;M0 0H1200V60Q900 10 600 60T0 60Z;M0 0H1200V45Q900 95 600 45T0 45Z"/></path>
<text x="600" y="122" text-anchor="middle" font-family="{SANS}" font-size="38" font-weight="800" letter-spacing="2" fill="url(#rb)">Hi, I’m Catouis</text>
<g fill="{C['yellow']}"><path d="M392 100l3 7 7 3-7 3-3 7-3-7-7-3 7-3z"><animate attributeName="opacity" values="1;.2;1" dur="2s" repeatCount="indefinite"/></path>
<path d="M808 96l2 5 5 2-5 2-2 5-2-5-5-2 5-2z"><animate attributeName="opacity" values=".2;1;.2" dur="2.4s" repeatCount="indefinite"/></path></g>
</svg>''')

# ---------- section headers ----------
ICONS = {  # 8x8 pixel bitmaps: char -> colour key
    'cat': ['m......m', 'mm....mm', 'mmmmmmmm', 'mtmmmmtm', 'mmmmmmmm', 'mmmrrmmm', '.mmmmmm.', '..m..m..'],
    'spark': ['...y....', '...y....', '..yyy...', 'yyyyyyy.', '..yyy...', '...y....', '...y..p.', '.....ppp'],
    'chart': ['......b.', '......b.', '....g.b.', '....g.b.', '..r.g.b.', '..r.g.b.', 'm.r.g.b.', 'mmmmmmmm'],
    'folder': ['ppp.....', 'pppppppp', 'pyyyyyyp', 'pyyyyyyp', 'pyyyyyyp', 'pyyyyyyp', 'pppppppp', '........'],
    'ghost': ['..mmmm..', '.mmmmmm.', 'mmwmmwmm', 'mmbmmbmm', 'mmmmmmmm', 'mmmmmmmm', 'mmmmmmmm', 'm.mm.mm.'],
}
CK = dict(m=C['mauve'], t=C['teal'], r=C['red'], y=C['yellow'], p=C['peach'], b=C['blue'], g=C['green'], w='#ffffff')


def pixels(name, x0, y0, s=6):
    out = []
    for r, row in enumerate(ICONS[name]):
        for c, ch in enumerate(row):
            if ch != '.':
                out.append(f'<rect x="{x0 + c * s}" y="{y0 + r * s}" width="{s}" height="{s}" fill="{CK[ch]}"/>')
    return ''.join(out)


SECTIONS = [('about', 'cat', 'ABOUT ME', 'who is behind the keyboard'),
            ('ai', 'spark', 'AI TOOLS & TECH', 'what I build with'),
            ('stats', 'chart', 'GITHUB ANALYTICS & STREAK', 'numbers, refreshed daily'),
            ('projects', 'folder', 'FEATURED PROJECTS', 'pinned & recently shipped'),
            ('progress', 'ghost', 'A LITTLE PROGRESS, EVERY DAY', 'waka waka through my contributions')]
for key, icon, title, sub in SECTIONS:
    write(f'headers/{key}.svg', f'''
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="84" viewBox="0 0 1200 84" role="img" aria-label="{html.escape(title.title())}">
<defs>{RAINBOW}<linearGradient id="ln"><stop stop-color="#cba6f7"/><stop offset=".6" stop-color="#f38ba8" stop-opacity=".5"/><stop offset="1" stop-color="#f38ba8" stop-opacity="0"/></linearGradient></defs>
{REDUCED}
<g shape-rendering="crispEdges">{pixels(icon, 8, 14)}<animateTransform attributeName="transform" type="translate" values="0 0;0 -3;0 0" dur="1.6s" repeatCount="indefinite"/></g>
<text x="76" y="50" font-family="{SANS}" font-size="30" font-weight="800" letter-spacing="3" fill="url(#rb)">{html.escape(title)}</text>
<text x="1192" y="50" text-anchor="end" font-family="{MONO}" font-size="15" fill="{C['dim']}">// {html.escape(sub)}</text>
<rect x="76" y="68" width="1116" height="2" fill="url(#ln)"/>
<circle cy="69" r="3" fill="{C['pink']}"><animate attributeName="cx" values="76;1192" dur="5s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0" dur="5s" repeatCount="indefinite"/></circle>
</svg>''')

# ---------- about card (terminal) ----------
K, S, P, Pn = C['mauve'], C['green'], C['blue'], C['sub']
lines = [
    [(C['red'], 'const '), (C['yellow'], 'catouis'), (Pn, ' = {')],
    [(P, '  role'), (Pn, ':       '), (S, '"Vibe coder · AI-assisted builder"'), (Pn, ',')],
    [(P, '  location'), (Pn, ':   '), (S, '"Vietnam"'), (Pn, ',')],
    [(P, '  approach'), (Pn, ':   ['), (S, '"describe"'), (Pn, ', '), (S, '"build"'), (Pn, ', '), (S, '"try"'), (Pn, ', '), (S, '"improve"'), (Pn, '],')],
    [(P, '  playground'), (Pn, ': '), (S, '"AI-assisted dev & whatever I feel like next"'), (Pn, ',')],
    [(P, '  mindset'), (Pn, ':    '), (S, '"learning by shipping — one experiment at a time"'), (Pn, ',')],
    [(P, '  fuel'), (Pn, ':       ['), (S, '"curiosity"'), (Pn, ', '), (S, '"coffee"'), (Pn, ', '), (S, '"AI"'), (Pn, '],')],
    [(P, '  mood'), (Pn, ':       '), (S, '"huhu"'), (Pn, ',  '), (C['dim'], '// but still shipping')],
    [(Pn, '};')],
]
rows = []
for i, parts in enumerate(lines):
    y = 112 + i * 34
    spans = ''.join(f'<tspan fill="{col}">{html.escape(t)}</tspan>' for col, t in parts)
    rows.append(f'<text class="ln" style="animation-delay:{0.12 * i:.2f}s" x="96" y="{y}" xml:space="preserve">{spans}</text>'
                f'<text x="72" y="{y}" text-anchor="end" fill="{C["surface"]}">{i + 1}</text>')
H = 112 + len(lines) * 34 + 20
write('about.svg', f'''
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{H}" viewBox="0 0 1200 {H}" role="img" aria-labelledby="t d">
<title id="t">About Catouis</title>
<desc id="d">Vibe coder and AI-assisted builder from Vietnam. Approach: describe, build, try, improve. Mindset: learning by shipping, one experiment at a time.</desc>
<defs><linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#f38ba8"/><stop offset=".5" stop-color="#cba6f7"/><stop offset="1" stop-color="#89b4fa"/></linearGradient>
<filter id="glow" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="5"/></filter></defs>
<style>text{{font-family:{MONO};font-size:21px}} .ln{{opacity:0;animation:in .5s ease forwards}}
@keyframes in{{from{{opacity:0;transform:translateX(-10px)}}to{{opacity:1;transform:none}}}}
.cur{{animation:blink 1s steps(1) infinite}}@keyframes blink{{50%{{opacity:0}}}}
@media (prefers-reduced-motion: reduce){{.ln{{animation:none;opacity:1}}.cur{{animation:none}}}}</style>
<rect x="10" y="10" width="1180" height="{H - 20}" rx="18" fill="none" stroke="url(#bd)" stroke-width="4" filter="url(#glow)" opacity=".7"/>
<rect x="10" y="10" width="1180" height="{H - 20}" rx="18" fill="{C['base']}" stroke="url(#bd)" stroke-width="2"/>
<rect x="11" y="11" width="1178" height="46" rx="17" fill="{C['crust']}"/><rect x="11" y="40" width="1178" height="17" fill="{C['crust']}"/>
<circle cx="42" cy="34" r="7" fill="#f38ba8"/><circle cx="66" cy="34" r="7" fill="#f9e2af"/><circle cx="90" cy="34" r="7" fill="#a6e3a1"/>
<text x="600" y="40" text-anchor="middle" style="font-size:16px" fill="{C['sub']}">catouis.config.ts</text>
{''.join(rows)}
<rect class="cur" x="130" y="{112 + (len(lines) - 1) * 34 - 18}" width="12" height="22" fill="{C['pink']}"/>
<g transform="translate(1010 150)" shape-rendering="crispEdges" opacity=".9">{pixels('cat', 0, 0, 14)}
<animateTransform attributeName="transform" type="translate" values="1010 150;1010 140;1010 150" dur="2.2s" repeatCount="indefinite"/></g>
</svg>''')

# ---------- AI tools chips ----------
GLYPH = {
    'claude': '<g stroke="#fff" stroke-width="4" stroke-linecap="round">' + ''.join(
        f'<line x1="0" y1="-5" x2="0" y2="-15" transform="rotate({a})"/>' for a in range(0, 360, 45)) + '</g>',
    'chatgpt': '<path d="M-14-11h28a4 4 0 0 1 4 4v14a4 4 0 0 1-4 4H-4l-8 7v-7h-2a4 4 0 0 1-4-4V-7a4 4 0 0 1 4-4z" fill="#fff"/>',
    'codex': '<path d="M-6-11L-16 0L-6 11M6-11L16 0L6 11" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>',
    'antigravity': '<path d="M0-16C8-8 8 4 5 10H-5C-8 4-8-8 0-16z" fill="#fff"/><circle cy="-3" r="3" fill="#1e1e2e"/><path d="M-5 10l-5 6M5 10l5 6M0 12v6" stroke="#fff" stroke-width="3" stroke-linecap="round"/>',
}
TOOLS = [('claude', 'Claude', '#d97757', '#f5a37f'), ('chatgpt', 'ChatGPT', '#10a37f', '#74aa9c'),
         ('codex', 'Codex', '#8839ef', '#cba6f7'), ('antigravity', 'Antigravity', '#1e66f5', '#89b4fa')]
chips, defs = [], []
for i, (key, label, c1, c2) in enumerate(TOOLS):
    x = 10 + i * 297
    defs.append(f'<linearGradient id="g{i}" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>')
    chips.append(f'''<g class="chip" style="animation-delay:{0.6 * i:.1f}s">
<rect x="{x}" y="14" width="282" height="76" rx="38" fill="url(#g{i})"/>
<rect x="{x}" y="14" width="282" height="76" rx="38" fill="url(#shine)"/>
<g transform="translate({x + 44} 52)">{GLYPH[key]}</g>
<text x="{x + 82}" y="62" font-family="{SANS}" font-size="27" font-weight="800" fill="#fff">{label}</text>
{'<text x="' + str(x + 262) + '" y="40" text-anchor="end" font-family="' + SANS + '" font-size="13" font-weight="700" fill="#fff" opacity=".85">#1</text>' if i == 0 else ''}
</g>''')
write('ai-tools.svg', f'''
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="104" viewBox="0 0 1200 104" role="img" aria-label="AI tools: Claude, ChatGPT, Codex, Antigravity">
<defs>{''.join(defs)}
<linearGradient id="shine" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".28"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
<animateTransform attributeName="gradientTransform" type="translate" values="-1.2 0;1.2 0;1.2 0" keyTimes="0;.5;1" dur="3.5s" repeatCount="indefinite"/></linearGradient></defs>
<style>.chip{{animation:bob 2.4s ease-in-out infinite}}@keyframes bob{{50%{{transform:translateY(-4px)}}}}
@media (prefers-reduced-motion: reduce){{.chip{{animation:none}}}}</style>
{''.join(chips)}
</svg>''')
print('ok')
