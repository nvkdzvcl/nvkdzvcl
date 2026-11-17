"""Render a self-hosted GitHub stats card (assets/stats.svg) — no third-party render service."""
import html
import json
import math
import os
from pathlib import Path
import urllib.request

USER = os.environ.get('PROFILE_USER', 'nvkdzvcl')
TOKEN = os.environ['GITHUB_TOKEN']
OUT = Path(os.environ.get('STATS_OUT', 'assets/stats.svg'))

QUERY = '''
query($login: String!, $after: String) {
  user(login: $login) {
    followers { totalCount }
    pullRequests(first: 1) { totalCount }
    openIssues: issues(states: OPEN) { totalCount }
    closedIssues: issues(states: CLOSED) { totalCount }
    repositoriesContributedTo(first: 1, contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]) { totalCount }
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
      totalPullRequestReviewContributions
    }
    repositories(first: 100, after: $after, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
      nodes { stargazerCount }
      pageInfo { hasNextPage endCursor }
    }
  }
}'''


def graphql(variables):
    body = json.dumps({'query': QUERY, 'variables': variables}).encode()
    req = urllib.request.Request('https://api.github.com/graphql', data=body, headers={
        'Authorization': 'Bearer ' + TOKEN, 'User-Agent': 'Catouis-profile', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=45) as response:
        payload = json.load(response)
    if payload.get('errors'):
        raise SystemExit(f"GraphQL error: {payload['errors']}")
    return payload['data']['user']


user, stars, cursor = None, 0, None
while True:
    page = graphql({'login': USER, 'after': cursor})
    user = user or page
    stars += sum(r['stargazerCount'] for r in page['repositories']['nodes'])
    info = page['repositories']['pageInfo']
    if not info['hasNextPage']:
        break
    cursor = info['endCursor']

cc = user['contributionsCollection']
commits = cc['totalCommitContributions'] + cc['restrictedContributionsCount']
prs = user['pullRequests']['totalCount']
issues = user['openIssues']['totalCount'] + user['closedIssues']['totalCount']
reviews = cc['totalPullRequestReviewContributions']
followers = user['followers']['totalCount']
contributed = user['repositoriesContributedTo']['totalCount']

# Same rank formula as github-readme-stats (percentile vs. typical GitHub users).
exp_cdf = lambda x: 1 - 2 ** -x
log_cdf = lambda x: x / (1 + x)
weights = [(2, exp_cdf(commits / 250)), (3, exp_cdf(prs / 50)), (1, exp_cdf(issues / 25)),
           (1, exp_cdf(reviews / 2)), (4, log_cdf(stars / 50)), (1, log_cdf(followers / 10))]
percentile = (1 - sum(w * v for w, v in weights) / sum(w for w, _ in weights)) * 100
levels = ['S', 'A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']
thresholds = [1, 12.5, 25, 37.5, 50, 62.5, 75, 87.5, 100]
rank = levels[next(i for i, t in enumerate(thresholds) if percentile <= t)]

rows = [
    ('Total Stars Earned', stars, '#f9e2af'),
    ('Commits (last year)', commits, '#f38ba8'),
    ('Pull Requests', prs, '#cba6f7'),
    ('Issues', issues, '#89b4fa'),
    ('Contributed to', contributed, '#a6e3a1'),
]

W, H = 495, 195
radius = 40
circ = 2 * math.pi * radius
progress = max(0.0, min(1.0, 1 - percentile / 100))
p = []
p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">')
p.append(f'<title id="t">Catouis\'s GitHub Stats — rank {rank}</title>')
p.append('''<defs>
  <linearGradient id="border" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#f38ba8"/><stop offset="50%" stop-color="#cba6f7"/><stop offset="100%" stop-color="#89b4fa"/>
  </linearGradient>
  <linearGradient id="ring" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#f5c2e7"/><stop offset="100%" stop-color="#cba6f7"/>
  </linearGradient>
  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3.5"/></filter>
  <linearGradient id="title" x1="0" x2="1" spreadMethod="reflect">
    <stop offset="0" stop-color="#f38ba8"/><stop offset=".33" stop-color="#fab387"/><stop offset=".66" stop-color="#cba6f7"/><stop offset="1" stop-color="#89b4fa"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="6s" repeatCount="indefinite"/>
  </linearGradient>
  <style>
    @media (prefers-reduced-motion: reduce){*{animation:none!important}.row{opacity:1}}
    .row{opacity:0;animation:in .6s ease forwards}
    @keyframes in{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}
    .arc{animation:fill 1.4s ease-out forwards}
    @keyframes fill{from{stroke-dashoffset:%(circ).2f}}
    .glow{animation:pulse 2.4s ease-in-out infinite}
    @keyframes pulse{0%%,100%%{opacity:.35}50%%{opacity:.8}}
    text{font-family:"Segoe UI",Ubuntu,Arial,sans-serif}
  </style>
</defs>'''.replace('%(circ).2f', f'{circ:.2f}').replace('%%', '%'))
p.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="14" fill="none" stroke="url(#border)" stroke-width="3" filter="url(#glow)" opacity=".85"/>')
p.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="14" fill="#181825" stroke="url(#border)" stroke-width="1.5"/>')
p.append('<text x="25" y="38" font-size="18" font-weight="800" fill="url(#title)">Catouis\'s GitHub Stats</text>')
for i, (label, value, color) in enumerate(rows):
    y = 72 + i * 25
    p.append(f'<g class="row" style="animation-delay:{0.15 * (i + 1):.2f}s">')
    p.append(f'<circle cx="31" cy="{y - 5}" r="5" fill="{color}"/>')
    p.append(f'<text x="45" y="{y}" font-size="14" font-weight="600" fill="#cdd6f4">{html.escape(label)}:</text>')
    p.append(f'<text x="225" y="{y}" font-size="14" font-weight="700" fill="{color}">{value:,}</text>')
    p.append('</g>')
cx, cy = 400, 105
p.append(f'<circle class="glow" cx="{cx}" cy="{cy}" r="{radius + 8}" fill="none" stroke="#cba6f7" stroke-width="2" stroke-opacity=".4"/>')
p.append(f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="#313244" stroke-width="7"/>')
p.append(f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="url(#ring)" stroke-width="7" stroke-linecap="round" filter="url(#glow)" '
         f'stroke-dasharray="{circ:.2f}" stroke-dashoffset="{circ * (1 - progress):.2f}" transform="rotate(-90 {cx} {cy})"/>')
p.append(f'<circle class="arc" cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="url(#ring)" stroke-width="7" stroke-linecap="round" '
         f'stroke-dasharray="{circ:.2f}" stroke-dashoffset="{circ * (1 - progress):.2f}" transform="rotate(-90 {cx} {cy})"/>')
p.append(f'<text x="{cx}" y="{cy + 9}" font-size="26" font-weight="800" fill="#f5c2e7" text-anchor="middle">{rank}</text>')
p.append(f'<text x="{cx}" y="{cy + radius + 26}" font-size="11" fill="#a6adc8" text-anchor="middle">top {percentile:.1f}%</text>')
p.append('</svg>')

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text('\n'.join(p), encoding='utf-8')
print(f'wrote {OUT}: rank {rank} (top {percentile:.1f}%), stars={stars} commits={commits} prs={prs} issues={issues}')
