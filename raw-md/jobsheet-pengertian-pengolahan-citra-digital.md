# JOBSHEET PRAKTIKUM
**Representasi Citra Digital: Piksel, Ukuran $M \times N$, Cropping, dan Kuantisasi**

| Informasi Praktikum | Detail |
| :--- | :--- |
| **Mata Kuliah** | Pengolahan Citra Digital |
| **Topik** | Pengertian Pengolahan Citra Digital (Bab 1) |
| **Alokasi Waktu** | 2 x 50 menit |
| **Nama / NIM** | Adinda Massa Merah Lawan Tirani / 3.34.24.2.01 |
| **Kelas / Tanggal** | IK-3C / 07 Oktober 2026 |

---

## A. Tujuan

Setelah praktikum, mahasiswa mampu:

1. Membaca citra ke dalam komputer dan menyatakannya sebagai larik $f(m, n)$ berukuran $M \times N$.
2. Mengakses nilai piksel dan memahami perbedaan koordinat citra dengan koordinat kartesian.
3. Melakukan *cropping* dan membuat citra berukuran pangkat 2.
4. Melakukan kuantisasi dan mengamati pengaruh jumlah aras intensitas terhadap kualitas citra.

---

## B. Alat dan Bahan

| Komponen | Yang dipakai |
| :--- | :--- |
| **Komputer / OS** | Windows 10 Pro 64-bit |
| **Python** | 3.13.13 (`C:\Program Files\Python313\python.exe`) |
| **Pustaka** | Pillow 12.3.0, NumPy 2.4.4, Matplotlib 3.11.2 |
| **Editor kode** | VS Code / terminal |
| **File citra** | `assets/citra.jpg` — 256 x 256 piksel, mode RGB, JPEG, 16,4 KB |
| **Script** | `tugas/scripts/citra_jobsheet.py` (semua percobaan 1-4 + tugas mandiri) |

Persiapan (`pip install pillow numpy`) sudah beres — semua pustaka terpasang dan bisa dipakai langsung.

![Persiapan: cek library dan file citra](assets/ss/citra0_setup_execution.png)

---

## C. Dasar Teori Singkat

- Citra itu sebaran gelap-terang (atau warna) di atas bidang datar. Di komputer, nilainya ditulis sebagai angka intensitas.
- Citra asli namanya $f(x, y)$ (kontinu). Versi yang masuk komputer ditulis $f(m, n)$, dengan $m = 0, 1, \dots, M-1$ dan $n = 0, 1, \dots, N-1$, jadi jumlah seluruh posisinya $M \times N$.
- Tiap posisi $(m, n)$ berisi satu angka yang disebut **piksel**.
- Titik asal $(0,0)$ pada citra ada di **pojok kiri atas** — beda dengan koordinat kartesian yang asalnya di kiri bawah.
- Standar kuantisasi: 256 aras intensitas = kode biner 8 bit (1 byte) per piksel.

---

## D. Langkah Kerja

Semua percobaan dijalankan lewat satu script: `python tugas/scripts/citra_jobsheet.py`.
Log tiap percobaan disimpan sebagai screenshot di `assets/ss/citraN_execution.png`,
sedangkan hasil gambarnya disimpan sebagai PNG resolusi 200 DPI di folder yang sama.

### Percobaan 1: Membaca citra dan ukuran $M \times N$

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

![Percobaan 1 - log eksekusi](assets/ss/citra1_execution.png)

Hasilnya: citra berukuran **256 x 256**, jadi ada **65.536 piksel**, tipenya `uint8`
(0-255), intensitasnya berkisar **1 sampai 254** (mean 110,37). Artinya gambar ini
betul-betul cuma kumpulan 65.536 angka dalam satu larik.

![Percobaan 1 - citra grayscale dan histogramnya](assets/ss/citra1_histogram.png)

---

### Percobaan 2: Mengakses piksel dan koordinat citra

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

