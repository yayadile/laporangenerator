# JOBSHEET PELATIHAN MACHINE LEARNING & DEEP LEARNING REFRESHER
**Supervised/Unsupervised • Neural Network • CNN • Transformer • Training & Inference**

| Parameter | Keterangan |
| :--- | :--- |
| **Nama Peserta** | Adinda Massa Merah Lawan Tirani |
| **Kelas / Kelompok** | IK-3C — NIM 3.34.24.2.01 |
| **Tanggal Pelaksanaan** | 07 Oktober 2026 |
| **Alokasi Waktu** | 4 x 45 menit |
| **Kode Jobsheet** | JS-AI-02 |
| **Instruktur** | Angga Wahyu Wibowo, S.Kom., M.Eng., Ph.D |

---

## A. Tujuan Pembelajaran

Setelah menyelesaikan jobsheet ini, peserta diharapkan mampu:

1. Melatih dan mengevaluasi model *supervised learning* (klasifikasi) serta menafsirkan metrik *precision*, *recall*, dan $F_1$.
2. Menerapkan *clustering* dan reduksi dimensi pada data tanpa label (*unsupervised learning*).
3. Mengenali *overfitting* dari perbandingan akurasi data latih dan data uji.
4. Membangun dan melatih *neural network* (MLP) dan CNN menggunakan PyTorch.
5. Menjelaskan mekanisme *self-attention* pada Transformer melalui implementasi kecil.
6. Membedakan proses *training* dan *inference* serta mengukur latensi *inference*.

---

## B. Dasar Teori Singkat

Machine Learning (ML) belajar pola dari data. Pada *supervised learning*, model dilatih dengan pasangan input dan label untuk klasifikasi atau regresi; pada *unsupervised learning*, model mencari struktur pada data tanpa label, misalnya *clustering* dan reduksi dimensi. Model yang terlalu menghafal data latih mengalami *overfitting*, sehingga performanya turun pada data baru.

Deep Learning menggunakan *neural network* berlapis. Bobot dipelajari lewat *backpropagation* dan *optimizer*. CNN memakai filter konvolusi untuk mengekstrak fitur lokal pada gambar, sedangkan Transformer memakai *self-attention* agar setiap token dapat memperhatikan token lain dalam satu urutan. *Training* memperbarui bobot model, sedangkan *inference* hanya menjalankan *forward pass* dengan bobot tetap.

---

## C. Alat dan Bahan

| Komponen | Spesifikasi yang Dipakai |
| :--- | :--- |
| **Hardware** | CPU (`torch.cuda.is_available() = False`, seluruh training dan benchmark dijalankan di CPU) |
| **Sistem / Python** | Windows 10 Pro 64-bit — Python 3.13.13 (`C:\Program Files\Python313\python.exe`) |
| **Library** | torch 2.14.1+cpu, torchvision 0.29.1+cpu, scikit-learn 1.8.0, numpy 2.4.4, matplotlib 3.11.2, Pillow 12.3.0 |
| **Dataset** | Breast Cancer & Iris (bawaan scikit-learn), MNIST (torchvision, terunduh otomatis ke `data/MNIST/raw/`) |
| **Script eksekusi** | `tugas/scripts/setup_env.py`, `job1_3.py`, `job4_5.py`, `job6_7.py` (semua log & grafik disimpan ke `assets/ss/`) |
| **Dokumen pendukung** | Slide "Machine Learning & Deep Learning Refresher" dan lembar jobsheet ini |

![Langkah 1 - Setup lingkungan dan impor library](assets/ss/job0_setup_execution.png)

---

## D. Langkah Kerja

| # | Langkah Kerja | Bukti Eksekusi (screenshot) |
| :--: | :--- | :--- |
| 1 | Pelajari materi presentasi, siapkan lingkungan Python, impor library yang dibutuhkan | `assets/ss/job0_setup_execution.png` |
| 2 | Kerjakan Job 1–3 (supervised, unsupervised, overfitting) dan catat hasilnya pada tabel hasil | `assets/ss/job1_execution.png`, `job2_execution.png`, `job3_execution.png` |
| 3 | Kerjakan Job 4–5 (MLP dan CNN dengan PyTorch) dan catat akurasi serta jumlah parameter | `assets/ss/job4_execution.png`, `job5_execution.png` |
| 4 | Kerjakan Job 6–7 (*self-attention* dan *inference*) dan catat hasil pengamatan | `assets/ss/job6_execution.png`, `job7_execution.png` |
| 5 | Lengkapi Lembar Kerja 1 (perbandingan konsep) dan Lembar Kerja 3 (perbandingan arsitektur) | Terisi pada Bagian E |
| 6 | Jawab pertanyaan evaluasi pada Bagian F secara individu, lalu tulis kesimpulan pada Bagian G | Terisi pada Bagian F dan G |
| 7 | Kumpulkan jobsheet beserta notebook `NIM_Nama_Jobsheet_ML_DL` kepada instruktur | Kode berjalan tersimpan di `tugas/scripts/*.py` |

> Seluruh kode dijalankan pada **Python 3.10+ (versi 3.13.13)** di lingkungan lokal.
> Setiap langkah kerja menghasilkan **snapshot log terminal** berformat `assets/ss/jobN_execution.png`
> dan seluruh grafik diekspor sebagai **PNG resolusi 200 DPI** ke folder yang sama.

