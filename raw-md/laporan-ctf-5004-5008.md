## I. TUJUAN PRAKTIKUM

Setelah menyelesaikan praktikum ini, mahasiswa diharapkan mampu:
1. Menjelaskan konsep dasar kerentanan pada OWASP Top 10 kategori *Broken Access Control*, mulai dari *parameter tampering*, kebocoran data di sisi klien, IDOR, hingga kelemahan penyimpanan kredensial.
2. Melakukan identifikasi dan eksploitasi nyata pada aplikasi web target melalui manipulasi parameter URL, inspeksi penyimpanan browser, pengubahan identifier, serta *cracking* hash password.
3. Menganalisis akar masalah dari setiap celah yang ditemukan serta menyusun rekomendasi mitigasi yang dapat diterapkan pada aplikasi produksi.


## II. DASAR TEORI

### 2.1 Broken Access Control

*Broken Access Control* adalah kelas kerentanan di mana aplikasi gagal membatasi apa yang boleh dilakukan pengguna terhadap resource. Dalam praktikum ini kita menyentuh empat wujudnya yang paling sering muncul di lapangan. *Parameter tampering* terjadi ketika aplikasi mengambil keputusan sensitif — misalnya menampilkan profil siapa — hanya berdasarkan nilai yang bebas diubah pengguna di URL. Kebocoran sisi klien terjadi ketika data rahasia disimpan di `localStorage`, `sessionStorage`, atau cookie yang bisa dibaca siapa saja dengan DevTools. IDOR sendiri adalah kasus klasik di mana nomor objek di URL dipercaya mentah tanpa dibandingkan dengan identitas pemilik sesi. Terakhir, penyimpanan password dalam bentuk hash yang lemah membuat aplikasi seolah terproteksi, padahal hash-nya sendiri bocor dan bisa dipecahkan dalam hitungan detik.

### 2.2 Hashing, MD5, dan Rainbow Table

Hash satu arah memang tidak bisa dibalik, tetapi karena MD5 sangat cepat dan tidak menggunakan *salt*, seluruh ruang kandidat kata umum sudah tercakup di *rainbow table* publik. Konsekuensinya, cukup dengan menempelkan hash ke layanan *lookup* atau menjalankan *wordlist* biasa, plaintext-nya langsung ketemu. Di praktikum ini kita membuktikan sendiri bahwa hash MD5 maupun SHA1 yang terekspos di komentar HTML aplikasi tidak memberikan perlindungan berarti.

### 2.3 Alat dan Bahan

- **Sistem Operasi:** Windows 11
- **Aplikasi / Tools:** Google Chrome (headless + Chrome DevTools Protocol), PowerShell `curl`, Python 3.13 (`hashlib`), `websocket-client`
- **Target:** `http://172.16.92.212:5000` (portal submit) dengan challenge pada port 5004 sampai 5008
- **Bukti visual:** seluruh tangkapan layar disimpan di folder `assets/ss/`


## III. LANGKAH KERJA DAN HASIL PRAKTIKUM

### 3.0 Tahap Reconnaissance Awal

Praktikum dimulai dari portal utama `http://172.16.92.212:5000/`, sebuah halaman submit flag bernama *Cybersafe CTF* yang juga berperan sebagai papan daftar challenge. Dari sidebar kanannya kita bisa membaca nama challenge beserta poin tiap port, sehingga tidak perlu menebak-nebak lagi targetnya. Tampilan portal beserta daftar challenge terekam pada tangkapan layar berikut.

![Portal Utama Cybersafe CTF](assets/ss/00_portal_utama.png)

Sebelum masuk ke tiap port, saya cek dulu kelayakan port 5000 sampai 5010 dengan `Test-NetConnection`. Hasilnya cukup mengejutkan: semua port merespons kecuali **5005** yang tidak mau menerima koneksi sama sekali. Kondisi ini kemudian saya dokumentasikan sebagai bahan analisis di sub-bab 3.1.

![Hasil Pemindaian Kelayakan Port](assets/ss/port_scan_5005.png)


### 3.1 Port 5004 — Social Media (Parameter Tampering)

Membuka `http://172.16.92.212:5004/` langsung dialihkan ke `/profile?view=user`. Halaman ini menampilkan profil bernama *John Doe* dengan label *Standard User* dan status "No special privileges". Kode sumbernya sendiri cukup blak-blakan: ada kalimat yang bilang sistem memutuskan profil apa yang tampil berdasarkan parameter URL, plus kotak hint hitam yang mengingatkan kita untuk mengutak-atik parameter di address bar dan menebak peran apa lagi yang mungkin ada.