![Percobaan 2 - log eksekusi](assets/ss/citra2_execution.png)

Yang didapat:

- `f(0, 0) = 11` → pojok kiri atas gelap.
- `f(M-1, N-1) = 147` → pojok kanan bawah lebih terang.
- Blok 5x5 di (10,10) nilainya sekitar 223-227 (area terang).
- Konversi `(m, n) = (20, 30)` menjadi `(x, y) = (30, 235)`, dan nilai pikselnya sama
  (dicek lewat `f[20, 30]` = `f[M-1-235, 30]` = **36**) — jadi cuma beda cara baca, bukan beda gambar.

![Percobaan 2 - penempatan piksel dan bedanya sumbu citra vs kartesian](assets/ss/citra2_koordinat.png)

---

### Percobaan 3: Cropping dan ukuran pangkat 2

```python
crop = f[50:178, 50:178]                  # 128 x 128 (2 pangkat 7)
Image.fromarray(crop).save("hasil_crop.png")
print("Ukuran crop:", crop.shape)

# Ubah ukuran menjadi 256 x 256 (pangkat 2)
img256 = img.resize((256, 256))
img256.save("hasil_256.png")
print("Ukuran baru:", img256.size)
```

![Percobaan 3 - log eksekusi](assets/ss/citra3_execution.png)

Hasilnya:

- Crop `f[50:178, 50:178]` jadi **128 x 128** piksel — itu 2 pangkat 7, persis
  seperti diminta. Isinya potongan bagian tengah foto (mulai baris 50, kolom 50).
- Hasil resize jadi **256 x 256** (2 pangkat 8). Karena citra asli memang sudah
  256 x 256, hasilnya sama persis dengan gambar asli — ukuran pangkat 2 sudah terpenuhi sejak awal.
- Ukuran file: foto asli 16,4 KB (JPEG), crop 9,9 KB, hasil 256 x 256 jadi 36,3 KB (PNG).

![Percobaan 3 - citra asli, hasil crop, dan hasil resize](assets/ss/citra3_crop_resize.png)

File hasil crop dan resize juga disimpan terpisah:

- `assets/ss/citra3_hasil_crop.png` (128 x 128)
- `assets/ss/citra3_hasil_256.png` (256 x 256)

---

### Percobaan 4: Kuantisasi

```python
def kuantisasi(f, L):
    langkah = 256 // L
    return ((f // langkah) * langkah).astype("uint8")

for L in (256, 64, 16, 4, 2):
    hasil = kuantisasi(f, L)
    Image.fromarray(hasil).save(f"kuantisasi_{L}.png")
    print("Aras:", L, "| aras unik terdeteksi:", len(np.unique(hasil)))
```

![Percobaan 4 - log eksekusi](assets/ss/citra4_execution.png)

Hasilnya:

| Aras $L$ | Langkah | Aras unik terdeteksi | Kesan pertama |
| :---: | :---: | :---: | :--- |
| 256 | 1 | 253 | Sama persis dengan asli (cuma 3 aras yang tidak terpakai, yaitu 0, 255, dan satu lagi) |
| 64 | 4 | 64 | Masih enak dilihat, bedanya hampir tak terasa |
| 16 | 16 | 16 | Gradasi mulai pecah jadi bercak |
| 4 | 64 | 4 | Sangat kelihatan, cuma 4 tingkat abu |
| 2 | 128 | 2 | Tinggal hitam-putih |

![Percobaan 4 - perbandingan hasil kuantisasi](assets/ss/citra4_kuantisasi.png)

Makin sedikit aras, makin kecil file-nya, tapi gambarnya makin rusak. Angka
perbandingannya:

![Percobaan 4 - memori teoritis vs ukuran file asli](assets/ss/citra4_memori.png)

Hasil simpan per aras juga ada terpisah di `assets/ss/citra4_kuantisasi_{256,64,16,4,2}.png`.

