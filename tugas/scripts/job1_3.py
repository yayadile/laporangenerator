"""Job 1 (supervised), Job 2 (unsupervised), Job 3 (overfitting)."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import load_breast_cancer, load_iris
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    silhouette_score,
)
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

import matplotlib.pyplot as plt

from common import SS, run_job, save_metrics


# --------------------------------------------------------------------- Job 1
def job1():
    X, y = load_breast_cancer(return_X_y=True)
    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    models = [
        ("LogisticRegression", LogisticRegression(max_iter=5000)),
        ("RandomForest", RandomForestClassifier(random_state=42)),
    ]
    res = {}
    cms = []
    for name, m in models:
        m.fit(Xtr, ytr)
        pred = m.predict(Xte)
        print(name)
        print(classification_report(yte, pred, digits=4))
        res[name] = dict(
            accuracy=round(accuracy_score(yte, pred), 4),
            precision_macro=round(precision_score(yte, pred, average="macro"), 4),
            recall_macro=round(recall_score(yte, pred, average="macro"), 4),
            f1_macro=round(f1_score(yte, pred, average="macro"), 4),
            f1_weighted=round(f1_score(yte, pred, average="weighted"), 4),
            f1_class0=round(f1_score(yte, pred, average=None)[0], 4),
            f1_class1=round(f1_score(yte, pred, average=None)[1], 4),
            test_size=int(len(yte)),
        )
        cms.append(confusion_matrix(yte, pred))
        print(
            f"-> accuracy={res[name]['accuracy']}  "
            f"precision(macro)={res[name]['precision_macro']}  "
            f"recall(macro)={res[name]['recall_macro']}  "
            f"F1(macro)={res[name]['f1_macro']}\n"
        )

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
    for ax, (name, cm) in zip(axes, zip([m[0] for m in models], cms)):
        im = ax.imshow(cm, cmap="Blues")
        ax.set_xticks([0, 1], ["Malignant (0)", "Benign (1)"])
        ax.set_yticks([0, 1], ["Malignant (0)", "Benign (1)"])
        ax.set_xlabel("Prediksi")
        ax.set_ylabel("Aktual")
        ax.set_title(f"Confusion Matrix - {name}")
        for i in range(2):
            for j in range(2):
                ax.text(
                    j,
                    i,
                    str(cm[i, j]),
                    ha="center",
                    va="center",
                    color="white" if cm[i, j] > cm.max() / 2 else "black",
                    fontsize=13,
                )
        fig.colorbar(im, ax=ax, fraction=0.046)
    fig.suptitle("Job 1 - Evaluasi Klasifikasi Breast Cancer (20% data uji)")
    fig.tight_layout()
    fig.savefig(SS / "job1_confusion_matrix.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"[figure] {SS / 'job1_confusion_matrix.png'}")
    save_metrics("job1", res)


# --------------------------------------------------------------------- Job 2
def job2():
    X, y = load_iris(return_X_y=True)
    pca = PCA(n_components=2)
    Z = pca.fit_transform(X)
    print(
        f"PCA: explained variance ratio = "
        f"{pca.explained_variance_ratio_.round(4)} "
        f"(total {pca.explained_variance_ratio_.sum():.4f})\n"
    )

    sil = {}
    for k in range(2, 7):
        lab = KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(X)
        sil[k] = round(float(silhouette_score(X, lab)), 4)
        print(f"k={k}: silhouette={sil[k]}")
    print("-> silhouette tertinggi:", max(sil, key=sil.get), "\n")

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))
    ari = {}
    for ax, k in zip(axes, [2, 3, 4]):
        lab = KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(X)
        sc = ax.scatter(Z[:, 0], Z[:, 1], c=lab, cmap="viridis", s=42)
        ax.set_title(f"K-Means k={k} (silhouette={sil[k]})")
        ax.set_xlabel("PC1")
        ax.set_ylabel("PC2")
        fig.colorbar(sc, ax=ax, fraction=0.046)
        # label asli hanya untuk analisis (tidak dipakai saat fitting)
        from sklearn.metrics import adjusted_rand_score

        ari[k] = round(float(adjusted_rand_score(y, lab)), 4)
    fig.suptitle("Job 2 - Clustering K-Means pada Ruang PCA (dataset Iris)")
    fig.tight_layout()
    fig.savefig(SS / "job2_pca_clusters.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"[figure] {SS / 'job2_pca_clusters.png'}")
    print("ARI vs label asli (hanya untuk analisis):", ari)
    save_metrics("job2", {"silhouette": sil, "ari": ari})


# --------------------------------------------------------------------- Job 3
def job3():
    X, y = load_breast_cancer(return_X_y=True)
    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    rows = []
    print(f"{'depth':>5} {'train':>7} {'test':>7} {'gap':>7}")
    for d in range(1, 16):
        t = DecisionTreeClassifier(max_depth=d, random_state=42).fit(Xtr, ytr)
        tr, te = t.score(Xtr, ytr), t.score(Xte, yte)
        rows.append((d, round(tr, 3), round(te, 3), round(tr - te, 3)))
        print(f"{d:>5} {tr:>7.3f} {te:>7.3f} {tr - te:>7.3f}")

    max_gap = max(rows, key=lambda r: r[3])
    first_wide = next(r for r in rows if r[3] >= 0.03)
    print(
        f"\n-> selisih terbesar: depth={max_gap[0]} "
        f"train={max_gap[1]} test={max_gap[2]} gap={max_gap[3]}"
    )
    print(f"-> selisih mulai melebar (gap>=0.03): depth={first_wide[0]}")

    depths = [r[0] for r in rows]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(depths, [r[1] for r in rows], "o-", label="Akurasi latih", lw=2)
    ax.plot(depths, [r[2] for r in rows], "s--", label="Akurasi uji", lw=2)
    ax.fill_between(
        depths,
        [r[1] for r in rows],
        [r[2] for r in rows],
        color="orange",
        alpha=0.25,
        label="Gap (overfitting)",
    )
    ax.set_xlabel("max_depth")
    ax.set_ylabel("Akurasi")
    ax.set_title("Job 3 - Overfitting pada Decision Tree (Breast Cancer)")
    ax.set_xticks(depths)
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(SS / "job3_overfitting.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"[figure] {SS / 'job3_overfitting.png'}")
    save_metrics(
        "job3",
        {
            "rows": rows,
            "max_gap": max_gap,
            "first_wide": first_wide,
        },
    )


if __name__ == "__main__":
    run_job("job1", "Job 1 - Supervised Learning (Klasifikasi)  [Breast Cancer]", job1)
    run_job("job2", "Job 2 - Unsupervised Learning (KMeans + PCA)  [Iris]", job2)
    run_job("job3", "Job 3 - Overfitting (Decision Tree, max_depth 1-15)", job3)
