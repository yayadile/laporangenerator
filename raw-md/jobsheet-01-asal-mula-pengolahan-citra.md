# JOBSHEET 01: Asal Mula Pengolahan Citra
**Asal Mula Pengolahan Citra & Pengertian Pengolahan Citra Digital**

| Informasi Praktikum | Detail |
| :--- | :--- |
| **Mata Kuliah** | Pengolahan Citra Digital |
| **Topik / Bab** | Bab 1 – Pendahuluan Pengolahan Citra |
| **Sub Topik** | 1.1 Asal Mula Pengolahan Citra <br> 1.2 Pengertian Pengolahan Citra Digital |
| **Pertemuan Ke-** | 1 (satu) |
| **Alokasi Waktu** | 2 x 50 menit |
| **Nama / NIM** | Adinda Massa Merah Lawan Tirani / 3.34.24.2.01 |
| **Kelas / Tanggal** | IK-3C / 07 Oktober 2026 |

---

## A. Tujuan

Setelah menyelesaikan jobsheet ini, mahasiswa diharapkan mampu:

1. Menjelaskan sejarah awal pengolahan citra, mulai dari *Bartlane cable picture transmission* (1921) sampai lahirnya pengolahan citra digital berbasis komputer (awal 1960-an).
2. Membedakan citra yang dikirim tanpa komputer dengan citra hasil pengolahan citra digital yang benar-benar digital.
3. Menjelaskan pengertian citra menurut KBBI dan menurut kamus Webster.
4. Menemukan contoh citra dalam kehidupan sehari-hari dan memaknainya sebagai sebaran intensitas keabuan/warna.
5. Mengamati struktur piksel sebuah citra digital (ukuran, zoom, grayscale) memakai perangkat lunak pengolah citra.

---

## B. Dasar Teori (Ringkasan)

### 1.1 Asal Mula Pengolahan Citra

- **Tahun 1921** — Foto berhasil dikirim dari New York ke London lewat kabel bawah laut Atlantik. Sistemnya disebut *Bartlane cable picture transmission system* (Harry G. Bartholomew & Maynard D. McFarlane). Gambarnya cuma punya **5 tingkat keabuan**, dan waktu kirim turun dari beberapa minggu jadi **3 jam**.
- **Tahun 1929** — Pengkodean naik jadi **15 tingkat keabuan**, jadi gambarnya lebih halus. Tapi ini **belum** pengolahan citra digital karena belum ada komputer yang bekerja di dalamnya.
- **Awal 1960-an** — Komputer mulai cukup cepat dan memorinya cukup besar untuk menyimpan data gambar. Ditambah dorongan dari **program antariksa**, pengolahan citra digital berbasis komputer akhirnya lahir.
- **31 Juli 1964** — Wahana *Ranger 7* memotret Bulan. Citra permukaan Bulan yang tadinya berdistorsi diperbaiki memakai komputer. Inilah contoh nyata pengolahan citra digital.

### 1.2 Pengertian Pengolahan Citra Digital

- **Menurut KBBI:** *pengolahan* = proses mengusahakan sesuatu menjadi lain atau lebih sempurna; *citra* = rupa/gambar yang diperoleh melalui sistem visual.
- **Menurut kamus Webster:** citra adalah representasi, kemiripan, atau imitasi dari suatu objek.
- **Bentuk citra:** bisa foto, lukisan, coretan di kertas, atau tampilan layar monitor. Intinya semua itu adalah **sebaran variasi gelap-terang / redup-cerah / warna pada suatu bidang datar**, dan di komputer sebaran itu disimpan sebagai angka intensitas.

---

## C. Alat dan Bahan

| Komponen | Yang dipakai |
| :--- | :--- |
| **Komputer / OS** | Windows 10 Pro 64-bit |
| **Python** | 3.13.13 (`C:\Program Files\Python313\python.exe`) |
| **Pustaka** | Pillow 12.3.0, NumPy 2.4.4, Matplotlib 3.11.2 |
| **Editor / terminal** | VS Code + terminal |
| **File citra** | 5 foto di `assets/citra seharihari/` — semuanya 256 x 256 piksel, RGB, JPEG |
| **Script** | `tugas/scripts/asal_jobsheet.py` (persiapan + langkah D.1, D.2, D.3) |
| **Jobsheet & alat tulis** | jobsheet ini untuk mencatat hasil pengamatan |