---

## E. Lembar Kerja

### Lembar Kerja 1 — Perbandingan Konsep

| Konsep | Definisi Singkat | Contoh Nyata |
| :--- | :--- | :--- |
| **Supervised Learning** | Belajar dari data yang **sudah berlabel** (pasangan input $x$ dan target $y$) sehingga model dapat memprediksi label pada data baru. | Klasifikasi tumor **Breast Cancer** (0 = *malignant*, 1 = *benign*) dengan Logistic Regression: akurasi **0,9649**, $F_1$ **0,9619** pada 20% data uji (Job 1). |
| **Unsupervised Learning** | Mencari **struktur/pola pada data tanpa label**; model mengelompokkan atau mereduksi data berdasarkan kemiripan statistiknya sendiri. | **K-Means (k=3)** untuk *clustering* dan **PCA** untuk reduksi dimensi pada dataset Iris — label sengaja diabaikan saat *fitting* (Job 2). |
| **Overfitting** | Model **terlalu menghafal data latih** (termasuk noise) sehingga generalisasi ke data baru memburuk; cirinya akurasi latih jauh lebih tinggi daripada akurasi uji. | Decision Tree `max_depth=7`: akurasi latih **1,000** tetapi akurasi uji hanya **0,912** → selisih **0,088**, terbesar pada percobaan ini (Job 3). |
| **Training vs Inference** | ***Training***: *forward pass* → *loss* → *backward* → *update* bobot (bobot berubah). ***Inference***: *forward pass* saja dengan **bobot tetap**, tanpa penyimpanan gradien. | *Training* CNN 5 epoch (loss 0,3683 → 0,0472) vs *inference* `model.eval()` + `torch.no_grad()` (Job 7): latensi **0,195 ms** pada batch 1. |

---

### Lembar Kerja 2 — Praktik Kode

#### Job 1 — Supervised Learning (Klasifikasi)

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

X, y = load_breast_cancer(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2,
                                      stratify=y, random_state=42)
for m in [LogisticRegression(max_iter=5000),
          RandomForestClassifier(random_state=42)]:
    m.fit(Xtr, ytr)
    print(type(m).__name__)
    print(classification_report(yte, m.predict(Xte)))
```

![Job 1 - Log eksekusi klasifikasi Breast Cancer](assets/ss/job1_execution.png)

**Tabel hasil Job 1 (data uji 114 sampel: 42 *malignant*, 72 *benign*)**

| Model | Accuracy | Precision (macro) | Recall (macro) | $F_1$ (macro) | $F_1$ kelas 0 (*malignant*) | $F_1$ kelas 1 (*benign*) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | **0,9649** | **0,9672** | **0,9573** | **0,9619** | **0,9512** | **0,9726** |
| **Random Forest** | 0,9561 | 0,9551 | 0,9504 | 0,9526 | 0,9398 | 0,9655 |

| Confusion Matrix (baris = aktual, kolom = prediksi) | Prediksi *malignant* | Prediksi *benign* |
| :--- | :---: | :---: |
| Aktual *malignant* (LogReg / RF) | 39 / 39 | 3 / 3 |
| Aktual *benign* (LogReg / RF) | 1 / 2 | 71 / 70 |

![Job 1 - Confusion matrix kedua model](assets/ss/job1_confusion_matrix.png)

**Jawaban tugas Job 1**

- **Model yang lebih baik: Logistic Regression.** Seluruh metrik agregatnya lebih unggul: akurasi 0,9649 > 0,9561, $F_1$ makro 0,9619 > 0,9526, dan *recall* makro 0,9573 > 0,9504. Pada kelas *malignant*, $F_1$ LogReg 0,9512 vs Random Forest 0,9398. Karena selisihnya kecil, kesimpulannya keduanya setara secara praktis, tetapi Logistic Regression lebih konsisten pada kelas minoritas dan juga lebih ringan/deterministik.
- **Mengapa *recall* penting pada deteksi kanker:** *recall* = TP / (TP + FN), sehingga semakin tinggi *recall*, semakin sedikit **false negative** — pasien yang benar-benar sakit tetapi dinyatakan sehat. Dalam kasus kanker, *false negative* berarti diagnosis terlewat dan penanganan tertunda (konsekuensinya fatal), sedangkan *false positive* masih dapat ditindaklanjuti dengan pemeriksaan lanjutan yang relatif murah. Karena itu *recall* pada kelas *malignant* harus diprioritaskan (dalam percobaan ini kedua model mencatat *recall* 0,9286 — 3 dari 42 kasus *malignant* terlewat).

---

#### Job 2 — Unsupervised Learning (Clustering + PCA)

```python
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

