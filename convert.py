#!/usr/bin/env python3
"""Convert all ebook markdown files to styled HTML."""

import re
import os

PROJECT_DIR = "/home/ubuntu/.openclaw/workspace-dian-sastro/projects/imam-method"
HTML_DIR = os.path.join(PROJECT_DIR, "html")

EBOOKS = [
    ("ebook-1-mvp-test/EBOOK-MINI-MVP-TEST.md", "mini-mvp-test.html", "Mini-MVP Test - Validasi Ide Bisnis dalam 14 Hari"),
    ("ebook-2-pirate-first/EBOOK-PIRATE-FIRST.md", "pirate-first.html", "Pirate First - Bootstrapping Bisnis Tanpa Investor"),
    ("ebook-3-reverse-engineer/EBOOK-REVERSE-ENGINEER.md", "reverse-engineer.html", "Reverse Engineer - Bongkar Rahasia Bisnis Pesaing"),
    ("ebook-4-body-checkup/EBOOK-BODY-CHECKUP.md", "body-checkup.html", "Body Checkup - Diagnosa Kesehatan Bisnis"),
    ("ebook-5-five-whys/EBOOK-FIVE-WHYS.md", "five-whys.html", "Five Whys - Teknik Sederhana untuk Masalah Kompleks"),
    ("ebook-6-business-xray/EBOOK-BUSINESS-XRAY.md", "business-xray.html", "Business X-Ray - Lihat Bisnis dari Dalam"),
    ("ebook-7-cell-division/EBOOK-CELL-DIVISION.md", "cell-division.html", "Cell Division - Strategi Membagi Tim"),
    ("ebook-8-gamification/EBOOK-GAMIFICATION.md", "gamification.html", "Gamification - Teknik Game untuk Performa Bisnis"),
    ("ebook-9-compass-leadership/EBOOK-COMPASS-LEADERSHIP.md", "compass-leadership.html", "Compass Leadership - Navigasi Kepemimpinan"),
    ("ebook-10-scale-trigger/EBOOK-SCALE-TRIGGER.md", "scale-trigger.html", "Scale Trigger - Kapan Harus Scale Up"),
]

CSS = """
:root {
  --primary: #2563eb;
  --primary-dark: #1d4ed8;
  --bg: #f8fafc;
  --text: #1e293b;
  --text-light: #64748b;
  --border: #e2e8f0;
  --accent: #f59e0b;
  --success: #10b981;
  --danger: #ef4444;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.7;
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}
h1 { font-size: 2.2em; color: var(--primary); margin: 1.5em 0 0.5em; border-bottom: 3px solid var(--primary); padding-bottom: 0.3em; }
h2 { font-size: 1.6em; color: var(--primary-dark); margin: 1.5em 0 0.5em; border-bottom: 1px solid var(--border); padding-bottom: 0.2em; }
h3 { font-size: 1.3em; color: #334155; margin: 1.2em 0 0.4em; }
h4 { font-size: 1.1em; color: #475569; margin: 1em 0 0.3em; }
p { margin: 0.8em 0; }
a { color: var(--primary); text-decoration: none; }
a:hover { text-decoration: underline; }
blockquote {
  border-left: 4px solid var(--accent);
  padding: 0.8em 1.2em;
  margin: 1.2em 0;
  background: #fffbeb;
  border-radius: 0 8px 8px 0;
  font-style: italic;
}
code {
  background: #f1f5f9;
  padding: 0.15em 0.4em;
  border-radius: 4px;
  font-size: 0.9em;
  font-family: 'Fira Code', monospace;
}
pre {
  background: #1e293b;
  color: #e2e8f0;
  padding: 1.2em;
  border-radius: 8px;
  overflow-x: auto;
  margin: 1em 0;
}
pre code { background: none; color: inherit; }
table {
  width: 100%;
  border-collapse: collapse;
  margin: 1em 0;
}
th, td {
  padding: 0.6em 0.8em;
  border: 1px solid var(--border);
  text-align: left;
}
th { background: var(--primary); color: white; }
tr:nth-child(even) { background: #f8fafc; }
ul, ol { margin: 0.8em 0; padding-left: 2em; }
li { margin: 0.4em 0; }
hr { border: none; border-top: 2px solid var(--border); margin: 2em 0; }
strong { color: #1e293b; }
@media (max-width: 600px) {
  body { padding: 12px; }
  h1 { font-size: 1.6em; }
  h2 { font-size: 1.3em; }
}
"""

NAV = '<nav style="margin-bottom: 2em; padding: 1em; background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);"><a href="index.html">← Kembali ke Index</a></nav>'
FOOTER = '<footer style="margin-top: 3em; padding: 1.5em; text-align: center; color: var(--text-light); border-top: 1px solid var(--border);"><p>© 2026 Imam Business Hacking Methods</p></footer>'


