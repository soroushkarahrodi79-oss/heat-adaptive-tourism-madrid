"""Build the bounded HATI-Madrid ResearchGate release PDF.

The scientific body comes from manuscript/MANUSCRIPT_TMP_v0.2.md. Only publication-
administration text is replaced; scientific results, methods, references, and captions
are not recalculated or rewritten.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
)

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = Path(__file__).resolve().parent
SOURCE = ROOT / "manuscript" / "MANUSCRIPT_TMP_v0.2.md"
OUTPUT = PACKAGE / "HATI_Madrid_Preprint_v1.0.pdf"
TITLE = (
    "Thermal representation as a decision variable in heat-adaptive tourism "
    "opportunity screening: evidence from a Madrid pilot"
)
REPO_URL = "https://github.com/soroushkarahrodi79-oss/heat-adaptive-tourism-madrid"

FIGURES = [
    ("Figure 1", ROOT / "outputs/publication/figures/FIG01_STUDY_DESIGN_v0.1.png"),
    ("Figure 2", ROOT / "outputs/publication/figures/FIG02_THERMAL_METHOD_DIVERGENCE_v0.1.png"),
    ("Figure 3", ROOT / "outputs/publication/figures/FIG03_SCREENING_CONSEQUENCE_v0.1.png"),
    ("Figure 4", ROOT / "outputs/publication/figures/FIG04_TESTED_UNCERTAINTY_v0.1.png"),
]


def normalize_pdf_text(value: str) -> str:
    """Use printable punctuation and ASCII hyphens while retaining names/units."""
    substitutions = {
        "\u2010": "-",
        "\u2011": "-",
        "\u2012": "-",
        "\u2013": "-",
        "\u2014": "-",
        "\u2212": "-",
        "\u2192": "->",
        "\u2248": "approximately ",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u00a0": " ",
    }
    for old, new in substitutions.items():
        value = value.replace(old, new)
    return value


def release_markdown() -> str:
    source = SOURCE.read_text(encoding="utf-8")
    first_break = source.index("\n---\n")
    body = source[first_break + len("\n---\n") :]

    declarations_start = body.index("# Declarations")
    references_start = body.index("# References")
    declarations = f"""# Release information

**Author:** Soroush Karahrodi

**Publication status.** Version 1.0 public preprint, prepared 2026-09-11 for public archival
dissemination. This document has not been peer reviewed and is not an operational or real-time
tourism product.

**Data/code availability.** Public materials are available from the repository below. It
contains the code, documented provenance, derived tables, and locked publication figures.
Repository URL: {REPO_URL}. Third-party data and software remain subject to their original
licences. No repository DOI has been assigned.

**License:** Creative Commons Attribution 4.0 International (CC BY 4.0).

**Ethics.** The study used open environmental and spatial data and involved no human
participants, personal data, interventions, surveys, or observed visitor behaviour.

"""
    body = body[:declarations_start] + declarations + body[references_start:]
    front = f"""# {TITLE}

**Soroush Karahrodi**

Version 1.0 - public preprint - 2026-09-11

**Non-peer-reviewed preprint / research work**

