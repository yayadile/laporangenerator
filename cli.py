"""CLI Generator Laporan Polines - render raw-md/ -> PDF & DOCX.

Interaktif (default):
    python cli.py
Non-interaktif:
    python cli.py laporan-ctf-5007-idor.md --matkul "ETHICAL HACKING" --judul "LAB 03 IDOR"
"""
import argparse
import sys
from pathlib import Path

import renderer
from renderer import RenderError

DEFAULT_FORMATS = ("pdf", "docx")


def choose_option(prompt: str, options: list[str], new_hint: str = "") -> str:
    """Pilih dari daftar via angka/teks (case-insensitive), boleh bikin baru."""
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    if new_hint:
        print(f"  ({new_hint})")
    while True:
        pick = input(prompt).strip()
        if pick.isdigit() and 1 <= int(pick) <= len(options):
            return options[int(pick) - 1]
        if not pick:
            continue
        match = next((o for o in options if o.upper() == pick.upper()), None)
        if match:
            return match
        if new_hint:
            return pick.upper()
        print("  Input tidak dikenali, coba lagi.")


def list_raw_md() -> list[Path]:
    return sorted(renderer.RAW_MD_DIR.glob("*.md"))


def list_matkul() -> list[str]:
    names = set()
    if renderer.OUTPUT_DIR.is_dir():
        names.update(p.name for p in renderer.OUTPUT_DIR.iterdir() if p.is_dir())
    names.update(renderer.load_dosen_map().keys())
    return sorted(names, key=str.upper)


def choose_md(preselect: str | None) -> Path:
    files = list_raw_md()
    if not files:
        raise RenderError(f"Tidak ada file .md di {renderer.RAW_MD_DIR}")

    if preselect:
        path = Path(preselect)
        if not path.exists():
            path = renderer.RAW_MD_DIR / preselect
        if not path.exists():
            path = renderer.RAW_MD_DIR / f"{preselect}.md"
        if not path.is_file():
            raise RenderError(f"File tidak ditemukan: {preselect}")
        return path

    print("\nFile markdown di raw-md/:")
    names = [f.name for f in files]
    chosen = choose_option("Pilih file (angka/nama): ", names)
    return renderer.RAW_MD_DIR / chosen


def parse_formats(value: str | None) -> tuple:
    if not value:
        return DEFAULT_FORMATS
    formats = tuple(f.strip().lower() for f in value.split(",") if f.strip())
    invalid = set(formats) - set(DEFAULT_FORMATS)
    if invalid:
        raise RenderError(f"Format tidak didukung: {', '.join(invalid)}")
    return formats


def main() -> int:
    parser = argparse.ArgumentParser(description="Render laporan markdown -> PDF/DOCX")
    parser.add_argument("markdown", nargs="?", help="file di raw-md/ (atau path), default: pilih dari daftar")
    parser.add_argument("--matkul", help="nama matkul (folder output), default: pilih dari daftar")
    parser.add_argument("--judul", help="judul jobsheet, default: ditanya saat interaktif")
    parser.add_argument("--dosen", help="override dosen (default: otomatis dari dosen_map.json)")
    parser.add_argument("--formats", help="pdf,docx (default: pdf,docx)")
    args = parser.parse_args()

    print("=" * 50)
    print("   CLI GENERATOR LAPORAN JOBSHEET POLINES")
    print("=" * 50)

    try:
        formats = parse_formats(args.formats)
        md_path = choose_md(args.markdown)
        print(f"-> File: {md_path.name}")

        matkul = args.matkul or choose_option(
            "\nPilih folder matkul: ", list_matkul(), new_hint="ketik nama baru untuk bikin folder")
        matkul = matkul.strip().upper()

        dosen = args.dosen or renderer.get_dosen(matkul)
        print(f"-> Dosen otomatis: {dosen}")

        judul = args.judul
        if not judul:
            judul = input("Masukkan Judul Jobsheet (contoh: LAB 03 Analisis IDOR): ").strip()

        print(f"\nSedang me-render {', '.join(formats).upper()}...")
        outputs = renderer.render_file(
            md_path, matkul, judul, formats,
            metadata={"dosen": dosen} if dosen else None,
        )

        print("\nSUCCESS! File tersimpan di:")
        for p in outputs:
            print(f"  - {p}")
        return 0

    except (RenderError, KeyboardInterrupt) as e:
        msg = "\nDibatalkan." if isinstance(e, KeyboardInterrupt) else f"\nERROR: {e}"
        print(msg)
        return 1


if __name__ == "__main__":
    sys.exit(main())
