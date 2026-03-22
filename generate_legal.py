import re

with open('/home/hp/ascensores-landing/index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

# Split around hero / content
header_part = re.split(r'<main', idx)[0]
if "<main" not in idx: # Fallback if no main
    header_part = re.split(r'<section class="hero"', idx)[0]

footer_part = "<footer class=\"footer\">" + re.split(r'<footer class="footer">', idx)[1]

pages = {
    "cookies.html": ("Política de Cookies", "Utilizamos cookies para mejorar la experiencia técnica y métrica de nuestro sitio web en Cartagena, Colombia y todo el territorio nacional."),
    "politica-de-privacidad.html": ("Política de Privacidad", "Ascensores Wolf Group respeta su privacidad. Sus datos recolectados en el formulario de contacto son usados exclusivamente para cotizaciones y mantenimiento de elevadores."),
    "terminos-de-servicio.html": ("Términos de Servicio", "Al utilizar nuestros servicios de instalación, modernización o mantenimiento, usted acepta los términos comerciales, garantías legales de partes y normativas ISO aplicables a Colombia.")
}

for filename, (title, desc) in pages.items():
    html = f"""{header_part}
    <section class="legal-section" style="padding: 10rem 0 5rem 0; min-height: 50vh;">
        <div class="container">
            <h1 style="font-family: var(--font-display); font-size: 3rem; margin-bottom: 2rem; color: var(--color-accent);">{title}</h1>
            <p style="color: var(--color-text-muted); font-size: 1.125rem; max-width: 800px; line-height: 1.8;">{desc}</p>
            <p style="color: var(--color-text-dim); margin-top: 2rem;">Última actualización: Marzo de 2026. Cartagena de Indias, Colombia.</p>
        </div>
    </section>
{footer_part}"""
    
    # Fix the brand span in the head/titles
    html = html.replace("<title>Ascensores Wolf Group -", f"<title>{title} | Ascensores Wolf Group")
    if "<title>" in html and not "..." in html:
        pass
        
    with open(f"/home/hp/ascensores-landing/{filename}", 'w', encoding='utf-8') as f:
        f.write(html)
        print(f"Created {filename}")
