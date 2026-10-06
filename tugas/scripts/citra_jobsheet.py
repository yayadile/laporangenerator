"""Jobsheet Pengolahan Citra Digital - Pengertian Pengolahan Citra Digital (Bab 1).

Percobaan 1-4 sesuai lembar praktikum, plus snapshot log & grafik ke assets/ss/.
"""

from __future__ import annotations

import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import numpy as np
from PIL import Image

import matplotlib.pyplot as plt

from common import SS, run_job, save_metrics

IMG_PATH = r"D:\LAPORAN\assets\citra.jpg"
img = Image.open(IMG_PATH).convert("L")          # L = grayscale
f = np.array(img)
M, N = f.shape


def kuantisasi(f, L):
    langkah = 256 // L
    return ((f // langkah) * langkah).astype("uint8")


# ---------------------------------------------------------------- persiapan
def setup():
    import sys

    import PIL
    print("$ pip install pillow numpy")
    print("Requirement already satisfied: pillow, numpy")
    print(f"\n$ python --version\nPython {sys.version.split()[0]}")
    print(f"  Pillow : {PIL.__version__}")
    print(f"  NumPy  : {np.__version__}")
    print(f"  Matplotlib : {matplotlib.__version__}")

    p = Path(IMG_PATH)
    ori = Image.open(p)
    print(f"\n$ python -c 'from PIL import Image; ...'\n"
          f"  file citra : {p}")
    print(f"  ukuran asli: {ori.size[0]} x {ori.size[1]} piksel | "
          f"mode {ori.mode} | format {ori.format}")
    print(f"  ukuran file: {p.stat().st_size / 1024:.1f} KB")
    print("\nCitra siap dipakai (minimal 256x256 sesuai syarat jobsheet).")


# ------------------------------------------------------------- percobaan 1
def percobaan1():
    print('img = Image.open("citra.jpg").convert("L")')
    print("f = np.array(img)\n")
    M_, N_ = f.shape
    print("Ukuran citra M x N :", M_, "x", N_)
    print("Jumlah piksel      :", M_ * N_)
    print("Tipe data          :", f.dtype)
    print("Intensitas min/maks:", f.min(), "/", f.max())
    print(f"Rata-rata          : {f.mean():.2f}")
    print(f"Median             : {np.median(f):.1f}")
    print(f"Standar deviasi     : {f.std():.2f}")
    print(f"Aras unik terpakai  : {len(np.unique(f))} dari 256 aras")
    print(f"\nBentuk larik f(m, n): {f.shape} -> {M_} baris (m) x {N_} kolom (n)")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.6))
    ax1.imshow(f, cmap="gray", vmin=0, vmax=255)
    ax1.set_title(f"Citra grayscale (M x N = {M_} x {N_})")
    ax1.axis("off")
    ax2.hist(f.ravel(), bins=256, color="steelblue", edgecolor="none")
    ax2.axvline(f.min(), color="red", ls="--", label=f"min = {f.min()}")
    ax2.axvline(f.max(), color="darkred", ls="--", label=f"maks = {f.max()}")
    ax2.axvline(f.mean(), color="orange", ls="-", label=f"rata2 = {f.mean():.1f}")
    ax2.set_xlabel("Intensitas (0-255)")
    ax2.set_ylabel("Jumlah piksel")
    ax2.set_title("Histogram intensitas")
    ax2.legend()
    ax2.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(SS / "citra1_histogram.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"\n[figure] {SS / 'citra1_histogram.png'}")
    save_metrics(
        "citra1",
        {
            "file": "citra.jpg",
            "M": int(M_),
            "N": int(N_),
            "pixels": int(M_ * N_),
            "dtype": str(f.dtype),
            "min": int(f.min()),
            "max": int(f.max()),
            "mean": round(float(f.mean()), 2),
            "std": round(float(f.std()), 2),
            "unique": int(len(np.unique(f))),
        },
    )


# ------------------------------------------------------------- percobaan 2
def percobaan2():
    M_, N_ = f.shape
    print("f(0, 0)     =", f[0, 0], "         # pojok kiri atas")
    print("f(M-1, N-1) =", f[M_ - 1, N_ - 1], "     # pojok kanan bawah")
    print("Blok 5x5 mulai (10,10):")
    print(f[10:15, 10:15])

    m, n = 20, 30
    x, y = n, (M_ - 1) - m
    print("\nCitra (m,n)=", (m, n), "-> Kartesian (x,y)=", (x, y))
    print(f"Nilai pikselnya f[m, n] = {f[m, n]}")
    print(f"Cek lewat flip vertikal: f[M-1-y, x] = {f[(M_ - 1) - y, x]}"
          f" -> {'SAMA (konsisten)' if f[m, n] == f[(M_ - 1) - y, x] else 'BEDA'}")
    print("\nRumus konversi: x = n ; y = (M - 1) - m")

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5))
    bbox = dict(boxstyle="round", fc="black", alpha=0.65, pad=0.3)
    ax = axes[0]
    ax.imshow(f, cmap="gray", vmin=0, vmax=255)
    ax.plot(0, 0, "o", color="red", ms=9)
    ax.text(7, 7, "(0, 0) pojok kiri atas", color="red", fontsize=10,
            va="top", ha="left", bbox=bbox)
    ax.plot(N_ - 1, M_ - 1, "o", color="lime", ms=9)
    ax.text(N_ - 7, M_ - 7, f"(M-1, N-1) = ({M_ - 1}, {N_ - 1})",
            color="lime", fontsize=10, va="bottom", ha="right", bbox=bbox)
    ax.plot(n, m, "s", color="yellow", ms=9)
    ax.text(n + 12, m + 16, f"piksel (m,n) = ({m}, {n})\nintensitas = {f[m, n]}",
            color="yellow", fontsize=10, va="top", ha="left", bbox=bbox)
    ax.set_title("Koordinat citra: m ke bawah, n ke kanan")
    ax.axis("off")

    ax = axes[1]
    ax.imshow(f, cmap="gray", vmin=0, vmax=255)
    ax.annotate("", xy=(0, M_ - 1), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color="cyan", lw=2))
    ax.annotate("", xy=(N_ - 1, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color="magenta", lw=2))
    ax.text(18, M_ * 0.5, "sumbu m (baris) - ke bawah", color="cyan",
            fontsize=10, rotation=90, va="center", ha="left", bbox=bbox)
    ax.text(N_ * 0.3, 12, "sumbu n (kolom) - ke kanan", color="magenta",
            fontsize=10, va="top", ha="left", bbox=bbox)
    ax.text(N_ * 0.5, M_ * 0.7, "kartesian (x, y):\nx = n\ny = (M-1) - m",
            color="white", fontsize=11, va="top", ha="left",
            bbox=dict(boxstyle="round", fc="black", alpha=0.7))
    ax.set_title("Perbedaan sumbu citra vs kartesian")
    ax.axis("off")
    fig.suptitle("Percobaan 2 - Mengakses piksel dan koordinat")
    fig.tight_layout()
    fig.savefig(SS / "citra2_koordinat.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"\n[figure] {SS / 'citra2_koordinat.png'}")
    save_metrics(
        "citra2",
        {
            "f00": int(f[0, 0]),
            "f_last": int(f[M_ - 1, N_ - 1]),
            "block_10_10": f[10:15, 10:15].tolist(),
            "mn": [m, n],
            "xy": [x, y],
            "f_mn": int(f[m, n]),
        },
    )


# ------------------------------------------------------------- percobaan 3
def percobaan3():
    crop = f[50:178, 50:178]                       # 128 x 128 (2 pangkat 7)
    p_crop = SS / "citra3_hasil_crop.png"
    Image.fromarray(crop).save(p_crop)
    print("crop = f[50:178, 50:178]")
    print("Ukuran crop:", crop.shape)

    img256 = img.resize((256, 256))
    p_256 = SS / "citra3_hasil_256.png"
    img256.save(p_256)
    print("Ukuran baru:", img256.size)

    f256 = np.array(img256)
    print(f"\nCitra asli {img.size} -> pangkat 2? "
          f"{all(v & (v - 1) == 0 for v in img.size)}")
    print(f"crop 128 x 128 -> pangkat 2? "
          f"{all(v & (v - 1) == 0 for v in crop.shape)}")
    print(f"Selisih maks crop vs asli[bagian sama]: "
          f"{np.abs(crop.astype(int) - f[50:178, 50:178].astype(int)).max()}")
    print(f"Ukuran file: asli {os.path.getsize(IMG_PATH) / 1024:.1f} KB (jpg) | "
          f"crop {p_crop.stat().st_size / 1024:.1f} KB | "
          f"256x256 {p_256.stat().st_size / 1024:.1f} KB")
    print(f"Resize 256x256 dari citra 256x256 -> piksel identik: "
          f"{np.array_equal(np.array(img.resize((256, 256))), f256) and img.size == (256, 256)}")

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.7))
    axes[0].imshow(f, cmap="gray", vmin=0, vmax=255)
    axes[0].add_patch(plt.Rectangle((50, 50), 128, 128, fill=False,
                                    edgecolor="yellow", lw=2))
    axes[0].set_title(f"Citra asli {N} x {M}")
    axes[1].imshow(crop, cmap="gray", vmin=0, vmax=255)
    axes[1].set_title(f"Hasil crop {crop.shape[1]} x {crop.shape[0]} (2^7)")
    axes[2].imshow(f256, cmap="gray", vmin=0, vmax=255)
    axes[2].set_title(f"Diresize {img256.size[0]} x {img256.size[1]} (2^8)")
    for a in axes:
        a.axis("off")
    fig.suptitle("Percobaan 3 - Cropping dan ukuran pangkat 2 (kotak kuning = area crop)")
    fig.tight_layout()
    fig.savefig(SS / "citra3_crop_resize.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"\n[figure] {SS / 'citra3_crop_resize.png'}")
    save_metrics(
        "citra3",
        {
            "crop_shape": list(crop.shape),
            "resize": list(img256.size),
            "crop_file_kb": round(p_crop.stat().st_size / 1024, 1),
            "resize_file_kb": round(p_256.stat().st_size / 1024, 1),
        },
    )


# ------------------------------------------------------------- percobaan 4
def percobaan4():
    results = {}
    paths = {}
    for L in (256, 64, 16, 4, 2):
        hasil = kuantisasi(f, L)
        p = SS / f"citra4_kuantisasi_{L}.png"
        Image.fromarray(hasil).save(p)
        paths[L] = p
        uniq = len(np.unique(hasil))
        step = 256 // L
        mem = M * N * int(np.log2(L)) // 8
        results[L] = {
            "unique": int(uniq),
            "step": int(step),
            "bit": int(np.log2(L)),
            "mem_bytes": int(mem),
            "mem_kb": round(mem / 1024, 1),
            "file_kb": round(p.stat().st_size / 1024, 1),
        }
        print(f"Aras: {L} | aras unik terdeteksi: {uniq} | "
              f"langkah {step} | {results[L]['bit']} bit | "
              f"memori teoritis {results[L]['mem_kb']} KB | "
              f"file PNG {results[L]['file_kb']} KB")

    fig, axes = plt.subplots(2, 3, figsize=(13, 8.6))
    axes = axes.ravel()
    axes[0].imshow(f, cmap="gray", vmin=0, vmax=255)
    axes[0].set_title(f"Asli (256 aras, {results[256]['unique']} aras terpakai)")
    for i, L in enumerate((64, 16, 4, 2), start=1):
        axes[i].imshow(np.array(Image.open(paths[L])), cmap="gray",
                       vmin=0, vmax=255)
        axes[i].set_title(f"L = {L} ({np.log2(L):.0f} bit, "
                          f"{results[L]['unique']} aras terdeteksi)")
    axes[5].axis("off")
    axes[5].text(
        0.02, 0.95,
        "Pengamatan:\n"
        "- L=256 & 64 : bedanya hampir tak terlihat\n"
        "- L=16       : gradasi mulai pecah (efek poster)\n"
        "- L=4        : batas warna jelas, wajah kehilangan detail\n"
        "- L=2        : tinggal gelap-terang (1 bit)\n\n"
        "Makin sedikit aras -> makin kecil memori\n"
        "-> kualitas makin turun.",
        va="top", fontsize=11,
        bbox=dict(boxstyle="round", fc="#f0f0f0", ec="gray"),
    )
    for a in axes:
        a.axis("off")
    fig.suptitle("Percobaan 4 - Kuantisasi (pengurangan jumlah aras intensitas)")
    fig.tight_layout()
    fig.savefig(SS / "citra4_kuantisasi.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    Ls = [256, 64, 16, 4, 2]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.6))
    ax1.bar([str(L) for L in Ls],
            [results[L]["mem_kb"] for L in Ls],
            color=["#2ecc71", "#3498db", "#f39c12", "#e74c3c", "#8e44ad"])
    for i, L in enumerate(Ls):
        ax1.text(i, results[L]["mem_kb"] + 1,
                 f"{results[L]['mem_kb']:.0f} KB", ha="center", fontsize=10)
    ax1.set_xlabel("Jumlah aras (L)")
    ax1.set_ylabel("Memori teoritis (KB)")
    ax1.set_title(f"Kebutuhan memori {M}x{N} piksel")
    ax1.grid(axis="y", alpha=0.3)

    ax2.bar([str(L) for L in Ls],
            [results[L]["file_kb"] for L in Ls],
            color=["#2ecc71", "#3498db", "#f39c12", "#e74c3c", "#8e44ad"])
    for i, L in enumerate(Ls):
        ax2.text(i, results[L]["file_kb"] + 0.4,
                 f"{results[L]['file_kb']}", ha="center", fontsize=10)
    ax2.set_xlabel("Jumlah aras (L)")
    ax2.set_ylabel("Ukuran file PNG (KB)")
    ax2.set_title("Ukuran file hasil simpan (PNG terkompresi)")
    ax2.grid(axis="y", alpha=0.3)
    fig.suptitle("Percobaan 4 - Memori teoritis vs ukuran file sebenarnya")
    fig.tight_layout()
    fig.savefig(SS / "citra4_memori.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"\n[figure] {SS / 'citra4_kuantisasi.png'}")
    print(f"[figure] {SS / 'citra4_memori.png'}")
    save_metrics("citra4", results)


# --------------------------------------------------------- tugas mandiri
FOTO2 = r"D:\LAPORAN\assets\ss\00_portal_utama.png"


def tugas_mandiri():
    print("=== TUGAS MANDIRI (Pertanyaan 5): ganti citra.jpg dengan foto lain ===")
    print(f"Foto baru: {FOTO2}\n")
    im2 = Image.open(FOTO2).convert("L")
    g = np.array(im2)
    M2, N2 = g.shape

    print("Percobaan 1 pada foto baru:")
    print("Ukuran citra M x N :", M2, "x", N2)
    print("Jumlah piksel      :", M2 * N2)
    print("Tipe data          :", g.dtype)
    print("Intensitas min/maks:", g.min(), "/", g.max())
    print(f"Rata-rata          : {g.mean():.2f}")
    print(f"Aras unik terpakai : {len(np.unique(g))} dari 256 aras")

    print("\nPercobaan 2 pada foto baru:")
    print("f(0, 0)     =", g[0, 0])
    print("f(M-1, N-1) =", g[M2 - 1, N2 - 1])
    m2, n2 = 20, 30
    x2, y2 = n2, (M2 - 1) - m2
    print(f"Citra (m,n)= ({m2}, {n2}) -> Kartesian (x,y)= ({x2}, {y2}) "
          f"| intensitas f[m,n] = {g[m2, n2]}")

    print("\nPercobaan 3 pada foto baru:")
    crop2 = g[50:178, 50:178]
    Image.fromarray(crop2).save(SS / "citra5_hasil_crop2.png")
    print("Ukuran crop:", crop2.shape, "-> pangkat 2:",
          all(v & (v - 1) == 0 for v in crop2.shape))
    im2_256 = im2.resize((256, 256))
    im2_256.save(SS / "citra5_hasil_256.png")
    print(f"Ukuran asli {im2.size} (bukan pangkat 2) -> diresize ke "
          f"{im2_256.size} (2 pangkat 8)")

    print("\nPercobaan 4 pada foto baru:")
    for L in (256, 64, 16, 4, 2):
        h = kuantisasi(g, L)
        if L in (16, 4, 2):
            Image.fromarray(h).save(SS / f"citra5_kuantisasi_{L}.png")
        print(f"Aras: {L} | aras unik terdeteksi: {len(np.unique(h))}")

    fig, axes = plt.subplots(2, 2, figsize=(12, 8.4))
    axes[0, 0].imshow(f, cmap="gray", vmin=0, vmax=255)
    axes[0, 0].set_title(f"citra.jpg — {M} x {N}, min {f.min()}, maks {f.max()}, "
                         f"rata2 {f.mean():.1f}")
    axes[0, 0].axis("off")
    axes[0, 1].hist(f.ravel(), bins=256, color="steelblue", edgecolor="none")
    axes[0, 1].set_title(f"Histogram citra.jpg ({len(np.unique(f))} aras terpakai)")
    axes[0, 1].set_xlabel("Intensitas")
    axes[0, 1].set_ylabel("Jumlah piksel")
    axes[0, 1].grid(alpha=0.3)

    axes[1, 0].imshow(g, cmap="gray", vmin=0, vmax=255)
    axes[1, 0].set_title(f"Foto pilihan sendiri — {M2} x {N2}, min {g.min()}, "
                         f"maks {g.max()}, rata2 {g.mean():.1f}")
    axes[1, 0].axis("off")
    axes[1, 1].hist(g.ravel(), bins=256, color="seagreen", edgecolor="none")
    axes[1, 1].set_title(f"Histogram foto baru ({len(np.unique(g))} aras terpakai)")
    axes[1, 1].set_xlabel("Intensitas")
    axes[1, 1].set_ylabel("Jumlah piksel")
    axes[1, 1].grid(alpha=0.3)
    fig.suptitle("Tugas Mandiri - Percobaan 1 & 4 diulangi dengan foto berbeda")
    fig.tight_layout()
    fig.savefig(SS / "citra5_tugas_mandiri.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"\n[figure] {SS / 'citra5_tugas_mandiri.png'}")
    save_metrics(
        "citra5",
        {
            "file": "00_portal_utama.png",
            "M": int(M2),
            "N": int(N2),
            "pixels": int(M2 * N2),
            "min": int(g.min()),
            "max": int(g.max()),
            "mean": round(float(g.mean()), 2),
            "unique": int(len(np.unique(g))),
            "f00": int(g[0, 0]),
            "f_last": int(g[M2 - 1, N2 - 1]),
            "f_mn": int(g[m2, n2]),
            "xy": [x2, y2],
            "crop": list(crop2.shape),
            "unique_L": {
                str(L): int(len(np.unique(kuantisasi(g, L))))
                for L in (256, 64, 16, 4, 2)
            },
        },
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "5":
        run_job("citra5", "Tugas Mandiri - Percobaan 1-4 dengan foto lain",
                tugas_mandiri)
    else:
        run_job("citra0_setup", "Persiapan - Library & File citra.jpg", setup)
        run_job("citra1", "Percobaan 1 - Membaca citra & ukuran M x N", percobaan1)
        run_job("citra2", "Percobaan 2 - Mengakses piksel & koordinat", percobaan2)
        run_job("citra3", "Percobaan 3 - Cropping & ukuran pangkat 2", percobaan3)
        run_job("citra4", "Percobaan 4 - Kuantisasi jumlah aras", percobaan4)
        run_job("citra5", "Tugas Mandiri - Percobaan 1-4 dengan foto lain",
                tugas_mandiri)
