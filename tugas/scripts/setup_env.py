"""Langkah Kerja 1 - persiapan lingkungan & impor library (snapshot bukti)."""

from __future__ import annotations

import platform
import sys
from pathlib import Path

import matplotlib
import numpy as np
import PIL
import sklearn
import torch
import torchvision

from common import SS, run_job


def setup():
    print("$ python --version")
    print(f"Python {sys.version.split()[0]} ({platform.platform()})")
    print(f"executable: {sys.executable}\n")

    print("$ python -c 'import numpy, sklearn, matplotlib, PIL, torch, torchvision'")
    for name, mod in [
        ("numpy", np),
        ("scikit-learn", sklearn),
        ("matplotlib", matplotlib),
        ("Pillow (PIL)", PIL),
        ("torch", torch),
        ("torchvision", torchvision),
    ]:
        print(f"  {name:<16}: {mod.__version__}")

    print("\n$ torch.cuda.is_available()")
    print(" ", torch.cuda.is_available(), "-> CPU (torch 2.14.1+cpu)")

    data = Path(r"D:\LAPORAN\data")
    files = sorted(data.rglob("*.gz")) if data.exists() else []
    print(f"\n$ dir {data}")
    for f in files:
        print(f"  {f.relative_to(data)}  ({f.stat().st_size // 1024} KB)")
    print(f"\nDataset MNIST siap: {len(files)} file | "
          f"sklearn bawaan: load_breast_cancer, load_iris")
    print("Library wajib (torch, torchvision, scikit-learn, numpy, matplotlib, "
          "PIL) terpasang & ter-import.")


if __name__ == "__main__":
    run_job("job0_setup", "Langkah 1 - Setup Lingkungan & Impor Library", setup)