---

## E. Data Hasil Pengamatan

### Tabel 1. Informasi citra

| Parameter | Hasil |
| :--- | :--- |
| Nama file citra | `citra.jpg` (JPEG, RGB, 16,4 KB) |
| $M$ (jumlah baris) | 256 |
| $N$ (jumlah kolom) | 256 |
| Jumlah piksel $M \times N$ | 65.536 piksel |
| Intensitas minimum / maksimum | 1 / 254 (tipe data `uint8`, rata-rata 110,37, 253 aras terpakai) |

### Tabel 2. Nilai piksel dan koordinat

| Besaran | Nilai | Keterangan |
| :--- | :--- | :--- |
| $f(0, 0)$ | 11 | Pojok kiri atas, termasuk gelap |
| $f(M-1, N-1)$ | 147 | Pojok kanan bawah, nilai abu-abu sedang |
| $(m, n) = (20, 30)$ | $(x, y) =$ (30, 235) | Pakai $x = n$, $y = (M-1) - m$; nilai pikselnya 36, sama dengan `f[20, 30]` |

### Tabel 3. Pengaruh kuantisasi

| Aras ($L$) | Bit per piksel | Perkiraan memori ($M \times N \times \text{bit}/8$ byte) | Pengamatan visual |
| :---: | :---: | :--- | :--- |
| **256** | 8 | 65.536 byte = **64 KB** (file PNG: 36,3 KB) | Sama dengan asli, halus, 253 aras terpakai |
| **64** | 6 | 49.152 byte = **48 KB** (file PNG: 23,5 KB) | Masih halus, beda dengan asli hampir tak terlihat |
| **16** | 4 | 32.768 byte = **32 KB** (file PNG: 13,2 KB) | Gradasi mulai pecah jadi bercak, detail rambut hilang |
| **4** | 2 | 16.384 byte = **16 KB** (file PNG: 4,9 KB) | Jelas kelihatan, cuma 4 tingkat abu, wajah rata |
| **2** | 1 | 8.192 byte = **8 KB** (file PNG: 2,3 KB) | Tinggal hitam-putih, ekspresi hilang |

Catatan: memori di kolom ketiga adalah hitungan teoritis (belum dikompresi).
File PNG aslinya lebih kecil karena PNG mengompres gambar.

---

## F. Pertanyaan dan Tugas

**1. Mengapa titik asal $(0,0)$ pada koordinat citra berbeda dengan koordinat kartesian? Tuliskan rumus konversi dari $(m, n)$ ke $(x, y)$.**

Karena cara komputer menyimpan gambar berbeda dari cara matematika menulis grafik.
Gambar disimpan **baris demi baris dari atas** (kayak baca buku: kiri-kanan, lalu
turun satu baris), jadi baris 0 berada di paling atas — makin besar nomor baris,
makin ke bawah. Sedangkan koordinat kartesian dibuat untuk matematika: titik asal
di kiri bawah dan sumbu $y$ naik ke atas. Jadi cuma beda "arah baca", bukan beda isi
gambar.

Rumus konversinya:

$$x = n, \qquad y = (M - 1) - m$$

dan kebalikannya $m = (M-1) - y$, $n = x$. Cek di praktikum: $(m, n) = (20, 30)$
jadi $(x, y) = (30, 235)$, nilai pikselnya tetap 36.

**2. Mengapa ukuran citra untuk proses transformasi umumnya dipilih berupa pangkat 2?**

Alasannya praktis:

1. Banyak operasi gambar jalan dengan **membagi ukuran dengan 2 terus** — misalnya
   *resize* setengah ukuran, *pooling* 2x2 di CNN, atau blok 8x8 saat kompresi JPEG.
   Kalau ukurannya pangkat 2, hasilnya selalu bilangan bulat dan tak ada sisa piksel.
2. Algoritma transformasi yang populer (FFT, DCT) paling cepat dan paling mudah
   dihitung kalau panjang datanya pangkat 2.
