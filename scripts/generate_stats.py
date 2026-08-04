"""Generate pink-themed GitHub stats SVG"""
import json, urllib.request, os

USER = "lynn-lelelele"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

def gh(path):
    req = urllib.request.Request(f"https://api.github.com{path}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("User-Agent", "stats-generator")
    req.add_header("Accept", "application/vnd.github+json")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

# Fetch data
user = gh(f"/users/{USER}")
repos = gh(f"/users/{USER}/repos?per_page=100&sort=pushed")
events = gh(f"/users/{USER}/events/public?per_page=100")

# Calculate stats
total_stars = sum(r.get("stargazers_count", 0) for r in repos)
total_forks = sum(r.get("forks_count", 0) for r in repos)
repo_count = len(repos)
followers = user.get("followers", 0)
following = user.get("following", 0)
public_repos = user.get("public_repos", 0)

# Count languages
langs = {}
for r in repos:
    lang = r.get("language")
    if lang:
        langs[lang] = langs.get(lang, 0) + 1
top_langs = sorted(langs.items(), key=lambda x: x[1], reverse=True)[:4]

# Count commits (approximate from push events)
commit_count = sum(e.get("payload", {}).get("size", 0) for e in events if e.get("type") == "PushEvent")

W, H = 500, 210
PINK = "#ffb6c1"
PURPLE = "#dda0dd"
DARK = "#333333"
LIGHT_BG = "#ffffff"
DARK_BG = "#1a1a2e"

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fff5f7"/>
      <stop offset="100%" stop-color="#fff0f5"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{PINK}"/>
      <stop offset="100%" stop-color="{PURPLE}"/>
    </linearGradient>
  </defs>

  <!-- Card background -->
  <rect width="{W}" height="{H}" rx="14" fill="url(#bg)" stroke="{PINK}" stroke-width="2"/>

  <!-- Header -->
  <text x="25" y="40" font-family="Segoe UI, sans-serif" font-size="18" font-weight="bold" fill="{DARK}">
    lynn-lelelele's stats
  </text>
  <line x1="25" y1="50" x2="225" y2="50" stroke="url(#accent)" stroke-width="3" stroke-linecap="round"/>

  <!-- Stat boxes -->
  <!-- Row 1 -->
  <rect x="25" y="65" width="140" height="55" rx="8" fill="white" stroke="{PINK}" stroke-width="1"/>
  <text x="95" y="86" font-family="monospace" font-size="21" font-weight="bold" fill="{DARK}" text-anchor="middle">{total_stars}</text>
  <text x="95" y="108" font-family="Segoe UI, sans-serif" font-size="11" fill="#888" text-anchor="middle">Total Stars</text>

  <rect x="180" y="65" width="140" height="55" rx="8" fill="white" stroke="{PURPLE}" stroke-width="1"/>
  <text x="250" y="86" font-family="monospace" font-size="21" font-weight="bold" fill="{DARK}" text-anchor="middle">{commit_count}</text>
  <text x="250" y="108" font-family="Segoe UI, sans-serif" font-size="11" fill="#888" text-anchor="middle">Commits</text>

  <rect x="335" y="65" width="140" height="55" rx="8" fill="white" stroke="{PINK}" stroke-width="1"/>
  <text x="405" y="86" font-family="monospace" font-size="21" font-weight="bold" fill="{DARK}" text-anchor="middle">{followers}</text>
  <text x="405" y="108" font-family="Segoe UI, sans-serif" font-size="11" fill="#888" text-anchor="middle">Followers</text>

  <!-- Row 2 -->
  <rect x="25" y="130" width="140" height="55" rx="8" fill="white" stroke="{PURPLE}" stroke-width="1"/>
  <text x="95" y="151" font-family="monospace" font-size="21" font-weight="bold" fill="{DARK}" text-anchor="middle">{public_repos}</text>
  <text x="95" y="173" font-family="Segoe UI, sans-serif" font-size="11" fill="#888" text-anchor="middle">Repos</text>

  <rect x="180" y="130" width="140" height="55" rx="8" fill="white" stroke="{PINK}" stroke-width="1"/>
  <text x="250" y="151" font-family="monospace" font-size="21" font-weight="bold" fill="{DARK}" text-anchor="middle">{total_forks}</text>
  <text x="250" y="173" font-family="Segoe UI, sans-serif" font-size="11" fill="#888" text-anchor="middle">Forks</text>

  <rect x="335" y="130" width="140" height="55" rx="8" fill="white" stroke="{PURPLE}" stroke-width="1"/>
  <text x="405" y="151" font-family="monospace" font-size="21" font-weight="bold" fill="{DARK}" text-anchor="middle">{following}</text>
  <text x="405" y="173" font-family="Segoe UI, sans-serif" font-size="11" fill="#888" text-anchor="middle">Following</text>
</svg>'''

os.makedirs("assets", exist_ok=True)
with open("assets/stats.svg", "w") as f:
    f.write(svg)

print(f"Generated stats: {total_stars} stars, {commit_count} commits, {followers} followers")
print(f"Top langs: {', '.join(f'{l}={c}' for l,c in top_langs)}")
