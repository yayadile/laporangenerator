"""Job 6 (self-attention) dan Job 7 (benchmark inference)."""

from __future__ import annotations

import json
import time

import matplotlib

matplotlib.use("Agg")

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

import matplotlib.pyplot as plt

from common import CKPT, METRICS_JSON, SS, run_job, save_metrics


# --------------------------------------------------------------------- Job 6
def job6():
    np.random.seed(0)
    T, d = 4, 8                              # 4 token, dimensi 8
    X = np.random.randn(T, d)
    Wq, Wk, Wv = [np.random.randn(d, d) for _ in range(3)]

    Q, K, V = X @ Wq, X @ Wk, X @ Wv
    S = Q @ K.T / np.sqrt(d)                 # skor kecocokan
    A = np.exp(S) / np.exp(S).sum(axis=1, keepdims=True)   # softmax per baris
    out = A @ V
    print("Matriks A (attention weight):")
    print(A.round(2))
    print("shape output:", out.shape)
    print("jumlah tiap baris A:", A.sum(axis=1).round(6))
    print("cek |baris - 1| maksimum:", float(np.abs(A.sum(axis=1) - 1).max()))
    print("sqrt(d) =", round(float(np.sqrt(d)), 4), "\n")

    S_noscale = Q @ K.T
    A_noscale = np.exp(S_noscale - S_noscale.max()) / np.exp(
        S_noscale - S_noscale.max()
    ).sum(axis=1, keepdims=True)

    def entropy(a):
        return float(-(a * np.log(a + 1e-12)).sum(axis=1).mean())

    print("Tanpa pembagian sqrt(d):")
    print(A_noscale.round(2))
    print(
        f"entropi rata-rata: dengan skala={entropy(A):.4f} "
        f"vs tanpa skala={entropy(A_noscale):.4f} (batas maks ln T = {np.log(T):.4f})"
    )
    print(
        "-> skor dibagi sqrt(d) agar varians Q@K.T menjadi 1 sehingga softmax "
        "tidak jatuh ke mode one-hot (gradient tetap stabil).\n"
    )

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
    for ax, (M, t) in zip(
        axes,
        [
            (A, "dengan scaling /sqrt(d)"),
            (A_noscale, "tanpa scaling"),
        ],
    ):
        im = ax.imshow(M, cmap="viridis")
        ax.set_xticks(range(T), [f"tok{j}" for j in range(T)])
        ax.set_yticks(range(T), [f"tok{i}" for i in range(T)])
        ax.set_xlabel("Key (j)")
        ax.set_ylabel("Query (i)")
        ax.set_title(f"A (softmax) - {t}")
        for i in range(T):
            for j in range(T):
                ax.text(
                    j,
                    i,
                    f"{M[i, j]:.2f}",
                    ha="center",
                    va="center",
                    color="white" if M[i, j] < M.max() * 0.6 else "black",
                    fontsize=10,
                )
        fig.colorbar(im, ax=ax, fraction=0.046)
    fig.suptitle("Job 6 - Matriks Self-Attention (T=4 token, d=8)")
    fig.tight_layout()
    fig.savefig(SS / "job6_attention_heatmap.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"[figure] {SS / 'job6_attention_heatmap.png'}")

    save_metrics(
        "job6",
        {
            "A": A.round(4).tolist(),
            "row_sums": A.sum(axis=1).round(6).tolist(),
            "out_shape": list(out.shape),
            "entropy_scaled": round(entropy(A), 4),
            "entropy_unscaled": round(entropy(A_noscale), 4),
            "sqrt_d": round(float(np.sqrt(d)), 4),
        },
    )


# --------------------------------------------------------------------- Job 7
def job7():
    tf = transforms.ToTensor()
    test = DataLoader(
        datasets.MNIST(r"D:\LAPORAN\data", train=False, download=True, transform=tf),
        batch_size=256,
    )
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    cnn = nn.Sequential(
        nn.Conv2d(1, 16, 3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Conv2d(16, 32, 3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Flatten(),
        nn.Linear(32 * 7 * 7, 10),
    )
    cnn.load_state_dict(torch.load(CKPT / "cnn.pt", weights_only=True))
    cnn.to(dev)
    cnn.eval()
    print(f"device={dev} | model=CNN (job5) dalam mode eval()")

    x, _ = next(iter(test))
    x = x.to(dev)

    loss_fn = nn.CrossEntropyLoss()
    ybatch = torch.randint(0, 10, (256,), device=dev)

    def bench(bs, mode, iters=50, repeats=3):
        """mode: 'nograd' | 'grad' | 'fwd+bwd' (training)."""
        xb = x[:bs]
        yb = ybatch[:bs]
        with torch.no_grad():          # warmup
            for _ in range(10):
                cnn(xb)
        times = []
        for _ in range(repeats):
            if mode == "nograd":
                ctx = torch.no_grad()
            else:
                ctx = torch.enable_grad()
            with ctx:
                t0 = time.perf_counter()
                for _ in range(iters):
                    out = cnn(xb)
                    if mode == "fwd+bwd":
                        loss_fn(out, yb).backward()
                        cnn.zero_grad(set_to_none=True)
                times.append((time.perf_counter() - t0) / iters * 1000)
        return round(min(times), 3)

    rows = []
    print(
        f"\n{'batch':>6} {'no_grad (ms)':>14} {'grad (ms)':>11} "
        f"{'fwd+bwd (ms)':>14} {'training/inference':>20}"
    )
    for bs in [1, 32, 256]:
        a, b, c = bench(bs, "nograd"), bench(bs, "grad"), bench(bs, "fwd+bwd")
        rows.append((bs, a, b, c, round(c / a, 2)))
        print(f"{bs:>6} {a:>14.3f} {b:>11.3f} {c:>14.3f} {c / a:>19.2f}x")

    # verifikasi: grad hanya dibuat saat mode aktif
    cnn.zero_grad(set_to_none=True)
    with torch.enable_grad():
        cnn(x[:8]).sum().backward()
    n_with_grad = sum(
        p.grad is not None for p in cnn.parameters()
    )
    cnn.zero_grad(set_to_none=True)
    with torch.no_grad():
        cnn(x[:8])
    n_without_grad = sum(p.grad is not None for p in cnn.parameters())
    print(
        f"\nparameter dengan .grad setelah mode enable_grad : {n_with_grad} "
        f"/ {len(list(cnn.parameters()))}"
    )
    print(
        f"parameter dengan .grad setelah mode no_grad     : {n_without_grad} "
        f"/ {len(list(cnn.parameters()))}"
    )
    print(
        "\nno_grad tidak menyimpan activation untuk autograd (hemat memori), "
        "eval() menonaktifkan dropout/BatchNorm mode latih."
    )
    print("CUDA tersedia:", torch.cuda.is_available(), "-> benchmark di CPU")

    fig, ax = plt.subplots(figsize=(9, 4.8))
    idx = np.arange(3)
    w = 0.26
    ax.bar(idx - w, [r[1] for r in rows], w, label="inference (no_grad)")
    ax.bar(idx, [r[2] for r in rows], w, label="forward (enable_grad)")
    ax.bar(idx + w, [r[3] for r in rows], w, label="training (fwd + backward)")
    ax.set_xticks(idx, [f"batch={r[0]}" for r in rows])
    ax.set_ylabel("Latensi rata2 per iterasi (ms)")
    ax.set_title("Job 7 - Latensi Inference vs Training CNN (CPU, 50 iter x 3)")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    for i, r in enumerate(rows):
        ax.text(i - w, r[1] + 1, f"{r[1]}", ha="center", fontsize=8)
        ax.text(i, r[2] + 1, f"{r[2]}", ha="center", fontsize=8)
        ax.text(i + w, r[3] + 1, f"{r[3]}", ha="center", fontsize=8)
    fig.tight_layout()
    fig.savefig(SS / "job7_latency.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"[figure] {SS / 'job7_latency.png'}")
    save_metrics("job7", {"rows": rows, "device": dev, "iters": "50x3 (min)"})


if __name__ == "__main__":
    run_job("job6", "Job 6 - Self-Attention (Konsep Transformer)", job6)
    run_job("job7", "Job 7 - Benchmark Inference CNN", job7)