X, _ = load_iris(return_X_y=True)   # label sengaja diabaikan
labels = KMeans(n_clusters=3, n_init=10, random_state=42).fit_predict(X)
Z = PCA(n_components=2).fit_transform(X)
plt.scatter(Z[:, 0], Z[:, 1], c=labels)
plt.title("K-Means (k=3) pada ruang PCA"); plt.show()
```

![Job 2 - Log eksekusi K-Means dan PCA](assets/ss/job2_execution.png)

**Hasil pengukuran (silhouette dihitung pada data asli 4 fitur, PCA 2 komponen menjelaskan 97,77% varians)**

| $k$ | 2 | 3 | 4 | 5 | 6 |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **Silhouette** | **0,6810** | 0,5528 | 0,4981 | 0,4912 | 0,3648 |
| ARI vs label asli (hanya analisis) | 0,5399 | **0,7302** | 0,6498 | — | — |

![Job 2 - Scatter plot K-Means pada ruang PCA (k=2, 3, 4)](assets/ss/job2_pca_clusters.png)

**Jawaban tugas Job 2**

- **Visualisasi `n_clusters = 2`:** klaster kiri (setosa) terpisah sangat rapi, sedangkan versicolor dan virginica **digabung menjadi satu klaster besar** di sisi kanan → silhouette justru paling tinggi (0,6810) karena dua kelompok yang jauh terpisah membuat koherensi klaster naik.
- **Visualisasi `n_clusters = 4`:** satu klaster hasil split buatan membelah sebaran yang sebenarnya menyatu (versicolor/virginica terpecah tidak wajar) → silhouette turun ke 0,4981 dan klaster menjadi "berlubang"/tidak padat.
- **Visualisasi `n_clusters = 3` (paling masuk akal):** tiga gugusan sesuai struktur data dan memberi ARI tertinggi (0,7302) terhadap label asli.
- **Mengapa menentukan jumlah cluster sulit tanpa label:** tidak ada satu jawaban "benar" yang bisa diverifikasi — berbagai indikator saling bertentangan (silhouette memilih $k=2$, sedangkan struktur gugusan dan ARI memilih $k=3$), hasilnya sangat bergantung pada skala fitur, jarak yang dipakai, *scaling*, *initialization*, dan apakah klaster berbentuk sferis. Tanpa label, *clustering* hanya menghasilkan **hipotesis struktur** yang tetap butuh validasi domain (mis. fakta biologi bahwa Iris punya 3 spesies).

---

#### Job 3 — Overfitting (menggunakan `Xtr, Xte, ytr, yte` dari Job 1)

```python
from sklearn.tree import DecisionTreeClassifier

for d in range(1, 16):
    t = DecisionTreeClassifier(max_depth=d, random_state=42).fit(Xtr, ytr)
    print(d, round(t.score(Xtr, ytr), 3), round(t.score(Xte, yte), 3))
```

![Job 3 - Log eksekusi Decision Tree max_depth 1-15](assets/ss/job3_execution.png)

**Tabel hasil Job 3 (sebagian — data lengkap 1–15 ada pada log)**

| `max_depth` | 1 | 2 | 3 | 4 | 5 | 6 | **7** | 8–15 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Akurasi latih | 0,923 | 0,958 | 0,976 | 0,987 | 0,993 | 0,998 | **1,000** | 1,000 |
| Akurasi uji | 0,921 | **0,895** | 0,939 | 0,939 | 0,921 | 0,912 | **0,912** | 0,912 |
| Selisih (gap) | 0,002 | 0,064 | 0,037 | 0,048 | 0,072 | 0,086 | **0,088** | 0,088 |

![Job 3 - Kurva akurasi latih vs uji terhadap max_depth](assets/ss/job3_overfitting.png)

**Jawaban tugas Job 3**

- **Selisih mulai melebar pada `max_depth = 2`** (latih 0,958 vs uji 0,895 → gap **0,064**), lalu melebar terus seiring kedalaman. **Selisih terbesar = 0,088 pada `max_depth ≥ 7`**, tepatnya saat akurasi latih mencapai 1,000 (pohon hafal seluruh data latih) sedangkan akurasi uji justru menurun ke 0,912 — tanda klasik *overfitting*.
- **Dua cara mengurangi *overfitting* (dari percobaan ini):**
  1. **Membatasi kompleksitas model / regularisasi** — misalnya menetapkan `max_depth` kecil (3–4), menaikkan `min_samples_leaf`, atau melakukan *pruning*; pada tabel terlihat `max_depth=3–4` memberi keseimbangan terbaik (uji 0,939 dengan gap hanya 0,037–0,048).
  2. **Menambah/memperkaya data dan validasi silang** — *cross-validation* (mis. k-fold 5/10), *early stopping*, dan *data augmentation* membuat estimasi generalisasi lebih stabil sehingga pemilihan model tidak bergantung pada satu pembagian data uji. (Alternatif: *ensemble* seperti Random Forest yang mereduksi varians pohon tunggal.)

---

#### Job 4 — Neural Network (MLP) dengan PyTorch

```python
import torch, torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

tf = transforms.ToTensor()
train = DataLoader(datasets.MNIST("data", train=True, download=True,
                   transform=tf), batch_size=128, shuffle=True)
test = DataLoader(datasets.MNIST("data", train=False, transform=tf),
                  batch_size=256)
dev = "cuda" if torch.cuda.is_available() else "cpu"

@torch.no_grad()
def evaluate(model):
    model.eval(); ok = n = 0
    for x, y in test:
        x, y = x.to(dev), y.to(dev)
        ok += (model(x).argmax(1) == y).sum().item(); n += len(y)
    return ok / n

