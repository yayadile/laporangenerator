# JOBSHEET PELATIHAN Machine Learning & Deep Learning Refresher
**Supervised/Unsupervised • Neural Network • CNN • Transformer • Training & Inference**

| Parameter | Keterangan |
| :--- | :--- |
| **Nama Peserta** | |
| **Kelas / Kelompok** | |
| **Tanggal Pelaksanaan** | |
| **Alokasi Waktu** | 4 x 45 menit |
| **Kode Jobsheet** | JS-AI-02 |
| **Instruktur** | Angga Wahyu Wibowo, S.Kom., M.Eng., Ph.D |

---

## A. Tujuan Pembelajaran
Setelah menyelesaikan jobsheet ini, peserta diharapkan mampu:
1. Melatih dan mengevaluasi model *supervised learning* (klasifikasi) serta menafsirkan metrik *precision*, *recall*, dan $F1$.
2. Menerapkan *clustering* dan reduksi dimensi pada data tanpa label (*unsupervised learning*).
3. Mengenali *overfitting* dari perbandingan akurasi data latih dan data uji.
4. Membangun dan melatih *neural network* (MLP) dan CNN menggunakan PyTorch.
5. Menjelaskan mekanisme *self-attention* pada Transformer melalui implementasi kecil.
6. Membedakan proses *training* dan *inference* serta mengukur latensi *inference*.

---

## B. Dasar Teori Singkat
Machine Learning (ML) belajar pola dari data. Pada *supervised learning*, model dilatih dengan pasangan input dan label untuk klasifikasi atau regresi; pada *unsupervised learning*, model mencari struktur pada data tanpa label, misalnya *clustering* dan reduksi dimensi. Model yang terlalu menghafal data latih mengalami *overfitting*, sehingga performanya turun pada data baru.

Deep Learning menggunakan *neural network* berlapis. Bobot dipelajari lewat *backpropagation* dan *optimizer*. CNN memakai filter konvolusi untuk mengekstrak fitur lokal pada gambar, sedangkan Transformer memakai *self-attention* agar setiap token dapat memperhatikan token lain dalam satu urutan. *Training* memperbarui bobot model, sedangkan *inference* hanya menjalankan *forward pass* dengan bobot tetap. Pelajari kembali presentasi "Machine Learning & Deep Learning Refresher" sebelum praktik.

---

## C. Alat dan Bahan
- Laptop / PC dengan akses internet (atau Google Colab)
- Python 3.10+ dengan library `numpy`, `matplotlib`, `scikit-learn`, `torch`, `torchvision` (`pip install numpy matplotlib scikit-learn torch torchvision`)
- Dataset bawaan: Breast Cancer dan Iris (`scikit-learn`), MNIST (`torchvision`, terunduh otomatis)
- Slide presentasi "Machine Learning & Deep Learning Refresher" dan lembar jobsheet ini

---

## D. Langkah Kerja
1. Pelajari materi presentasi, lalu siapkan lingkungan Python atau Colab dan impor library yang dibutuhkan.
2. Kerjakan Job 1–3 pada Lembar Kerja 2 (*supervised*, *unsupervised*, *overfitting*) dan catat hasilnya pada tabel hasil.
3. Kerjakan Job 4–5 (MLP dan CNN dengan PyTorch) dan catat akurasi serta jumlah parameter.
4. Kerjakan Job 6–7 (*self-attention* dan *inference*) dan catat hasil pengamatan.
5. Lengkapi Lembar Kerja 1 (perbandingan konsep) dan Lembar Kerja 3 (perbandingan arsitektur).
6. Jawab pertanyaan evaluasi pada Bagian F secara individu, lalu tulis kesimpulan pada Bagian G.
7. Kumpulkan jobsheet beserta notebook (`.ipynb`) berformat `NIM_Nama_Jobsheet_ML_DL` kepada instruktur.

---

## E. Lembar Kerja

### Lembar Kerja 1 — Perbandingan Konsep