![Profil Default view=user](assets/ss/5004_profile_user.png)

Dari situ saya coba mengganti nilai `view` dengan sederet kandidat peran: `admin`, `administrator`, `root`, `moderator`, `superuser`, `super`, `staff`, `editor`, dan `user`. Hanya `admin` yang menghasilkan halaman berbeda — yang lain tetap memantulkan profil John Doe. Perintah enumerasinya sederhana saja:

1. `curl -s "http://172.16.92.212:5004/profile?view=admin"`

Nilai `admin` membuka *Admin Dashboard* dengan badge **ADMINISTRATOR**, `Access Level: Full System`, dan di dalam kotak putih bercorak hitam tercetak flag-nya.

![Eksploitasi Parameter view=admin](assets/ss/5004_profile_admin.png)

Flag port 5004: `CYBERSAFE{p4r4m3t3r_t4mp3r1ng}`


### 3.2 Port 5005 — Cookie Monster (Tidak Dapat Diakses)

Saya mencoba port 5005 berulang kali sepanjang sesi praktikum ini, dari percobaan pertama sampai percobaan terakhir. Responsenya tidak pernah berubah: koneksi yang berputar-putar lalu *timeout* (`curl` exit code 28), dan pada beberapa percobaan malah langsung ditolak (`connection refused`, exit code 7). Pengecekan port dengan `Test-NetConnection` juga konsisten mengembalikan `TcpTestSucceeded = False`, sementara port di sekitarnya 5004, 5006, 5007, dan 5008 semuanya `True`.

![Halaman Gagal Muat Port 5005](assets/ss/5005_unreachable.png)

Karena challenge *cookie-monster* ini menuntut interaksi dengan cookie aplikasi, sementara layanannya sendiri tidak mau melayani permintaan apa pun, sub-bab ini saya tandai sebagai **skip** sesuai instruksi. Tidak ada payload yang bisa diuji, sehingga tidak ada flag yang bisa ditarik dari port ini. Temuan yang tetap bernilai di sini adalah adanya anomala availability: satu dari lima service pada rentang challenge tidak konsisten dalam menerima koneksi, yang sayang untuk dilewatkan begitu saja sebagai temuan sekunder.


### 3.3 Port 5006 — Secure Vault (Kebocoran LocalStorage)

Port 5006 menyajikan aplikasi bernama *Secure Vault* yang mengaku sebagai *password manager* pribadi dengan tagline "All secrets are stored safely in your browser". Di tengah halaman terdapat tiga entri kredensial — GitHub, AWS Console, dan Jira — lengkap dengan tombol *Copy*. Kotak hint berwarna kuning di bawahnya justru lebih jujur: ia menanyakan apakah kita sudah mengecek tab *Application* di developer tools.

![Halaman Secure Vault](assets/ss/5006_vault.png)

Membuka sumber halaman memperlihatkan blok `<script>` yang isinya langsung menaruh empat nilai ke `localStorage` browser. Untuk dokumentasi yang meyakinkan, saya tidak sekadar menyalin teksnya, melainkan membuka aplikasi lewat Chrome DevTools Protocol, membaca isi `localStorage` lewat `Runtime.evaluate`, lalu me-render hasilnya sebagai overlay di atas halaman asli sebelum tangkapan layar diambil.

1. `localStorage.getItem("session_id") = "sess_8f3a9b2c1d4e5f6a7b8c9d0e"`
2. `localStorage.getItem("github_token") = "ghp_xJ9kL2mN4pQr5StUv7WxYz"`
3. `localStorage.getItem("aws_access_key") = "AKIAIOSFODNN7EXAMPLE"`
4. `localStorage.getItem("vault_secret") = "CYBERSAFE{l0c4lst0r4g3_l34k}"`

![Inspeksi Isi LocalStorage di DevTools](assets/ss/5006_localstorage_leak.png)

Flag port 5006: `CYBERSAFE{l0c4lst0r4g3_l34k}`


### 3.4 Port 5007 — IDOR Hospital (Broken Access Control)

