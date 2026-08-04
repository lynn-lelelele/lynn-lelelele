"""Generate pink achievement badges SVG"""
import os

achievements = [
    ("💻", "Systems Programming", "C · algorithms · data structures"),
    ("🐍", "Python", "automation · scripting"),
    ("🔧", "Version Control", "Git · GitHub · CI/CD"),
    ("🏆", "AdvX Hackathon", "echo · uni-app · shipped"),
    ("📦", "Open Source", "cs-journey · public projects"),
    ("🎓", "ANU", "B Advanced Computing"),
]

COLS = 3
GAP_X, GAP_Y = 24, 24
CARD_W, CARD_H = 150, 80
PAD = 20
ROWS = (len(achievements) + COLS - 1) // COLS

W = PAD * 2 + COLS * CARD_W + (COLS - 1) * GAP_X
H = 50 + PAD * 2 + ROWS * CARD_H + (ROWS - 1) * GAP_Y

PINK = "#ffb6c1"
PURPLE = "#dda0dd"
DARK = "#333"
GRAY = "#888"

cards = ""
for i, (icon, title, desc) in enumerate(achievements):
    col = i % COLS
    row = i // COLS
    x = PAD + col * (CARD_W + GAP_X)
    y = 50 + PAD + row * (CARD_H + GAP_Y)

    cards += f'''
  <!-- {title} -->
  <rect x="{x}" y="{y}" width="{CARD_W}" height="{CARD_H}" rx="12"
        fill="white" stroke="{PINK}" stroke-width="1.5" filter="url(#shadow)"/>
  <!-- icon circle -->
  <circle cx="{x + CARD_W//2}" cy="{y + 22}" r="16" fill="{PINK}" opacity="0.2"/>
  <text x="{x + CARD_W//2}" y="{y + 27}" font-size="18" text-anchor="middle">{icon}</text>
  <!-- title -->
  <text x="{x + CARD_W//2}" y="{y + 52}" font-family="Segoe UI, sans-serif"
        font-size="13" font-weight="bold" fill="{DARK}" text-anchor="middle">{title}</text>
  <!-- desc -->
  <text x="{x + CARD_W//2}" y="{y + 70}" font-family="Segoe UI, sans-serif"
        font-size="11" fill="{GRAY}" text-anchor="middle">{desc}</text>'''

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <filter id="shadow">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.08"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="{W}" height="{H}" rx="14" fill="#fff5f7" stroke="{PINK}" stroke-width="2"/>

  <!-- Title -->
  <text x="25" y="32" font-family="Segoe UI, sans-serif" font-size="16" font-weight="bold" fill="{DARK}">
    achievements
  </text>
  <circle cx="140" cy="27" r="5" fill="{PINK}" opacity="0.5"/>
  <circle cx="154" cy="27" r="5" fill="{PURPLE}" opacity="0.5"/>
  <circle cx="168" cy="27" r="5" fill="{PINK}" opacity="0.5"/>

  {cards}
</svg>'''

os.makedirs("assets", exist_ok=True)
with open("assets/badges.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print(f"Generated achievements: {W}x{H}")
