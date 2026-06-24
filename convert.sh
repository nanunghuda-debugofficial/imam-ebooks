#!/bin/bash
# Convert all ebook markdown files to HTML

PROJECT_DIR="/home/ubuntu/.openclaw/workspace-dian-sastro/projects/imam-method"
HTML_DIR="$PROJECT_DIR/html"

# HTML template function
convert_ebook() {
    local md_file="$1"
    local html_file="$2"
    local title="$3"
    
    # Use pandoc if available, otherwise use python
    if command -v pandoc &> /dev/null; then
        pandoc "$md_file" -f markdown -t html5 --standalone -o "$html_file"
    else
        python3 -c "
import re, sys

with open('$md_file', 'r') as f:
    md = f.read()

# Simple markdown to HTML conversion
lines = md.split('\n')
html_parts = []
in_table = False
in_code = False
in_blockquote = False
in_ul = False

for line in lines:
    stripped = line.strip()
    
    # Code blocks
    if stripped.startswith('\`\`\`'):
        if in_code:
            html_parts.append('</code></pre>')
            in_code = False
        else:
            lang = stripped[3:].strip()
            html_parts.append(f'<pre><code class=\"language-{lang}\">' if lang else '<pre><code>')
            in_code = True
        continue
    
    if in_code:
        html_parts.append(line.replace('<', '&lt;').replace('>', '&gt;'))
        continue
    
    # Skip empty lines
    if not stripped:
        if in_ul:
            html_parts.append('</ul>')
            in_ul = False
        if in_blockquote:
            html_parts.append('</blockquote>')
            in_blockquote = False
        html_parts.append('')
        continue
    
    # Horizontal rule
    if stripped == '---':
        html_parts.append('<hr/>')
        continue
    
    # Blockquote
    if stripped.startswith('>'):
        text = stripped[1:].strip()
        if stripped.startswith('> **'):
            # Bold blockquote
            text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        if not in_blockquote:
            html_parts.append('<blockquote>')
            in_blockquote = True
        html_parts.append(f'<p>{text}</p>')
        continue
    
    if in_blockquote and not stripped.startswith('>'):
        html_parts.append('</blockquote>')
        in_blockquote = False
    
    # Headers
    if stripped.startswith('# '):
        html_parts.append(f'<h1>{stripped[2:]}</h1>')
        continue
    elif stripped.startswith('## '):
        html_parts.append(f'<h2>{stripped[3:]}</h2>')
        continue
    elif stripped.startswith('### '):
        html_parts.append(f'<h3>{stripped[4:]}</h3>')
        continue
    elif stripped.startswith('#### '):
        html_parts.append(f'<h4>{stripped[5:]}</h4>')
        continue
    
    # Table
    if '|' in stripped and stripped.startswith('|'):
        cells = [c.strip() for c in stripped.split('|')[1:-1]]
        if all(set(c) <= set('-: ') for c in cells):
            continue  # skip separator
        if not in_table:
            html_parts.append('<table><thead><tr>')
            for c in cells:
                c = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', c)
                c = re.sub(r'\*(.*?)\*', r'<em>\1</em>', c)
                html_parts.append(f'<th>{c}</th>')
            html_parts.append('</tr></thead><tbody>')
            in_table = True
        else:
            html_parts.append('<tr>')
            for c in cells:
                c = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', c)
                c = re.sub(r'\*(.*?)\*', r'<em>\1</em>', c)
                html_parts.append(f'<td>{c}</td>')
            html_parts.append('</tr>')
        continue
    else:
        if in_table:
            html_parts.append('</tbody></table>')
            in_table = False
    
    # List items
    if stripped.startswith('- ') or stripped.startswith('* '):
        text = stripped[2:]
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
        if not in_ul:
            html_parts.append('<ul>')
            in_ul = True
        html_parts.append(f'<li>{text}</li>')
        continue
    
    # Numbered list
    if re.match(r'^\d+\.\s', stripped):
        text = re.sub(r'^\d+\.\s', '', stripped)
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
        if not in_ul:
            html_parts.append('<ol>')
            in_ul = True
        html_parts.append(f'<li>{text}</li>')
        continue
    else:
        if in_ul:
            html_parts.append('</ul>')  # or </ol>
            in_ul = False
    
    # Paragraph with inline formatting
    text = stripped
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = re.sub(r'\`(.*?)\`', r'<code>\1</code>', text)
    html_parts.append(f'<p>{text}</p>')

if in_table:
    html_parts.append('</tbody></table>')
if in_ul:
    html_parts.append('</ul>')
if in_blockquote:
    html_parts.append('</blockquote>')

body = '\n'.join(html_parts)

full_html = f'''<!DOCTYPE html>
<html lang=\"id\">
<head>
<meta charset=\"UTF-8\">
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
<title>{title}</title>
<style>
:root {{
  --primary: #2563eb;
  --primary-dark: #1d4ed8;
  --bg: #f8fafc;
  --text: #1e293b;
  --text-light: #64748b;
  --border: #e2e8f0;
  --accent: #f59e0b;
  --success: #10b981;
  --danger: #ef4444;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.7;
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}}
h1 {{ font-size: 2.2em; color: var(--primary); margin: 1.5em 0 0.5em; border-bottom: 3px solid var(--primary); padding-bottom: 0.3em; }}
h2 {{ font-size: 1.6em; color: var(--primary-dark); margin: 1.5em 0 0.5em; border-bottom: 1px solid var(--border); padding-bottom: 0.2em; }}
h3 {{ font-size: 1.3em; color: #334155; margin: 1.2em 0 0.4em; }}
h4 {{ font-size: 1.1em; color: #475569; margin: 1em 0 0.3em; }}
p {{ margin: 0.8em 0; }}
a {{ color: var(--primary); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
blockquote {{
  border-left: 4px solid var(--accent);
  padding: 0.8em 1.2em;
  margin: 1.2em 0;
  background: #fffbeb;
  border-radius: 0 8px 8px 0;
  font-style: italic;
}}
code {{
  background: #f1f5f9;
  padding: 0.15em 0.4em;
  border-radius: 4px;
  font-size: 0.9em;
  font-family: 'Fira Code', monospace;
}}
pre {{
  background: #1e293b;
  color: #e2e8f0;
  padding: 1.2em;
  border-radius: 8px;
  overflow-x: auto;
  margin: 1em 0;
}}
pre code {{ background: none; color: inherit; }}
table {{
  width: 100%;
  border-collapse: collapse;
  margin: 1em 0;
}}
th, td {{
  padding: 0.6em 0.8em;
  border: 1px solid var(--border);
  text-align: left;
}}
th {{ background: var(--primary); color: white; }}
tr:nth-child(even) {{ background: #f8fafc; }}
ul, ol {{ margin: 0.8em 0; padding-left: 2em; }}
li {{ margin: 0.4em 0; }}
hr {{ border: none; border-top: 2px solid var(--border); margin: 2em 0; }}
strong {{ color: #1e293b; }}
em {{ color: var(--text-light); }}
@media (max-width: 600px) {{
  body {{ padding: 12px; }}
  h1 {{ font-size: 1.6em; }}
  h2 {{ font-size: 1.3em; }}
}}
</style>
</head>
<body>
<nav style=\"margin-bottom: 2em; padding: 1em; background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);\">
<a href=\"index.html\">← Kembali ke Index</a>
</nav>
<article>
{body}
</article>
<footer style=\"margin-top: 3em; padding: 1.5em; text-align: center; color: var(--text-light); border-top: 1px solid var(--border);\">
<p>© 2026 Imam Business Hacking Methods</p>
</footer>
</body>
</html>'''

with open('$html_file', 'w') as f:
    f.write(full_html)
print(f'Converted: $html_file')
"
    fi
}