Persiapan sudah beres — library terpasang dan kelima foto siap dipakai.

![Persiapan: cek library dan 5 file citra](assets/ss/asal0_setup_execution.png)

---

## D. Langkah Kerja

Semua langkah dijalankan lewat satu script: `python tugas/scripts/asal_jobsheet.py`.
Log tiap langkah disimpan sebagai tangkapan layar `assets/ss/asalN_execution.png`,
sedangkan hasil gambarnya disimpan sebagai PNG 200 DPI dengan awalan nama `asal`.

### D.1 Garis waktu pengolahan citra (diskusi kelompok)

Kode intinya: empat peristiwa disimpan sebagai list `(tahun, judul, keterangan)`, lalu digambar sebagai garis horizontal dengan kotak keterangan di atas dan di bawah garis.

```python
events = [
    ("1921", "Bartlane cable picture transmission",
     "Foto dikirim dari New York ke London lewat kabel laut Atlantik. ..."),
    ("1929", "Pengkodean naik ke 15 tingkat keabuan", "..."),
    ("Awal 1960-an", "Komputer cukup cepat dan muat memori", "..."),
    ("31 Juli 1964", "Ranger 7 memotret Bulan", "..."),
]
```

![Langkah D.1 - log eksekusi](assets/ss/asal1_execution.png)

Hasil: **4 peristiwa** (syarat minimal 4).

| No | Tahun | Peristiwa | Keterangan singkat |
| :-: | :--- | :--- | :--- |
| 1 | 1921 | *Bartlane cable picture transmission* | Foto New York → London lewat kabel laut, 5 tingkat keabuan, kirim 3 jam |
| 2 | 1929 | Pengkodean naik ke 15 tingkat keabuan | Gambar lebih halus, tapi belum ada komputer |
| 3 | Awal 1960-an | Komputer cepat + memori cukup | Didorong program antariksa, pengolahan citra digital lahir |
| 4 | 31 Juli 1964 | *Ranger 7* memotret Bulan | Citra Bulan yang berdistorsi diperbaiki komputer |

![Langkah D.1 - garis waktu pengolahan citra](assets/ss/asal1_timeline.png)

### D.2 Identifikasi bentuk citra di sekitar kita

Kode intinya: tiap foto dibuka, jumlah warna unik dihitung, lalu maknanya dipadukan dengan definisi KBBI dan Webster.

```python
im = Image.open(FOLDER / name).convert("RGB")
warna = len(np.unique(np.array(im).reshape(-1, 3), axis=0))
print(f"{name}: {warna} warna unik, objek = {KETERANGAN[name]}")
```

![Langkah D.2 - log eksekusi](assets/ss/asal2_execution.png)

| No | File | Objek asli | Versi Webster | Versi KBBI |
| :-: | :--- | :--- | :--- | :--- |
| 1 | `bebi.jpg` | kucing tidur | representasi/kemiripan kucing yang asli | gambar hasil sistem visual (jepretan kamera) |
| 2 | `belnder.jpg` | blender | representasi/kemiripan blender yang asli | gambar hasil sistem visual (jepretan kamera) |
| 3 | `laptop.jpg` | laptop | representasi/kemiripan laptop yang asli | gambar hasil sistem visual (jepretan kamera) |
| 4 | `selotip_listrik.jpg` | selotip listrik | representasi/kemiripan selotip yang asli | gambar hasil sistem visual (jepretan kamera) |
| 5 | `tas.jpg` | tas punggung | representasi/kemiripan tas yang asli | gambar hasil sistem visual (jepretan kamera) |

Kelima-limanya masuk definisi citra: hasil foto yang mirip dengan bendanya, tinggal sebaran warna di atas bidang datar.

![Langkah D.2 - 5 contoh citra sehari-hari](assets/ss/asal2_contoh_citra.png)

### D.3 Praktik pengamatan citra digital

Kode intinya:

```python
im = Image.open("laptop.jpg")          # 256 x 256, RGB
g = im.convert("L")                    # grayscale
print(im.size, len(np.unique(np.array(im).reshape(-1,3), axis=0)),
      len(np.unique(np.array(g))))     # ukuran, warna unik, tingkat keabuan

crop = im.crop((96, 96, 112, 112))     # potong 16 x 16 piksel
zoom = crop.resize((416, 416), Image.NEAREST)   # perbesar 26x biar kotak piksel kelihatan
```

