import os
import re

base_dir = "/home/hp/ascensores-landing"
html_files = []
for root, _, files in os.walk(base_dir):
    for f in files:
        if f.endswith(".html"):
            html_files.append(os.path.join(root, f))

# Regex to find href="something.html"
link_re = re.compile(r'href=[\'\"]([^\'\"#\?]+\.html)(#[^\'\"]*)?[\'\"]')

for html_file in html_files:
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()

    def replacer(match):
        link = match.group(1)
        hash_frag = match.group(2) or ""
        
        # Handle index.html specially
        if link == "index.html" or link == "../index.html":
            # Just keep the relative path without index.html
            new_link = link.replace("index.html", "")
            if new_link == "": new_link = "./"
        elif link.endswith("/index.html"):
            new_link = link[:-10] # Removes index.html
        else:
            new_link = link[:-5] # Removes .html
            
        return f'href="{new_link}{hash_frag}"'

    new_content = link_re.sub(replacer, content)
    
    if new_content != content:
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated links in {os.path.relpath(html_file, base_dir)}")