Sekali lagi dibuka, `http://172.16.92.212:5007/` langsung melempar ke `/login`, halaman *Patient Portal* milik *City General Hospital*. Beruntung, aplikasinya menampilkan sendiri akun demo di dalam kotak hint, jadi tidak perlu nebak-nebak kredensial.

![Halaman Login Patient Portal](assets/ss/5007_login.png)

Setelah login dengan `rofiq.fauzi` / `password123`, server mengirim cookie `session` berisi payload Base64 URL-safe. Dekodenya berbunyi `{"patient_id":105, "user":"rofiq.fauzi"}` — artinya identitas saya di mata server hanyalah angka `105`. Dashboard yang muncul menampilkan sederet menu cepat, dan di situ ada satu tombol yang mengarah ke `/patient/105`, yaitu rekam medis milik saya sendiri.

![Dashboard Setelah Autentikasi](assets/ss/5007_dashboard.png)

![Rekam Medis Milik Sendiri (ID 105)](assets/ss/5007_my_record.png)

Di sinilah dugaan IDOR mulai diuji. Kalau server hanya mempercayai angka di URL tanpa membandingkannya dengan isi session, seharusnya saya bisa membuka rekam medis orang lain cukup dengan mengganti angkanya. Saya enumerasi rentang ID dari 1 sampai 110 lewat loop PowerShell berikut:

