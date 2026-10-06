"""Job 4 (MLP) dan Job 5 (CNN) pada MNIST dengan PyTorch."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

import matplotlib.pyplot as plt

from common import CKPT, SS, run_job, save_metrics

torch.manual_seed(42)
DATA = r"D:\LAPORAN\data"
EPOCHS = 5

tf = transforms.ToTensor()
train_dl = DataLoader(
    datasets.MNIST(DATA, train=True, download=True, transform=tf),
    batch_size=128,
    shuffle=True,
)
test_dl = DataLoader(
    datasets.MNIST(DATA, train=False, download=True, transform=tf),
    batch_size=256,
)
dev = "cuda" if torch.cuda.is_available() else "cpu"
print(f"device={dev} | train={len(train_dl.dataset)} test={len(test_dl.dataset)}")


@torch.no_grad()
def evaluate(model, dl=test_dl):
    model.eval()
    ok = n = 0
    for x, y in dl:
        x, y = x.to(dev), y.to(dev)
        ok += (model(x).argmax(1) == y).sum().item()
        n += len(y)
    return ok / n


def fit(model, epochs=EPOCHS, tag=""):
    model.to(dev)
    opt = torch.optim.Adam(model.parameters(), 1e-3)
    loss_fn = nn.CrossEntropyLoss()
    hist = {"loss": [], "acc": []}
    for e in range(epochs):
        model.train()
        tot = cnt = 0.0
        for x, y in train_dl:
            x, y = x.to(dev), y.to(dev)
            opt.zero_grad()
            loss = loss_fn(model(x), y)
            loss.backward()
            opt.step()
            tot += loss.item() * len(y)
            cnt += len(y)
        avg = tot / cnt
        acc = evaluate(model)
        hist["loss"].append(round(avg, 4))
        hist["acc"].append(round(acc, 4))
        print(
            f"{tag}epoch {e + 1}/{epochs} loss {avg:.4f} "
            f"acc {acc:.4f}  (eval() + no_grad)"
        )
    return hist


def nparams(m):
    return sum(p.numel() for p in m.parameters())


# --------------------------------------------------------------------- Job 4
def job4():
    print(f"Perangkat: {dev} | torch {torch.__version__}\n")
    results = {}
    curves = {}
    for h in [32, 128, 512]:
        torch.manual_seed(42)
        mlp = nn.Sequential(
            nn.Flatten(), nn.Linear(784, h), nn.ReLU(), nn.Linear(h, 10)
        )
        print(f"--- MLP hidden={h} | parameter={nparams(mlp):,} ---")
        hist = fit(mlp, EPOCHS, tag=f"[mlp{h}] ")
        acc3 = hist["acc"][2]
        results[h] = {
            "params": nparams(mlp),
            "acc_per_epoch": hist["acc"],
            "acc_epoch3": acc3,
            "acc_epoch5": hist["acc"][-1],
            "loss_per_epoch": hist["loss"],
        }
        curves[f"MLP-{h}"] = hist
        if h == 128:
            torch.save(mlp.cpu().state_dict(), CKPT / "mlp128.pt")
        print(
            f"=> MLP hidden={h}: parameter={results[h]['params']:,} | "
            f"akurasi epoch3={acc3:.4f} | akurasi epoch5={hist['acc'][-1]:.4f}\n"
        )

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.6))
    for name, h in curves.items():
        ax1.plot(range(1, EPOCHS + 1), h["loss"], "o-", label=name, lw=2)
        ax2.plot(range(1, EPOCHS + 1), h["acc"], "o-", label=name, lw=2)
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Loss (rata-rata batch)")
    ax1.set_title("Job 4 - Training Loss MLP")
    ax1.grid(alpha=0.3)
    ax1.legend()
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Akurasi uji")
    ax2.set_title("Job 4 - Akurasi Uji MLP per Epoch")
    ax2.grid(alpha=0.3)
    ax2.legend()
    fig.tight_layout()
    fig.savefig(SS / "job4_training_curve.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"[figure] {SS / 'job4_training_curve.png'}")
    save_metrics("job4", results)


# --------------------------------------------------------------------- Job 5
def job5():
    torch.manual_seed(42)
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
    print(f"--- CNN | parameter={nparams(cnn):,} ---")
    hist = fit(cnn, EPOCHS, tag="[cnn] ")
    torch.save(cnn.cpu().state_dict(), CKPT / "cnn.pt")

    mlp128 = nn.Sequential(
        nn.Flatten(), nn.Linear(784, 128), nn.ReLU(), nn.Linear(128, 10)
    )
    mlp_params = nparams(mlp128)
    cnn_params = nparams(cnn)
    print(
        f"=> CNN: parameter={cnn_params:,} | "
        f"akurasi epoch3={hist['acc'][2]:.4f} | akurasi epoch5={hist['acc'][-1]:.4f}"
    )
    print(
        f"=> MLP-128: parameter={mlp_params:,} | "
        f"rasio parameter CNN/MLP = {cnn_params / mlp_params:.3f} "
        f"({100 * cnn_params / mlp_params:.1f}%)"
    )

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.6))
    ax1.plot(range(1, EPOCHS + 1), hist["loss"], "o-", label="CNN", lw=2, color="tab:red")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Loss (rata-rata batch)")
    ax1.set_title("Job 5 - Training Loss CNN")
    ax1.grid(alpha=0.3)
    ax1.legend()
    ax2.plot(range(1, EPOCHS + 1), hist["acc"], "o-", label="CNN", lw=2, color="tab:red")
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Akurasi uji")
    ax2.set_title("Job 5 - Akurasi Uji CNN per Epoch")
    ax2.grid(alpha=0.3)
    ax2.legend()
    fig.tight_layout()
    fig.savefig(SS / "job5_training_curve.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"[figure] {SS / 'job5_training_curve.png'}")

    mlp_acc = 0.0
    import json
    from common import METRICS_JSON

    if METRICS_JSON.exists():
        m = json.loads(METRICS_JSON.read_text(encoding="utf-8")).get("job4", {})
        mlp_acc = m.get("128", {}).get("acc_epoch5", 0.0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4))
    ax1.bar(["MLP-128", "CNN"], [mlp_acc, hist["acc"][-1]], color=["tab:blue", "tab:red"])
    ax1.set_ylim(0.9, 1.0)
    ax1.set_ylabel("Akurasi uji (epoch 5)")
    ax1.set_title("Akurasi Uji")
    for i, v in enumerate([mlp_acc, hist["acc"][-1]]):
        ax1.text(i, v + 0.001, f"{v:.4f}", ha="center")
    ax2.bar(["MLP-128", "CNN"], [mlp_params, cnn_params], color=["tab:blue", "tab:red"])
    ax2.set_yscale("log")
    ax2.set_ylabel("Jumlah parameter (log)")
    ax2.set_title("Jumlah Parameter")
    for i, v in enumerate([mlp_params, cnn_params]):
        ax2.text(i, v * 1.1, f"{v:,}", ha="center")
    fig.suptitle("Job 5 - Perbandingan MLP vs CNN (MNIST)")
    fig.tight_layout()
    fig.savefig(SS / "job5_mlp_vs_cnn.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"[figure] {SS / 'job5_mlp_vs_cnn.png'}")
    save_metrics(
        "job5",
        {
            "params": cnn_params,
            "acc_per_epoch": hist["acc"],
            "loss_per_epoch": hist["loss"],
            "acc_epoch3": hist["acc"][2],
            "acc_epoch5": hist["acc"][-1],
            "mlp128_params": mlp_params,
            "mlp128_acc_epoch5": mlp_acc,
        },
    )


if __name__ == "__main__":
    run_job("job4", "Job 4 - Neural Network (MLP) dengan PyTorch  [MNIST]", job4)
    run_job("job5", "Job 5 - CNN dengan PyTorch  [MNIST]", job5)
