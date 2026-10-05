"""Generate templates/reference.docx dari default pandoc, lalu di-styling.

Aturan style (ubah di sini, lalu jalankan ulang - jangan edit reference.docx langsung:
pandoc hanya membaca STYLES, dan file hasil generate akan menimpa edit manual):
    - Semua teks : Times New Roman 12pt
    - Heading    : Times New Roman 12pt bold (ukuran seragam)
    - Cover      : Times New Roman 14pt
    - Code block : Consolas 10.5pt (monospace)

Jalankan: python make_reference.py
"""
import subprocess
import sys
from pathlib import Path

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parent
REFERENCE = ROOT / "templates" / "reference.docx"
BLACK = RGBColor(0, 0, 0)
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def get_pandoc():
    for candidate in ("pandoc", str(Path.home() / "AppData/Local/Programs/pandoc/pandoc.exe")):
        try:
            subprocess.run([candidate, "--version"], capture_output=True, check=True)
            return candidate
        except (OSError, subprocess.CalledProcessError):
            continue
    sys.exit("pandoc tidak ditemukan")


def dump_default_reference(pandoc: str):
    data = subprocess.run([pandoc, "--print-default-data-file", "reference.docx"],
                          capture_output=True, check=True).stdout
    REFERENCE.write_bytes(data)


def set_run_font(rPr, font: str, half_points: int):
    """Set w:rFonts (ascii/hAnsi/cs/eastAsia) + w:sz pada elemen w:rPr."""
    for tag in ("rFonts", "sz", "szCs"):
        el = rPr.find(qn(f"w:{tag}"))
        if el is not None:
            rPr.remove(el)
    rFonts = rPr.makeelement(qn("w:rFonts"), {
        qn("w:ascii"): font, qn("w:hAnsi"): font,
        qn("w:cs"): font, qn("w:eastAsia"): font,
    })
    rPr.insert(0, rFonts)
    for tag in ("sz", "szCs"):
        rPr.append(rPr.makeelement(qn(f"w:{tag}"), {qn("w:val"): str(half_points)}))


def set_doc_defaults(doc: Document):
    """docDefaults: TNR 12pt — style tanpa definisi eksplisit tetap ikut."""
    styles_el = doc.styles.element
    rPr_default = styles_el.find(
        f"{W}docDefaults/{W}rPrDefault/{W}rPr")
    if rPr_default is None:
        doc_defaults = styles_el.find(f"{W}docDefaults")
        r_pr_default = doc_defaults.makeelement(f"{W}rPrDefault", {})
        rPr_default = r_pr_default.makeelement(f"{W}rPr", {})
        r_pr_default.append(rPr_default)
        doc_defaults.insert(0, r_pr_default)
    set_run_font(rPr_default, "Times New Roman", 24)  # 24 half-points = 12pt


def style(doc: Document):
    styles = doc.styles
    set_doc_defaults(doc)

    # Margin halaman: samakan dengan template LaTeX (2.5cm)
    for sec in doc.sections:
        sec.top_margin = sec.bottom_margin = Cm(2.5)
        sec.left_margin = sec.right_margin = Cm(2.5)

    for s in styles:
        name = s.name
        if "Verbatim" in name or "Source Code" in name:
            # Teks monospace (inline code & code block) — jangan kena TNR
            s.font.name = "Consolas"
            s.font.size = Pt(10.5)
            continue
        if s.type != WD_STYLE_TYPE.PARAGRAPH:
            continue

        s.font.name = "Times New Roman"
        s.font.size = Pt(12)

        if name in ("Normal", "Body Text", "First Paragraph", "Compact"):
            pf = s.paragraph_format
            pf.line_spacing = 1.5
            pf.space_before = Pt(0)
            pf.space_after = Pt(6)
            pf.first_line_indent = Pt(0)
        elif name.startswith("Heading"):
            s.font.bold = True
            s.font.color.rgb = BLACK
            pf = s.paragraph_format
            pf.line_spacing = 1.0
            pf.space_before = Pt(12)
            pf.space_after = Pt(6)
        elif name in ("Image Caption", "Table Caption", "Caption"):
            s.font.italic = True
            s.font.color.rgb = BLACK

    # Style khusus cover DOCX (dipakai oleh renderer.py via custom-style) — 14pt
    cover_styles = {
        "Cover Title":  (True, Pt(0), Pt(6)),
        "Cover Matkul": (True, Pt(6), Pt(6)),
        "Cover Judul":  (True, Pt(6), Pt(24)),
        "Cover Image":  (False, Pt(0), Pt(24)),
        "Cover Info":   (False, Pt(0), Pt(6)),
        "Cover Footer": (True, Pt(0), Pt(2)),
    }
    for name, (bold, before, after) in cover_styles.items():
        if name in styles:
            s = styles[name]
        else:
            s = styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
            s.base_style = styles["Normal"]
        s.font.name = "Times New Roman"
        s.font.size = Pt(14)
        s.font.bold = bold
        s.font.color.rgb = BLACK
        pf = s.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf.line_spacing = 1.0
        pf.space_before = before
        pf.space_after = after

    # Code block DOCX: kotak (border) + latar abu muda, monospace 10.5pt
    if "Source Code" in styles:
        code = styles["Source Code"]
    else:
        code = styles.add_style("Source Code", WD_STYLE_TYPE.PARAGRAPH)
        code.base_style = styles["Normal"]
    code.font.name = "Consolas"
    code.font.size = Pt(10.5)
    code.font.color.rgb = BLACK
    pf = code.paragraph_format
    pf.line_spacing = 1.0
    pf.space_before = Pt(6)
    pf.space_after = Pt(6)
    pf.first_line_indent = Pt(0)
    _add_code_box(code)


def _add_code_box(style):
    """Beri border + shading pada style paragraph code block (mirip snugshade PDF)."""
    pPr = style.element.get_or_add_pPr()

    shd = pPr.makeelement(qn("w:shd"), {
        qn("w:val"): "clear", qn("w:color"): "auto", qn("w:fill"): "F5F5F5",
    })
    pPr.append(shd)

    pBdr = pPr.makeelement(qn("w:pBdr"), {})
    for edge in ("top", "left", "bottom", "right"):
        pBdr.append(pPr.makeelement(qn(f"w:{edge}"), {
            qn("w:val"): "single", qn("w:sz"): "4",
            qn("w:space"): "6", qn("w:color"): "A6A6A6",
        }))
    pPr.append(pBdr)


def main():
    dump_default_reference(get_pandoc())
    doc = Document(str(REFERENCE))
    style(doc)
    doc.save(str(REFERENCE))
    print(f"OK: {REFERENCE}")


if __name__ == "__main__":
    main()
