# JOBSHEET PRAKTIKUM
**Representasi Citra Digital: Piksel, Ukuran $M \times N$, Cropping, dan Kuantisasi**

| Informasi Praktikum | Detail |
| :--- | :--- |
| **Mata Kuliah** | Pengolahan Citra Digital |
| **Topik** | Pengertian Pengolahan Citra Digital (Bab 1) |
| **Alokasi Waktu** | 2 x 50 menit |
| **Nama / NIM** | ……………………………………………… |
| **Kelas / Tanggal** | ……………………………………………… |

---

## A. Tujuan
Setelah praktikum, mahasiswa mampu:
1. Membaca citra ke dalam komputer dan menyatakannya sebagai larik $f(m, n)$ berukuran $M \times N$.
2. Mengakses nilai piksel dan memahami perbedaan koordinat citra dengan koordinat kartesian.
3. Melakukan *cropping* dan membuat citra berukuran pangkat 2.
4. Melakukan kuantisasi dan mengamati pengaruh jumlah aras intensitas terhadap kualitas citra.

---

## B. Alat dan Bahan
- Komputer dengan Python 3.8 atau lebih baru, beserta pustaka Pillow dan NumPy.
- Editor kode (VS Code, Jupyter Notebook, atau Google Colab).
- Satu file citra berformat JPG/PNG (beri nama `citra.jpg`), disarankan berukuran minimal $256 \times 256$ piksel. Boleh memakai citra "Lena" atau "Boat".
- **Persiapan:** Jalankan perintah berikut pada terminal bila pustaka belum terpasang:
  ```bash
  pip install pillow numpy
  ```

---

## C. Dasar Teori Singkat
- Citra adalah sebaran variasi gelap-terang atau warna pada bidang datar, dinyatakan dengan angka-angka intensitas pada arah mendatar dan tegak.
- Citra kontinu ditulis $f(x, y)$. Versi diskret untuk komputer ditulis $f(m, n)$, dengan $m = 0, 1, \dots, M-1$ dan $n = 0, 1, \dots, N-1$, sehingga terdapat $M \times N$ posisi.
- Setiap posisi $(m, n)$ berisi satu unsur gambar yang disebut **piksel**.
- Titik asal $(0,0)$ pada koordinat citra berada di **pojok kiri atas**, berbeda dengan koordinat kartesian yang berada di **kiri bawah**.
- Standar kuantisasi adalah 256 aras intensitas dengan kode biner 8 bit (1 byte) per piksel.

---

## D. Langkah Kerja

### Percobaan 1: Membaca citra dan ukuran $M \times N$
Buat file `praktikum1.py`, lalu ketik kode berikut:
```python
from PIL import Image
import numpy as np

img = Image.open("citra.jpg").convert("L")   # L = grayscale
f = np.array(img)

M, N = f.shape
print("Ukuran citra M x N :", M, "x", N)
print("Jumlah piksel      :", M * N)
print("Tipe data          :", f.dtype)
print("Intensitas min/maks:", f.min(), "/", f.max())
```
Jalankan program, lalu catat hasilnya pada Tabel 1.

---

### Percobaan 2: Mengakses piksel dan koordinat citra
Tambahkan kode berikut:
```python
print("f(0, 0)     =", f[0, 0])          # pojok kiri atas
print("f(M-1, N-1) =", f[M-1, N-1])      # pojok kanan bawah
print("Blok 5x5 mulai (10,10):")
print(f[10:15, 10:15])

# Konversi ke koordinat kartesian (x, y)
m, n = 20, 30
x, y = n, (M - 1) - m
print("Citra (m,n)=", (m, n), "-> Kartesian (x,y)=", (x, y))
```
Catat nilai piksel dan hasil konversi koordinat pada Tabel 2.

---

### Percobaan 3: Cropping dan ukuran pangkat 2
Tambahkan kode berikut:
```python
crop = f[50:178, 50:178]                  # 128 x 128 (2 pangkat 7)
Image.fromarray(crop).save("hasil_crop.png")
print("Ukuran crop:", crop.shape)

# Ubah ukuran menjadi 256 x 256 (pangkat 2)
img256 = img.resize((256, 256))
img256.save("hasil_256.png")
print("Ukuran baru:", img256.size)
```
Buka `hasil_crop.png` dan `hasil_256.png`, lalu bandingkan dengan citra asli.

---

### Percobaan 4: Kuantisasi
Tambahkan kode berikut untuk membuat citra dengan jumlah aras yang berbeda:
```python
def kuantisasi(f, L):
    langkah = 256 // L
    return ((f // langkah) * langkah).astype("uint8")

for L in (256, 64, 16, 4, 2):
    hasil = kuantisasi(f, L)
    Image.fromarray(hasil).save(f"kuantisasi_{L}.png")
    print("Aras:", L, "| aras unik terdeteksi:", len(np.unique(hasil)))
```
Bandingkan kelima gambar. Catat pada Tabel 3 pada jumlah aras berapa mulai terlihat penurunan kualitas.

---

## E. Data Hasil Pengamatan

### Tabel 1. Informasi citra
| Parameter | Hasil |
| :--- | :--- |
| Nama file citra | |
| $M$ (jumlah baris) | |
| $N$ (jumlah kolom) | |
| Jumlah piksel $M \times N$ | |
| Intensitas minimum / maksimum | |

### Tabel 2. Nilai piksel dan koordinat
| Besaran | Nilai | Keterangan |
| :--- | :--- | :--- |
| $f(0, 0)$ | | |
| $f(M-1, N-1)$ | | |
| $(m, n) = (20, 30)$ | $(x, y) =$ | |

### Tabel 3. Pengaruh kuantisasi
| Aras ($L$) | Bit per piksel | Perkiraan memori ($M \times N \times \text{bit}/8\text{ byte}$) | Pengamatan visual |
| :---: | :---: | :--- | :--- |
| **256** | 8 | | |
| **64** | 6 | | |
| **16** | 4 | | |
| **4** | 2 | | |
| **2** | 1 | | |

---

## F. Pertanyaan dan Tugas
1. Mengapa titik asal $(0,0)$ pada koordinat citra berbeda dengan koordinat kartesian? Tuliskan rumus konversi dari $(m, n)$ ke $(x, y)$.
2. Mengapa ukuran citra untuk proses transformasi umumnya dipilih berupa pangkat 2?
3. Hitung kebutuhan memori citra $512 \times 512$ piksel dengan 256 aras. Berapa kebutuhan memorinya bila hanya 16 aras?
4. Jelaskan perbedaan citra analog dan citra digital berdasarkan hasil Percobaan 4.
5. **Tugas Mandiri:** Ganti citra dengan foto pilihan sendiri, ulangi Percobaan 1–4, lalu tuliskan perbedaan hasilnya.

---

## G. Kesimpulan
Tuliskan kesimpulan praktikum Anda dalam 3–5 kalimat:
$$\text{}$$
$$\text{}$$

---

## H. Penilaian

| No | Komponen | Bobot | Nilai |
| :-: | :--- | :---: | :---: |
| **1** | Percobaan 1–4 berjalan dan tabel data terisi lengkap | 40% | |
| **2** | Jawaban pertanyaan dan tugas | 30% | |
| **3** | Analisis dan kesimpulan | 20% | |
| **4** | Ketepatan waktu dan kerapian laporan | 10% | |
| | **Total** | **100%** | |