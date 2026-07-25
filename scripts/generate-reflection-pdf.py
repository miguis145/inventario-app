from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output" / "pdf"
OUTPUT_PATH = OUTPUT_DIR / "Informe_Reflexion_CI_CD_Inventario.pdf"

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_X = 18 * mm
MARGIN_TOP = 21 * mm
MARGIN_BOTTOM = 17 * mm

NAVY = colors.HexColor("#132238")
BLUE = colors.HexColor("#1D4ED8")
CYAN = colors.HexColor("#0EA5A4")
LIGHT_BLUE = colors.HexColor("#EAF2FF")
LIGHT_CYAN = colors.HexColor("#E7F8F6")
LIGHT_GRAY = colors.HexColor("#F3F5F7")
MID_GRAY = colors.HexColor("#64748B")
DARK = colors.HexColor("#172033")
RED = colors.HexColor("#B42318")
GREEN = colors.HexColor("#147D64")


def register_fonts():
    regular = Path("C:/Windows/Fonts/arial.ttf")
    bold = Path("C:/Windows/Fonts/arialbd.ttf")
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("ReportRegular", str(regular)))
        pdfmetrics.registerFont(TTFont("ReportBold", str(bold)))
        return "ReportRegular", "ReportBold"
    return "Helvetica", "Helvetica-Bold"


FONT, FONT_BOLD = register_fonts()


def make_styles():
    styles = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title",
            parent=styles["Title"],
            fontName=FONT_BOLD,
            fontSize=22,
            leading=25,
            textColor=colors.white,
            alignment=TA_LEFT,
            spaceAfter=0,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=styles["Normal"],
            fontName=FONT,
            fontSize=10.5,
            leading=14,
            textColor=colors.HexColor("#DCE8FF"),
        ),
        "section": ParagraphStyle(
            "Section",
            parent=styles["Heading2"],
            fontName=FONT_BOLD,
            fontSize=13,
            leading=16,
            textColor=NAVY,
            spaceBefore=5,
            spaceAfter=6,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=styles["BodyText"],
            fontName=FONT,
            fontSize=9.2,
            leading=13.1,
            textColor=DARK,
            spaceAfter=6,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=styles["BodyText"],
            fontName=FONT,
            fontSize=8.2,
            leading=10.8,
            textColor=DARK,
        ),
        "metric": ParagraphStyle(
            "Metric",
            parent=styles["BodyText"],
            fontName=FONT_BOLD,
            fontSize=9,
            leading=11.5,
            textColor=NAVY,
            alignment=TA_CENTER,
        ),
        "table_header": ParagraphStyle(
            "TableHeader",
            parent=styles["BodyText"],
            fontName=FONT_BOLD,
            fontSize=8.1,
            leading=10,
            textColor=colors.white,
            alignment=TA_CENTER,
        ),
        "table_cell": ParagraphStyle(
            "TableCell",
            parent=styles["BodyText"],
            fontName=FONT,
            fontSize=7.7,
            leading=9.8,
            textColor=DARK,
            alignment=TA_CENTER,
        ),
        "callout": ParagraphStyle(
            "Callout",
            parent=styles["BodyText"],
            fontName=FONT_BOLD,
            fontSize=9.2,
            leading=12.5,
            textColor=NAVY,
        ),
        "footer": ParagraphStyle(
            "Footer",
            parent=styles["BodyText"],
            fontName=FONT,
            fontSize=7.5,
            textColor=MID_GRAY,
            alignment=TA_CENTER,
        ),
    }


STYLES = make_styles()


def p(text, style="body"):
    return Paragraph(text, STYLES[style])


def bullet(text):
    return Paragraph(
        f"<font color='#1D4ED8'>●</font>&nbsp;&nbsp;{text}",
        ParagraphStyle(
            "Bullet",
            parent=STYLES["body"],
            fontSize=8.4,
            leading=11.0,
            leftIndent=4 * mm,
            firstLineIndent=-4 * mm,
            spaceAfter=3,
        ),
    )


def section_title(number, title):
    return p(f"<font color='#1D4ED8'>{number}</font>  {title}", "section")