| Konsep | Definisi Singkat (isi sendiri) | Contoh Nyata |
| :--- | :--- | :--- |
| **Supervised Learning** | | |
| **Unsupervised Learning** | | |
| **Overfitting** | | |
| **Training vs Inference** | | |

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
> **Tugas:** Catat *accuracy*, *precision*, *recall*, dan $F1$ kedua model. Model mana yang lebih baik, dan mengapa *recall* penting pada deteksi kanker?

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
> **Tugas:** Ubah `n_clusters` menjadi 2 dan 4. Bagaimana hasil visualnya, dan mengapa menentukan jumlah cluster sulit tanpa label?

---

#### Job 3 — Overfitting (gunakan Xtr, Xte, ytr, yte dari Job 1)
```python
from sklearn.tree import DecisionTreeClassifier

for d in range(1, 16):
    t = DecisionTreeClassifier(max_depth=d, random_state=42).fit(Xtr, ytr)
    print(d, round(t.score(Xtr, ytr), 3), round(t.score(Xte, yte), 3))
```
> **Tugas:** Pada `max_depth` berapa selisih akurasi *train* dan *test* mulai melebar? Sebutkan dua cara mengurangi *overfitting*.

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
> **Tugas:** Ubah jumlah neuron (128 menjadi 32 dan 512) dan jumlah epoch. Catat akurasi dan jumlah parameter. Jelaskan peran `loss.backward()` dan `opt.step()`.

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
> **Tugas:** Bandingkan akurasi dan jumlah parameter CNN dengan MLP. Mengapa CNN cocok untuk gambar (sebut *weight sharing* dan *local connectivity*)?

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
> **Tugas:** 
> - (a) Pastikan tiap baris $A$ berjumlah 1; 
> - (b) Jelaskan arti nilai $A[i][j]$; 
> - (c) Mengapa skor dibagi $\sqrt{d}$?

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
> **Tugas:** Isi tabel hasil. Mengapa `model.eval()` dan `torch.no_grad()` dipakai saat *inference*? Sebutkan tiga teknik optimasi *inference*.

---

### Tabel Hasil Praktik

| Job | Metrik yang Dicatat | Hasil | Catatan |
| :---: | :--- | :--- | :--- |
| **1** | $F1$ (LogReg / Random Forest) | | |
| **2** | Jumlah cluster yang paling masuk akal | | |
| **3** | Selisih akurasi train-test terbesar | | |
| **4** | Akurasi MLP / jumlah parameter | | |
| **5** | Akurasi CNN / jumlah parameter | | |
| **6** | Jumlah tiap baris matriks $A$ | | |
| **7** | Latensi batch 1 / 256 (ms) | | |

---

### Lembar Kerja 3 — Perbandingan Arsitektur

| Arsitektur | Cara Kerja Utama (isi sendiri) | Cocok untuk Data / Tugas |
| :--- | :--- | :--- |
| **MLP** | | |
| **CNN** | | |
| **Transformer** | | |

---

## F. Pertanyaan Evaluasi

1. Jelaskan perbedaan *supervised* dan *unsupervised learning* beserta satu contoh masing-masing!
   $$\text{}$$
   $$\text{}$$

2. Apa hubungan *overfitting* dengan *bias-variance*? Bagaimana cara mendeteksinya?
   $$\text{}$$
   $$\text{}$$

3. Jelaskan alur satu iterasi *training* (*forward pass*, *loss*, *backward*, *update* bobot)!
   $$\text{}$$
   $$\text{}$$

4. Mengapa Transformer lebih mudah diparalelkan dibandingkan RNN?
   $$\text{}$$
   $$\text{}$$

5. Apa perbedaan komputasi saat *training* dan *inference*, dan teknik apa yang dapat mempercepat *inference*?
   $$\text{}$$
   $$\text{}$$

---

## G. Kesimpulan
Tuliskan kesimpulan hasil praktik dan diskusi kelompok Anda:
$$\text{}$$
$$\text{}$$

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
| **Peserta:** ( ......................................... ) |
| **Instruktur:** ( ......................................... ) |