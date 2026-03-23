#!/usr/bin/env python3
"""
Run this in the same folder as your index.html:
  python3 patch_index.py
It will update index.html in place with 3 changes.
"""
import re, shutil, sys

path = "index.html"
try:
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
except FileNotFoundError:
    print("ERROR: index.html not found in current directory.")
    sys.exit(1)

changed = 0

# 1. Update total-count from 1 to 2
old1 = '<span class="stat-num" id="total-count">1</span>'
new1 = '<span class="stat-num" id="total-count">2</span>'
if old1 in html:
    html = html.replace(old1, new1, 1)
    changed += 1
    print("OK: total-count updated to 2")
else:
    print("SKIP: total-count marker not found (may already be 2?)")

# 2. Remove LATEST badge from March 21 card
# The badge sits inside the March 21 card title div
old2 = 'SIGNAL//213 Daily Tech Brief\n          <span class="latest-badge">LATEST</span>\n        </div>\n        <div class="card-meta">OpenAI Superapp'
new2 = 'SIGNAL//213 Daily Tech Brief\n        </div>\n        <div class="card-meta">OpenAI Superapp'
if old2 in html:
    html = html.replace(old2, new2, 1)
    changed += 1
    print("OK: LATEST badge removed from March 21 card")
else:
    print("WARN: March 21 badge pattern not found - check indentation")

# 3. Insert March 22 card before the FUTURE ENTRIES comment
marker = "    <!-- FUTURE ENTRIES WILL BE ADDED ABOVE THIS LINE -->"
card22 = """    <!-- MARCH 22, 2026 -->
    <a class="briefing-card" href="2026-03-22.html" data-search="openai ads chatgpt claude code channels comet ios perplexity horizon worlds quantum signal threema apple airpods meta ray-ban facial recognition sunday march 2026">
      <div class="card-date">
        <span class="day-of-week">Sunday</span>
        March 22, 2026
        <div class="issue-num">ISSUE #002</div>
      </div>
      <div>
        <div class="card-title">
          📡 SIGNAL//213 Daily Tech Brief
          <span class="latest-badge">LATEST</span>
        </div>
        <div class="card-meta">ChatGPT Ads · Claude Channels · Comet iOS · Horizon Reversal · Quantum Messaging</div>
        <div class="card-tags">
          <span class="tag tag-ai">OpenAI</span>
          <span class="tag tag-ai">Claude</span>
          <span class="tag tag-ai">Perplexity</span>
          <span class="tag tag-apple">Apple</span>
          <span class="tag tag-wearables">Meta Glasses</span>
          <span class="tag tag-privacy">Signal</span>
          <span class="tag tag-privacy">Threema</span>
        </div>
        <div class="read-time">~ 7 min read</div>
      </div>
      <span class="read-link">READ →</span>
    </a>

    <!-- FUTURE ENTRIES WILL BE ADDED ABOVE THIS LINE -->"""
if marker in html:
    html = html.replace(marker, card22, 1)
    changed += 1
    print("OK: March 22 card inserted")
else:
    print("ERROR: FUTURE ENTRIES marker not found")

# Verify LATEST badge count
badges = re.findall(r'class="latest-badge"', html)
print(f"\nVerification: {len(badges)} LATEST badge(s) present (should be 1)")

# Write output
shutil.copy(path, path + ".bak")
with open(path, "w", encoding="utf-8") as f:
    f.write(html)
print(f"\nDone: {changed}/3 changes applied. Backup saved as index.html.bak")