def header_footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setFillColor(NAVY)
        canvas.rect(0, PAGE_HEIGHT - 11 * mm, PAGE_WIDTH, 11 * mm, fill=1, stroke=0)
        canvas.setFont(FONT_BOLD, 8)
        canvas.setFillColor(colors.white)
        canvas.drawString(MARGIN_X, PAGE_HEIGHT - 7.2 * mm, "INVENTARIO APP  /  REFLEXION CI/CD")

    canvas.setStrokeColor(colors.HexColor("#D8DEE8"))
    canvas.line(MARGIN_X, 12 * mm, PAGE_WIDTH - MARGIN_X, 12 * mm)
    canvas.setFont(FONT, 7.5)
    canvas.setFillColor(MID_GRAY)
    canvas.drawString(MARGIN_X, 7.8 * mm, "José Vanegas · Miguel Vanegas")
    canvas.drawRightString(
        PAGE_WIDTH - MARGIN_X,
        7.8 * mm,
        f"25 de julio de 2026  |  Página {doc.page} de 2",
    )
    canvas.restoreState()


def metric_card(value, label, color):
    card = Table(
        [[p(value, "metric")], [p(label, "small")]],
        colWidths=[50 * mm],
        rowHeights=[11 * mm, 12 * mm],
    )
    card.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("BOX", (0, 0), (-1, -1), 1.1, color),
                ("LINEBELOW", (0, 0), (-1, 0), 0.6, color),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return card


