# JOBSHEET 01: 1.1 Asal Mula Pengolahan Citra
**Asal Mula Pengolahan Citra & Pengertian Pengolahan Citra Digital**

| Informasi Praktikum | Detail |
| :--- | :--- |
| **Mata Kuliah** | Pengolahan Citra Digital |
| **Topik / Bab** | Bab 1 – Pendahuluan Pengolahan Citra |
| **Sub Topik** | 1.1 Asal Mula Pengolahan Citra <br> 1.2 Pengertian Pengolahan Citra Digital |
| **Pertemuan Ke-** | 1 (satu) |
| **Alokasi Waktu** | 2 x 50 menit (1 sks teori + orientasi praktik) |
| **Program Studi** | Teknik Informatika / Ilmu Komputer |

---

## A. Capaian Pembelajaran / Tujuan
Setelah menyelesaikan jobsheet ini, mahasiswa diharapkan mampu:
1. Menjelaskan sejarah awal mula pengolahan citra, termasuk sistem *Bartlane cable picture transmission* (1921) dan peran program antariksa pada lahirnya pengolahan citra digital berbasis komputer (tahun 1960-an).
2. Membedakan citra digital yang dihasilkan tanpa komputer dengan citra hasil pengolahan citra digital yang sesungguhnya.
3. Menjelaskan pengertian pengolahan citra digital menurut KBBI dan makna citra menurut kamus Webster.
4. Mengidentifikasi bentuk-bentuk citra dalam kehidupan sehari-hari dan merepresentasikannya sebagai sebaran intensitas keabuan/warna.
5. Mendemonstrasikan pengamatan sederhana terhadap struktur piksel sebuah citra digital menggunakan perangkat lunak pengolah citra.

---

## B. Dasar Teori (Ringkasan)

### 1.1 Asal Mula Pengolahan Citra
- **Tahun 1921:** Keberhasilan pengiriman foto secara digital dari New York ke London melalui kabel bawah laut Atlantik — dikenal sebagai *Bartlane cable picture transmission system* (Harry G. Bartholomew & Maynard D. McFarlane). Waktu kirim berkurang dari beberapa minggu menjadi 3 jam.
- **Perkembangan Pengkodean:** Kemampuan pengkodean berkembang dari 5 tingkat keabuan (1921) menjadi 15 tingkat keabuan (1929). Namun proses ini belum tergolong pengolahan citra digital karena tidak melibatkan komputer.
- **Awal 1960-an:** Komputer mulai memiliki kecepatan proses dan kapasitas memori yang memadai, didorong oleh program antariksa, sehingga lahir pengolahan citra digital yang sesungguhnya — contohnya perbaikan distorsi citra permukaan Bulan hasil pemotretan Ranger 7 (31 Juli 1964).

### 1.2 Pengertian Pengolahan Citra Digital
- **Menurut KBBI:** Pengolahan adalah proses mengusahakan sesuatu menjadi lain atau lebih sempurna; citra berarti rupa/gambar yang diperoleh melalui sistem visual.
- **Menurut Kamus Webster:** Citra adalah representasi, kemiripan, atau imitasi dari suatu objek.
- **Representasi Citra:** Citra dapat berupa hasil fotografi, lukisan, corat-coret di kertas/kanvas, atau tampilan di layar monitor — yaitu sebaran variasi gelap-terang, redup-cerah, dan/atau warna-warni pada suatu bidang datar yang direpresentasikan dalam bentuk angka intensitas.

---

## C. Alat dan Bahan
- Komputer / laptop dengan sistem operasi Windows, macOS, atau Linux.
- Perangkat lunak pengolah citra: Python 3 (pustaka NumPy, OpenCV/Pillow, Matplotlib) atau alternatif seperti MATLAB / GIMP.
- Minimal 3 (tiga) buah citra digital contoh (format `.jpg`/`.png`) — boleh hasil jepretan sendiri, dengan objek berbeda-beda (misalnya wajah, benda, dan pemandangan).
- Lembar kerja (jobsheet) ini dan alat tulis untuk mencatat hasil pengamatan.

---

