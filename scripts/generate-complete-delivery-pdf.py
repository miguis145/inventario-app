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
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output" / "pdf"
OUTPUT_PATH = OUTPUT_DIR / "Entrega_Completa_Inventario_App.pdf"
EVIDENCE_DIR = ROOT / "evidencias" / "capturas-reales"

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_X = 18 * mm
MARGIN_TOP = 18 * mm
MARGIN_BOTTOM = 16 * mm

BLACK = colors.HexColor("#111111")
GRAY = colors.HexColor("#666666")
LIGHT_GRAY = colors.HexColor("#F2F2F2")
TABLE_GRAY = colors.HexColor("#E8E8E8")
BORDER = colors.HexColor("#B8B8B8")
CODE_BG = colors.HexColor("#F7F7F7")


def register_fonts():
    arial = Path("C:/Windows/Fonts/arial.ttf")
    arial_bold = Path("C:/Windows/Fonts/arialbd.ttf")
    consolas = Path("C:/Windows/Fonts/consola.ttf")
    if arial.exists() and arial_bold.exists():
        pdfmetrics.registerFont(TTFont("ReportRegular", str(arial)))
        pdfmetrics.registerFont(TTFont("ReportBold", str(arial_bold)))
        regular = "ReportRegular"
        bold = "ReportBold"
    else:
        regular = "Helvetica"
        bold = "Helvetica-Bold"

    if consolas.exists():
        pdfmetrics.registerFont(TTFont("ReportMono", str(consolas)))
        mono = "ReportMono"
    else:
        mono = "Courier"
    return regular, bold, mono


FONT, FONT_BOLD, FONT_MONO = register_fonts()


def make_styles():
    base = getSampleStyleSheet()
    return {
        "cover_title": ParagraphStyle(
            "CoverTitle",
            parent=base["Title"],
            fontName=FONT_BOLD,
            fontSize=22,
            leading=27,
            alignment=TA_CENTER,
            textColor=BLACK,
            spaceAfter=8,
        ),
        "cover_subtitle": ParagraphStyle(
            "CoverSubtitle",
            parent=base["Normal"],
            fontName=FONT,
            fontSize=12,
            leading=16,
            alignment=TA_CENTER,
            textColor=GRAY,
        ),
        "h1": ParagraphStyle(
            "Heading1",
            parent=base["Heading1"],
            fontName=FONT_BOLD,
            fontSize=15,
            leading=18,
            textColor=BLACK,
            spaceBefore=2,
            spaceAfter=7,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "Heading2",
            parent=base["Heading2"],
            fontName=FONT_BOLD,
            fontSize=11.5,
            leading=14,
            textColor=BLACK,
            spaceBefore=6,
            spaceAfter=4,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName=FONT,
            fontSize=9.3,
            leading=13,
            textColor=BLACK,
            spaceAfter=6,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName=FONT,
            fontSize=8.1,
            leading=10.5,
            textColor=BLACK,
            spaceAfter=4,
        ),
        "caption": ParagraphStyle(
            "Caption",
            parent=base["BodyText"],
            fontName=FONT,
            fontSize=7.4,
            leading=9,
            textColor=GRAY,
            alignment=TA_CENTER,
            spaceBefore=3,
            spaceAfter=5,
        ),
        "table_header": ParagraphStyle(
            "TableHeader",
            parent=base["BodyText"],
            fontName=FONT_BOLD,
            fontSize=8,
            leading=9.5,
            textColor=BLACK,
            alignment=TA_CENTER,
        ),
        "table_cell": ParagraphStyle(
            "TableCell",
            parent=base["BodyText"],
            fontName=FONT,
            fontSize=7.7,
            leading=9.5,
            textColor=BLACK,
        ),
        "table_cell_center": ParagraphStyle(
            "TableCellCenter",
            parent=base["BodyText"],
            fontName=FONT,
            fontSize=7.7,
            leading=9.5,
            textColor=BLACK,
            alignment=TA_CENTER,
        ),
        "code": ParagraphStyle(
            "Code",
            parent=base["Code"],
            fontName=FONT_MONO,
            fontSize=7.25,
            leading=9.2,
            leftIndent=0,
            rightIndent=0,
            textColor=BLACK,
        ),
        "note": ParagraphStyle(
            "Note",
            parent=base["BodyText"],
            fontName=FONT,
            fontSize=8.3,
            leading=11,
            textColor=BLACK,
            leftIndent=5 * mm,
            rightIndent=5 * mm,
            borderColor=BORDER,
            borderWidth=0.5,
            borderPadding=5,
            backColor=LIGHT_GRAY,
            spaceBefore=3,
            spaceAfter=6,
        ),
        "footer": ParagraphStyle(
            "Footer",
            parent=base["BodyText"],
            fontName=FONT,
            fontSize=7,
            textColor=GRAY,
            alignment=TA_CENTER,
        ),
    }


