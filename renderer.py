"""Core renderer: markdown laporan -> PDF (LaTeX) + DOCX.

Dipakai oleh cli.py (lokal) dan app.py (Flask API).
Jalankan dari root proyek, semua path relatif ROOT.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW_MD_DIR = ROOT / "raw-md"
OUTPUT_DIR = ROOT / "output_matkul"
METADATA_FILE = ROOT / "sample_metadata.json"
DOSEN_MAP_FILE = ROOT / "dosen_map.json"
LATEX_TEMPLATE = ROOT / "templates" / "polines_jobsheet.latex"
REFERENCE_DOCX = ROOT / "templates" / "reference.docx"
DEFAULT_FORMATS = ("pdf", "docx")


class RenderError(RuntimeError):
    pass


def _ensure_tool_path():
    """Install per-user (tanpa admin) tidak selalu masuk PATH shell."""
    candidates = [
        Path.home() / "AppData/Local/Programs/pandoc",
        Path.home() / "AppData/Local/Programs/MiKTeX/miktex/bin/x64",
    ]
    path = os.environ.get("PATH", "")
    for d in candidates:
        if d.is_dir() and str(d) not in path:
            path = f"{path}{os.pathsep}{d}"
            os.environ["PATH"] = path


_ensure_tool_path()


def load_static_metadata() -> dict:
    with open(METADATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def load_dosen_map() -> dict:
    if not DOSEN_MAP_FILE.exists():
        return {}
    with open(DOSEN_MAP_FILE, encoding="utf-8") as f:
        return {k.upper(): v for k, v in json.load(f).items()}


def get_dosen(matkul: str) -> str:
    return load_dosen_map().get(matkul.strip().upper(), "Dosen Pengampu")


def sanitize_filename(name: str) -> str:
    name = re.sub(r'[\\/:*?"<>|]', "", name)
    name = re.sub(r"\s+", "_", name.strip())
    name = re.sub(r"_+", "_", name).strip("._")
    return name or "laporan"


def build_docx_cover(meta: dict) -> str:
    """Cover DOCX memakai style custom dari templates/reference.docx."""
    info_lines = [
        f"Dosen: {meta.get('dosen', '')}\\",
        "Disusun oleh\\",
        f"Nama : {meta.get('author', '')}\\",
        f"NIM : {meta.get('nim', '')}\\",
        f"Kelas : {meta.get('kelas', '')}",
    ]
    footer_lines = [
        f"PROGRAM STUDI {meta.get('prodi', '')}\\",
        f"JURUSAN {meta.get('jurusan', '')}\\",
        "POLITEKNIK NEGERI SEMARANG\\",
        f"TAHUN {meta.get('tahun', '')}",
    ]
    page_break = '```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```'

    def block(style: str, body: str) -> str:
        return f'::: {{custom-style="{style}"}}\n{body}\n:::'

    parts = [
        block("Cover Title", "LAPORAN PRAKTIKUM"),
        block("Cover Matkul", str(meta.get("matkul", ""))),
        block("Cover Judul", str(meta.get("judul_jobsheet", ""))),
        block("Cover Image", f"![]({meta.get('logo', '')}){{width=5cm}}"),
        block("Cover Info", "\n".join(info_lines)),
        block("Cover Footer", "\n".join(footer_lines)),
        page_break,
    ]
    return "\n\n".join(parts)


def _run(cmd: list, input_text: str = None) -> None:
    try:
        proc = subprocess.run(
            cmd, input=input_text, capture_output=True, text=True,
            encoding="utf-8", errors="replace", cwd=str(ROOT),
        )
    except FileNotFoundError:
        raise RenderError(
            f"'{cmd[0]}' tidak ditemukan. Pastikan pandoc & MiKTeX terinstall "
            f"dan PATH sudah di-update (restart terminal lalu coba lagi)."
        )
    stderr = (proc.stderr or "").strip()
    # Buang noise MiKTeX (nag update) & tampilkan warning pandoc
    # (mis. gambar tidak ditemukan -> hilang diam-diam kalau tidak ditampilkan)
    for line in stderr.splitlines():
        if "have not checked for MiKTeX updates" in line:
            continue
        if line.startswith("[WARNING]"):
            print(f"  {line}", file=sys.stderr)
    if proc.returncode != 0:
        tail_lines = [
            l for l in stderr.splitlines()
            if "have not checked for MiKTeX updates" not in l
        ]
        raise RenderError(f"{cmd[0]} gagal (exit {proc.returncode}):\n"
                          + "\n".join(tail_lines[-15:]))


def _render_pdf(md_text: str, meta: dict, out_base: Path) -> Path:
    # .name + ".pdf" (bukan with_suffix) supaya titik di NIM tidak dipotong
    out = out_base.parent / (out_base.name + ".pdf")
    tmp = tempfile.NamedTemporaryFile(
        "w", suffix=".json", delete=False, encoding="utf-8")
    json.dump(meta, tmp, ensure_ascii=False)
    tmp.close()
    try:
        _run([
            "pandoc", "-f", "markdown+lists_without_preceding_blankline",
            "--metadata-file", tmp.name,
            "--template", str(LATEX_TEMPLATE),
            "--pdf-engine", "xelatex",
            "-o", str(out),
        ], input_text=md_text)
    finally:
        os.unlink(tmp.name)
    return out


def _render_docx(md_text: str, meta: dict, out_base: Path) -> Path:
    out = out_base.parent / (out_base.name + ".docx")
    combined = build_docx_cover(meta) + "\n\n" + md_text
    _run([
        "pandoc", "-f", "markdown+lists_without_preceding_blankline",
        "--reference-doc", str(REFERENCE_DOCX),
        "-o", str(out),
    ], input_text=combined)
    return out


def render_markdown(md_text: str, matkul: str, judul: str,
                    formats=DEFAULT_FORMATS, metadata: dict | None = None) -> list[Path]:
    """Render konten markdown laporan ke output_matkul/<MATKUL>/.

    Metadata statis dari sample_metadata.json, dosen otomatis dari
    dosen_map.json (kecuali di-override lewat `metadata`).
    """
    matkul = (matkul or "").strip().upper()
    judul = (judul or "").strip()
    if not matkul:
        raise RenderError("Nama matkul kosong.")
    if not judul:
        raise RenderError("judul_jobsheet kosong.")
    if not md_text.strip():
        raise RenderError("Kosong: konten markdown tidak ada.")

    meta = load_static_metadata()
    if metadata:
        meta.update({k: v for k, v in metadata.items() if v})
    meta["matkul"] = matkul
    meta["judul_jobsheet"] = judul
    if not meta.get("dosen"):
        meta["dosen"] = get_dosen(matkul)

    out_dir = OUTPUT_DIR / matkul
    out_dir.mkdir(parents=True, exist_ok=True)
    base = sanitize_filename(
        f"{meta.get('author', '')}_{meta.get('nim', '')}_{judul}")

    outputs = []
    if "pdf" in formats:
        outputs.append(_render_pdf(md_text, meta, out_dir / base))
    if "docx" in formats:
        outputs.append(_render_docx(md_text, meta, out_dir / base))
    return outputs


def render_file(md_path: str | Path, matkul: str, judul: str,
                formats=DEFAULT_FORMATS, metadata: dict | None = None) -> list[Path]:
    md_path = Path(md_path)
    if not md_path.is_file():
        raise RenderError(f"File tidak ditemukan: {md_path}")
    return render_markdown(
        md_path.read_text(encoding="utf-8"), matkul, judul, formats, metadata)
