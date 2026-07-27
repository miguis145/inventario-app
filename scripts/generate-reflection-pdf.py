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

NAVY = colors.HexColor("#1F2937")
BLUE = colors.HexColor("#315A8A")
CYAN = colors.HexColor("#4B748F")
LIGHT_BLUE = colors.HexColor("#EDF3F8")
LIGHT_CYAN = colors.HexColor("#F2F6F8")
LIGHT_GRAY = colors.HexColor("#F5F5F4")
TABLE_HEADER = colors.HexColor("#E7E5E4")
MID_GRAY = colors.HexColor("#5F6368")
DARK = colors.HexColor("#202124")
RED = colors.HexColor("#B42318")
GREEN = colors.HexColor("#147D64")


def register_fonts():
    regular = Path("C:/Windows/Fonts/times.ttf")
    bold = Path("C:/Windows/Fonts/timesbd.ttf")
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("ReportRegular", str(regular)))
        pdfmetrics.registerFont(TTFont("ReportBold", str(bold)))
        return "ReportRegular", "ReportBold"
    return "Times-Roman", "Times-Bold"


FONT, FONT_BOLD = register_fonts()


def make_styles():
    styles = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title",
            parent=styles["Title"],
            fontName=FONT_BOLD,
            fontSize=18,
            leading=21,
            textColor=DARK,
            alignment=TA_CENTER,
            spaceAfter=0,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=styles["Normal"],
            fontName=FONT,
            fontSize=10.5,
            leading=13,
            textColor=MID_GRAY,
            alignment=TA_CENTER,
        ),
        "section": ParagraphStyle(
            "Section",
            parent=styles["Heading2"],
            fontName=FONT_BOLD,
            fontSize=11.5,
            leading=14,
            textColor=NAVY,
            spaceBefore=7,
            spaceAfter=4,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=styles["BodyText"],
            fontName=FONT,
            fontSize=9.6,
            leading=13.2,
            textColor=DARK,
            spaceAfter=6,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=styles["BodyText"],
            fontName=FONT,
            fontSize=8.6,
            leading=11.2,
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
            textColor=DARK,
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
        "table_cell_left": ParagraphStyle(
            "TableCellLeft",
            parent=styles["BodyText"],
            fontName=FONT,
            fontSize=7.5,
            leading=9.4,
            textColor=DARK,
            alignment=TA_LEFT,
        ),
        "tiny": ParagraphStyle(
            "Tiny",
            parent=styles["BodyText"],
            fontName=FONT,
            fontSize=7.2,
            leading=8.8,
            textColor=MID_GRAY,
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
    number = number.lstrip("0") or "0"
    return p(f"<font color='#315A8A'>{number}.</font> {title}", "section")


def header_footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setStrokeColor(BLUE)
        canvas.setLineWidth(0.8)
        canvas.line(MARGIN_X, PAGE_HEIGHT - 12 * mm, PAGE_WIDTH - MARGIN_X, PAGE_HEIGHT - 12 * mm)
        canvas.setFont(FONT, 8)
        canvas.setFillColor(MID_GRAY)
        canvas.drawString(MARGIN_X, PAGE_HEIGHT - 9.2 * mm, "Informe de práctica: CI/CD y Kubernetes")

    canvas.setStrokeColor(colors.HexColor("#D8DEE8"))
    canvas.line(MARGIN_X, 12 * mm, PAGE_WIDTH - MARGIN_X, 12 * mm)
    canvas.setFont(FONT, 7.5)
    canvas.setFillColor(MID_GRAY)
    canvas.drawString(MARGIN_X, 7.8 * mm, "José Vanegas · Miguel Vanegas")
    canvas.drawRightString(
        PAGE_WIDTH - MARGIN_X,
        7.8 * mm,
        f"27 de julio de 2026  |  Página {doc.page} de 2",
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

    heading = Table(
        [
            [p("INFORME DE PRÁCTICA", "subtitle")],
            [p("Pruebas, métricas DORA y reflexión sobre el pipeline CI/CD", "title")],
            [p("Inventario App: Docker, GitHub Actions y Kubernetes", "subtitle")],
        ],
        colWidths=[PAGE_WIDTH - 2 * MARGIN_X],
    )
    heading.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("LINEBELOW", (0, -1), (-1, -1), 1.2, BLUE),
                ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
                ("TOPPADDING", (0, 0), (-1, 0), 1 * mm),
                ("TOPPADDING", (0, 1), (-1, 1), 2 * mm),
                ("BOTTOMPADDING", (0, -1), (-1, -1), 3 * mm),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story.extend([heading, Spacer(1, 4 * mm)])

    meta = Table(
        [
            [
                p("<b>Integrantes:</b>", "small"),
                p("José Vanegas y Miguel Vanegas", "small"),
            ],
            [
                p("<b>Trabajo:</b>", "small"),
                p("Parte II: pruebas y elaboración del informe", "small"),
            ],
            [
                p("<b>Repositorio:</b>", "small"),
                p("github.com/miguis145/inventario-app", "small"),
            ],
            [
                p("<b>Fecha:</b>", "small"),
                p("27 de julio de 2026", "small"),
            ],
        ],
        colWidths=[32 * mm, 142 * mm],
    )
    meta.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#D8DEE8")),
                ("LINEBELOW", (0, 0), (-1, -2), 0.3, colors.HexColor("#D8DEE8")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    story.extend([meta, Spacer(1, 3 * mm)])

    story.append(section_title("01", "Verificación reproducible"))
    story.append(
        p(
            "El README reúne los comandos en el orden en que se ejecutaron. Las salidas reales están "
            "en <b>evidencias/capturas-reales</b>, los registros de despliegue y el CSV de métricas. "
            "Con ese material, otra persona puede repetir las pruebas sin depender de explicaciones "
            "adicionales."
        )
    )

    verification_data = [
        [
            p("Elemento comprobado", "table_header"),
            p("Evidencia del repositorio", "table_header"),
            p("Resultado observado", "table_header"),
        ],
        [
            p("Pipeline base", "table_cell_left"),
            p("Secciones README 8 a 17; capturas 52 a 60", "table_cell_left"),
            p("6 pruebas, build multi-stage, Actions en verde, GHCR y Rolling Update 2/2", "table_cell_left"),
        ],
        [
            p("Blue-Green", "table_cell_left"),
            p("Capturas 65 y 66; blue-green-final.txt", "table_cell_left"),
            p("Service en slot=green; respuesta v2/green; rollback a Blue verificado", "table_cell_left"),
        ],
        [
            p("Buenas prácticas", "table_cell_left"),
            p("Capturas 59, 66, 67 y 68", "table_cell_left"),
            p("Secret sin exponer la clave, Trivy sin CRITICAL y readiness 503 hasta quedar 1/1", "table_cell_left"),
        ],
    ]
    verification_table = Table(
        verification_data,
        colWidths=[35 * mm, 55 * mm, 84 * mm],
    )
    verification_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#C9D1DC")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.extend([verification_table, Spacer(1, 2 * mm)])

    story.append(section_title("02", "Justificación de Blue-Green"))
    story.append(
        p(
            "Elegimos Blue-Green porque la aplicación expone <b>/version</b> con versión, color y "
            "hostname. Esto permite comprobar Green por separado y cambiar el tráfico modificando "
            "solo el selector <b>slot</b> del Service. Blue permanece activo, de modo que el rollback "
            "consiste en devolver el selector a <b>slot=blue</b>."
        )
    )
    story.append(
        p(
            "Canary habría servido para repartir solicitudes entre versiones, pero habría complicado "
            "la demostración con una muestra pequeña. Blue-Green consume más recursos porque mantiene "
            "dos versiones completas, pero el corte y el regreso a Blue son claros y reproducibles."
        )
    )

    story.append(section_title("03", "Persistencia al recrear el pod"))
    story.append(
        p(
            "El producto creado desde la interfaz quedó en <b>/app/data/products.json</b> dentro del "
            "contenedor que atendió la solicitud. Al eliminar ese pod, Kubernetes creó otro desde la "
            "imagen y el producto desapareció. Además, cada réplica conserva su propia copia, por lo "
            "que dos solicitudes pueden mostrar catálogos distintos."
        )
    )
    callout = Table(
        [[p("Conclusión: el Deployment repone procesos, pero no comparte ni conserva los archivos de los contenedores. Un entorno real necesitaría almacenamiento persistente o una base de datos común.", "callout")]],
        colWidths=[PAGE_WIDTH - 2 * MARGIN_X],
    )
    callout.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#A8A29E")),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.append(callout)

    story.append(PageBreak())

    story.append(section_title("04", "Métricas DORA con datos propios"))
    story.append(
        p(
            "Git aporta la hora del commit, GitHub registra la finalización de cada run y Kubernetes "
            "confirma cuándo la imagen quedó disponible en el clúster. El lead time termina en el "
            "despliegue real, no en la publicación de GHCR. Todas las horas están en UTC-05.",
            "small",
        )
    )

    summary_data = [
        [
            p("Indicador", "table_header"),
            p("Cálculo realizado", "table_header"),
            p("Resultado", "table_header"),
            p("Nivel", "table_header"),
        ],
        [
            p("Lead time for changes", "table_cell_left"),
            p("(00:03:31 + 00:02:19) / 2", "table_cell"),
            p("00:02:55", "table_cell"),
            p("Élite", "table_cell"),
        ],
        [
            p("Frecuencia de despliegue", "table_cell_left"),
            p("2 cambios correctos / 1 día", "table_cell"),
            p("2 por día", "table_cell"),
            p("Élite", "table_cell"),
        ],
        [
            p("Change failure rate", "table_cell_left"),
            p("1 corrección / 3 intentos × 100", "table_cell"),
            p("33,33 %", "table_cell"),
            p("Medio", "table_cell"),
        ],
    ]
    summary_table = Table(
        summary_data,
        colWidths=[48 * mm, 63 * mm, 34 * mm, 29 * mm],
    )
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER),
                ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#A8A29E")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.extend([summary_table, Spacer(1, 4 * mm)])

    dora_data = [
        [
            p("#", "table_header"),
            p("SHA", "table_header"),
            p("Commit", "table_header"),
            p("Run correcto", "table_header"),
            p("En el clúster", "table_header"),
            p("Lead time", "table_header"),
        ],
        [
            p("1", "table_cell"),
            p("8a26dc3", "table_cell"),
            p("25-jul<br/>16:57:29", "table_cell"),
            p("Run 30176640875<br/>16:59:15", "table_cell"),
            p("25-jul<br/>17:01:00", "table_cell"),
            p("00:03:31", "table_cell"),
        ],
        [
            p("2", "table_cell"),
            p("85eaa0f", "table_cell"),
            p("25-jul<br/>17:02:01", "table_cell"),
            p("Run 30176786798<br/>17:03:10", "table_cell"),
            p("25-jul<br/>17:04:20", "table_cell"),
            p("00:02:19", "table_cell"),
        ],
    ]
    dora_table = Table(
        dora_data,
        colWidths=[14 * mm, 23 * mm, 32 * mm, 43 * mm, 35 * mm, 27 * mm],
    )
    dora_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.55, colors.HexColor("#C9D1DC")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(dora_table)
    story.append(Spacer(1, 3 * mm))
    story.append(
        p(
            "<b>Cálculos.</b> Dos promociones correctas en un día equivalen a <b>2 despliegues/día</b>. "
            "El promedio de 00:03:31 y 00:02:19 es <b>00:02:55</b>. Hubo tres intentos: uno necesitó "
            "corrección y dos terminaron bien. La frecuencia cuenta los dos cambios que sí quedaron "
            "corriendo; el CFR incluye los tres intentos. Por eso, <b>1 / 3 × 100 = 33,33 %</b>.",
            "small",
        )
    )
    story.append(
        p(
            "<b>Niveles.</b> El lead time menor de una hora y los dos despliegues diarios sitúan la "
            "velocidad en <b>ÉLITE</b>. El CFR de 33,33 %, dentro del rango didáctico de 31 % a 45 %, "
            "deja la estabilidad en <b>MEDIO</b>. La muestra contiene solo tres intentos, por lo que "
            "esta clasificación es orientativa.",
            "small",
        )
    )
    story.append(
        p(
            "Fuentes: Git, runs 30176640875 y 30176786798, evidencias/despliegue-8a26dc3.txt, "
            "evidencias/despliegue-85eaa0f.txt y evidencias/dora-deployments.csv.",
            "tiny",
        )
    )

    story.append(section_title("05", "Problemas reales y resolución"))
    problems_data = [
        [
            p("Problema observado", "table_header"),
            p("Diagnóstico y solución aplicada", "table_header"),
        ],
        [
            p("BuildKit omitía la etapa de pruebas.", "table_cell_left"),
            p("Producción no dependía de test. Ahora copia el código desde esa etapa y el build exige las seis pruebas.", "table_cell_left"),
        ],
        [
            p("Una etiqueta inexistente causó ImagePullBackOff.", "table_cell_left"),
            p("Se verificó GHCR, se publicó un SHA válido y se repitió el rollout hasta obtener 2/2 réplicas.", "table_cell_left"),
        ],
        [
            p("/health respondía 200 durante el arranque.", "table_cell_left"),
            p("Se implementó STARTUP_DELAY_SECONDS. Ahora devuelve 503 durante la espera y 200 cuando el pod está listo.", "table_cell_left"),
        ],
        [
            p("Trivy agotó el tiempo al descargar su base.", "table_cell_left"),
            p("Se usó el repositorio público alternativo. El pipeline final terminó sin hallazgos CRITICAL.", "table_cell_left"),
        ],
        [
            p("PowerShell alteraba el JSON de kubectl patch.", "table_cell_left"),
            p("Los parches se guardaron en archivos y se aplicaron con --patch-file.", "table_cell_left"),
        ],
    ]
    problems_table = Table(problems_data, colWidths=[59 * mm, 115 * mm])
    problems_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#C9D1DC")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(problems_table)

    story.append(section_title("06", "Reflexión final"))
    story.append(
        p(
            "La práctica nos obligó a comprobar cada afirmación con una salida real. Vimos que una "
            "imagen publicada no cuenta como desplegada hasta que Kubernetes la ejecuta, que un pod "
            "nuevo no recupera archivos locales y que un rollout correcto depende tanto de la imagen "
            "como del readiness. El proceso terminó rápido, pero el CFR muestra una mejora concreta: "
            "validar la existencia del SHA en GHCR antes de tocar el Deployment.",
            "small",
        )
    )

    doc.build(story)
    print(OUTPUT_PATH)


if __name__ == "__main__":
    build_pdf()
