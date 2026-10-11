#!/usr/bin/env python3
"""Build the blog: posts/<slug>.md -> <slug>/index.html, plus the post list at index.html.

Post format: front matter (title, date, summary, term) between --- lines,
then `## Heading` sections made of blank-line separated paragraphs.
`term` is the giscus discussion name for that post's comments.
"""
import html, re, glob, os, shutil

SITE = "Dead Bytes"
HEAD = '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="stylesheet" href="{root}assets/style.css">
</head>
<body>
'''

def slugify(t):
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')

def inline(t):
    t = html.escape(t, quote=False)
    return re.sub(r'([\w.]+@[\w.]+\.\w+)', r'<a href="mailto:\1">\1</a>', t)

def parse(path):
    raw = open(path).read()
    _, fm, body = raw.split('---\n', 2)
    meta = dict(l.split(': ', 1) for l in fm.strip().split('\n'))
    secs, cur = [], None
    for line in body.split('\n'):
        if line.startswith('## '):
            cur = (line[3:].strip(), []); secs.append(cur)
        elif line.strip() and cur:
            cur[1].append(line.strip())
    meta['sections'] = secs
    meta['slug'] = os.path.splitext(os.path.basename(path))[0]
    words = sum(len(p.split()) for _, ps in secs for p in ps)
    meta['mins'] = max(1, round(words / 220))
    return meta

def post_page(m):
    secs = [(slugify(h), h, ps) for h, ps in m['sections']]
    secs.append(('discussion', 'Like, share &amp; comment', None))
    toc = "\n".join(f'<li><a href="#{i}">{h}</a></li>' for i, h, _ in secs)
    body = "\n".join(
        f'<section id="{i}">\n<h2>{h}</h2>\n' + "\n".join(f'<p>{inline(p)}</p>' for p in ps) + '\n</section>'
        for i, h, ps in secs if ps)
    engage = f'''<section id="discussion" class="engage">
<h2>Like, share &amp; comment</h2>
<p class="hint">Enjoyed it? Pass it on, then react or comment below (sign in with GitHub).</p>
<div class="share">
<button id="native-share" hidden>Share…</button>
<button id="copy-link">Copy link</button>
<a id="share-x" target="_blank" rel="noopener">Post on X</a>
<a id="share-li" target="_blank" rel="noopener">LinkedIn</a>
</div>
<div id="comments" data-term="{html.escape(m['term'])}"></div>
</section>'''
    return (HEAD.format(title=html.escape(m['title']), desc=html.escape(m['summary']), root='../') + f'''<div class="wrap">
<aside class="side"><nav aria-label="Contents"><strong>Contents</strong><ol>
{toc}
</ol></nav></aside>
<main>
<a class="back" href="../">← All posts</a>
<h1>{html.escape(m['title'])}</h1>
<div class="by">{SITE} · {m['date']} · {m['mins']} min read · <a href="https://github.com/Dead-Bytes">GitHub</a></div>
<details><summary>Contents</summary><nav aria-label="Contents"><ol>
{toc}
</ol></nav></details>
{body}
{engage}
</main>
</div>
<script src="../assets/post.js"></script>
</body>
</html>
''')

def index_page(posts):
    cards = "\n".join(f'''<a class="card" href="{m['slug']}/">
<h2>{html.escape(m['title'])}</h2>
<div class="meta">{m['date']} · {m['mins']} min read</div>
<p>{html.escape(m['summary'])}</p>
</a>''' for m in posts)
    return (HEAD.format(title=f"{SITE} — Blog", desc="Notes on software, AI and the people who build it.", root='') + f'''<main class="list">
<h1>{SITE}</h1>
<div class="by">Notes on software, AI and the people who build it · <a href="https://github.com/Dead-Bytes">GitHub</a></div>
{cards}
</main>
</body>
</html>
''')

posts = sorted((parse(p) for p in glob.glob('posts/*.md')), key=lambda m: m['date'], reverse=True)
for m in posts:
    os.makedirs(m['slug'], exist_ok=True)
    open(f"{m['slug']}/index.html", 'w').write(post_page(m))
open('index.html', 'w').write(index_page(posts))
print(f"built {len(posts)} post(s)")