3. File dan buffer di memori lebih rapi karena ukurannya selalu habis dibagi 2.

Bukti dari praktikum: crop 128 x 128 (2^7) dan resize 256 x 256 (2^8) langsung pas,
tanpa ada piksel yang terpotong ganjil.

**3. Hitung kebutuhan memori citra $512 \times 512$ piksel dengan 256 aras. Berapa kebutuhan memorinya bila hanya 16 aras?**

- 256 aras = 8 bit/piksel.
  $512 \times 512 \times 8 / 8 = 262.144$ byte = **256 KB**.
- 16 aras = 4 bit/piksel.
  $512 \times 512 \times 4 / 8 = 131.072$ byte = **128 KB**.

Jadi kalau arasnya dipangkas dari 256 ke 16, kebutuhan memori tinggal **setengahnya**
— tapi gambarnya juga makin kasar (ingat hasil Percobaan 4).

**4. Jelaskan perbedaan citra analog dan citra digital berdasarkan hasil Percobaan 4.**

- **Citra digital** isinya angka yang jumlahnya dibatasi (discrete). Di praktikum ini
  kita bisa bebas mengatur jumlah arasnya: 256, 64, 16, 4, bahkan 2. Begitu arasnya
  dikurangi, langsung kelihatan "tangga"-nya — gradasi yang tadinya halus pecah jadi
  bercak (efek poster), dan di L=2 tinggal hitam-putih. Artinya, citra digital cuma
  kumpulan angka; kualitasnya tergantung berapa bit yang kita sisakan.
- **Citra analog** (foto film, cetakan) menyimpan perubahan terang-gelap secara
  **lurus dan tak terputus-putus** — tidak ada piksel, tidak ada aras, jadi tidak
  bisa dibuat "kasar" seperti L=2. Konsekuensinya, analog tidak bisa langsung
  diolah komputer; harus dipindai dulu menjadi angka, dan proses memindai itulah
  yang namanya kuantisasi (menyamakan nilai terus-menerus ke sejumlah aras tetap).

**5. Tugas Mandiri: ganti citra dengan foto pilihan sendiri, ulangi Percobaan 1-4, lalu tuliskan perbedaan hasilnya.**

Foto kedua yang dipakai: `assets/ss/00_portal_utama.png` (1400 x 1100 piksel).
Log lengkapnya ada di `assets/ss/citra5_execution.png`.

![Tugas Mandiri - percobaan 1 dan 4 diulangi dengan foto berbeda](assets/ss/citra5_tugas_mandiri.png)

| Hal yang dibandingkan | `citra.jpg` (Percobaan 1-4) | Foto baru (Tugas Mandiri) |
| :--- | :--- | :--- |
| Ukuran $M \times N$ | 256 x 256 = 65.536 piksel | 1100 x 1400 = **1.540.000 piksel** (23,6x lebih banyak) |
| Intensitas min / maks | 1 / 254 | 0 / 255 (memenuhi rentang penuh) |
| Rata-rata terang | 110,37 (agak gelap) | 236,69 (lebih terang, banyak area putih) |
| Aras unik terpakai | 253 | 252 |
| $f(0, 0)$ / $f(M-1, N-1)$ | 11 / 147 | 255 / 246 |
| Konversi $(m,n)=(20,30)$ | $(x, y) = (30, 235)$, nilai 36 | $(x, y) = (30, 1079)$, nilai 102 |
| Ukuran awal pangkat 2? | Ya (256 x 256) | **Tidak** (1400 x 1100) → harus diresize ke 256 x 256 |
| Crop `f[50:178, 50:178]` | 128 x 128, isi wajah | 128 x 128, isi sudut halaman web |
| Aras unik saat $L=256/64/16/4/2$ | 253 / 64 / 16 / 4 / 2 | 252 / 64 / 16 / 4 / 2 |

