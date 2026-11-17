"""Render featured project cards (assets/projects.svg): pinned repos first, then recently pushed ones."""
import datetime as dt
import html
import json
import os
from pathlib import Path
import urllib.request

USER = os.environ.get('PROFILE_USER', 'nvkdzvcl')
TOKEN = os.environ['GITHUB_TOKEN']
OUT = Path(os.environ.get('PROJECTS_OUT', 'assets/projects.svg'))
SKIP = {USER.lower(), f'{USER.lower()}.github.io'}
LIMIT = 4

REPO_FIELDS = 'name description stargazerCount forkCount pushedAt isFork isPrivate primaryLanguage { name color }'
QUERY = f'''
query($login: String!) {{
  user(login: $login) {{
    pinnedItems(first: 6, types: REPOSITORY) {{ nodes {{ ... on Repository {{ {REPO_FIELDS} }} }} }}
    repositories(first: 30, ownerAffiliations: OWNER, privacy: PUBLIC, orderBy: {{field: PUSHED_AT, direction: DESC}}) {{
      nodes {{ {REPO_FIELDS} }}
    }}
  }}
}}'''

req = urllib.request.Request('https://api.github.com/graphql',
                             data=json.dumps({'query': QUERY, 'variables': {'login': USER}}).encode(),
                             headers={'Authorization': 'Bearer ' + TOKEN, 'User-Agent': 'Catouis-profile',
                                      'Content-Type': 'application/json'})
with urllib.request.urlopen(req, timeout=45) as response:
    payload = json.load(response)
if payload.get('errors'):
    raise SystemExit(f"GraphQL error: {payload['errors']}")
user = payload['data']['user']

pinned = {r['name'] for r in user['pinnedItems']['nodes'] if r}
picked, seen = [], set()
for repo in user['pinnedItems']['nodes'] + user['repositories']['nodes']:
    if not repo or repo['isFork'] or repo['isPrivate'] or repo['name'].lower() in SKIP or repo['name'] in seen:
        continue
    seen.add(repo['name'])
    picked.append(repo)
    if len(picked) == LIMIT:
        break


def ago(stamp):
    days = (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(stamp.replace('Z', '+00:00'))).days
    if days < 1:
        return 'updated today'
    if days < 30:
        return f'updated {days}d ago'
    if days < 365:
        return f'updated {days // 30}mo ago'
    return f'updated {days // 365}y ago'


def clip(text, n):
    return text if len(text) <= n else text[:n - 1].rstrip() + '…'


ACCENTS = [('#f38ba8', '#fab387'), ('#cba6f7', '#f5c2e7'), ('#89b4fa', '#94e2d5'), ('#a6e3a1', '#f9e2af')]
CW, CH, GAP = 585, 150, 20
rows = (len(picked) + 1) // 2 or 1
W, H = 1200, rows * CH + (rows - 1) * GAP + 10
p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">',
     f'<title id="t">Featured projects: {html.escape(", ".join(r["name"] for r in picked))}</title><defs>']
for i, (a, b) in enumerate(ACCENTS):
    p.append(f'<linearGradient id="a{i}" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>')
p.append('''</defs><style>
text{font-family:"Segoe UI",Ubuntu,Helvetica,Arial,sans-serif}
.card{opacity:0;animation:up .6s ease forwards}
@keyframes up{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion: reduce){.card{animation:none;opacity:1}}
</style>''')
for i, repo in enumerate(picked):
    x, y = 5 + (i % 2) * (CW + GAP), 5 + (i // 2) * (CH + GAP)
    lang = repo['primaryLanguage'] or {'name': 'Code', 'color': '#a6adc8'}
    desc = repo['description'] or f'A {lang["name"]} project — README has the details.'
    p.append(f'<g class="card" style="animation-delay:{0.15 * i:.2f}s">')
    p.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="16" fill="#181825" stroke="url(#a{i % 4})" stroke-width="2"/>')
    p.append(f'<rect x="{x}" y="{y + 22}" width="6" height="{CH - 44}" rx="3" fill="url(#a{i % 4})"/>')
    p.append(f'<text x="{x + 28}" y="{y + 46}" font-size="24" font-weight="800" fill="url(#a{i % 4})">{html.escape(clip(repo["name"], 34))}</text>')
    p.append(f'<text x="{x + 28}" y="{y + 82}" font-size="17" fill="#bac2de">{html.escape(clip(desc, 58))}</text>')
    p.append(f'<circle cx="{x + 36}" cy="{y + 119}" r="7" fill="{lang["color"] or "#a6adc8"}"/>')
    p.append(f'<text x="{x + 50}" y="{y + 125}" font-size="16" fill="#cdd6f4">{html.escape(lang["name"])}</text>')
    p.append(f'<text x="{x + 200}" y="{y + 125}" font-size="16" fill="#f9e2af">★ {repo["stargazerCount"]}</text>')
    p.append(f'<text x="{x + 270}" y="{y + 125}" font-size="16" fill="#94e2d5">⑂ {repo["forkCount"]}</text>')
    p.append(f'<text x="{x + CW - 24}" y="{y + 125}" text-anchor="end" font-size="15" fill="#7f849c">{ago(repo["pushedAt"])}</text>')
    if repo['name'] in pinned:
        p.append(f'<text x="{x + CW - 24}" y="{y + 44}" text-anchor="end" font-size="14" font-weight="700" fill="#f5c2e7">📌 pinned</text>')
    p.append('</g>')
p.append('</svg>')

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text('\n'.join(p), encoding='utf-8')
print(f'wrote {OUT}: {[r["name"] for r in picked]}')