## D. Langkah Kerja
1. **Diskusi Kelompok (10 menit):** Bacalah kembali ringkasan sejarah pada bagian B, lalu buatlah garis waktu (*timeline*) singkat yang memuat minimal 4 peristiwa penting perkembangan pengolahan citra beserta tahunnya.
2. **Identifikasi Bentuk Citra (10 menit):** Amati lingkungan sekitar Anda dan catat 5 contoh benda/peristiwa yang dapat disebut sebagai “citra” sesuai definisi KBBI maupun Webster, lalu jelaskan representasi/kemiripannya terhadap objek aslinya.
3. **Praktik Pengamatan Citra Digital (20 menit):** Buka salah satu citra contoh menggunakan perangkat lunak yang tersedia, lalu:
   - Amati dan catat ukuran citra (lebar $\times$ tinggi dalam piksel);
   - Perbesar (*zoom in*) salah satu bagian citra hingga terlihat kotak-kotak piksel, lalu ambil tangkapan layarnya;
   - Ubah citra berwarna tersebut menjadi citra keabuan (*grayscale*) menggunakan menu/fungsi yang tersedia, lalu bandingkan tampilannya dengan citra asli.
4. Diskusikan hasil pengamatan dengan rekan sekelompok, lalu isi Tabel Hasil Pengamatan dan jawab Soal Evaluasi pada bagian E dan F.
5. Susun laporan sesuai format pada bagian G, kemudian kumpulkan sesuai tenggat waktu yang ditentukan pengajar.

---

## E. Tabel Hasil Pengamatan

| No. | Nama File Citra | Ukuran (piksel) | Catatan Hasil Grayscale |
| :-: | :--- | :--- | :--- |
| **1** | | | |
| **2** | | | |
| **3** | | | |

---

## F. Soal Evaluasi
1. Jelaskan mengapa foto yang dikirimkan melalui sistem *Bartlane cable picture transmission* pada tahun 1921 belum dapat dianggap sebagai hasil pengolahan citra digital.
2. Sebutkan dua faktor yang mendorong lahirnya pengolahan citra digital berbasis komputer pada awal tahun 1960-an.
3. Bandingkan pengertian citra menurut KBBI dan menurut kamus Webster. Apa persamaan dan perbedaan maknanya?
4. Mengapa nilai informasi pada sebuah citra dikatakan bersifat subyektif? Berikan satu contoh dari pengalaman Anda sendiri.
5. Berdasarkan hasil praktik pada langkah D.3, jelaskan dengan kalimat sendiri apa yang dimaksud dengan citra sebagai “sebaran variasi intensitas keabuan/warna pada suatu bidang datar”.

---

## G. Format Laporan
1. **Halaman Sampul:** Judul jobsheet, nama, NIM, kelas, dan tanggal praktikum di halaman terakhir dari jobsheet ini.
2. **Tabel Hasil Pengamatan (bagian E)** beserta tangkapan layar citra asli, citra *zoom-in*, dan citra *grayscale*.
3. **Jawaban Soal Evaluasi (bagian F)** ditulis lengkap dengan penjelasan, bukan hanya jawaban singkat.
4. **Kesimpulan Singkat** (maksimal 1 paragraf) mengenai apa yang dipelajari dari jobsheet ini.
5. Laporan dikumpulkan dalam format PDF melalui platform/LMS yang ditentukan pengajar.

---

## H. Rubrik Penilaian

| Aspek Penilaian | Kriteria | Bobot |
| :--- | :--- | :---: |
| **Ketepatan Konsep Sejarah** | Ketepatan *timeline* & penjelasan peristiwa Bartlane, Ranger 7, dan era komputer 1960-an | 25% |
| **Ketepatan Pengertian Citra** | Ketepatan penjelasan definisi KBBI, Webster, dan contoh citra sehari-hari | 25% |
| **Hasil Praktik Pengamatan** | Kelengkapan tabel pengamatan, tangkapan layar, dan hasil *grayscale* | 25% |
| **Jawaban Soal Evaluasi** | Kedalaman analisis dan ketepatan jawaban soal evaluasi | 15% |
| **Kerapian & Ketepatan Waktu** | Format laporan sesuai ketentuan dan dikumpulkan tepat waktu | 10% |

---

## JAWABAN

| Identitas Mahasiswa | Detail |
| :--- | :--- |
| **Nama Mahasiswa** | |
| **NIM** | |
| **Program Studi & Kelas** | |

**Catatan Pengajar:**
$$\text{}$$
$$\text{}$$