import os
import re

directory = "/home/hp/ascensores-landing/servicios"

faqs_data = {
    "con-cuarto-maquina.html": [
        ("¿Es obligatorio tener el cuarto de máquinas en la azotea?", "Generalmente sí en modelos antiguos por tracción directa. Depende del diferencial y sistema de poleas."),
        ("¿Cada cuánto se debe revisar el motor y las poleas tradicionales?", "La normativa legal exige una revisión preventiva obligatoria mensual."),
        ("¿Se puede reducir el ruido que el motor transmite al último piso habitacional?", "Por supuesto. Nuestros técnicos instalan silentblocks de última generación."),
        ("¿Tienen stock de piezas para modelos o maquinarias muy antiguas?", "Trabajamos con una amplia red de proveedores multimarca y poseemos repuestos."),
        ("¿Es más económico el mantenimiento de este prototipo tradicional de ascensor?", "Absolutamente. Debido a su diseño mecánico robusto y facilidad de acceso.")
    ],
    "sin-cuarto-maquina.html": [
        ("¿Dónde se encuentra exactamente el motor si no existe cuarto de máquinas?", "El grupo tractor se instala en el extremo superior de las propias guías dentro del hueco."),
        ("¿Son estructuralmente más ruidosos al estar operando directamente en el hueco?", "Todo lo contrario. Utilizan mecanismos insonoros gearless provistos de imanes permanentes."),
        ("¿Qué ventajas energéticas ecológicas tiene concretamente el MRL?", "Logran ser hasta un 50% más eficientes en consumo que los hidráulicos clásicos."),
        ("¿Cómo realizan sus técnicos el rescate urgente de pasajeros?", "El cuadro maestro de control se instala con seguridad en el marco protector superior."),
        ("¿Se requiere cumplir con alguna temperatura especial?", "Sí. Exigimos un estándar de ventilación natural en su parte alta para disipación de calor.")
    ],
    "panoramicos.html": [
        ("¿El cristal térmico de la cabina requiere limpieza especializada?", "Requiere inspecciones técnicas mensuales para cerciorarse de microfisuras."),
        ("¿Qué ocurre en el mantenimiento si el elevador es para exteriores?", "Incluye purgar cajas eléctricas y lubricar tensores en acero inoxidable."),
        ("¿Son realmente seguros si el cristal llegara a golpearse?", "Totalmente. Utilizan forzosamente cristales laminados estructurales de seguridad."),
        ("¿Cómo evitan ustedes que los rodamientos y guías luzcan feos?", "Instalamos guías recubiertas y patines secos de teflón sin manchas grasas."),
        ("¿Requieren servicios mecánicos de climatización (A/C) integrados?", "Recomendables por la radiación solar. Los ingenieros reparan su aire acondicionado interno.")
    ],
    "carga.html": [
        ("¿Realizan mantenimientos en horarios de inactividad industrial?", "Por supuesto. En frigoríficos o fábricas adecuamos mantenimientos en la noche u horarios especiales."),
        ("¿Cada cuánto tiempo deben tensar los cables metálicos de tracción?", "Revisamos con dinamómetro de extrema precisión la ecualización tensora mes a mes."),
        ("¿Cuentan con capacidad para ejecutar pruebas dinámicas de impacto?", "Ejecutamos ensayos de rotura periódica saturando la cabina con test estandarizados."),
        ("¿Qué diferencia técnica hay entre uno hidráulico y uno eléctrico?", "El hidráulico requiere control del aceite; el eléctrico control en poleas."),
        ("¿Arreglan también el desgaste del suelo ranurado de la placa?", "Ejecutamos reemplazos modulares de la placa chapa dañada interior del montacargas pesado.")
    ],
    "vehiculares.html": [
        ("¿El sistema previene que ocurra un escalón al meter el coche?", "Ese es nuestro mayor enfoque operativo para garajes vehiculares. Calibramos válvulas micro de renivelación rápida."),
        ("¿Estos colosos exigen inspección normativa especial del gobierno?", "Requieren certificación. Verificamos barreras láser gigantes que impidan rayar vehículos."),
        ("¿Qué velocidad y protocolo de emergencia en atrapamiento garantizan?", "Nuestro manual tiene pasos mecánicos usando bomba neumática sin luz para el desalojo rápido."),
        ("¿Cómo evalúan el mantenimiento a semáforos integrados de advertencia?", "La maniobrabilidad depende absolutamente tanto del elevador físico bajando como sistema luminoso y loops asfálticos."),
        ("¿Garantiza durabilidad este mega-ascensor hidráulico operado con cilindro?", "Evaluamos paralelismo de embolos, aceites ecológicos y cambio de filtros logrando operatividad vital.")
    ],
    "camilleros.html": [
        ("¿Cómo logran un ajuste tan liso en la llegada a planta pensando en operados?", "Para clínica aplicamos tecnología inteligente VVVF sin generar tirones dolorosos o ruidosos."),
        ("¿Un mecánico no propagará micro-partículas antihigiénicas entre las salas blancas?", "Empleamos botas especializadas estériles y químicos inodoros no inflamables o tóxicos para el quirófano general."),
        ("¿De qué manera priorizan nivel respuesta frente a otros clientes urbanos?", "La urgencia es Nivel Cero y la asistencia llega en minutos frente a paros vitales de ascensores camilleros hospitalarios."),
        ("¿Hacen prueba a la red generador eléctrico en cortes públicos en hospitales?", "Cercioramos maniobras de rescate automatizada a piso con la batería médica propia interna para que abran las compuertas."),
        ("¿El mantenimiento al panel del ascensor no estropeará aleaciones por la lejía sanitaria?", "Botoneras biotecnológicas garantizadas resistentes a líquidos e impermeabilidad química hospitalaria desinfectante exigida.")
    ],
    "modernizacion.html": [
        ("¿Cuánto lapso sin ascensor deberé soportar si encaro esta urgente restructuración?", "Una modificación parcial tarda unos dias y total a veces unas 3 semanas super efectivas planificadas paso a paso."),
        ("¿Resulta obligatorio demoler mi valioso elevador metálico antiguo destrozando la pared?", "Jamás. Mantenemos el marco hierro, vigas, guía sólidas de toda base adaptándolo a las nuevas piezas electrónicas eficientes nuevas de última onda moderna."),
        ("¿Cuál será la ganancia inmediata desde el primerísimo instante en que lo use moderno?", "Suavidad milimétrica libre en sacudidas abruptas molestas de ruidos feos e inmensa eficiencia del uso eléctrico reducida muy dramáticamente."),
        ("¿Cumple la obra sobre carcasas viejas con normativas estrictas en inclusión cívica y auditivas rampa?", "Homologamos absoluto en Braille parlante botones accesibles a ciegos discapacitados sillas ruedas rampas etc legal aprobada de pleno sin falla de registro en edificios habitacionales del siglo XXI."),
        ("¿Si adelanto pagos al recambio me otorgan pólizas legales absolutas de fabrica incondicional repuestos?", "Protección ética con Wolf Group integral sobre la mano obra motores piezas nuevas traídas importadas tal cual un elevador del paquete entero comprado hace 1 día entregado brillante al cliente.")
    ]
}