```powershell
$s = New-Object Microsoft.PowerShell.Commands.WebRequestSession
Invoke-WebRequest "http://172.16.92.212:5007/login" -Method POST `
    -Body @{username="rofiq.fauzi";password="password123"} `
    -WebSession $s -UseBasicParsing -MaximumRedirection 0 | Out-Null

foreach ($i in 1..110) {
    $r = Invoke-WebRequest "http://172.16.92.212:5007/patient/$i" `
        -WebSession $s -UseBasicParsing
    if ($r.Content -match 'CYBERSAFE\{[^}]+\}') { "FLAG pada ID $i : $($matches[0])" }
}
```

Enumerasi itu berhenti tepat di `ID 1`. Halaman rekam medis milik *Dr. Richard Vane* terbuka lebar tanpa satu pun peringatan, lengkap dengan data pribadi, nomor asuransi, alamat rumah, sampai kontak darurat. Dan di bagian paling bawah, pada blok **Physician Notes**, flag-nya tertulis jelas di dalam kotak hijau.

![Eksploitasi IDOR pada Rekam Medis VIP](assets/ss/5007_idor_vip.png)

Flag port 5007: `CYBERSAFE{1d0r_h0sp1t4l_br34ch}`


### 3.5 Port 5008 — Secret Note (Cracking Hash)

Port terakhir menampilkan *Secret Note*, sebuah dokumen yang dikunci password. Kotak hint di halaman awal sudah memberi arah yang cukup jelas: kalau kita bisa menemukan hash-nya, maka *cracking tool* online tinggal meneruskan pekerjaannya.

![Halaman Terkunci Secret Note](assets/ss/5008_locked.png)

Petunjuk pertama ada di link `/hint`. Secara tampilan halaman itu hanya berisi pesan bahwa fitur *password reset* sudah dimatikan oleh administrator, tetapi di balik komentar HTML yang tidak tampil di browser tersembunyi jejak sistem: arsip log backup berisi dua nilai hash yang pernah disimpan sebelum fitur itu dimatikan, lengkap dengan anjuran untuk segera mengrotasi kredensial jika komentar ini pernah terekspos.

![Komentar HTML Tersembunyi pada Halaman Hint](assets/ss/5008_hint.png)

1. MD5: `0f6e4a1df0cf5ee97c2066953bed21b2`
2. SHA1: `e026e197bb77b12d16ab6986e068751f016d0ea5`

Langkah pertama saya adalah menguji kedua hash ini terhadap daftar kandidat password umum lewat Python `hashlib`, sekaligus melakukan brute force menyeluruh terhadap seluruh kombinasi digit 1 sampai 8 karakter dan huruf kecil 1 sampai 6 karakter. Total lebih dari 300 juta kandidat dicoba dan tidak ada yang cocok. Percobaan terhadap layanan *lookup* publik juga tidak membuahkan hasil, sebagian diblokir 403 dan sebagian tidak punya indeks untuk hash ini.

Karena jalur otomatis mentok, saya beralih ke pendekatan OSINT: mencari teks hash-nya langsung di mesin pencari. Ternyata hash MD5 tersebut adalah contoh yang berulang di dokumentasi Apache Guacamole, dan dari beberapa hasil muncul satu kandidat yang menjanjikan, yaitu `StrongPassword`. Saya verifikasi langsung:

```python
import hashlib
hashlib.md5(b"StrongPassword").hexdigest()   # 0f6e4a1df0cf5ee97c2066953bed21b2
hashlib.sha1(b"StrongPassword").hexdigest()  # e026e197bb77b12d16ab6986e068751f016d0ea5
```

Kedua hash cocok persis. Password itu kemudian dikirim lewat form:

```bash
curl -s -X POST -d "password=StrongPassword" http://172.16.92.212:5008/
```

Server merespons dengan halaman *Note Unlocked*, memperlihatkan isi surat dari Dr. Aris Thorne beserta flag-nya di kotak hijau.

![Secret Note Berhasil Dibuka](assets/ss/5008_unlocked.png)

Flag port 5008: `CYBERSAFE{s3cr3t_n0t3_cr4ck3d}`


## IV. PEMBAHASAN DAN ANALISIS

### 4.1 Port 5004 — Keputusan Aplikasi Berdasar Parameter yang Tidak Divalidasi

Akar masalahnya sangat sederhana namun berbahaya: aplikasi membiarkan parameter `view` menentukan objek profil apa yang dirender, tanpa memverifikasi apakah *caller*-nya berhak melihat objek tersebut. Server menganggap permintaan `view=admin` sama sahnya dengan `view=user`, sehingga seluruh data administrator menjadi publik. Dalam terminologi OWASP ini masuk kategori **A01:2021 – Broken Access Control**, lebih spesifiknya ke keluarga *parameter tampering*. Perbaikannya adalah memindahkan keputusan peran ke sisi server berdasarkan identitas terautentikasi, bukan membaca peran dari query string, dan menolak permintaan yang meminta objek di luar hak pengguna. Nilai `view` juga sebaiknya dipetakan ke enum yang di-whitelist sehingga nilai apa pun di luar daftar itu langsung ditolak, bukan ditampilkan sebagai fallback diam-diam.

### 4.2 Port 5005 — Anomala Ketersediaan Layanan

Dari sisi keamanan, port 5005 tidak memberi celah yang bisa dieksploitasi karena service-nya memang tidak melayani koneksi. Namun temuan ini tetap layak dicatat: dalam satu rangkaian challenge yang berdekatan, ada satu service yang jatuh tanpa pesan error yang jelas, dan dari sisi klien gejalanya bercampur antara *timeout* dan *connection refused*. Kombinasi gejala itu biasanya menandakan proses di balik port-nya memang mati atau firewall-nya memblokir trafik secara selektif, bukan sekadar aplikasi yang lambat. Sebagai catatan praktis, ketersediaan service adalah bagian dari postur keamanan juga; service yang mati tanpa monitoring berarti tidak ada yang tahu kapan ia gagal melayani pengguna.

### 4.3 Port 5006 — Data Rahasia Disimpan di Sisi Klien

Kerentanan di sini bukan pada enkripsi atau bug kriptografi, melainkan pada keputusan arsitektur: aplikasi menaruh token GitHub, kunci akses AWS, dan flag langsung di `localStorage` pada saat halaman dimuat. `localStorage` itu sendiri bersifat *persistent*, terikat per-origin, dan bisa dibaca oleh setiap skrip yang berjalan di origin tersebut — termasuk skrip injeksi XSS pihak ketiga. Tagline "stored safely in your browser" justru menggambarkan masalahnya dengan tepat: yang disimpan aman dari jaringan, tetapi terbuka lebar bagi siapa pun yang bisa menjalankan kode di browser korban atau bagi siapa pun yang sekadar membuka DevTools. Untuk data ses sensitif ini sebaiknya disimpan di sisi server dalam sesi berumur pendek, atau paling tidak dienkripsi dengan kunci yang tidak ikut disimpan di tempat yang sama. Token dan kunci akses juga sebaiknya dibuat *short-lived* dan mudah dicabut.

### 4.4 Port 5007 — Otorisasi Tidak Pernah Diperiksa di Server

Session cookie secara jelas menyimpan `patient_id` bernilai `105`, tetapi route `/patient/<int:pid>` tidak pernah membandingkan `pid` dari URL dengan angka di session. Server hanya memastikan bahwa pengguna sudah login, lalu langsung menyerahkan objek sesuai permintaan. Ini pola IDOR yang paling umum: autentikasi benar, otorisasi hilang. dampaknya bukan sekadar bocornya satu rekam medis, melainkan seluruh basis data pasien dapat diurutkan satu per satu hanya dengan mengganti angka. Perbaikannya harus dilakukan di server dengan membandingkan kepemilikan objek terhadap identitas sesi sebelum render, memakai identifier acak seperti UUIDv4 agar ID tidak lagi bisa ditebak, serta menerapkan *deny by default* pada setiap endpoint yang menyentuh data pribadi.

### 4.5 Port 5008 — Hash yang Bocor dan Algoritma yang Rapuh

Aplikasi menyimpan password dalam bentuk MD5 dan SHA1, lalu — ironisnya — menaruh kedua hash itu di komentar HTML yang bisa dibaca siapa pun yang membuka sumber halaman. Dari titik itu rantai exploitasinya tinggal satu langkah: cari plaintext-nya. Karena MD5 tidak menggunakan salt dan sangat cepat, nilai `0f6e4a1df0cf5ee97c2066953bed21b2` sudah tercakup di berbagai basis data hash publik, sehingga cukup dengan pencarian teks hash di mesin pencari pun plaintext-nya ketemu. Meski brute force murni dengan 300 juta kandidat tidak menemukan apa-apa, jalur OSINT langsung membawa kita ke `StrongPassword`. Pelajarannya ganda: hash password tidak boleh pernah disertakan dalam artefak yang bisa dibaca pengguna, dan password seperti `StrongPassword` sendiri sudah pasti jatuh di ranjau *dictionary attack*. Untuk penyimpanan password seharusnya dipakai algoritma yang sengaja lambat dan bersalt seperti bcrypt, scrypt, atau Argon2, dan *code review* wajib memeriksa komentar HTML yang ikut ter-deploy ke produksi.

### 4.6 Rekapitulasi Flag

| Port | Nama Challenge | Kerentanan | Flag |
|------|----------------|------------|------|
| 5004 | Social Media | Parameter Tampering | `CYBERSAFE{p4r4m3t3r_t4mp3r1ng}` |
| 5005 | Cookie Monster | Service tidak tersedia | *(dilewati)* |
| 5006 | Secure Vault | Kebocoran LocalStorage | `CYBERSAFE{l0c4lst0r4g3_l34k}` |
| 5007 | IDOR Hospital | IDOR / Broken Access Control | `CYBERSAFE{1d0r_h0sp1t4l_br34ch}` |
| 5008 | Secret Note | Kebocoran & cracking hash password | `CYBERSAFE{s3cr3t_n0t3_cr4ck3d}` |


## V. KESIMPULAN

Berdasarkan praktikum pengujian keamanan yang telah dilaksanakan pada rentang port 5004 sampai 5008, dapat disimpulkan bahwa:

1. Empat dari lima challenge berhasil dikuasai dan menghasilkan flag, yaitu port 5004, 5006, 5007, dan 5008, sementara port 5005 tidak dapat diakses sama sekali sehingga dilewati sesuai instruksi.
2. Pola kerentanan yang muncul sangat beragam namun semuanya bermuara pada satu akar masalah yang sama: aplikasi terlalu mempercayai input dari pengguna. Baik parameter `view` di URL, isi `localStorage`, angka `pid`, maupun hash yang ditaruh di komentar HTML, semuanya diperlakukan sebagai data yang sah tanpa verifikasi.
3. Flag `CYBERSAFE{p4r4m3t3r_t4mp3r1ng}` diperoleh hanya dengan mengganti satu nilai parameter, `CYBERSAFE{l0c4lst0r4g3_l34k}` dari sekadar membuka DevTools, `CYBERSAFE{1d0r_h0sp1t4l_br34ch}` dari pengubahan angka ID, dan `CYBERSAFE{s3cr3t_n0t3_cr4ck3d}` dari hash yang terekspos di komentar HTML.
4. Mitigasi yang disarankan untuk seluruh temuan adalah konsisten: lakukan seluruh pemeriksaan otorisasi di sisi server, jangan pernah menyimpan rahasia di penyimpanan yang bisa dibaca klien, hindari identifier numerik yang bisa ditebak, gunakan algoritma hashing password yang tahan brute force, dan pastikan tidak ada artefak sensitif yang ikut terkirim dalam kode sumber halaman.