**Perbedaan yang terasa:**

1. Angka-angka hasil Percobaan 1 dan 2 **pasti berbeda** karena isi fotonya beda —
   ukuran, rentang intensitas, nilai piksel di titik yang sama, dan histogramnya
   ikut berubah. Foto baru lebih terang (mean 236,69) dan lebih besar (1,54 juta piksel).
2. Di Percobaan 3, foto baru **tidak pangkat 2 sejak awal**, jadi langkah resize ke
   256 x 256 benar-benar diperlukan (kalau `citra.jpg` langkah itu terasa sia-sia
   karena ukurannya sudah pas).
3. Di Percobaan 4, hasil jumlah aras unik-nya **hampir sama** (253/64/16/4/2 vs
   252/64/16/4/2). Ini bukti kalau rumus kuantisasi tidak peduli isi foto — yang
   berubah cuma tampilannya.
4. Kesimpulan kecilnya: proses/rumusnya tetap, yang beda cuma data masukannya.

---

## G. Kesimpulan

1. Citra digital itu cuma larik angka $f(m, n)$: `citra.jpg` berukuran 256 x 256 =
   65.536 piksel, tipenya `uint8`, intensitasnya 1-254.
2. Titik asal citra ada di pojok kiri atas; konversinya $x = n$ dan $y = (M-1) - m$
   — dibuktikan dengan nilai piksel (20, 30) = 36 yang sama setelah dikonversi.
3. *Cropping* `f[50:178, 50:178]` menghasilkan 128 x 128 (pangkat 2) dan resize
   menghasilkan 256 x 256; ukuran pangkat 2 memudahkan operasi gambar berulang
   seperti *resize* dan kompresi.
4. Kuantisasi menunjukkan adanya trade-off: dari 64 KB (256 aras) turun ke 8 KB
   (2 aras), tapi tampilannya berubah dari halus menjadi hitam-putih — mulai rusak
   terlihat di 16 aras ke bawah.
5. Tugas mandiri membuktikan angka praktikum bergantung pada foto yang dipakai,
   sementara cara dan rumusnya tetap sama untuk foto mana pun.

---

## H. Penilaian

| No | Komponen | Bobot | Nilai |
| :-: | :--- | :---: | :---: |
| **1** | Percobaan 1-4 berjalan dan tabel data terisi lengkap | 40% | |
| **2** | Jawaban pertanyaan dan tugas | 30% | |
| **3** | Analisis dan kesimpulan | 20% | |
| **4** | Ketepatan waktu dan kerapian laporan | 10% | |
| | **Total** | **100%** | |

---

### Lampiran - Daftar Berkas Eksekusi

| Berkas | Isi |
| :--- | :--- |
| `assets/ss/citra0_setup_execution.png` | Log persiapan: versi Python/pustaka + info `citra.jpg` |
| `assets/ss/citra1_execution.png` | Log Percobaan 1 + `citra1_histogram.png` |
| `assets/ss/citra2_execution.png` | Log Percobaan 2 + `citra2_koordinat.png` |
| `assets/ss/citra3_execution.png` | Log Percobaan 3 + `citra3_crop_resize.png`, `citra3_hasil_crop.png`, `citra3_hasil_256.png` |
| `assets/ss/citra4_execution.png` | Log Percobaan 4 + `citra4_kuantisasi.png`, `citra4_memori.png`, `citra4_kuantisasi_{256,64,16,4,2}.png` |
| `assets/ss/citra5_execution.png` | Log Tugas Mandiri + `citra5_tugas_mandiri.png`, `citra5_hasil_crop2.png`, `citra5_hasil_256.png`, `citra5_kuantisasi_{16,4,2}.png` |
| `tugas/scripts/citra_jobsheet.py` | Sumber kode semua percobaan |
| `tugas/scripts/metrics.json` | Angka terukur yang dipakai untuk mengisi Tabel 1-3 |