cta_banner_html = """
    <!-- CTA Final Banner -->
    <section class="cta-section cta-section--enhanced" style="padding: 5rem 0;">
        <div class="container">
            <div class="cta-content-wrapper" style="background: linear-gradient(135deg, rgba(201,160,80,0.1) 0%, rgba(0,0,0,0.8) 100%); padding: 4rem 2rem; border-radius: 12px; text-align: center; border: 1px solid rgba(201,160,80,0.3);">
                <h2 class="cta-section__title" style="margin-bottom: 1rem; font-size: 2.25rem; text-transform: uppercase;">¿Listo para mejorar la seguridad operativa de su ascensor?</h2>
                <p class="cta-section__text" style="color: #d4d4d8; margin-bottom: 2.5rem; max-width: 600px; margin-left: auto; margin-right: auto; font-size: 1.125rem;">Déjelo en manos de verdaderos expertos formados. Solicite una inspección técnica de campo sin ningún costo o letra pequeña oculta.</p>
                <div class="cta-section__buttons" style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                    <a href="../contacto.html" class="btn btn--primary" title="Ir a Solicitar presupuesto">Solicitar Presupuesto Técnico</a>
                    <a href="tel:+34900000000" class="btn btn--secondary" title="Llamada Urgente 24/7">Comuníquese Urgente al 900</a>
                </div>
            </div>
        </div>
    </section>
"""

for fname, qas in faqs_data.items():
    fpath = os.path.join(directory, fname)
    if not os.path.exists(fpath):
        continue
    
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    faq_html = "    <!-- Preguntas Frecuentes -->\n"
    faq_html += "    <section class=\"service-faq\" style=\"padding: 5rem 0; background: var(--color-background-alt, #111);\">\n"
    faq_html += "        <div class=\"container\">\n"
    faq_html += "            <header class=\"section-header\" style=\"text-align: center; margin-bottom: 3rem;\">\n"
    faq_html += "                <span class=\"section-header__badge\" style=\"color: var(--color-accent, #c9a050); text-transform: uppercase; letter-spacing: 2px; font-size: 0.875rem; font-weight: 600;\">DUDAS COMUNES</span>\n"
    faq_html += "                <h2 class=\"section-header__title\" style=\"font-size: 2.5rem; text-transform: uppercase;\"><span>Preguntas</span><span class=\"section-header__title-accent\" style=\"color: var(--color-accent, #c9a050);\"> Frecuentes</span></h2>\n"
    faq_html += "            </header>\n"
    faq_html += "            <div class=\"faq-grid\" style=\"max-width: 800px; margin: 0 auto; display: flex; flex-direction: column; gap: 1rem;\">\n"

    for q, a in qas:
        faq_html += "                <details class=\"faq-item\" style=\"background: rgba(255,255,255,0.05); border-radius: 8px; padding: 1.5rem; border: 1px solid rgba(255,255,255,0.1);\">\n"
        faq_html += f"                    <summary class=\"faq-item__question\" style=\"font-size: 1.125rem; font-weight: 600; cursor: pointer; list-style: none; display: flex; justify-content: space-between; align-items: center;\">{q}</summary>\n"
        faq_html += f"                    <p class=\"faq-item__answer\" style=\"margin-top: 1rem; color: #a1a1aa; line-height: 1.6;\">{a}</p>\n"
        faq_html += "                </details>\n"
        
    faq_html += "            </div>\n"
    faq_html += "        </div>\n"
    faq_html += "    </section>\n\n"
    faq_html += cta_banner_html

    start_tag = '<!-- Preguntas Frecuentes -->'
    end_tag = '<!-- Footer -->'
    
    if start_tag in content and end_tag in content:
        start_idx = content.find(start_tag)
        end_idx = content.find(end_tag)
        if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
            new_content = content[:start_idx] + faq_html + "\n\n    " + content[end_idx:]
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Personalizadas las FAQs en: {fname}")