STYLES = make_styles()


def p(text, style="body"):
    return Paragraph(text, STYLES[style])


def h1(number, title):
    return p(f"{number}. {title}", "h1")


def h2(title):
    return p(title, "h2")


def code(text):
    block = Preformatted(text.strip(), STYLES["code"])
    table = Table([[block]], colWidths=[PAGE_WIDTH - 2 * MARGIN_X])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def evidence_image(filename, caption, max_height=65 * mm):
    path = EVIDENCE_DIR / filename
    if not path.exists():
        return p(f"Evidencia no encontrada: {filename}", "small")
    image = Image(str(path))
    image._restrictSize(PAGE_WIDTH - 2 * MARGIN_X, max_height)
    return KeepTogether([image, p(caption, "caption")])


def simple_table(data, widths, header=True):
    table = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    style = [
        ("GRID", (0, 0), (-1, -1), 0.45, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        style.append(("BACKGROUND", (0, 0), (-1, 0), TABLE_GRAY))
    table.setStyle(TableStyle(style))
    return table


def header_footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setStrokeColor(colors.HexColor("#999999"))
        canvas.setLineWidth(0.45)
        canvas.line(MARGIN_X, PAGE_HEIGHT - 12 * mm, PAGE_WIDTH - MARGIN_X, PAGE_HEIGHT - 12 * mm)
        canvas.setFont(FONT, 7.5)
        canvas.setFillColor(GRAY)
        canvas.drawString(MARGIN_X, PAGE_HEIGHT - 9 * mm, "Entrega completa - Inventario App")

    canvas.setStrokeColor(colors.HexColor("#C5C5C5"))
    canvas.line(MARGIN_X, 11 * mm, PAGE_WIDTH - MARGIN_X, 11 * mm)
    canvas.setFont(FONT, 7)
    canvas.setFillColor(GRAY)
    canvas.drawString(MARGIN_X, 7.2 * mm, "José Vanegas y Miguel Vanegas")
    canvas.drawRightString(PAGE_WIDTH - MARGIN_X, 7.2 * mm, f"Página {doc.page}")
    canvas.restoreState()


def build_pdf():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    doc = BaseDocTemplate(
        str(OUTPUT_PATH),
        pagesize=A4,
        leftMargin=MARGIN_X,
        rightMargin=MARGIN_X,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
        title="Entrega completa - Inventario App",
        author="José Vanegas y Miguel Vanegas",
        subject="Pruebas, Docker, GitHub Actions, Kubernetes, Blue-Green y métricas DORA",
    )
    frame = Frame(
        MARGIN_X,
        MARGIN_BOTTOM,
        PAGE_WIDTH - 2 * MARGIN_X,
        PAGE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM,
        id="content",
    )
    doc.addPageTemplates([PageTemplate(id="complete", frames=[frame], onPage=header_footer)])

    story = []

    # Portada
    story.extend(
        [
            Spacer(1, 28 * mm),
            p("Entrega completa del proyecto", "cover_subtitle"),
            Spacer(1, 5 * mm),
            p("Inventario App", "cover_title"),
            p("Pipeline CI/CD con Docker, GitHub Actions y Kubernetes", "cover_subtitle"),
            Spacer(1, 22 * mm),
        ]
    )
    cover_data = [
        [p("<b>Integrantes</b>", "small"), p("José Vanegas y Miguel Vanegas", "small")],
        [p("<b>Repositorio público</b>", "small"), p("github.com/miguis145/inventario-app", "small")],
        [p("<b>Fecha</b>", "small"), p("28 de julio de 2026", "small")],
        [p("<b>Contenido</b>", "small"), p("Informe técnico, evidencias, métricas DORA y comandos de demostración", "small")],
    ]
    story.append(simple_table(cover_data, [45 * mm, 129 * mm], header=False))
    story.extend(
        [
            Spacer(1, 22 * mm),
            p(
                "Este documento reúne el trabajo realizado durante la práctica. El informe corto de "
                "reflexión se mantiene como entregable independiente; aquí se presenta el recorrido "
                "completo y un guion de comandos para demostrar el funcionamiento.",
                "note",
            ),
            Spacer(1, 10 * mm),
            p(
                "<b>Contenido</b><br/>"
                "1. Alcance del trabajo<br/>"
                "2. Pruebas locales y aplicación<br/>"
                "3. Docker y pipeline CI/CD<br/>"
                "4. Seguridad, GHCR y Minikube<br/>"
                "5. Kubernetes, persistencia y Rolling Update<br/>"
                "6. Blue-Green y readiness<br/>"
                "7. Métricas DORA y problemas reales<br/>"
                "8. Comandos para la demostración",
                "body",
            ),
            PageBreak(),
        ]
    )

    # Resumen
    story.append(h1("1", "Alcance del trabajo"))
    story.append(
        p(
            "La práctica comenzó con una aplicación Node.js que administra un catálogo de productos. "
            "A partir de esa base se prepararon pruebas automáticas, una imagen Docker multi-stage y "
            "un pipeline con dos jobs. El pipeline prueba el código, construye la imagen, la analiza "
            "con Trivy y publica etiquetas inmutables por SHA en GHCR."
        )
    )
    story.append(
        p(
            "Después se desplegó la aplicación en Minikube. Se probó un Rolling Update con dos réplicas "
            "y una estrategia Blue-Green con dos Deployments separados. El Service decide qué versión "
            "recibe el tráfico mediante la etiqueta slot. También se agregó un Secret, un readiness "
            "real con respuesta HTTP 503 durante el arranque y una prueba de persistencia al recrear un pod."
        )
    )

    scope_rows = [
        [p("Componente", "table_header"), p("Implementación", "table_header"), p("Comprobación", "table_header")],
        [p("Pruebas", "table_cell"), p("Node test runner, 6 casos", "table_cell"), p("6 pass, 0 fail", "table_cell")],
        [p("Docker", "table_cell"), p("Build multi-stage con Node 24 Alpine", "table_cell"), p("La etapa test es obligatoria", "table_cell")],
        [p("CI/CD", "table_cell"), p("Jobs build-test y build-push", "table_cell"), p("Fail-fast, Trivy y GHCR", "table_cell")],
        [p("Kubernetes", "table_cell"), p("Rolling Update, 2 réplicas", "table_cell"), p("2/2 disponibles", "table_cell")],
        [p("Blue-Green", "table_cell"), p("Blue v1 y Green v2", "table_cell"), p("Cambio y rollback por selector", "table_cell")],
        [p("Buenas prácticas", "table_cell"), p("Secret, readiness y SHA inmutable", "table_cell"), p("Clave no expuesta y 503 antes de Ready", "table_cell")],
    ]
    story.append(simple_table(scope_rows, [35 * mm, 67 * mm, 72 * mm]))
    story.append(h2("Estructura principal del repositorio"))
    story.append(
        code(
            """
.github/workflows/ci-cd.yml
Dockerfile
server.js
server.test.js
k8s/deployment.yaml
k8s/service.yaml
k8s/blue-green/deployment-blue.yaml
k8s/blue-green/deployment-green.yaml
evidencias/capturas-reales/
evidencias/dora-deployments.csv
output/pdf/
"""
        )
    )
    story.append(
        p(
            "El README contiene los comandos completos y relaciona cada demostración con su captura. "
            "Las evidencias usadas en este documento no muestran tokens ni el valor de API_KEY."
        )
    )
    story.append(PageBreak())

    # Pruebas locales
    story.append(h1("2", "Pruebas locales y funcionamiento de la aplicación"))
    story.append(
        p(
            "La suite inicia el servidor en un puerto temporal. Comprueba /health, el arranque lento, "
            "/version, la creación y eliminación de productos y la validación de campos obligatorios. "
            "El resultado final fue de seis pruebas correctas y ninguna falla."
        )
    )
    story.append(evidence_image("52-pruebas-automaticas.png", "Evidencia: npm test termina con 6 pruebas correctas.", 72 * mm))

    endpoint_rows = [
        [p("Endpoint", "table_header"), p("Uso", "table_header"), p("Resultado esperado", "table_header")],
        [p("/", "table_cell"), p("Interfaz del catálogo", "table_cell"), p("HTML de la aplicación", "table_cell")],
        [p("/health", "table_cell"), p("Salud y readiness", "table_cell"), p("200 ok o 503 starting", "table_cell")],
        [p("/version", "table_cell"), p("Versión, color y pod", "table_cell"), p("v1/blue o v2/green", "table_cell")],
        [p("/api/products", "table_cell"), p("Catálogo en JSON", "table_cell"), p("Lista de productos", "table_cell")],
    ]
    story.append(simple_table(endpoint_rows, [30 * mm, 63 * mm, 81 * mm]))
    story.append(h2("Resultado observado"))
    story.append(
        p(
            "La aplicación respondió correctamente en el puerto 3000. /version también indicó si "
            "API_KEY estaba configurada mediante un booleano, sin devolver la clave. Esta misma ruta "
            "se utilizó después para identificar qué versión atendía el tráfico en Kubernetes."
        )
    )
    story.append(PageBreak())

    # Docker y Actions
    story.append(h1("3", "Docker y pipeline de GitHub Actions"))
    story.append(
        p(
            "El Dockerfile tiene dos etapas. La primera instala todas las dependencias y ejecuta las "
            "pruebas. La segunda instala solo producción y copia el código desde la etapa de test. "
            "Esa dependencia evita que BuildKit genere la imagen final si la suite falla."
        )
    )
    story.append(evidence_image("53-docker-build-multistage.png", "Evidencia: construcción multi-stage y ejecución de la etapa test.", 66 * mm))
    story.append(
        p(
            "GitHub Actions repite la misma idea. El job build-test ejecuta npm ci y npm test. "
            "build-push depende de ese job, construye la imagen, ejecuta Trivy y publica en GHCR "
            "solo cuando los controles anteriores terminan correctamente."
        )
    )
    story.append(evidence_image("32-github-actions-dos-jobs.jpg", "Evidencia: los dos jobs del pipeline terminan correctamente.", 50 * mm))
    pipeline_rows = [
        [p("Job", "table_header"), p("Pasos principales", "table_header"), p("Qué detiene el flujo", "table_header")],
        [p("build-test", "table_cell"), p("Checkout, Node 24, npm ci y npm test", "table_cell"), p("Cualquier prueba fallida", "table_cell")],
        [p("build-push", "table_cell"), p("Buildx, Trivy, login y push", "table_cell"), p("CRITICAL o error de construcción", "table_cell")],
    ]
    story.append(simple_table(pipeline_rows, [36 * mm, 78 * mm, 60 * mm]))
    story.append(PageBreak())

    # Seguridad, GHCR y Minikube
    story.append(h1("4", "Seguridad, GHCR y preparación del clúster"))
    story.append(
        p(
            "Trivy analiza vulnerabilidades del sistema operativo y bibliotecas. La política usada "
            "detiene el pipeline si encuentra una vulnerabilidad CRITICAL con corrección disponible. "
            "La verificación final usó la base publicada en public.ecr.aws y reportó cero hallazgos CRITICAL."
        )
    )
    story.append(evidence_image("59-trivy-sin-critical.png", "Evidencia: resumen del escaneo Trivy sin vulnerabilidades CRITICAL.", 86 * mm))
    story.append(
        p(
            "Las imágenes se publican como ghcr.io/miguis145/inventario-app:SHA y también como latest. "
            "Los manifiestos utilizan SHA porque es una referencia inmutable. latest queda disponible "
            "para descarga manual, pero no se usa para identificar un despliegue medido."
        )
    )
    story.append(h2("Minikube y Secret"))
    story.append(
        p(
            "El clúster local se ejecutó con el perfil ci-cd sobre Docker. Antes de desplegar se creó "
            "inventario-secret. Los Deployments leen API_KEY mediante secretKeyRef. La comprobación "
            "muestra solo los metadatos del Secret y el booleano apiKeyConfigured."
        )
    )
    story.append(evidence_image("60-minikube-ready.png", "Evidencia: nodo Ready y componentes de Minikube en ejecución.", 47 * mm))
    story.append(PageBreak())

    # Kubernetes y persistencia
    story.append(h1("5", "Kubernetes, Rolling Update y persistencia"))
    story.append(
        p(
            "El Deployment base usa dos réplicas, maxUnavailable igual a 1 y maxSurge igual a 1. "
            "La readinessProbe evita que un pod reciba tráfico antes de estar disponible. Se promovieron "
            "dos SHA distintos y ambos rollouts terminaron con 2/2 réplicas."
        )
    )
    story.append(evidence_image("64-rolling-update-final.png", "Evidencia: Rolling Update con dos imágenes SHA y 2/2 réplicas.", 64 * mm))
    story.append(h2("Acceso y respuesta"))
    story.append(
        p(
            "El Service expone el puerto 80 dentro del clúster. Para la demostración local se usa "
            "kubectl port-forward hacia 127.0.0.1:8080. Desde otra terminal se consultan /health, "
            "/version y /api/products."
        )
    )
    story.append(h2("Qué ocurrió al recrear un pod"))
    story.append(
        p(
            "Se agregó un producto y luego se eliminó el pod que había guardado el archivo. Kubernetes "
            "creó un reemplazo, pero el producto desapareció. db.js escribe el catálogo dentro del "
            "contenedor y no existe un PersistentVolume. Además, cada réplica conserva su propia copia. "
            "El resultado demuestra que el Deployment recupera el proceso, no los datos locales."
        )
    )
    persist_rows = [
        [p("Antes de eliminar", "table_header"), p("Después de eliminar", "table_header"), p("Conclusión", "table_header")],
        [p("Producto visible en el pod", "table_cell"), p("Pod nuevo con datos iniciales", "table_cell"), p("Se necesita almacenamiento compartido", "table_cell")],
    ]
    story.append(simple_table(persist_rows, [56 * mm, 56 * mm, 62 * mm]))
    story.append(PageBreak())

    # Blue-Green
    story.append(h1("6", "Estrategia Blue-Green"))
    story.append(
        p(
            "Blue ejecuta v1 y Green ejecuta v2. Ambos Deployments permanecen activos. El Service "
            "incluye app=inventario-app y un selector slot. Cambiar slot de blue a green promueve la "
            "nueva versión sin reconstruir imágenes. Volver a blue realiza el rollback."
        )
    )
    story.append(evidence_image("65-blue-green-activos-final.png", "Evidencia: Blue y Green activos con dos pods por versión.", 45 * mm))
    story.append(evidence_image("66-service-green-secret-final.png", "Evidencia: selector Green, respuesta v2 y API_KEY configurada.", 36 * mm))
    bg_rows = [
        [p("Estado", "table_header"), p("Selector del Service", "table_header"), p("Respuesta de /version", "table_header")],
        [p("Inicial", "table_cell_center"), p("slot=blue", "table_cell_center"), p("v1, blue", "table_cell_center")],
        [p("Promoción", "table_cell_center"), p("slot=green", "table_cell_center"), p("v2, green", "table_cell_center")],
        [p("Rollback", "table_cell_center"), p("slot=blue", "table_cell_center"), p("v1, blue", "table_cell_center")],
        [p("Estado final", "table_cell_center"), p("slot=green", "table_cell_center"), p("v2, green", "table_cell_center")],
    ]
    story.append(simple_table(bg_rows, [45 * mm, 62 * mm, 67 * mm]))
    story.append(
        p(
            "Se eligió Blue-Green porque /version hace visible qué ambiente respondió y porque el "
            "rollback se puede demostrar cambiando un solo selector. Canary habría requerido repartir "
            "tráfico y tomar varias muestras para justificar el porcentaje recibido por cada versión."
        )
    )
    story.append(PageBreak())

    # Readiness y problemas
    story.append(h1("7", "Readiness y problemas encontrados"))
    story.append(
        p(
            "STARTUP_DELAY_SECONDS simula un arranque lento. Durante ese tiempo /health devuelve HTTP "
            "503 y status starting. Cuando termina, devuelve 200 y status ok. Kubernetes mantiene el "
            "pod en Running 0/1 hasta que la sonda recibe la respuesta correcta."
        )
    )
    story.append(evidence_image("67-readiness-green-transicion-final.png", "Evidencia: transición de 0/1 a 1/1 durante el rollout de Green.", 62 * mm))
    problem_rows = [
        [p("Problema real", "table_header"), p("Corrección aplicada", "table_header")],
        [p("BuildKit omitía inicialmente test", "table_cell"), p("Producción copia el código desde la etapa test", "table_cell")],
        [p("ImagePullBackOff por SHA inexistente", "table_cell"), p("Verificación de GHCR y uso de una etiqueta publicada", "table_cell")],
        [p("/health respondía 200 durante el arranque", "table_cell"), p("Se implementó STARTUP_DELAY_SECONDS y una prueba 503/200", "table_cell")],
        [p("Trivy agotó el tiempo al descargar su base", "table_cell"), p("Uso del repositorio público alternativo", "table_cell")],
        [p("PowerShell modificaba el JSON de kubectl patch", "table_cell"), p("Uso de patch-green.json y patch-blue.json", "table_cell")],
        [p("Port-forward seguía conectado a Blue", "table_cell"), p("Reinicio del port-forward después de cambiar el selector", "table_cell")],
    ]
    story.append(simple_table(problem_rows, [72 * mm, 102 * mm]))
    story.append(
        p(
            "Los errores se conservaron como parte de la evidencia. El intento fallido de despliegue "
            "también se incluye en el cálculo del change failure rate."
        )
    )
    story.append(PageBreak())

    # DORA
    story.append(h1("8", "Métricas DORA propias"))
    story.append(
        p(
            "El lead time termina cuando Kubernetes registra NewReplicaSetAvailable. No se usa la hora "
            "de publicación de GHCR como sustituto. Los dos cambios medidos corresponden a imágenes SHA distintas."
        )
    )
    dora_rows = [
        [
            p("SHA", "table_header"),
            p("Commit", "table_header"),
            p("Despliegue", "table_header"),
            p("Lead time", "table_header"),
        ],
        [
            p("8a26dc3", "table_cell_center"),
            p("25-jul 16:57:29", "table_cell_center"),
            p("25-jul 17:01:00", "table_cell_center"),
            p("00:03:31", "table_cell_center"),
        ],
        [
            p("85eaa0f", "table_cell_center"),
            p("25-jul 17:02:01", "table_cell_center"),
            p("25-jul 17:04:20", "table_cell_center"),
            p("00:02:19", "table_cell_center"),
        ],
    ]
    story.append(simple_table(dora_rows, [38 * mm, 50 * mm, 50 * mm, 36 * mm]))
    metric_rows = [
        [p("Métrica", "table_header"), p("Cálculo", "table_header"), p("Resultado", "table_header"), p("Nivel", "table_header")],
        [p("Lead time", "table_cell"), p("(00:03:31 + 00:02:19) / 2", "table_cell"), p("00:02:55", "table_cell_center"), p("Élite", "table_cell_center")],
        [p("Frecuencia", "table_cell"), p("2 despliegues / 1 día", "table_cell"), p("2 por día", "table_cell_center"), p("Élite", "table_cell_center")],
        [p("CFR", "table_cell"), p("1 corrección / 3 intentos x 100", "table_cell"), p("33,33 %", "table_cell_center"), p("Medio", "table_cell_center")],
    ]
    story.extend([Spacer(1, 4 * mm), simple_table(metric_rows, [42 * mm, 70 * mm, 35 * mm, 27 * mm])])
    story.append(
        p(
            "La velocidad quedó en nivel Élite porque ambos cambios llegaron al clúster en pocos minutos "
            "y hubo dos despliegues correctos en un día. La estabilidad quedó en nivel Medio porque uno "
            "de los tres intentos necesitó corrección. La muestra es pequeña, por lo que estos niveles "
            "sirven para interpretar la práctica y deben recalcularse con más despliegues."
        )
    )
    story.append(evidence_image("69-dora-final.png", "Evidencia: commits, despliegues, lead times y resultado de los intentos.", 45 * mm))
    story.append(
        p(
            "Fuentes: evidencias/dora-deployments.csv, evidencias/despliegue-8a26dc3.txt y "
            "evidencias/despliegue-85eaa0f.txt. Los cambios se relacionan con los runs "
            "30176640875 y 30176786798 de GitHub Actions."
        )
    )
    story.append(PageBreak())

    # Demo 1
    story.append(h1("9", "Comandos para la demostración"))
    story.append(
        p(
            "Los siguientes bloques están preparados para PowerShell. Ejecutar desde la raíz del "
            "repositorio. Conviene usar dos terminales cuando se llegue al port-forward."
        )
    )
    story.append(h2("9.1 Herramientas y pruebas"))
    story.append(
        code(
            r"""
Set-Location "C:\Users\Fr4nk\Downloads\inventario-app\inventario-app"

node --version
npm.cmd --version
git --version
docker --version
kubectl version --client
minikube version

npm.cmd ci
npm.cmd test
"""
        )
    )
    story.append(p("<b>Debe observarse:</b> las versiones instaladas y 6 pruebas correctas, 0 fallidas.", "small"))

    story.append(h2("9.2 Construcción y contenedor Docker"))
    story.append(
        code(
            """
docker build -t inventario-app:local .
docker images inventario-app

docker rm -f inventario-local 2>$null
docker run -d --name inventario-local -p 3000:3000 inventario-app:local
docker ps --filter name=inventario-local
docker logs inventario-local

curl.exe http://localhost:3000/health
curl.exe http://localhost:3000/version
curl.exe http://localhost:3000/api/products
"""
        )
    )
    story.append(
        p(
            "<b>Debe observarse:</b> la etapa test durante el build, el contenedor Up y respuestas "
            "JSON con status ok, version v1, color blue y el catálogo.",
            "small",
        )
    )
    story.append(h2("9.3 Escaneo Trivy"))
    story.append(
        code(
            """
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock `
  -v trivy-cache:/root/.cache/ aquasec/trivy:0.72.0 image `
  --quiet --timeout 10m `
  --db-repository public.ecr.aws/aquasecurity/trivy-db:2 `
  --scanners vuln --vuln-type os,library --format table `
  --exit-code 1 --ignore-unfixed --severity CRITICAL `
  inventario-app:local
"""
        )
    )
    story.append(p("<b>Debe observarse:</b> el resumen del análisis sin vulnerabilidades CRITICAL.", "small"))
    story.append(PageBreak())

    # Demo 2
    story.append(h1("10", "Demostración en Kubernetes"))
    story.append(h2("10.1 Iniciar o comprobar Minikube"))
    story.append(
        code(
            """
minikube -p ci-cd status

# Ejecutar start solo si el perfil está detenido:
minikube -p ci-cd start --driver=docker --cpus=4 --memory=4096

kubectl get nodes
"""
        )
    )
    story.append(p("<b>Debe observarse:</b> el nodo ci-cd en estado Ready.", "small"))

    story.append(h2("10.2 Crear el Secret y desplegar la versión base"))
    story.append(
        code(
            """
kubectl create secret generic inventario-secret `
  --from-literal=API_KEY=CLAVE_LOCAL_DEMO `
  --dry-run=client -o yaml | kubectl apply -f -

kubectl get secret inventario-secret
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl rollout status deployment/inventario-app --timeout=240s
kubectl get deployment inventario-app -o wide
kubectl get pods -l app=inventario-app
"""
        )
    )
    story.append(
        p(
            "<b>Debe observarse:</b> Secret con un dato, Deployment 2/2 y dos pods Running 1/1. "
            "No mostrar el valor de API_KEY.",
            "small",
        )
    )

    story.append(h2("10.3 Abrir el acceso local"))
    story.append(p("<b>Terminal 1:</b>", "small"))
    story.append(code("kubectl port-forward service/inventario-service 8080:80"))
    story.append(p("<b>Terminal 2:</b>", "small"))
    story.append(
        code(
            """
$URL = "http://127.0.0.1:8080"
curl.exe "$URL/health"
curl.exe "$URL/version"
curl.exe "$URL/api/products"
"""
        )
    )
    story.append(
        p(
            "<b>Debe observarse:</b> health ok, la versión activa y la lista de productos. "
            "Mantener abierta la Terminal 1.",
            "small",
        )
    )
    story.append(PageBreak())

    # Demo 3
    story.append(h1("11", "Blue-Green, readiness y métricas"))
    story.append(h2("11.1 Aplicar Blue y Green"))
    story.append(
        code(
            """
kubectl apply -f k8s/blue-green/deployment-blue.yaml
kubectl apply -f k8s/blue-green/deployment-green.yaml
kubectl apply -f k8s/blue-green/service.yaml

kubectl rollout status deployment/inventario-app-blue --timeout=240s
kubectl rollout status deployment/inventario-app-green --timeout=240s
kubectl get pods -l app=inventario-app --show-labels
"""
        )
    )
    story.append(p("<b>Debe observarse:</b> dos pods Blue y dos pods Green en Running 1/1.", "small"))

    story.append(h2("11.2 Promover Green y demostrar rollback"))
    story.append(
        code(
            """
kubectl patch service inventario-service --type merge `
  --patch-file patch-green.json
kubectl get service inventario-service `
  -o jsonpath="{.spec.selector.slot}"

# Reiniciar el port-forward y luego consultar:
$URL = "http://127.0.0.1:8080"
curl.exe "$URL/version"

kubectl patch service inventario-service --type merge `
  --patch-file patch-blue.json
kubectl get service inventario-service `
  -o jsonpath="{.spec.selector.slot}"

# Reiniciar otra vez el port-forward:
curl.exe "$URL/version"
"""
        )
    )
    story.append(
        p(
            "<b>Debe observarse:</b> Green devuelve v2/green. Después del rollback, Blue devuelve "
            "v1/blue. El port-forward se debe detener con Ctrl+C y abrir otra vez después de cada cambio.",
            "small",
        )
    )

    story.append(h2("11.3 Readiness y métricas"))
    story.append(
        code(
            """
kubectl rollout restart deployment/inventario-app-green
kubectl get pods -l app=inventario-app,slot=green -w

# En otra terminal:
kubectl rollout status deployment/inventario-app-green --timeout=240s
kubectl get events --sort-by=.metadata.creationTimestamp |
  Select-String "inventario-app-green|Unhealthy" |
  Select-Object -Last 15

git log --pretty=format:"%h | %cI | %s" -10
Import-Csv evidencias/dora-deployments.csv |
  Format-Table attempt_id,version,commit_at,deployed_at,lead_time,result
"""
        )
    )
    story.append(
        p(
            "<b>Debe observarse:</b> pods que pasan de 0/1 a 1/1, eventos 503 de readiness y la tabla "
            "DORA con dos despliegues correctos y un intento fallido.",
            "small",
        )
    )

    story.append(h2("11.4 Limpieza al terminar"))
    story.append(
        code(
            """
docker rm -f inventario-local

# Detener port-forward con Ctrl+C antes de continuar.
kubectl delete -f k8s/blue-green/service.yaml --ignore-not-found
kubectl delete -f k8s/blue-green/deployment-blue.yaml --ignore-not-found
kubectl delete -f k8s/blue-green/deployment-green.yaml --ignore-not-found
minikube -p ci-cd stop
"""
        )
    )
    story.append(
        p(
            "La limpieza es opcional durante la exposición. Si se necesita repetir la demostración, "
            "conviene dejar Minikube iniciado y ejecutar solo los comandos de comprobación.",
            "note",
        )
    )

    doc.build(story)
    print(OUTPUT_PATH)


if __name__ == "__main__":
    build_pdf()
