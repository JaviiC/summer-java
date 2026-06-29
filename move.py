import re
import os

with open('intensivo.html', 'r', encoding='utf-8') as f:
    intensivo = f.read()
    
with open('index.html', 'r', encoding='utf-8') as f:
    index = f.read()

# 1. Extract Ace script
ace_script = '<script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.32.7/ace.min.js"></script>'
intensivo = intensivo.replace(ace_script + '\n', '')

# 2. Extract CSS
css_match = re.search(r'(?s)(    /\* ─── PLAYGROUND ─── \*/.*?)(    /\* ─── RESPONSIVE ─── \*/)', intensivo)
if css_match:
    css_content = css_match.group(1)
    intensivo = intensivo.replace(css_content, '')
else:
    print("CSS not found!")

# 3. Extract HTML
html_match = re.search(r'(?s)(  <!-- PLAYGROUND -->.*?</section>\n)(?=\n  <!-- TIMELINE DETALLADO -->)', intensivo)
if html_match:
    html_content = html_match.group(1)
    intensivo = intensivo.replace(html_content, '')
else:
    print("HTML not found!")

# 4. Extract JS
js_match = re.search(r'(?s)(    /\* ── PLAYGROUND ── \*/.*?)(\n  </script>)', intensivo)
if js_match:
    js_content = js_match.group(1)
    intensivo = intensivo.replace(js_content, '')
else:
    print("JS not found!")

# Now process index.html

# Insert Ace script
index = index.replace('</style>', '</style>\n  ' + ace_script)

# Insert CSS before RESPONSIVE
index = index.replace('    /* ─── RESPONSIVE ─── */', css_content + '    /* ─── RESPONSIVE ─── */')

# Replace SOBRE MI with Playground HTML
sobre_mi_match = re.search(r'(?s)(  <!-- SOBRE MÍ -->.*?)(  <div class="divider"></div>\n\n  <!-- FAQ -->)', index)
if sobre_mi_match:
    index = index.replace(sobre_mi_match.group(1), html_content)
else:
    print("Sobre Mi not found!")
    
# Update Playground section id
index = index.replace('<section class="playground-section">', '<section class="playground-section" id="playground">')

# Replace JS before </script>
index = index.replace('\n  </script>', '\n\n' + js_content + '\n  </script>')

# Replace links
index = index.replace('#sobre-mi', '#playground')
index = index.replace('>Sobre mí<', '>Pruébalo<')

# Also delete the floating divider that might be left in intensivo.html
intensivo = intensivo.replace('  <div class="divider"></div>\n\n  <div class="divider"></div>', '  <div class="divider"></div>')

with open('intensivo.html', 'w', encoding='utf-8') as f:
    f.write(intensivo)
    
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index)

print("Done moving sections.")
