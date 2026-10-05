# I. TUJUAN PRAKTIKUM

Setelah menyelesaikan praktikum ini, mahasiswa diharapkan mampu:
1. Menjelaskan konsep dasar [Topik Praktikum].
2. Melakukan konfigurasi dan pengujian pada [Sistem/Aplikasi].
3. Menganalisis hasil temuan serta menyusun laporan bukti praktikum secara sistematis.


# II. DASAR TEORI

## 2.1 Pengenalan Topik
Tuliskan penjelasan teori singkat mengenai praktikum yang dilakukan di sini.

## 2.2 Alat dan Bahan
- **Sistem Operasi:** Kali Linux / Windows 11
- **Aplikasi / Tools:** Wireshark, Burp Suite, Terminal / PowerShell
- **Target:** `http://172.16.92.212:5007`


# III. LANGKAH KERJA DAN HASIL PRAKTIKUM

1. Melakukan pengujian awal (*Reconnaissance*) menggunakan perintah Nmap untuk mengidentifikasi port dan layanan yang terbuka pada server target.

   ![Scanning Nmap](assets/screenshot_01.png)

2. Mengakses halaman login portal pasien via browser dan mencoba autentikasi dengan kredensial akun demo.

   ![Halaman Login Portal](assets/screenshot_02.png)

3. Melakukan pengubahan parameter ID pasien pada URL (`/patient/1`) untuk menguji kerentanan Broken Access Control (IDOR).

   ![Eksploitasi IDOR Rekam Medis VIP](assets/screenshot_03.png)


# IV. PEMBAHASAN DAN ANALISIS

Jelaskan analisis dari hasil yang kamu dapatkan pada Bab III di sini. Apa kerentanannya, kenapa bisa terjadi, dan bagaimana solusinya.


# V. KESIMPULAN

Berdasarkan praktikum yang telah dilaksanakan, dapat disimpulkan bahwa:
1. Kesimpulan pertama mengenai hasil pengujian.
2. Kesimpulan kedua mengenai solusi atau mitigasi yang disarankan.