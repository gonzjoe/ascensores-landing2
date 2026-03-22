import os

directory = "/home/hp/ascensores-landing"

replacements = {
    "+34900000000": "+573000000000",
    "+34600000000": "+573000000000",
    "+34-900-000-000": "+57-300-000-0000",
    "Comuníquese Urgente al 900": "Línea Urgente +57 300",
    "Calle Principal 123": "Bocagrande, Cra 2 # 12-34",
    "\"Madrid\"": "\"Cartagena\"",
    "\"ES\"": "\"CO\"",
    "toda España": "toda Colombia",
    "en España": "en Colombia",
    "Calle Example, 123<br>28001 Madrid, España": "Bocagrande, Cra 2 # 12-34<br> Cartagena, Colombia",
    "MAPA - Calle Example, 123, Madrid": "MAPA - Cartagena, Colombia",
    "+34 900 000 000": "+57 300 000 0000"
}

html_files = []
for root, _, files in os.walk(directory):
    for f in files:
        if f.endswith(".html"):
            html_files.append(os.path.join(root, f))

for fpath in html_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
        
    original = content
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    if content != original:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Localized: {os.path.relpath(fpath, directory)}")
