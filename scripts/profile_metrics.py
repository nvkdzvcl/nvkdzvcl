"""Build a public-data GitHub infographic without third-party render services."""
import collections
import datetime as dt
import html
import json
import os
from pathlib import Path
import urllib.request

USER = os.environ.get('PROFILE_USER', 'nvkdzvcl')
HEADERS = {'User-Agent': 'Catouis-profile', 'Accept': 'application/vnd.github+json'}
if os.environ.get('GITHUB_TOKEN'):
    HEADERS['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']

def get(path):
    with urllib.request.urlopen(urllib.request.Request('https://api.github.com' + path, headers=HEADERS), timeout=45) as response:
        return json.load(response)

repos = []
for page in range(1, 21):
    batch = get(f'/users/{USER}/repos?type=owner&per_page=100&page={page}')
    repos.extend(r for r in batch if not r['fork'] and not r['private'])
    if len(batch) < 100:
        break
languages = collections.Counter()
for repo in repos:
    languages.update(get(f'/repos/{USER}/{repo["name"]}/languages'))
events = get(f'/users/{USER}/events/public?per_page=100')
hours = collections.Counter()
for event in events:
    timestamp = dt.datetime.fromisoformat(event['created_at'].replace('Z', '+00:00'))
    hours[timestamp.astimezone(dt.timezone(dt.timedelta(hours=7))).hour] += 1

palette = ['#cba6f7', '#f38ba8', '#89b4fa', '#a6e3a1', '#f9e2af', '#94e2d5']
parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="800" height="650" viewBox="0 0 800 650" role="img" aria-labelledby="title desc">', '<title id="title">Catouis — Behind the Vibes</title>', '<desc id="desc">Public repositories, repository language bytes, and recent public event hours in UTC+7.</desc>', '<rect width="800" height="650" rx="20" fill="#181825"/>']
def text(x, y, value, size=15, color='#cdd6f4', weight='400'):
    parts.append(f'<text x="{x}" y="{y}" font-family="Segoe UI,Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{html.escape(str(value))}</text>')
def rect(x, y, w, h, color, radius=4):
    parts.append(f'<rect x="{x}" y="{y}" width="{w:.2f}" height="{h:.2f}" rx="{radius}" fill="{color}"/>')
text(32, 44, 'BEHIND THE VIBES', 24, '#cba6f7', '700')
text(32, 70, 'Small experiments. Real progress.', 14, '#a6adc8')
for i, (label, value) in enumerate([('PUBLIC REPOS', len(repos)), ('STARS', sum(r['stargazers_count'] for r in repos)), ('LANGUAGES', len(languages))]):
    x = 32 + i * 248
    rect(x, 92, 232, 80, '#242438', 10)
    text(x + 16, 117, label, 12, '#a6adc8')
    text(x + 16, 152, value, 28, palette[i], '700')
text(32, 209, 'Languages across my public repositories', 18, '#f38ba8', '600')
total = sum(languages.values())
for i, (name, amount) in enumerate(languages.most_common(6)):
    y = 239 + i * 27
    pct = amount / total * 100
    text(32, y, name, 14)
    rect(180, y-11, 490, 9, '#313244')
    rect(180, y-11, max(2, 490 * pct / 100), 9, palette[i])
    text(691, y, f'{pct:.1f}%', 13, palette[i])
if not total:
    text(32, 242, 'No public language data available yet.', 14, '#a6adc8')
text(32, 412, 'Share of code bytes; not a measure of proficiency. Forks excluded.', 12, '#a6adc8')
text(32, 451, 'When I am active · UTC+7', 18, '#89b4fa', '600')
maximum = max(hours.values(), default=1)
for hour in range(24):
    height = 85 * hours[hour] / maximum
    rect(38+hour*30, 551-height, 20, max(2,height), palette[hour//4])
    if hour % 3 == 0:
        text(38+hour*30, 573, f'{hour:02}', 11, '#a6adc8')
text(32, 605, f'Based on {len(events)} latest available public events; all event types, not coding hours.', 12, '#a6adc8')
text(32, 628, 'Updated ' + dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M UTC'), 11, '#a6adc8')
parts.append('</svg>')
Path('assets').mkdir(exist_ok=True)
Path('assets/metrics.svg').write_text('\n'.join(parts), encoding='utf-8')
print(f'Generated infographic: {len(repos)} public repos, {len(languages)} languages, {len(events)} events.')