def fit(model, epochs=3):
    model.to(dev)
    opt = torch.optim.Adam(model.parameters(), 1e-3)
    loss_fn = nn.CrossEntropyLoss()
    for e in range(epochs):
        model.train()
        for x, y in train:
            x, y = x.to(dev), y.to(dev)
            opt.zero_grad()
            loss = loss_fn(model(x), y)
            loss.backward()
            opt.step()
        print(f"epoch {e+1} loss {loss.item():.4f} acc {evaluate(model):.4f}")

mlp = nn.Sequential(nn.Flatten(), nn.Linear(784, 128), nn.ReLU(),
                    nn.Linear(128, 10))
fit(mlp)
print("Parameter MLP:", sum(p.numel() for p in mlp.parameters()))
```

*Variasi yang dijalankan: jumlah neuron tersembunyi **32, 128, 512** dan jumlah epoch **1–5** (default jobsheet = 3 epoch, dijalankan 5 epoch agar efek epoch terlihat).*

![Job 4 - Log eksekusi training MLP](assets/ss/job4_execution.png)

**Tabel hasil Job 4 — pengaruh jumlah neuron dan epoch (akurasi uji MNIST)**

| Neuron tersembunyi | Jumlah parameter | Epoch 1 | Epoch 2 | **Epoch 3 (default)** | Epoch 4 | **Epoch 5** | Loss epoch 5 |
| :---: | ---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **32** | 25.450 | 0,9165 | 0,9307 | 0,9431 | 0,9484 | 0,9517 | 0,1601 |
| **128 (default)** | 101.770 | 0,9341 | 0,9538 | 0,9598 | 0,9678 | 0,9712 | 0,0880 |
| **512** | 407.050 | 0,9564 | 0,9715 | 0,9736 | 0,9783 | 0,9780 | 0,0449 |

![Job 4 - Kurva loss dan akurasi uji MLP per epoch](assets/ss/job4_training_curve.png)

**Jawaban tugas Job 4**

- **Jumlah neuron:** semakin banyak neuron tersembunyi, semakin besar kapasitas model dan parameter (32 → 25.450 param; 128 → 101.770; 512 → 407.050 atau **4x** dari 128), akurasi ikut naik (0,9431 → 0,9598 → 0,9736 pada epoch 3), tetapi *reward* makin kecil dan biaya komputasi/memori makin besar; MLP-512 bahkan mulai datar (0,9783 → 0,9780 pada epoch 4→5).
- **Jumlah epoch:** akurasi terus naik tiap epoch dan *loss* terus turun, namun kenaikannya mengecil (*diminishing returns*) — misal MLP-128: epoch 1→2 naik +1,97 poin, epoch 4→5 hanya +0,34 poin. Peningkatan epoch hanya membantu selama model belum konvergen; kelebihan epoch justru berisiko *overfitting*.
- **Peran `loss.backward()`:** menghitung gradien $\partial \text{loss}/\partial \theta$ untuk seluruh parameter melalui *backpropagation* (rantai aturan) dan menyimpannya di `p.grad`. **Peran `opt.step()`:** optimizer (Adam) memakai gradien tersebut untuk memperbarui bobot, $\theta \leftarrow \theta - \eta \cdot \hat{m}/(\sqrt{\hat{v}}+\epsilon)$. Urutan wajib tiap iterasi: `zero_grad()` → `forward` → `backward()` → `step()`.

---

#### Job 5 — CNN

```python
cnn = nn.Sequential(
    nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Flatten(), nn.Linear(32 * 7 * 7, 10))
fit(cnn)
print("Parameter CNN:", sum(p.numel() for p in cnn.parameters()))
```

![Job 5 - Log eksekusi training CNN](assets/ss/job5_execution.png)

**Tabel hasil Job 5 — CNN vs MLP (epoch yang sama, 5 epoch)**

| Arsitektur | Jumlah parameter | Epoch 3 | **Epoch 5** | Loss epoch 5 |
| :--- | ---: | :---: | :---: | :---: |
| **CNN (Job 5)** | **20.490** | 0,9827 | **0,9859** | 0,0472 |
| MLP 128 neuron (Job 4) | 101.770 | 0,9598 | 0,9712 | 0,0880 |
| MLP 512 neuron (Job 4) | 407.050 | 0,9736 | 0,9780 | 0,0449 |

![Job 5 - Kurva loss dan akurasi uji CNN](assets/ss/job5_training_curve.png)

![Job 5 - Perbandingan akurasi dan jumlah parameter MLP vs CNN](assets/ss/job5_mlp_vs_cnn.png)

**Jawaban tugas Job 5**

- **Perbandingan:** CNN mencapai akurasi **0,9859** (epoch 5) dengan hanya **20.490 parameter**, sedangkan MLP-128 hanya 0,9712 dengan 101.770 parameter — CNN **lebih akurat +1,47 poin** sekaligus **5x lebih hemat parameter** (hanya 20,1% dari MLP-128; bahkan lebih kecil 20x dibanding MLP-512). CNN sudah melampaui MLP-512 (407.050 param) yang beratnya 20x lipat.
- **Mengapa CNN cocok untuk gambar:**
  1. ***Weight sharing*** — satu filter konvolusi (mis. 3x3x16) dipakai ulang di **seluruh posisi spasial** gambar, sehingga jumlah parameter tidak bergantung pada resolusi gambar dan model belajar fitur yang *translation invariant* (mis. tepi/titik tetap dikenali di sudut mana pun).
  2. ***Local connectivity*** — setiap neuron hanya terhubung ke *receptive field* lokal (3x3 piksel), sehingga hierarki fitur lokal (garis → tekstur → bentuk) dibangun berlapis, sesuai sifat citra yang pikselnya berdekatan bermakna; MLP justru "melempar" seluruh piksel ke satu lapisan penuh sehingga struktur spasial hilang dan parameternya membengkak (784x128 = 100.352 bobot hanya untuk lapisan pertama).

---

#### Job 6 — Self-Attention (Konsep Transformer)

```python
import numpy as np
np.random.seed(0)
T, d = 4, 8                              # 4 token, dimensi 8
X = np.random.randn(T, d)
Wq, Wk, Wv = [np.random.randn(d, d) for _ in range(3)]