def build_pdf():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    doc = BaseDocTemplate(
        str(OUTPUT_PATH),
        pagesize=A4,
        leftMargin=MARGIN_X,
        rightMargin=MARGIN_X,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
        title="Informe de reflexión CI/CD - Inventario App",
        author="José Vanegas y Miguel Vanegas",
        subject="Blue-Green, persistencia, problemas reales y métricas DORA",
    )
    frame = Frame(
        MARGIN_X,
        MARGIN_BOTTOM,
        PAGE_WIDTH - 2 * MARGIN_X,
        PAGE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM,
        id="content",
    )
    doc.addPageTemplates([PageTemplate(id="report", frames=[frame], onPage=header_footer)])

    story = []

    hero = Table(
        [
            [p("Informe de reflexión CI/CD", "title")],
            [
                p(
                    "Inventario App · Docker · GitHub Actions · Kubernetes · Blue-Green",
                    "subtitle",
                )
            ],
        ],
        colWidths=[PAGE_WIDTH - 2 * MARGIN_X],
        rowHeights=[21 * mm, 12 * mm],
    )
    hero.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("LEFTPADDING", (0, 0), (-1, -1), 9 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 4 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3 * mm),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story.extend([hero, Spacer(1, 5 * mm)])

    meta = Table(
        [
            [p("<b>Integrantes</b><br/>José Vanegas · Miguel Vanegas", "small"),
             p("<b>Repositorio público</b><br/>github.com/miguis145/inventario-app", "small")],
        ],
        colWidths=[82 * mm, 92 * mm],
    )
    meta.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#D8DEE8")),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D8DEE8")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.extend([meta, Spacer(1, 4 * mm)])

    story.append(section_title("01", "Síntesis del trabajo"))
    story.append(
        p(
            "La práctica llevó una aplicación Node.js desde pruebas locales hasta dos versiones "
            "desplegadas en Minikube. El flujo usa un Dockerfile multi-stage que ejecuta la suite "
            "antes de construir producción, dos jobs fail-fast en GitHub Actions, publicación por "
            "SHA en GHCR, Rolling Update y una estrategia Blue-Green nativa de Kubernetes. También "
            "se implementaron los tres componentes adicionales: Secret, escaneo Trivy y readiness "
            "con arranque lento real."
        )
    )

    story.append(section_title("02", "Por qué se eligió Blue-Green"))
    story.append(
        p(
            "Blue-Green encaja mejor que Canary en este laboratorio porque cada respuesta de "
            "<b>/version</b> identifica versión, color y pod. Mantener dos Deployments independientes "
            "permite validar Green completo sin mezclar respuestas con Blue. El corte se realiza "
            "cambiando únicamente el selector <b>slot</b> del Service, sin reconstruir imágenes ni "
            "reemplazar pods durante la promoción."
        )
    )
    story.append(
        p(
            "La decisión usa solo recursos nativos: <b>inventario-app-blue</b>, "
            "<b>inventario-app-green</b> e <b>inventario-service</b>. Frente a Canary, consume más "
            "recursos porque duplica dos réplicas, pero ofrece una demostración más determinista y "
            "un rollback inmediato: si Green falla, el selector vuelve a <b>slot=blue</b>."
        )
    )

    story.append(section_title("03", "Qué ocurrió con los datos al recrear el pod"))
    story.append(
        p(
            "El producto agregado desde la interfaz se escribió en <b>/app/data/products.json</b> "
            "dentro del contenedor que atendió la petición. Al eliminar ese pod, Kubernetes creó "
            "otro a partir de la imagen, pero no restauró el archivo modificado. El producto dejó "
            "de aparecer. Con dos réplicas también pueden observarse catálogos distintos, porque "
            "cada pod mantiene su propia copia local."
        )
    )
    callout = Table(
        [[p("Conclusión de persistencia: un Deployment mantiene procesos, no convierte el sistema de archivos del contenedor en almacenamiento compartido. En producción se necesitaría un PersistentVolume apropiado o, preferiblemente para varias réplicas, una base de datos externa.", "callout")]],
        colWidths=[PAGE_WIDTH - 2 * MARGIN_X],
    )
    callout.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_CYAN),
                ("BOX", (0, 0), (-1, -1), 0.8, CYAN),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.append(callout)

    story.append(PageBreak())

    story.append(section_title("04", "Métricas DORA propias"))
    story.append(
        p(
            "Los tiempos de commit provienen de Git y los tiempos de despliegue se registraron "
            "inmediatamente después de que <b>kubectl rollout status</b> confirmó cada versión. "
            "No se utilizó la hora de publicación de GHCR como sustituto del despliegue.",
            "small",
        )
    )

    cards = Table(
        [[
            metric_card("00:02:55", "Lead time promedio", BLUE),
            metric_card("2 por día", "Frecuencia de despliegue", CYAN),
            metric_card("33,33 %", "Change failure rate", RED),
        ]],
        colWidths=[56 * mm, 56 * mm, 56 * mm],
    )
    cards.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    story.extend([cards, Spacer(1, 4 * mm)])

    dora_data = [
        [
            p("Versión", "table_header"),
            p("Commit", "table_header"),
            p("Despliegue correcto", "table_header"),
            p("Lead time", "table_header"),
        ],
        [
            p("Release 1", "table_cell"),
            p("25-jul 16:57:29", "table_cell"),
            p("25-jul 17:01:00", "table_cell"),
            p("00:03:31", "table_cell"),
        ],
        [
            p("Release 2", "table_cell"),
            p("25-jul 17:02:01", "table_cell"),
            p("25-jul 17:04:20", "table_cell"),
            p("00:02:19", "table_cell"),
        ],
    ]
    dora_table = Table(dora_data, colWidths=[31 * mm, 45 * mm, 56 * mm, 36 * mm])
    dora_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.55, colors.HexColor("#C9D1DC")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(dora_table)
    story.append(Spacer(1, 3 * mm))
    story.append(
        p(
            "Cálculos: dos promociones correctas en un día equivalen a <b>2 despliegues/día</b>. "
            "El promedio de 00:03:31 y 00:02:19 es <b>00:02:55</b>. En el conjunto auditado hubo "
            "tres intentos versionados: una etiqueta inexistente falló y las dos imágenes corregidas "
            "funcionaron, por lo que <b>1 / 3 × 100 = 33,33 %</b>. El CFR conserva de forma transparente "
            "el fallo histórico y sigue siendo la principal oportunidad de mejora.",
            "small",
        )
    )

    story.append(section_title("05", "Problemas reales y resolución"))
    problems = [
        "<b>BuildKit omitía las pruebas.</b> La etapa final no dependía de <i>test</i>. Se corrigió copiando el código desde esa etapa, lo que obliga a ejecutar las seis pruebas.",
        "<b>ImagePullBackOff.</b> Un manifiesto apuntó a una etiqueta SHA inexistente. Se verificaron las etiquetas publicadas en GHCR y se reemplazó por el SHA Blue válido.",
        "<b>Arranque lento incompleto.</b> El YAML declaraba STARTUP_DELAY_SECONDS, pero /health no la leía. Ahora devuelve 503 durante la espera y 200 cuando está listo; una prueba controla ambos estados.",
        "<b>Trivy no descargaba su base.</b> Dos repositorios agotaron el timeout. Se confirmó que la caché estaba vacía, se usó el repositorio público alternativo y el escaneo final reportó cero hallazgos CRITICAL.",
        "<b>PowerShell alteró el JSON de kubectl patch.</b> Se movieron los parches a archivos JSON y se aplicaron con --patch-file.",
    ]
    story.extend([bullet(item) for item in problems])

    story.append(section_title("06", "Reflexión final"))
    story.append(
        p(
            "La práctica mostró que desplegar no es solo copiar una imagen: requiere conocer qué "
            "versión está activa, impedir tráfico prematuro, conservar una ruta de rollback, tratar "
            "los secretos fuera de Git y medir el proceso con datos. La evidencia de fallos resultó "
            "tan útil como la de éxito, porque permitió corregir el pipeline y señalar como siguiente "
            "prioridad la validación automática de etiquetas antes del despliegue.",
            "small",
        )
    )

    doc.build(story)
    print(OUTPUT_PATH)


if __name__ == "__main__":
    build_pdf()
