#!/usr/bin/env python
"""Kompres gambar di assets/ supaya repo tidak kegemukan.

Strategi (nama file & ekstensi TIDAK berubah -> path di markdown tetap valid):
  1. Downscale lebar maksimal --max-width px (LUANCZOS), cukup untuk cetak 150dpi
     di halaman A4 (lebar teks 16cm ~ 950px).
  2. Coba beberapa cara encode PNG (optimal truecolor / palet 256 warna +
     dither) dan pilih yang paling kecil.
  3. Simpan hanya bila lebih kecil minimal --min-saving (default 10%).

Pakai:
  python tools/compress_assets.py                 # dry-run: laporan saja
  python tools/compress_assets.py --out <dir>     # tulis hasil ke <dir> (preview)
  python tools/compress_assets.py --apply         # timpa file asli

Mengembalikan kondisi semula: git checkout -- assets
"""
from __future__ import annotations

import argparse
import io
import math
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DIR = ROOT / "assets"


def _psnr(ref: Image.Image, got: Image.Image) -> float:
    """Peak signal-to-noise ratio (dB) antara gambar asli vs hasil kompresi.

    ~inf = lossless, >40 dB = tak bedakan mata, <32 dB = posterization ketara.
    """
    from PIL import ImageChops, ImageStat

    diff = ImageChops.difference(ref.convert("RGB"), got.convert("RGB"))
    stat = ImageStat.Stat(diff)
    mse = sum(r * r for r in stat.rms) / len(stat.rms)
    if mse <= 0:
        return float("inf")
    return 10 * math.log10(255 * 255 / mse)


def _encode_variants(img: Image.Image) -> list[tuple[str, bytes, float]]:
    """Kembalikan [(metode, bytes PNG, psnr)] untuk beberapa strategi kompresi."""
    variants: list[tuple[str, bytes, float]] = []

    def dump(im: Image.Image, label: str, quality: float) -> None:
        buf = io.BytesIO()
        im.save(buf, format="PNG", optimize=True, compress_level=9)
        variants.append((label, buf.getvalue(), quality))

    # 1) truecolor optimal -> lossless, selalu kandidat sah
    dump(img, "truecolor", float("inf"))

    has_alpha = img.mode in ("RGBA", "LA") or "transparency" in img.info
    if has_alpha:
        rgba = img.convert("RGBA")
        # FASTOCTREE satu-satunya metode Pillow yang menjaga alpha saat quantize
        pal = rgba.quantize(colors=256, method=Image.Quantize.FASTOCTREE)
        dump(pal, "palet256+alpha", _psnr(rgba, pal))
    else:
        rgb = img.convert("RGB")
        pal = rgb.quantize(
            colors=256,
            method=Image.Quantize.MEDIANCUT,
            dither=Image.Dither.FLOYDSTEINBERG,
        )
        dump(pal, "palet256", _psnr(rgb, pal))
    return variants


def process(path: Path, out_dir: Path | None, max_width: int,
            min_saving: float, min_psnr: float, apply: bool) -> dict | None:
    before = path.read_bytes()
    with Image.open(path) as im:
        img = ImageOps.exif_transpose(im)
        resized = False
        if img.width > max_width:
            ratio = max_width / img.width
            img = img.resize(
                (max_width, max(1, round(img.height * ratio))),
                Image.Resampling.LANCZOS,
            )
            resized = True

        candidates = _encode_variants(img)
        # hanya pakai metode lossy bila kualitasnya masih di atas --min-psnr
        acceptable = [c for c in candidates if c[2] >= min_psnr] or candidates
        method, data, psnr = min(acceptable, key=lambda c: len(c[1]))

        if not resized:
            saved = 1 - len(data) / len(before)
            if saved < min_saving:
                return {
                    "name": path.name, "before": len(before), "after": len(before),
                    "method": "skip", "psnr": psnr, "size": (img.width, img.height),
                }

    target = (out_dir / path.relative_to(DEFAULT_DIR)) if out_dir else path
    if apply or out_dir:
        if out_dir:
            target.parent.mkdir(parents=True, exist_ok=True)
        # pastikan hasil valid sebelum menimpa
        with Image.open(io.BytesIO(data)) as chk:
            chk.verify()
        target.write_bytes(data)

    return {
        "name": str(path.relative_to(DEFAULT_DIR)),
        "before": len(before),
        "after": len(data),
        "method": f"{method}{' +resize' if resized else ''}",
        "psnr": psnr,
        "size": (img.width, img.height),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Kompres assets/ tanpa ganti nama file")
    ap.add_argument("--dir", type=Path, default=DEFAULT_DIR, help="folder gambar")
    ap.add_argument("--max-width", type=int, default=1600)
    ap.add_argument("--min-saving", type=float, default=0.10,
                    help="threshold penghematan agar file ditimpa (0-1)")
    ap.add_argument("--min-psnr", type=float, default=34.0,
                    help="batas kualitas (dB) untuk metode lossy; foto biasanya "
                         "gagal di sini dan otomatis pakai truecolor")
    ap.add_argument("--apply", action="store_true", help="timpa file asli")
    ap.add_argument("--out", type=Path, default=None,
                    help="tulis hasil ke folder ini (preview, file asli aman)")
    args = ap.parse_args()

    files = sorted(p for p in args.dir.rglob("*")
                   if p.suffix.lower() == ".png")
    if not files:
        print(f"Tidak ada PNG di {args.dir}")
        return 1

    results = []
    for f in files:
        r = process(f, args.out, args.max_width, args.min_saving,
                    args.min_psnr, args.apply)
        if r:
            results.append(r)

    print(f"{'file':<45} {'sebelum':>9} {'sesudah':>9} {'hemat':>7} {'psnr':>6}  cara")
    print("-" * 100)
    total_before = total_after = 0
    for r in results:
        total_before += r["before"]
        total_after += r["after"]
        saved = 1 - r["after"] / r["before"] if r["before"] else 0
        psnr = "lossless" if math.isinf(r["psnr"]) else f"{r['psnr']:.1f}"
        print(f"{r['name']:<45} {r['before']/1024:7.0f}K "
              f"{r['after']/1024:7.0f}K {saved*100:6.1f}% {psnr:>6}  {r['method']}")
    print("-" * 100)
    print(f"{'TOTAL':<45} {total_before/1024:7.0f}K {total_after/1024:7.0f}K "
          f"{(1-total_after/total_before)*100:6.1f}%")
    mode = "DITIMPA" if args.apply else (f"-> {args.out}" if args.out else "dry-run (belum diubah)")
    print(f"Mode: {mode} | {len(results)} file | "
          f"{(total_before-total_after)/1024/1024:.2f} MB dihemat")
    if not args.apply and not args.out:
        print("Jalankan dengan --apply untuk menimpa, atau --out <dir> untuk preview.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