**1) Ukuran dan jumlah warna kelima citra**

| File | Ukuran (piksel) | Jumlah piksel | Warna unik | Setelah grayscale |
| :--- | :---: | :---: | :---: | :--- |
| `bebi.jpg` | 256 x 256 | 65.536 | 15.117 | 169 tingkat keabuan (12–180) |
| `belnder.jpg` | 256 x 256 | 65.536 | 22.306 | 215 tingkat keabuan (7–233) |
| `laptop.jpg` | 256 x 256 | 65.536 | 22.714 | 253 tingkat keabuan (0–252) |
| `selotip_listrik.jpg` | 256 x 256 | 65.536 | 14.752 | 256 tingkat keabuan (0–255) |
| `tas.jpg` | 256 x 256 | 65.536 | 31.052 | 225 tingkat keabuan (0–226) |

**2) Zoom in sampai kotak piksel kelihatan**

Dipakai `laptop.jpg`, daerah (96, 96) seluas 16 x 16 piksel, diperbesar 26 kali dengan metode *nearest neighbor* (tiap piksel sengaja dibuat kotak besar, tidak dihaluskan). Kotak merah di gambar kiri menunjukkan area yang di-zoom.

![Langkah D.3 - zoom in sampai terlihat kotak-kotak piksel](assets/ss/asal3_zoom_pixel.png)

Angka nyata 1 piksel di area zoom (grayscale):

```
[[145 119 122 130]
 [170 136 128 128]
 [149 121 122 128]
 [127 108 115 117]]
```

**3) Citra warna vs grayscale**

![Langkah D.3 - laptop.jpg sebelum dan sesudah grayscale](assets/ss/asal3_grayscale.png)

![Langkah D.3 - 3 citra contoh: asli vs grayscale](assets/ss/asal3_tabel_grayscale.png)

![Langkah D.3 - log eksekusi lengkap (ukuran, zoom, grayscale)](assets/ss/asal3_execution.png)

### D.4 dan D.5 (diskusi & penyusunan laporan)

Hasil pengamatan dicatat ke Tabel Hasil Pengamatan (bagian E), jawaban soal evaluasi ditulis di bagian F,
lalu laporan disusun sesuai format bagian G dan dikumpulkan lewat LMS.

---

## E. Tabel Hasil Pengamatan

| No. | Nama File Citra | Ukuran (piksel) | Catatan Hasil Grayscale |
| :-: | :--- | :--- | :--- |
| **1** | `bebi.jpg` | 256 x 256 | Berubah jadi **169 tingkat keabuan** (rentang 12–180, rata-rata 84,0). Warna bulu oranye jadi abu-abu terang, lantai jadi abu gelap — pola tubuh tetap terbaca. |
| **2** | `laptop.jpg` | 256 x 256 | Berubah jadi **253 tingkat keabuan** (rentang 0–252, rata-rata 64,7). Layar biru dan suhu warna ruangan hilang, tapi teks kode di layar masih terbaca karena beda terang-gelapnya tetap ada. |
| **3** | `tas.jpg` | 256 x 256 | Berubah jadi **225 tingkat keabuan** (rentang 0–226, rata-rata 77,8). Motif semangka jadi bercak abu-abu, tas yang tadinya krem-merah jadi satu rona abu. |

**Tambahan (dua citra lain yang juga diamati):**

| No. | Nama File Citra | Ukuran (piksel) | Catatan Hasil Grayscale |
| :-: | :--- | :--- | :--- |
| 4 | `belnder.jpg` | 256 x 256 | 215 tingkat keabuan (7–233, rata-rata 60,8) — blender hijau jadi abu sedang. |
| 5 | `selotip_listrik.jpg` | 256 x 256 | 256 tingkat keabuan (0–255, rata-rata 66,9) — satu-satunya citra yang memakai rentang penuh 0–255. |

**Ringkasan pengamatan:**

- Kelima citra berukuran sama: **256 x 256 = 65.536 piksel**.
- Warna asli sangat banyak (14.752–31.052 warna unik), sesudah grayscale tinggal **169–256 tingkat keabuan**.
- Setelah di-zoom, satu piksel ternyata cuma **satu angka** (contoh 145, 119, 122, 130).

