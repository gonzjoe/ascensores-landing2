import os
import re

base_dir = "/home/hp/ascensores-landing"

html_files = []
for root, _, files in os.walk(base_dir):
    for f in files:
        if f.endswith(".html"):
            html_files.append(os.path.join(root, f))

link_re = re.compile(r'(href|src)="([^"]+)"')
errors = []

for html_file in html_files:
    file_dir = os.path.dirname(html_file)
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    matches = link_re.findall(content)
    for attr, link in matches:
        if link.startswith('http') or link.startswith('mailto:') or link.startswith('tel:') or link.startswith('data:') or link.startswith('#'):
            continue
            
        clean_link = link.split('?')[0].split('#')[0]
        if not clean_link: continue
        
        target_path = os.path.normpath(os.path.join(file_dir, clean_link))
        
        if not os.path.exists(target_path):
            errors.append(f"Broken: {os.path.relpath(html_file, base_dir)} -> {link}")

if errors:
    print("QA Report - Broken Links Found:")
    for e in sorted(set(errors)):
        print(e)
else:
    print("QA Report: All internal links and assets exist! No 404s found.")
