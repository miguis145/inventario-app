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

NAVY = colors.HexColor("#222222")
BLUE = colors.HexColor("#222222")
CYAN = colors.HexColor("#555555")
LIGHT_BLUE = colors.HexColor("#F2F2F2")
LIGHT_CYAN = colors.HexColor("#F7F7F7")
LIGHT_GRAY = colors.HexColor("#F7F7F7")
TABLE_HEADER = colors.HexColor("#EDEDED")
MID_GRAY = colors.HexColor("#666666")
DARK = colors.HexColor("#111111")
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
            fontSize=16,
            leading=19,
            textColor=DARK,
            alignment=TA_CENTER,
            spaceAfter=0,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=styles["Normal"],
            fontName=FONT,
            fontSize=10,
            leading=12,
            textColor=MID_GRAY,
            alignment=TA_CENTER,
        ),
        "section": ParagraphStyle(
            "Section",
            parent=styles["Heading2"],
            fontName=FONT_BOLD,
            fontSize=11,
            leading=13,
            textColor=NAVY,
            spaceBefore=6,
            spaceAfter=3,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=styles["BodyText"],
            fontName=FONT,
            fontSize=9.3,
            leading=12.6,
            textColor=DARK,
            spaceAfter=6,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=styles["BodyText"],
            fontName=FONT,
            fontSize=8.3,
            leading=10.7,
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
    return p(f"{number}. {title}", "section")


def header_footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setStrokeColor(colors.HexColor("#888888"))
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN_X, PAGE_HEIGHT - 12 * mm, PAGE_WIDTH - MARGIN_X, PAGE_HEIGHT - 12 * mm)
        canvas.setFont(FONT, 8)
        canvas.setFillColor(MID_GRAY)
        canvas.drawString(MARGIN_X, PAGE_HEIGHT - 9.2 * mm, "Informe de reflexión - Parte II")

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
            [p("Informe de reflexión - Parte II", "title")],
            [p("Pruebas del pipeline CI/CD y métricas DORA propias", "subtitle")],
        ],
        colWidths=[PAGE_WIDTH - 2 * MARGIN_X],
    )
    heading.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("LEFTPADDING", (0, 0), (-1, -1), 2 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 1 * mm),
                ("BOTTOMPADDING", (0, -1), (-1, -1), 2 * mm),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story.extend([heading, Spacer(1, 3 * mm)])

    meta = Table(
        [
            [
                p("<b>Integrantes:</b>", "small"),
                p("José Vanegas y Miguel Vanegas", "small"),
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
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("LINEBELOW", (0, -1), (-1, -1), 0.6, colors.HexColor("#888888")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    story.extend([meta, Spacer(1, 3 * mm)])

    story.append(section_title("01", "Verificación reproducible"))
    story.append(
        p(
            "Para ordenar la entrega fuimos colocando cada comando en el README junto con la salida "
            "que obtuvimos. Las capturas originales están en <b>evidencias/capturas-reales</b>. También "
            "dejamos los dos registros de despliegue y el archivo CSV que usamos para calcular DORA. "
            "Así se puede repetir la práctica siguiendo el mismo orden."
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
            "Escogimos Blue-Green porque era la forma más directa de mostrar el cambio entre dos "
            "versiones. El endpoint <b>/version</b> indica la versión, el color y el pod que respondió. "
            "Primero probamos Green sin mover el tráfico y después cambiamos el selector <b>slot</b> "
            "del Service. Blue quedó activo por si era necesario regresar."
        )
    )
    story.append(
        p(
            "Pensamos también en Canary, pero para esta práctica pequeña habría sido más difícil "
            "demostrar qué porcentaje de solicitudes llegaba a cada versión. Blue-Green usa más "
            "recursos porque mantiene los dos ambientes, aunque el cambio y el rollback se entienden "
            "mejor al revisar las salidas de los comandos."
        )
    )

    story.append(section_title("03", "Persistencia al recrear el pod"))
    story.append(
        p(
            "En esta prueba agregamos un producto desde la interfaz y luego eliminamos el pod que lo "
            "había guardado. El dato estaba en <b>/app/data/products.json</b>, dentro de ese contenedor. "
            "Cuando Kubernetes creó el reemplazo, el producto ya no apareció. También notamos que cada "
            "réplica tenía su propia copia del catálogo."
        )
    )
    story.append(
        p(
            "<b>Conclusión de la prueba:</b> recrear el pod recupera la aplicación, pero no los cambios "
            "hechos en sus archivos. Para conservar el catálogo entre réplicas necesitaríamos una base "
            "de datos o un volumen compartido."
        )
    )

    story.append(PageBreak())

    story.append(section_title("04", "Métricas DORA con datos propios"))
    story.append(
        p(
            "Tomamos la hora del commit desde Git y la comparamos con la hora en que "
            "<b>kubectl rollout status</b> confirmó el cambio en el clúster. También anotamos la "
            "finalización de cada run de GitHub Actions. Todas las horas están en UTC-05."
        )
    )

    story.append(
        p(
            "<b>Lead time for changes.</b> Los dos tiempos fueron 00:03:31 y 00:02:19. "
            "El promedio es <b>00:02:55</b>, que corresponde al nivel Élite de la tabla usada."
        )
    )
    story.append(
        p(
            "<b>Frecuencia de despliegue.</b> Promovimos dos cambios correctos durante un día de "
            "trabajo. El resultado es <b>2 despliegues por día</b>, también clasificado como Élite."
        )
    )
    story.append(
        p(
            "<b>Change failure rate.</b> Registramos tres intentos en total. Uno necesitó una "
            "corrección posterior por ImagePullBackOff. El cálculo es 1 / 3 × 100, por lo que el "
            "resultado es <b>33,33 %</b> y el nivel es Medio."
        )
    )
    story.append(Spacer(1, 2 * mm))

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
    story.append(Spacer(1, 2 * mm))
    story.append(
        p(
            "Fuentes: Git, runs 30176640875 y 30176786798, evidencias/despliegue-8a26dc3.txt, "
            "evidencias/despliegue-85eaa0f.txt y evidencias/dora-deployments.csv.",
            "tiny",
        )
    )

    story.append(section_title("05", "Problemas reales y resolución"))
    story.append(
        p(
            "<b>BuildKit y las pruebas:</b> al principio la etapa final no dependía de la etapa "
            "test, por lo que el build podía terminar sin ejecutar la suite. Cambiamos el Dockerfile "
            "para que producción copie el código desde test."
        )
    )
    story.append(
        p(
            "<b>Imagen incorrecta:</b> una etiqueta SHA que no existía produjo ImagePullBackOff. "
            "Revisamos GHCR, usamos una etiqueta publicada y repetimos el rollout hasta tener 2/2 pods."
        )
    )
    story.append(
        p(
            "<b>Readiness:</b> /health respondía 200 incluso durante el arranque lento. Agregamos "
            "STARTUP_DELAY_SECONDS y una prueba que comprueba primero el 503 y después el 200."
        )
    )
    story.append(
        p(
            "<b>Trivy y PowerShell:</b> Trivy agotó el tiempo al descargar su base y PowerShell "
            "modificaba el JSON de kubectl patch. Usamos el repositorio alternativo de Trivy y "
            "guardamos los parches en archivos JSON."
        )
    )

    story.append(section_title("06", "Reflexión final"))
    story.append(
        p(
            "Lo que más trabajo nos tomó fue comprobar que la versión correcta realmente estaba "
            "corriendo. Una salida parecía suficiente, pero otra prueba mostraba un problema, como "
            "ocurrió con la etiqueta inexistente y con /health durante el arranque. También entendimos "
            "por qué el catálogo no debe guardarse dentro del contenedor. Si repitiéramos la práctica, "
            "validaríamos el SHA en GHCR antes de actualizar el Deployment; eso habría evitado el "
            "intento fallido que elevó el CFR.",
        )
    )

    doc.build(story)
    print(OUTPUT_PATH)


if __name__ == "__main__":
    build_pdf()