Q, K, V = X @ Wq, X @ Wk, X @ Wv
S = Q @ K.T / np.sqrt(d)                 # skor kecocokan
A = np.exp(S) / np.exp(S).sum(axis=1, keepdims=True)   # softmax per baris
out = A @ V
print(A.round(2)); print(out.shape)
```

![Job 6 - Log eksekusi self-attention](assets/ss/job6_execution.png)

**Matriks attention yang dihasilkan**

$$
A=\begin{bmatrix}
0.00 & 0.99 & 0.01 & 0.00\\
0.03 & 0.35 & 0.09 & 0.54\\
0.00 & 0.00 & 1.00 & 0.00\\
0.00 & 0.93 & 0.07 & 0.00
\end{bmatrix},
\qquad
A\mathbf{1}=\begin{bmatrix}1\\1\\1\\1\end{bmatrix},
\qquad \text{out.shape}=(4,8)
$$

![Job 6 - Heatmap matriks attention (dengan dan tanpa scaling)](assets/ss/job6_attention_heatmap.png)

**Jawaban tugas Job 6**

- **(a)** Setiap baris $A$ berjumlah **1 persis** — deviasi terbesar hanya $1{,}11\times10^{-16}$ (batas presisi *floating point*). Ini terjamin karena $A$ adalah hasil **softmax per baris**, dan softmax secara definisi menormalkan sehingga $\sum_j A_{ij}=1$ (dibuktikan pada log: `[1. 1. 1. 1.]`).
- **(b)** Nilai $A[i][j]$ = **bobot perhatian token ke-$i$ terhadap token ke-$j$**: seberapa besar *query* token $i$ cocok dengan *key* token $j$, dan seberapa besar **nilai (value) token $j$** berkontribusi pada representasi keluaran token $i$ (output $=A\cdot V$, yaitu rata-rata tertimbang). Contoh: pada baris ke-2, token-2 menaruh bobot 1,00 pada dirinya sendiri (fokus penuh ke token-2), sedangkan baris ke-3 membagi bobot 0,54 ke token-4, 0,35 ke token-2, dst.
- **(c)** Skor dibagi $\sqrt{d}$ (di sini $\sqrt{8}=2{,}8284$) karena varians dari titik-dukung $QK^T$ tumbuh sebanding $d$; pembagian ini **menormalkan varians skor ke ~1** agar softmax tidak jatuh ke kondisi *saturasi* (hampir one-hot) saat dimensi besar. Akibat saturasi gradien sangat kecil dan training lambat. Terbukti pada percobaan: tanpa scaling seluruh baris langsung *pecah* ke nilai ekstrem (entropi rata-rata **0,1445** vs **0,3333** dengan scaling; batas maksimum untuk $T=4$ adalah $\ln 4 = 1{,}3863$).

---

#### Job 7 — Inference

```python
import time
cnn.eval()
x, _ = next(iter(test)); x = x.to(dev)

def bench(bs, grad):
    xb = x[:bs]
    ctx = torch.enable_grad() if grad else torch.no_grad()
    with ctx:
        t0 = time.perf_counter()
        for _ in range(50): cnn(xb)
        return (time.perf_counter() - t0) / 50 * 1000

for bs in [1, 32, 256]:
    a, b = bench(bs, False), bench(bs, True)
    print(bs, "no_grad:", round(a, 2), "ms | grad:", round(b, 2), "ms")