---

## F. Soal Evaluasi

**1. Mengapa foto yang dikirim lewat sistem *Bartlane cable picture transmission* tahun 1921 belum dapat dianggap sebagai hasil pengolahan citra digital?**

Karena di dalam sistem itu tidak ada komputer yang bekerja. Gambarnya dipecah menjadi garis-garis, tiap garis dikodekan jadi sinyal listrik (dulu cuma 5 tingkat keabuan), dikirim lewat kabel laut, lalu dicetak ulang di penerima. Prosesnya masih bersifat pemindahan dan pencetakan sinyal, bukan penghitungan data gambar oleh komputer. Syarat sebuah proses disebut pengolahan citra digital adalah **ada komputer yang membaca, mengubah, lalu menyimpan kembali data citra dalam bentuk angka** — hal itu baru ada di awal 1960-an.

**2. Sebutkan dua faktor yang mendorong lahirnya pengolahan citra digital berbasis komputer pada awal tahun 1960-an.**

1. **Komputer sudah cukup cepat dan memorinya cukup besar** untuk menampung data satu gambar (tiap piksel harus disimpan sebagai angka, jadi makin besar citra, makin besar memori yang dibutuhkan).
2. **Program antariksa** yang sangat bergantung pada citra — badan antariksa butuh foto permukaan planet dan Bulan yang bisa diperbaiki kualitasnya secara otomatis. Contohnya perbaikan citra *Ranger 7* pada 31 Juli 1964.

**3. Bandingkan pengertian citra menurut KBBI dan menurut kamus Webster. Apa persamaan dan perbedaannya?**

- **KBBI:** citra = rupa atau gambar yang diperoleh melalui sistem visual. Yang ditekankan adalah **cara memperolehnya**, yaitu lewat mata/sistem penglihatan.
- **Webster:** citra = representasi, kemiripan, atau imitasi dari suatu objek. Yang ditekankan adalah **hubungan dengan objek aslinya**.
- **Persamaan:** keduanya sepakat bahwa citra itu gambar/rupa dari sesuatu.
- **Perbedaan:** KBBI menjelaskan *dari mana gambarnya berasal* (sistem visual), sedangkan Webster menjelaskan *apa hubungan gambarnya dengan bendanya* (menyerupai/mewakili objek).

**4. Mengapa nilai informasi pada sebuah citra dikatakan bersifat subyektif? Berikan satu contoh dari pengalaman Anda sendiri.**

Karena yang menilai adalah manusia, bukan angka. Di dalam file, nilai setiap piksel sama persis untuk semua orang, tetapi manfaatnya bergantung pada apa yang sedang dicari orang tersebut. Contoh saya: foto `laptop.jpg` di bagian bawah agak gelap, buat saya yang hanya melihat sekilas fotonya "kurang jelas dan tidak informatif". Tapi begitu saya perhatikan layarnya, ternyata terlihat program yang sedang saya kerjakan — untuk saya foto itu justru sangat informatif. Foto yang sama bisa jadi tidak bermakna sama sekali bagi orang yang tidak tahu isi layarnya.

**5. Berdasarkan hasil praktik pada langkah D.3, jelaskan dengan kalimat sendiri apa yang dimaksud dengan citra sebagai "sebaran variasi intensitas keabuan/warna pada suatu bidang datar".**

Artinya, sebuah citra itu bukan gambar yang utuh dan "padat", melainkan **kumpulan kotak kecil (piksel) yang disusun rapi seperti tabel**, dan tiap kotak hanya berisi satu angka yang menyatakan seberapa terang atau seberapa berwarna titik itu. Hasil praktik membuktikannya: saat `laptop.jpg` diperbesar 26 kali, gambarnya pecah jadi kotak-kotak dan tiap kotak terbaca angkanya (145, 119, 122, 130, dan seterusnya). Saat dijadikan grayscale, 22.714 warna pada foto itu tinggal tersisa 253 tingkat keabuan, artinya warna-warna yang berbeda ternyata bisa disamakan jadi satu angka keabuan. Jadi citra = bidang datar berisi sebaran angka intensitas.

---

## G. Format Laporan