"""
    return normalize_pdf_text(front + body)


def register_fonts() -> tuple[str, str, str]:
    font_dir = Path("C:/Windows/Fonts")
    regular = font_dir / "arial.ttf"
    bold = font_dir / "arialbd.ttf"
    italic = font_dir / "ariali.ttf"
    if regular.exists() and bold.exists() and italic.exists():
        pdfmetrics.registerFont(TTFont("HATIRegular", str(regular)))
        pdfmetrics.registerFont(TTFont("HATIBold", str(bold)))
        pdfmetrics.registerFont(TTFont("HATIItalic", str(italic)))
        pdfmetrics.registerFontFamily(
            "HATIRegular",
            normal="HATIRegular",
            bold="HATIBold",
            italic="HATIItalic",
            boldItalic="HATIBold",
        )
        return "HATIRegular", "HATIBold", "HATIItalic"
    return "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"


def inline_markup(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<link href="\2">\1</link>', text)
    text = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    return text


def markdown_flowables(markdown: str, styles: dict[str, ParagraphStyle]):
    lines = markdown.splitlines()
    story = []
    paragraph: list[str] = []
    in_code = False
    code: list[str] = []

    def flush_paragraph():
        if paragraph:
            story.append(Paragraph(inline_markup(" ".join(paragraph)), styles["body"]))
            story.append(Spacer(1, 2.2 * mm))
            paragraph.clear()

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            flush_paragraph()
            if in_code:
                story.append(Preformatted("\n".join(code), styles["code"]))
                story.append(Spacer(1, 2 * mm))
                code.clear()
            in_code = not in_code
            continue
        if in_code:
            code.append(line)
            continue
        if not stripped:
            flush_paragraph()
            continue
        if stripped == "---":
            flush_paragraph()
            story.append(Spacer(1, 2 * mm))
            continue
        heading = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            level = len(heading.group(1))
            text = inline_markup(heading.group(2))
            if story and level == 1 and not heading.group(2).startswith(TITLE):
                story.append(PageBreak())
            story.append(Paragraph(text, styles[f"h{level}"]))
            story.append(Spacer(1, 2 * mm))
            continue
        bullet = re.match(r"^[-*]\s+(.+)$", stripped)
        if bullet:
            flush_paragraph()
            story.append(Paragraph(inline_markup(bullet.group(1)), styles["bullet"], bulletText="-"))
            continue
        paragraph.append(stripped)
    flush_paragraph()
    return story


def build() -> Path:
    for _, figure in FIGURES:
        if not figure.exists():
            raise FileNotFoundError(figure)

    regular, bold, italic = register_fonts()
    base = getSampleStyleSheet()
    styles = {
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName=regular,
            fontSize=9.2,
            leading=12.2,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#222222"),
            spaceAfter=0,
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontName=bold,
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#173A4A"),
            spaceBefore=4 * mm,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontName=bold,
            fontSize=12.5,
            leading=15,
            textColor=colors.HexColor("#24586C"),
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "H3",
            parent=base["Heading3"],
            fontName=bold,
            fontSize=10.5,
            leading=13,
            keepWithNext=True,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["BodyText"],
            fontName=regular,
            fontSize=9.2,
            leading=12.2,
            leftIndent=5 * mm,
            firstLineIndent=-3 * mm,
            spaceAfter=1.2 * mm,
        ),
        "code": ParagraphStyle(
            "Code",
            parent=base["Code"],
            fontName="Courier",
            fontSize=7.3,
            leading=9,
            leftIndent=4 * mm,
            textColor=colors.HexColor("#333333"),
        ),
        "caption": ParagraphStyle(
            "Caption",
            parent=base["BodyText"],
            fontName=italic,
            fontSize=8.3,
            leading=10.5,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#444444"),
        ),
        "footer": ParagraphStyle("Footer", fontName=regular, fontSize=7.5, textColor=colors.grey),
    }

    def page_frame(canvas, doc):
        canvas.saveState()
        canvas.setFont(regular, 7.5)
        canvas.setFillColor(colors.HexColor("#666666"))
        canvas.drawString(22 * mm, 12 * mm, "HATI-Madrid - non-peer-reviewed preprint")
        canvas.drawRightString(A4[0] - 22 * mm, 12 * mm, str(doc.page))
        canvas.restoreState()

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=22 * mm,
        leftMargin=22 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        title=TITLE,
        author="Soroush Karahrodi",
        subject="Non-peer-reviewed preprint",
        creator="HATI-Madrid reproducible PDF builder",
        invariant=1,
    )
    story = markdown_flowables(release_markdown(), styles)
    story.append(PageBreak())
    story.append(Paragraph("Embedded publication figures", styles["h1"]))
    story.append(Paragraph(
        "These are the locked repository figures. Captions and claim boundaries are retained "
        "in the manuscript and the package figure inventory.", styles["body"]
    ))
    for label, path in FIGURES:
        story.append(PageBreak())
        img = Image(str(path))
        max_width, max_height = 166 * mm, 225 * mm
        scale = min(max_width / img.imageWidth, max_height / img.imageHeight)
        img.drawWidth = img.imageWidth * scale
        img.drawHeight = img.imageHeight * scale
        story.append(KeepTogether([img, Spacer(1, 3 * mm), Paragraph(label, styles["caption"])]))

    doc.build(story, onFirstPage=page_frame, onLaterPages=page_frame)
    return OUTPUT


if __name__ == "__main__":
    print(build())