# Convert all ebooks
ebooks=(
    "ebook-1-mvp-test/EBOOK-MINI-MVP-TEST.md:mini-mvp-test.html:Mini-MVP Test - Validasi Ide Bisnis dalam 14 Hari"
    "ebook-2-pirate-first/EBOOK-PIRATE-FIRST.md:pirate-first.html:Pirate First - Bootstrapping Bisnis Tanpa Investor"
    "ebook-3-reverse-engineer/EBOOK-REVERSE-ENGINEER.md:reverse-engineer.html:Reverse Engineer - Bongkar Rahasia Bisnis Pesaing"
    "ebook-4-body-checkup/EBOOK-BODY-CHECKUP.md:body-checkup.html:Body Checkup - Diagnosa Kesehatan Bisnis"
    "ebook-5-five-whys/EBOOK-FIVE-WHYS.md:five-whys.html:Five Whys - Teknik Sederhana untuk Masalah Kompleks"
    "ebook-6-business-xray/EBOOK-BUSINESS-XRAY.md:business-xray.html:Business X-Ray - Lihat Bisnis dari Dalam"
    "ebook-7-cell-division/EBOOK-CELL-DIVISION.md:cell-division.html:Cell Division - Strategi Membagi Tim"
    "ebook-8-gamification/EBOOK-GAMIFICATION.md:gamification.html:Gamification - Teknik Game untuk Performa Bisnis"
    "ebook-9-compass-leadership/EBOOK-COMPASS-LEADERSHIP.md:compass-leadership.html:Compass Leadership - Navigasi Kepemimpinan"
    "ebook-10-scale-trigger/EBOOK-SCALE-TRIGGER.md:scale-trigger.html:Scale Trigger - Kapan Harus Scale Up"
)

for entry in "${ebooks[@]}"; do
    IFS=':' read -r md_file html_file title <<< "$entry"
    echo "Converting: $title"
    convert_ebook "$PROJECT_DIR/$md_file" "$HTML_DIR/$html_file" "$title"
done

echo "Done! All ebooks converted to HTML."
