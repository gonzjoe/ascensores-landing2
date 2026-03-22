import os

directory = "/home/hp/ascensores-landing/servicios"

for fname in os.listdir(directory):
    if not fname.endswith(".html"): continue
    
    fpath = os.path.join(directory, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace inline gold fallbacks and variables in service pages with blue
    new_content = content.replace("#c9a050", "#005aa9")
    new_content = new_content.replace("rgba(201,160,80,", "rgba(0,90,169,")
    
    if new_content != content:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Colors updated in: {fname}")