```

*Pengukuran diperkaya dengan mode `fwd+bwd` (latensi training nyata), warmup 10 iterasi, diulang 3 kali dan diambil nilai terkecil (50 iterasi x 3), CPU.*

![Job 7 - Log benchmark inference](assets/ss/job7_execution.png)

**Tabel hasil Job 7 — latensi rata-rata per iterasi (ms, CPU)**

| Batch | Inference `no_grad` | Forward `enable_grad` | Training `forward+backward` | Rasio training/inference | *Throughput* inference |
| :---: | ---: | ---: | ---: | :---: | ---: |
| **1** | **0,195 ms** | 0,267 ms | 0,969 ms | 4,97x | ~5.128 gambar/detik |
| **32** | 1,538 ms | 1,667 ms | 4,193 ms | 2,73x | ~20.806 gambar/detik |
| **256** | **12,791 ms** | 12,719 ms | 29,238 ms | 2,29x | ~20.014 gambar/detik |

![Job 7 - Grafik latensi inference vs training](assets/ss/job7_latency.png)

**Jawaban tugas Job 7**

- **Mengapa `model.eval()`:** menyalakan mode evaluasi — menonaktifkan *dropout* (bila ada) dan membuat *BatchNorm* memakai *running statistics* latih, sehingga keluaran **deterministik dan benar** untuk data baru. Tanpa ini, hasil *inference* bisa berbeda tiap kali dijalankan (mis. aktivasi malah mengandung *dropout*).
- **Mengapa `torch.no_grad()`:** menonaktifkan pembentukan graf autograd sehingga activation tidak disimpan untuk *backward* → **hemat memori dan sedikit lebih cepat**. Terverifikasi pada log: setelah `enable_grad` **6/6** parameter memiliki `.grad`, setelah `no_grad` **0/6** parameter memiliki `.grad`.
- **Tiga teknik optimasi *inference*:**
  1. **Kuantisasi** (FP16/INT8) — mengurangi ukuran model dan mempercepat aritmetika (mis. `torch.quantization`, TensorRT).
  2. **Optimasi grafik & fusi operator** — `torch.compile`, ONNX Runtime, atau TensorRT menggabungkan operasi konvolusi+ReLU dan memangkas *kernel launch*.
  3. **Pruning / *knowledge distillation* + *batching*** — memangkas bobot yang tidak penting, memadatkan model kecil yang setara, serta memproses banyak sampel sekaligus (pada pengukuran ini *throughput* melompat dari ~5.128 ke ~20.014 gambar/detik ketika batch dinaikkan dari 1 ke 256).

---

### Tabel Hasil Praktik

| Job | Metrik yang Dicatat | Hasil | Catatan |
| :---: | :--- | :--- | :--- |
| **1** | $F_1$ (LogReg / Random Forest) | **0,9619 / 0,9526** (makro); akurasi 0,9649 / 0,9561 | Logistic Regression unggul tipis; *recall* kelas *malignant* 0,9286 pada keduanya |
| **2** | Jumlah cluster yang paling masuk akal | **k = 3** | Silhouette justru memilih k=2 (0,6810) → konflik indikator; ARI k=3 = 0,7302 tertinggi |
| **3** | Selisih akurasi train-test terbesar | **0,088 pada `max_depth` 7–15** (1,000 vs 0,912); mulai melebar di `max_depth=2` (0,064) | Akurasi latih jenuh 1,000 sedangkan uji justru turun |
| **4** | Akurasi MLP / jumlah parameter | **0,9712 (128 neuron, epoch 5)** / **101.770**; 32 neuron: 0,9517 / 25.450; 512 neuron: 0,9780 / 407.050 | Epoch 3 (default): 0,9431 / 0,9598 / 0,9736 |
| **5** | Akurasi CNN / jumlah parameter | **0,9859 (epoch 5)** / **20.490** | 5x lebih hemat parameter dari MLP-128, akurasinya lebih tinggi 1,47 poin |
| **6** | Jumlah tiap baris matriks $A$ | **1.0 (persis)** — deviasi maks $1{,}11\times10^{-16}$ | Sifat softmax per baris; keluaran `A @ V` berbentuk (4, 8) |
| **7** | Latensi batch 1 / 256 (ms) | **0,195 ms / 12,791 ms** (`no_grad`); training 0,969 / 29,238 ms | Training 2,29–4,97x lebih berat daripada *inference* |

---

### Lembar Kerja 3 — Perbandingan Arsitektur

| Arsitektur | Cara Kerja Utama | Cocok untuk Data / Tugas |
| :--- | :--- | :--- |
| **MLP** | Semua input **diratakan (flatten)** lalu dilewatkan lapisan *fully connected* ($y=\sigma(Wx+b)$) secara berurutan; setiap neuron terhubung ke **semua** neuron lapisan sebelumnya, tanpa memanfaatkan struktur spasial/urutan. | Data tabular/fitur vektor (mis. 30 fitur Breast Cancer), regresi, klasifikasi sederhana, dan tahap klasifikasi akhir (*head*) dari arsitektur lain. Parameter besar bila input adalah gambar (784x128 bobot hanya lapisan pertama). |
| **CNN** | **Konvolusi 2D** dengan filter kecil yang digerakkan melintasi seluruh gambar (*weight sharing* + *local connectivity*), dilanjutkan *non-linearity* dan *pooling* untuk membangun hierarki fitur lokal → vektor fitur → lapisan klasifikasi. | Data spasial/grid: gambar (MNIST, foto), peta, sinyal 1D. Terbukti pada praktikum: **20.490 parameter** untuk akurasi **0,9859** (MNIST) — sangat efisien dibanding MLP. |
| **Transformer** | **Self-attention** ($\text{softmax}(QK^T/\sqrt{d})V$) menghitung interaksi semua pasang token dalam satu urutan secara paralel, ditambah *feed-forward network* dan *positional encoding* berlapis; hubungan antar token dipelajari lewat bobot *query/key/value*. | Data sekuensial/urutan dan hubungan jarak jauh: teks (BERT, GPT), terjemahan, time-series, audio, vision transformer; serta tugas yang butuh paralelisme tinggi pada urutan panjang. |

---

## F. Pertanyaan Evaluasi

**1. Jelaskan perbedaan *supervised* dan *unsupervised learning* beserta satu contoh masing-masing!**

*Supervised learning* belajar dari data yang **sudah berlabel** — tersedia pasangan $(x, y)$ sehingga model meminimalkan kesalahan prediksi terhadap label benar, lalu dipakai untuk memprediksi data baru; tugasnya berupa klasifikasi atau regresi. *Unsupervised learning* bekerja pada data **tanpa label** — model sendiri yang menemukan pola/struktur (asosiasi, kelompok, reduksi dimensi) berdasarkan kemiripan statistik data.

- **Contoh supervised:** klasifikasi tumor **Breast Cancer** dengan Logistic Regression pada Job 1 → $F_1$ 0,9619 (label 0 = *malignant*, 1 = *benign* tersedia saat *training*).
- **Contoh unsupervised:** **K-Means (k=3)** + **PCA** pada dataset Iris pada Job 2 — label diabaikan saat *fitting*, klaster murni dihitung dari jarak fitur.

**2. Apa hubungan *overfitting* dengan *bias-variance*? Bagaimana cara mendeteksinya?**

*Overfitting* adalah kondisi **variance tinggi**: model terlalu fleksibel sehingga menghafal noise data latih — error latih sangat rendah tetapi error uji tinggi (generalisasi buruk); kebalikannya *underfitting* berarti *bias* tinggi (model terlalu sederhana sehingga kedua error sama-sama tinggi). *Bias-variance tradeoff* menuntut keseimbangan: total error $\approx$ bias$^2$ + variance + noise. **Deteksi:** (1) membandingkan akurasi/loss latih vs uji seperti Job 3 — pada `max_depth=7` latih 1,000 vs uji 0,912 (gap **0,088**) padahal di `max_depth=1` gap hanya 0,002; (2) melihat kurva validasi *learning curve* (gap yang melebar terus seiring kompleksitas/epoch = *overfitting*); (3) memakai *cross-validation* sehingga performa antar-fold bervariasi tinggi menandakan varians model besar.

**3. Jelaskan alur satu iterasi *training* (*forward pass*, *loss*, *backward*, *update* bobot)!**

1. **Forward pass** — input $x$ dilewatkan model menghasilkan prediksi $\hat{y} = f_\theta(x)$ (mis. `logits = model(x)`).
2. **Hitung loss** — prediksi dibandingkan dengan label memakai fungsi kerugian (Job 4/5: `loss = CrossEntropyLoss(logits, y)`) → satu bilangan yang mewakili seberapa salah model.
3. **Backward** — `loss.backward()` menjalankan *backpropagation*: turunan rantai dihitung mundur dari loss ke setiap parameter, $\partial \text{loss}/\partial \theta$ disimpan di `p.grad`.
4. **Update bobot** — `opt.step()` memperbarui parameter dengan optimizer (Adam): $\theta \leftarrow \theta - \eta \cdot \widehat{m}/(\sqrt{\widehat{v}}+\epsilon)$.
5. **Reset gradien** — `opt.zero_grad()` mengosongkan `.grad` (atau `set_to_none=True`) agar gradien iterasi berikutnya tidak menumpuk.

Pada praktikum ini satu epoch = 469 iterasi (60.000 gambar / batch 128); *loss* CNN turun dari 0,3683 (epoch 1) ke 0,0472 (epoch 5) — bukti bobot berhasil diperbarui.

**4. Mengapa Transformer lebih mudah diparalelkan dibandingkan RNN?**

RNN memproses token **berurutan** — hidden state $h_t$ bergantung pada $h_{t-1}$ sehingga langkah $t+1$ tidak bisa dihitung sebelum $t$ selesai; ini membangun *sequential dependency* sehingga pelatihan hanya bisa paralel antar *batch*, bukan antar langkah waktu, dan rawan *vanishing gradient* pada urutan panjang. Transformer memakai **self-attention** yang mengevaluasi seluruh token **sekaligus dalam satu operasi matriks** ($Q$, $K$, $V$ untuk semua posisi dihitung bersamaan, skor $QK^T$ untuk semua pasang token tersedia serentak), sehingga tidak ada ketergantungan antar langkah → semua posisi dapat diproses bersamaan pada GPU/CPU, waktu training lebih pendek untuk data panjang, dan setiap token langsung terhubung ke token lain berapa pun jaraknya.

**5. Apa perbedaan komputasi saat *training* dan *inference*, dan teknik apa yang dapat mempercepat *inference*?**

| Aspek | *Training* | *Inference* |
| :--- | :--- | :--- |
| Tahapan per iterasi | forward + hitung loss + **backward** + update optimizer | **forward saja** |
| Graf autograd | Aktif — activation disimpan untuk *backward* | `torch.no_grad()` — tidak ada penyimpanan |
| Parameter / state | Bobot diperbarui, ada *optimizer state* (momen Adam) | Bobot tetap, tanpa optimizer state |
| Mode model | `model.train()` (dropout/BN aktif) | `model.eval()` (dropout/nonaktif, BN pakai statistik latih) |
| Kecepatan terukur (Job 7) | 0,969 ms (batch 1) / 29,238 ms (batch 256) | **0,195 ms** (batch 1) / **12,791 ms** (batch 256) → **2,29–4,97x lebih cepat** |

**Teknik mempercepat *inference*:** (1) **kuantisasi** FP16/INT8 — model lebih kecil dan operasi lebih cepat; (2) **optimasi grafik/fusi operator** (`torch.compile`, ONNX Runtime, TensorRT) yang menggabungkan operasi dan memangkas *overhead*; (3) ***batching* besar + *pruning*/*knowledge distillation*** — memproses banyak sampel sekaligus (pengukuran menunjukkan *throughput* naik dari ~5.128 ke ~20.014 gambar/detik saat batch 1 → 256) dan memangkas bobot tak penting.

---

## G. Kesimpulan

Berdasarkan praktikum JS-AI-02 yang telah dilaksanakan, dapat disimpulkan bahwa:

1. **Supervised (Job 1):** Logistic Regression (akurasi **0,9649**, $F_1$ **0,9619**) sedikit lebih unggul daripada Random Forest (0,9561 / 0,9526) pada Breast Cancer; *recall* kelas *malignant* menjadi metrik paling penting karena *false negative* = kanker yang lolos dari deteksi.
2. **Unsupervised (Job 2):** K-Means + PCA mampu memvisualkan struktur Iris pada 2 komponen (97,77% varians); pemilihan jumlah klaster sulit tanpa label — silhouette memilih $k=2$ (0,6810) padahal struktur sesungguhnya $k=3$ (ARI tertinggi 0,7302), sehingga keputusan akhir tetap butuh justifikasi domain.
3. **Overfitting (Job 3):** semakin dalam `max_depth`, akurasi latih menaik ke 1,000 sedangkan akurasi uji justru turun ke 0,912; selisih terbesar **0,088** dan mulai melebar pada `max_depth=2`. Pengendalian kompleksitas model dan validasi silang adalah dua mitigasi utamanya.
4. **MLP (Job 4):** akurasi dan jumlah parameter tumbuh seiring jumlah neuron (32: 0,9517/25.450 — 128: 0,9712/101.770 — 512: 0,9780/407.050) dan seiring epoch, namun dengan imbal hasil makin kecil; `loss.backward()` menghitung gradien, `opt.step()` memperbarui bobot.
5. **CNN (Job 5):** CNN mencapai **0,9859** dengan hanya **20.490 parameter** (20,1% dari MLP-128) berkat *weight sharing* dan *local connectivity* — terbukti paling efisien untuk data gambar.
6. **Transformer (Job 6):** matriks *attention* $A$ memiliki jumlah baris = **1 persis** (sifat softmax), $A[i][j]$ adalah bobot perhatian token $i$ terhadap token $j$, dan pembagian $\sqrt{d}$ mencegah softmax jatuh ke kondisi *one-hot* (entropi 0,3333 vs 0,1445 tanpa scaling).
7. **Training vs inference (Job 7):** *inference* dengan `eval()` + `no_grad()` **2,29–4,97x lebih cepat** daripada training (0,195 ms vs 0,969 ms pada batch 1) dan tidak membuat gradien (0/6 parameter memiliki `.grad`), sehingga latensi layanan dapat ditekan lewat kuantisasi, optimasi grafik, dan *batching*.

---

## H. Lembar Penilaian

| Aspek Penilaian | Skor Maks | Skor Diperoleh |
| :--- | :---: | :---: |
| Kode berjalan dan hasil benar (Job 1–7) | 40 | |
| Analisis pada bagian Tugas dan Lembar Kerja 2 | 20 | |
| Ketepatan Lembar Kerja 1 dan 3 | 15 | |
| Jawaban Pertanyaan Evaluasi | 15 | |
| Partisipasi, kerapian, dan ketepatan waktu | 10 | |
| **Total** | **100** | |

<br>

| Tanda Tangan |
| :--- |
| **Peserta:** ( Adinda Massa Merah Lawan Tirani ) |
| **Instruktur:** ( ......................................... ) |

---

### Lampiran A — Daftar Berkas Eksekusi

| Berkas | Isi |
| :--- | :--- |
| `assets/ss/job0_setup_execution.png` | Log Langkah 1: versi Python/library, device, dataset |
| `assets/ss/job1_execution.png` | Log Job 1 + `job1_confusion_matrix.png` |
| `assets/ss/job2_execution.png` | Log Job 2 + `job2_pca_clusters.png` |
| `assets/ss/job3_execution.png` | Log Job 3 + `job3_overfitting.png` |
| `assets/ss/job4_execution.png` | Log Job 4 + `job4_training_curve.png` |
| `assets/ss/job5_execution.png` | Log Job 5 + `job5_training_curve.png`, `job5_mlp_vs_cnn.png` |
| `assets/ss/job6_execution.png` | Log Job 6 + `job6_attention_heatmap.png` |
| `assets/ss/job7_execution.png` | Log Job 7 + `job7_latency.png` |
| `tugas/scripts/*.py` | Sumber kode yang dijalankan (dapat diubah menjadi notebook `3.34.24.2.01_Adinda_Jobsheet_ML_DL.ipynb`) |
| `tugas/scripts/metrics.json` | Metrik terukur otomatis yang menjadi dasar seluruh tabel di laporan ini |