def inline(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    return text


def convert_md(md):
    lines = md.split('\n')
    parts = []
    in_table = False
    in_code = False
    in_bq = False
    in_ul = False
    list_type = 'ul'

    for line in lines:
        s = line.strip()

        if s.startswith('```'):
            if in_code:
                parts.append('</code></pre>')
                in_code = False
            else:
                lang = s[3:].strip()
                cls = f' class="language-{lang}"' if lang else ''
                parts.append(f'<pre><code{cls}>')
                in_code = True
            continue

        if in_code:
            parts.append(line.replace('<', '&lt;').replace('>', '&gt;'))
            continue

        if not s:
            if in_ul:
                parts.append(f'</{list_type}>')
                in_ul = False
            if in_bq:
                parts.append('</blockquote>')
                in_bq = False
            parts.append('')
            continue

        if s == '---':
            parts.append('<hr/>')
            continue

        if s.startswith('>'):
            text = inline(s[1:].strip())
            if not in_bq:
                parts.append('<blockquote>')
                in_bq = True
            parts.append(f'<p>{text}</p>')
            continue

        if in_bq and not s.startswith('>'):
            parts.append('</blockquote>')
            in_bq = False

        if s.startswith('# '):
            parts.append(f'<h1>{inline(s[2:])}</h1>')
            continue
        elif s.startswith('## '):
            parts.append(f'<h2>{inline(s[3:])}</h2>')
            continue
        elif s.startswith('### '):
            parts.append(f'<h3>{inline(s[4:])}</h3>')
            continue
        elif s.startswith('#### '):
            parts.append(f'<h4>{inline(s[5:])}</h4>')
            continue

        if '|' in s and s.startswith('|'):
            cells = [c.strip() for c in s.split('|')[1:-1]]
            if all(set(c) <= set('-: ') for c in cells):
                continue
            if not in_table:
                parts.append('<table><thead><tr>')
                for c in cells:
                    parts.append(f'<th>{inline(c)}</th>')
                parts.append('</tr></thead><tbody>')
                in_table = True
            else:
                parts.append('<tr>')
                for c in cells:
                    parts.append(f'<td>{inline(c)}</td>')
                parts.append('</tr>')
            continue
        else:
            if in_table:
                parts.append('</tbody></table>')
                in_table = False

        if s.startswith('- ') or s.startswith('* '):
            text = inline(s[2:])
            if not in_ul or list_type != 'ul':
                if in_ul:
                    parts.append(f'</{list_type}>')
                parts.append('<ul>')
                in_ul = True
                list_type = 'ul'
            parts.append(f'<li>{text}</li>')
            continue

        if re.match(r'^\d+\.\s', s):
            text = inline(re.sub(r'^\d+\.\s', '', s))
            if not in_ul or list_type != 'ol':
                if in_ul:
                    parts.append(f'</{list_type}>')
                parts.append('<ol>')
                in_ul = True
                list_type = 'ol'
            parts.append(f'<li>{text}</li>')
            continue
        else:
            if in_ul:
                parts.append(f'</{list_type}>')
                in_ul = False

        parts.append(f'<p>{inline(s)}</p>')

    if in_table:
        parts.append('</tbody></table>')
    if in_ul:
        parts.append(f'</{list_type}>')
    if in_bq:
        parts.append('</blockquote>')

    return '\n'.join(parts)


def make_html(title, body):
    return f'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{CSS}</style>
</head>
<body>
{NAV}
<article>
{body}
</article>
{FOOTER}
</body>
</html>'''


def main():
    for md_rel, html_name, title in EBOOKS:
        md_path = os.path.join(PROJECT_DIR, md_rel)
        html_path = os.path.join(HTML_DIR, html_name)
        with open(md_path, 'r') as f:
            md = f.read()
        body = convert_md(md)
        html = make_html(title, body)
        with open(html_path, 'w') as f:
            f.write(html)
        print(f"✅ {html_name}")

    # Generate index.html
    index_items = []
    for _, html_name, title in EBOOKS:
        num = html_name.split('-')[0].replace('mini','').replace('mvp','')
        # Get clean title
        clean = title.split(' - ')[0] if ' - ' in title else title
        desc = title.split(' - ')[1] if ' - ' in title else ''
        index_items.append(f'<li><a href="{html_name}"><strong>{clean}</strong></a><br/><small>{desc}</small></li>')

    index_html = f'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>10 Ebook - Imam Business Hacking Methods</title>
<style>
:root {{ --primary: #2563eb; --primary-dark: #1d4ed8; --bg: #f8fafc; --text: #1e293b; --text-light: #64748b; --border: #e2e8f0; --accent: #f59e0b; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: var(--text); line-height: 1.7; padding: 20px; max-width: 800px; margin: 0 auto; }}
h1 {{ color: var(--primary); margin: 0.5em 0; font-size: 2em; }}
h2 {{ color: var(--primary-dark); margin: 1.5em 0 0.5em; font-size: 1.4em; }}
ul {{ list-style: none; padding: 0; }}
li {{ background: white; padding: 1em 1.2em; margin: 0.6em 0; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); border-left: 4px solid var(--primary); }}
li a {{ color: var(--primary); text-decoration: none; font-size: 1.1em; }}
li a:hover {{ text-decoration: underline; }}
li small {{ color: var(--text-light); font-size: 0.85em; }}
.subtitle {{ color: var(--text-light); margin-bottom: 2em; }}
footer {{ margin-top: 3em; padding: 1.5em; text-align: center; color: var(--text-light); border-top: 1px solid var(--border); }}
@media (max-width: 600px) {{ body {{ padding: 12px; }} h1 {{ font-size: 1.5em; }} }}
</style>
</head>
<body>
<h1>📦 10 Ebook — Imam Business Hacking Methods</h1>
<p class="subtitle">Koleksi 10 ebook strategi bisnis hasil pengalaman nyata di lapangan.</p>
<h2>Daftar Ebook</h2>
<ul>
{"".join(index_items)}
</ul>
<footer><p>© 2026 Imam Business Hacking Methods — Dibuat oleh Dian Sastro 🎯</p></footer>
</body>
</html>'''

    with open(os.path.join(HTML_DIR, 'index.html'), 'w') as f:
        f.write(index_html)
    print("✅ index.html")
    print("\n🎉 Semua ebook berhasil dikonversi ke HTML!")


if __name__ == '__main__':
    main()
