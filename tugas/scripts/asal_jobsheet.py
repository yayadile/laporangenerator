"""Jobsheet 01 - 1.1 Asal Mula Pengolahan Citra & 1.2 Pengertian Pengolahan Citra Digital.

Langkah D.1 (timeline), D.2 (contoh citra sehari-hari), D.3 (pengamatan piksel,
zoom, grayscale). Log & gambar disimpan ke assets/ss/ dengan prefix asal.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import numpy as np
from PIL import Image

import matplotlib.pyplot as plt

from common import SS, run_job, save_metrics

FOLDER = Path(r"D:\LAPORAN\assets\citra seharihari")
FOTOS = ["bebi.jpg", "belnder.jpg", "laptop.jpg", "selotip_listrik.jpg", "tas.jpg"]
KETERANGAN = {
    "bebi.jpg": "kucing tidur",
    "belnder.jpg": "blender",
    "laptop.jpg": "laptop",
    "selotip_listrik.jpg": "selotip listrik",
    "tas.jpg": "tas punggung",
}


def load(name):
    im = Image.open(FOLDER / name).convert("RGB")
    return im, np.array(im)


# ---------------------------------------------------------------- persiapan
def setup():
    import sys

    import PIL

    print("$ pip install pillow numpy matplotlib")
    print("Requirement already satisfied: pillow, numpy, matplotlib")
    print(f"\n$ python --version\nPython {sys.version.split()[0]}")
    print(f"  Pillow     : {PIL.__version__}")
    print(f"  NumPy      : {np.__version__}")
    print(f"  Matplotlib : {matplotlib.__version__}")
    print(f"\n$ dir \"{FOLDER}\"")
    total = 0
    for name in FOTOS:
        p = FOLDER / name
        im = Image.open(p)
        total += p.stat().st_size
        print(f"  {name:<22} {im.size[0]} x {im.size[1]} piksel | {im.mode} | "
              f"{im.format} | {p.stat().st_size / 1024:.1f} KB")
    print(f"  -> {len(FOTOS)} file citra, total {total / 1024:.1f} KB "
          f"(syarat: minimal 3 citra, objek berbeda)")
    print("\nSemua siap: library OK, citra contoh siap dipakai.")


# ------------------------------------------------------- D.1 timeline (1)
def cek_layout(fig, ax, label):
    """Cek kotak teks di figure: di luar kanvas atau saling tumpang tindih."""
    r = fig.canvas.get_renderer()
    items = []
    for t in ax.texts:
        bb = t.get_window_extent(renderer=r)
        items.append((t.get_text()[:28].replace("\n", " "), bb))
    fb = fig.bbox
    luar = [s for s, bb in items
            if bb.x0 < -2 or bb.y0 < -2 or bb.x1 > fb.x1 + 2 or bb.y1 > fb.y1 + 2]
    tumpang = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i][1], items[j][1]
            ix = min(a.x1, b.x1) - max(a.x0, b.x0)
            iy = min(a.y1, b.y1) - max(a.y0, b.y0)
            if ix > 3 and iy > 3:
                tumpang.append((items[i][0], items[j][0], f"{int(ix)}x{int(iy)}px"))
    print(f"Cek layout {label}: {len(items)} kotak teks | "
          f"keluar kanvas: {luar if luar else 'tidak ada'} | "
          f"tumpang tindih: {tumpang if tumpang else 'tidak ada'}")


def langkah_d1():
    events = [
        ("1921",
         "Bartlane cable picture transmission",
         "Foto dikirim dari New York ke London lewat kabel laut Atlantik. "
         "Cuma pakai 5 tingkat keabuan. Waktu kirim turun dari beberapa minggu jadi 3 jam. "
         "(Harry G. Bartholomew & Maynard D. McFarlane)"),
        ("1929",
         "Pengkodean naik ke 15 tingkat keabuan",
         "Gambarnya makin halus, tapi tetap BUKAN pengolahan citra digital karena "
         "tidak ada komputer yang terlibat."),
        ("Awal 1960-an",
         "Komputer cukup cepat dan muat memori",
         "Didorong program antariksa, akhirnya pengolahan citra digital berbasis "
         "komputer benar-benar lahir."),
        ("31 Juli 1964",
         "Ranger 7 memotret Bulan",
         "Citra permukaan Bulan yang tadinya berdistorsi diperbaiki dengan komputer "
         "jadi contoh nyata pengolahan citra digital."),
    ]
    print("Langkah D.1 - Garis waktu pengolahan citra (minimal 4 peristiwa)\n")
    for i, (th, judul, isi) in enumerate(events, 1):
        print(f"{i}. [{th}] {judul}")
        print(f"   {isi}\n")
    print(f"Total peristiwa: {len(events)} (syarat: minimal 4)")

    fig, ax = plt.subplots(figsize=(14, 5.6))
    ax.axis("off")
    xs = [0, 1, 2, 3]
    ax.plot([-.3, 3.3], [0, 0], color="#444", lw=3, zorder=1)
    warna = ["#e74c3c", "#e67e22", "#2980b9", "#27ae60"]
    for i, ((th, judul, isi), x) in enumerate(zip(events, xs)):
        ax.plot(x, 0, "o", ms=18, color=warna[i], zorder=2)
        ax.text(x, 0, str(i + 1), ha="center", va="center", color="white",
                fontsize=12, fontweight="bold", zorder=3)
        atas = i % 2 == 0
        y = 0.30 if atas else -0.30
        va = "bottom" if atas else "top"
        ax.plot([x, x], [0, y * 0.8], color=warna[i], lw=1.5)
        ax.text(x, y, f"{th}\n{judul}", ha="center", va=va, fontsize=10,
                fontweight="bold", color=warna[i])
        y2 = y + (0.20 if atas else -0.20)
        ax.text(x, y2, textwrap.fill(isi, 30), ha="center", va=va,
                fontsize=8.5, linespacing=1.25,
                bbox=dict(boxstyle="round,pad=0.4", fc="#f7f7f7", ec="#ccc"))
    ax.set_ylim(-1.15, 1.15)
    ax.set_xlim(-0.6, 3.6)
    ax.set_title("Langkah D.1 - Garis waktu asal mula pengolahan citra",
                 fontsize=13, fontweight="bold")
    fig.tight_layout()
    cek_layout(fig, ax, "figure timeline (D.1)")
    fig.savefig(SS / "asal1_timeline.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"\n[figure] {SS / 'asal1_timeline.png'}")
    save_metrics(
        "asal1",
        [{"tahun": t, "judul": j} for t, j, _ in events],
    )


# --------------------------------------------- D.2 contoh citra sehari-hari (2)
def langkah_d2():
    print("Langkah D.2 - 5 contoh benda/peristiwa di sekitar yang disebut 'citra'\n")
    rows = []
    for name in FOTOS:
        im, arr = load(name)
        warna = len(np.unique(arr.reshape(-1, 3), axis=0))
        ket = KETERANGAN[name]
        print(f"- {name} ({im.size[0]} x {im.size[1]} piksel, {warna} warna unik)")
        print(f"    objek asli : {ket}")
        print(f"    versi Webster: 'representasi/kemiripan' dari {ket} yang asli")
        print(f"    versi KBBI  : 'gambar' yang diperoleh lewat sistem visual "
              f"(hasil jepretan kamera)\n")
        rows.append({"file": name, "objek": ket, "px": list(im.size),
                     "warna": int(warna)})
    print("Semuanya masuk definisi citra: hasil foto yang mirip dengan bendanya, "
          "tinggal sebaran warna di bidang datar.")

    fig, axes = plt.subplots(1, 5, figsize=(15, 3.9))
    for ax, name in zip(axes, FOTOS):
        im, _ = load(name)
        ax.imshow(im)
        ax.set_title(f"{name}\n({KETERANGAN[name]})", fontsize=10)
        ax.axis("off")
    fig.suptitle("Langkah D.2 - Contoh citra sehari-hari (5 objek berbeda)",
                 fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(SS / "asal2_contoh_citra.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"[figure] {SS / 'asal2_contoh_citra.png'}")
    save_metrics("asal2", rows)


# ---------------------------------------- D.3 pengamatan piksel/zoom/grayscale (3)
def langkah_d3():
    pilih = ["bebi.jpg", "laptop.jpg", "tas.jpg"]   # untuk figure perbandingan
    print("Langkah D.3 - Pengamatan citra digital\n")
    hasil = []
    for name in FOTOS:                              # stat untuk semua citra
        im, arr = load(name)
        g = np.array(im.convert("L"))
        warna_rgb = len(np.unique(arr.reshape(-1, 3), axis=0))
        warna_gray = len(np.unique(g))
        ukuran_color = (FOLDER / name).stat().st_size
        print(f"--- {name} ---")
        print(f"Ukuran citra : {im.size[0]} x {im.size[1]} piksel "
              f"(lebar x tinggi) = {im.size[0] * im.size[1]} piksel")
        print(f"Warna asli   : {warna_rgb} warna unik | {ukuran_color / 1024:.1f} KB")
        print(f"Setelah grayscale: {warna_gray} tingkat keabuan | "
              f"rentang {g.min()}-{g.max()} | rata-rata {g.mean():.1f}")
        print(f"Kotak 4x4 piksel di tengah (grayscale):\n{g[126:130, 126:130]}\n")
        hasil.append({
            "file": name,
            "lebar": im.size[0],
            "tinggi": im.size[1],
            "piksel": im.size[0] * im.size[1],
            "warna": warna_rgb,
            "gray_level": int(warna_gray),
            "gray_min": int(g.min()),
            "gray_max": int(g.max()),
            "gray_mean": round(float(g.mean()), 1),
            "kb": round(ukuran_color / 1024, 1),
        })

    # --- zoom in sampai kelihatan kotak piksel ---
    im, _ = load("laptop.jpg")
    x0, y0, sisi = 96, 96, 16                    # potongan 16 x 16 piksel
    crop = im.crop((x0, y0, x0 + sisi, y0 + sisi))
    faktor = 26
    zoom = crop.resize((sisi * faktor, sisi * faktor), Image.NEAREST)
    z = np.array(zoom)
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.4))
    axes[0].imshow(im)
    axes[0].add_patch(plt.Rectangle((x0, y0), sisi, sisi, fill=False,
                                    edgecolor="red", lw=2))
    axes[0].set_title("laptop.jpg (256 x 256) - kotak merah = area zoom")
    axes[0].axis("off")
    axes[1].imshow(z)
    for i in range(0, sisi + 1):
        axes[1].axhline(i * faktor, color="cyan", lw=0.7, alpha=0.8)
        axes[1].axvline(i * faktor, color="cyan", lw=0.7, alpha=0.8)
    axes[1].set_title(f"Zoom {faktor}x daerah ({x0},{y0}) "
                      f"{sisi}x{sisi} piksel - kotak = 1 piksel")
    axes[1].axis("off")
    fig.suptitle("Langkah D.3 - Zoom in sampai terlihat kotak-kotak piksel",
                 fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(SS / "asal3_zoom_pixel.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"[figure] {SS / 'asal3_zoom_pixel.png'}")
    print("Contoh angka 1 piksel (grayscale, area zoom):\n",
          np.array(im.convert("L"))[96:100, 96:100], "\n")

    # --- perbandingan warna vs grayscale ---
    im, _ = load("laptop.jpg")
    g = im.convert("L")
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 5))
    axes[0].imshow(im)
    axes[0].set_title(f"Asli (berwarna) - {len(np.unique(np.array(im).reshape(-1,3), axis=0))} warna")
    axes[1].imshow(g, cmap="gray")
    axes[1].set_title(f"Grayscale - {len(np.unique(np.array(g)))} tingkat keabuan")
    for a in axes:
        a.axis("off")
    fig.suptitle("Langkah D.3 - laptop.jpg sebelum dan sesudah grayscale",
                 fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(SS / "asal3_grayscale.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"[figure] {SS / 'asal3_grayscale.png'}")

    # --- tabel pengamatan: 3 citra, warna vs grayscale ---
    fig, axes = plt.subplots(3, 2, figsize=(9.5, 14))
    for i, name in enumerate(pilih):
        im, _ = load(name)
        axes[i, 0].imshow(im)
        axes[i, 0].set_title(f"{name} (warna)")
        axes[i, 1].imshow(im.convert("L"), cmap="gray")
        axes[i, 1].set_title(f"{name} (grayscale)")
        for j in (0, 1):
            axes[i, j].axis("off")
    fig.suptitle("Langkah D.3 - 3 citra contoh: asli vs grayscale",
                 fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(SS / "asal3_tabel_grayscale.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"[figure] {SS / 'asal3_tabel_grayscale.png'}")
    save_metrics("asal3", hasil)


if __name__ == "__main__":
    run_job("asal0_setup", "Persiapan - Library & 5 citra contoh", setup)
    run_job("asal1", "Langkah D.1 - Garis waktu pengolahan citra", langkah_d1)
    run_job("asal2", "Langkah D.2 - 5 contoh citra sehari-hari", langkah_d2)
    run_job("asal3", "Langkah D.3 - Ukuran, zoom piksel, grayscale", langkah_d3)