| No | Syarat laporan | Sudah dipenuhi |
| :-: | :--- | :-: |
| 1 | Halaman sampul: judul jobsheet, nama, NIM, kelas, tanggal | ✔ (tabel informasi di halaman awal) |
| 2 | Tabel Hasil Pengamatan (bagian E) + tangkapan layar citra asli, zoom-in, dan grayscale | ✔ (bagian E + gambar pada D.3) |
| 3 | Jawaban Soal Evaluasi (bagian F) ditulis lengkap dengan penjelasan | ✔ |
| 4 | Kesimpulan singkat (maksimal 1 paragraf) | ✔ (di bawah) |
| 5 | Dikumpulkan dalam format PDF lewat LMS yang ditentukan | Menyesuaikan tenggat pengajar |

**Kesimpulan singkat:**

Pengolahan citra digital tidak langsung lahir begitu ada kamera — ia tumbuh dari kebutuhan mengirim dan memperbaiki gambar: dimulai dari sistem Bartlane tahun 1921 yang hanya memakai 5 tingkat keabuan tanpa komputer, berkembang ke 15 tingkat pada 1929, lalu benar-benar menjadi digital pada awal 1960-an ketika komputer cukup cepat dan bantuan program antariksa muncul, yang puncaknya terlihat pada perbaikan citra Bulan dari wahana Ranger 7 tahun 1964. Dari praktik langsung terbukti bahwa definisi citra menurut KBBI dan Webster ada wujud nyatanya di komputer: kelima foto berukuran 256 x 256 piksel (65.536 piksel per foto) ternyata hanyalah sebaran angka, karena saat diperbesar satu piksel terbaca sebagai satu angka, dan saat diubah ke grayscale ribuan warna berubah menjadi hanya ratusan tingkat keabuan.

---

## H. Rubrik Penilaian

| Aspek Penilaian | Kriteria | Bobot | Nilai |
| :--- | :--- | :---: | :---: |
| **Ketepatan Konsep Sejarah** | Ketepatan garis waktu & penjelasan peristiwa Bartlane, Ranger 7, dan era komputer 1960-an | 25% | |
| **Ketepatan Pengertian Citra** | Ketepatan penjelasan definisi KBBI, Webster, dan contoh citra sehari-hari | 25% | |
| **Hasil Praktik Pengamatan** | Kelengkapan tabel pengamatan, tangkapan layar, dan hasil grayscale | 25% | |
| **Jawaban Soal Evaluasi** | Kelengkapan analisis dan ketepatan jawaban soal evaluasi | 15% | |
| **Kerapian & Ketepatan Waktu** | Format laporan sesuai ketentuan dan dikumpulkan tepat waktu | 10% | |
| | **Total** | **100%** | |

---

## JAWABAN

| Identitas Mahasiswa | Detail |
| :--- | :--- |
| **Nama Mahasiswa** | Adinda Massa Merah Lawan Tirani |
| **NIM** | 3.34.24.2.01 |
| **Program Studi & Kelas** | Teknik Informatika / IK-3C |
| **Tanggal Praktikum** | 07 Oktober 2026 |

**Catatan Pengajar:**
$$\text{}$$
$$\text{}$$

---

### Lampiran - Daftar Berkas Eksekusi

| Berkas | Isi |
| :--- | :--- |
| `assets/ss/asal0_setup_execution.png` | Log persiapan: versi Python/pustaka + info 5 file citra |
| `assets/ss/asal1_execution.png` | Log langkah D.1 (4 peristiwa + cek layout figure) |
| `assets/ss/asal1_timeline.png` | Garis waktu pengolahan citra |
| `assets/ss/asal2_execution.png` | Log langkah D.2 (5 contoh citra + jumlah warna unik) |
| `assets/ss/asal2_contoh_citra.png` | Montase 5 citra sehari-hari |
| `assets/ss/asal3_execution.png` | Log langkah D.3 (ukuran, zoom, grayscale kelima citra) |
| `assets/ss/asal3_zoom_pixel.png` | Zoom 26x area 16 x 16 piksel `laptop.jpg` |
| `assets/ss/asal3_grayscale.png` | `laptop.jpg` sebelum dan sesudah grayscale |
| `assets/ss/asal3_tabel_grayscale.png` | 3 citra contoh: asli vs grayscale |
| `tugas/scripts/asal_jobsheet.py` | Sumber kode seluruh langkah kerja |
| `tugas/scripts/metrics.json` | Angka terukur yang dipakai mengisi tabel |
