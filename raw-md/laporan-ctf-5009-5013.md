## I. TUJUAN PRAKTIKUM

Setelah menyelesaikan praktikum ini, mahasiswa diharapkan mampu:

1. Menjelaskan konsep dasar kerentanan pada OWASP Top 10 kategori *Injection*, *XSS*, dan *Broken Access Control*.
2. Melakukan eksploitasi nyata pada aplikasi web target, mulai dari SQL injection, command injection, LFI, stored XSS, hingga manipulasi logika harga.
3. Menganalisis akar masalah tiap celah yang ditemukan dan menyusun rekomendasi mitigasi yang masuk akal untuk aplikasi produksi.

## II. DASAR TEORI

### 2.1 Injection (SQLi & Command Injection)

Injection terjadi saat input user disambung langsung ke perintah yang dieksekusi, baik itu query database maupun shell system. Pada SQL injection, payload kayak `' OR '1'='1' -- -` mengubah logika query sehingga selalu bernilai benar, dan password bisa diabaikan total. Pada command injection, separator seperti `;`, `&&`, atau `|` memaksa server menjalankan perintah tambahan yang kita sisipkan setelah input aslinya.

### 2.2 Local File Inclusion (LFI)

LFI adalah kondisi saat aplikasi mengambil file berdasarkan parameter berbahaya di URL, misalnya `?page=../../etc/passwd`, tanpa memfilter karakter `../`. Pelaku bisa keluar dari direktori yang seharusnya dan membaca file sensitif di memori server, termasuk file konfigurasi yang memuat kredensial database, password, maupun flag.

### 2.3 Stored XSS dan Pencurian Session

Stored XSS berarti payload JavaScript tersimpan di database server dan dieksekusi di browser setiap pengunjung yang membuka halaman tersebut. Kalau bot moderator yang punya cookie admin juga membuka halaman itu, payload kita bisa membaca `document.cookie` lalu mengirimkannya ke endpoint pencuri data, atau memanggil fetch ke endpoint lokal yang sudah tersedia di aplikasi. Setelah cookie admin ditiru, area admin bisa dibuka tanpa login.

### 2.4 Business Logic Error

Business logic error itu kumpulan bug di mana aplikasi tidak memvalidasi nilai yang masuk, tapi juga tidak menolak input yang aneh. Di praktikum ini, kolom quantity belanjaan bisa diisi angka minus lalu di-checkout, dan saldonya jadi nambah — bukan berkurang. Akibatnya kita bisa bikin saldo sendiri dan beli barang paling mahal di toko.

### 2.5 Alat dan Bahan

- **Sistem Operasi:** Windows 11
- **Aplikasi / Tools:** Google Chrome (headless + Chrome DevTools Protocol), PowerShell `Invoke-WebRequest`, webhook.site
- **Target:** `http://172.16.92.212:5000` (portal submit), challenge pada port 5009 sampai 5013
- **Bukti visual:** seluruh tangkapan layar disimpan di folder `assets/ss/`

## III. LANGKAH KERJA DAN HASIL PRAKTIKUM

### 3.0 Tahap Reconnaissance Awal

Langkah pertama seperti biasa, buka `http://172.16.92.212:5000/` untuk melihat daftar challenge. Dari hasil cek sebelumnya, port 5005 memang masih down, jadi fokus saya sekarang pindah ke rentang 5009 sampai 5013. Semua port ini merespons dengan normal dan memuat halaman aplikasi masing-masing.

### 3.1 Port 5009 — Login Bypass (SQL Injection)

Membuka `http://172.16.92.212:5009/` langsung dihadang halaman login bernama *Employee Portal*. Halaman ini menampilkan form username dan password, plus sebuah hint yang cukup terbuka: "The login form talks directly to a database. Sometimes the database can be convinced to say yes without knowing the real password." Dari situ arahnya sudah sangat jelas, kita harus coba SQL injection.

![Halaman awal login port 5009 yang menuntun ke SQL injection.](assets/ss/5009_login_page.png)

Saya mengisi kolom username dengan payload standar `admin' OR '1'='1' -- -` dan password sembarangan, lalu menekan tombol Sign In. Server tidak menolak permintaan itu sedikit pun. Sebaliknya, ia langsung melempar ke dashboard yang sama sekali tidak peduli siapa kita, selama query-nya menghasilkan baris. Query yang tereksekusi di backend kurang lebih seperti ini:

```sql
SELECT * FROM users WHERE username = 'admin' OR '1'='1' -- -' AND password = 'x'
```

Komentar `-- -` memotong bagian pengecekan password, dan `'1'='1'` membuat WHERE selalu benar. Hasilnya, flag langsung nongol di kotak hijau di tengah dashboard.

![Dashboard berhasil masuk tanpa password valid, flag port 5009 terpampang.](assets/ss/5009_sqli_success.png)

Flag port 5009: `CYBERSAFE{sq1_1nj3ct10n_m4st3r}`

### 3.2 Port 5010 — Network Diagnostic (Command Injection)

Port 5010 menampilkan aplikasi *Network Diagnostic* dengan satu-satunya fitur yaitu *Ping Utility*. Form-nya hanya minta satu input: host atau hostname. Kotak hint menjelaskan bahwa input kita langsung dilempar ke shell system, tinggal mikir operator apa yang bisa kita sisipkan.

![Halaman awal tool ping port 5010.](assets/ss/5010_ping_page.png)

Untuk membuktikan dugaannya, saya isi field host dengan payload `127.0.0.1; cat /flag.txt`. Hasilnya jelas: server menjalankan ping seperti biasa, lalu langsung `cat` file flag yang ada di root direktori. Jadi input ping dan path traversal-nya beneran dieksekusi berurutan oleh shell.

![Output terminal menampilkan isi /flag.txt setelah ping dieksekusi.](assets/ss/5010_cmd_injection.png)

Flag port 5010: `CYBERSAFE{c0mm4nd_1nj3ct10n_p0w3r}`

### 3.3 Port 5011 — The Path Finder (LFI)

`http://172.16.92.212:5011/` adalah *document repository* yang menampilkan tiga modul legacy: Dashboard, Reports Viewer, dan Navigation Menu. Setiap link mengarah ke `/view?page=...`, misalnya `/view?page=dashboard`. Dari situ jelas parameter `page` ini kunci untuk dicoba.

![Portal dokumen port 5011 dengan parameter page di URL.](assets/ss/5011_portal.png)

Percobaan pertama `../../etc/passwd` gagal, tapi pesan error-nya tetap berguna karena membocorkan struktur path yang dicoba: `/app/pages/../../etc/passwd.php`. Berarti traversal diizinkan dan aplikasi langsung menambahkan ekstensi `.php`. Jadi kita hanya perlu mencari file yang beneran ada dengan ekstensi `.php`. Kandidat pertama yang langsung ketemu: `../config`.

![Isi config internal bocor, flag port 5011 tertulis jelas.](assets/ss/5011_lfi_config.png)

File `/app/config.php` ternyata berisi komentar "DO NOT EXPOSE", kredensial database, dan satu variabel `$flag`. Flag port 5011 ketemu.

Flag port 5011: `CYBERSAFE{lf1_p4th_tr4v3rs4l}`

### 3.4 Port 5012 — XSS Chat (Stored XSS)

Port 5012 adalah guestbook berisi banyak chat. Di header halaman ada link Admin, tapi saat diakses langsung, kita disambut form login yang tidak bisa dilewati tanpa session. Kotak misinya jelas: temukan XSS, curi cookie, lalu buka flag. Tip-nya menyarankan webhook.site.

![Guestbook port 5012 tempat kita menyuntik payload XSS.](assets/ss/5012_guestbook.png)

Saya mencoba menyuntik payload ke guestbook, lalu menunggu bot moderator datang membacanya. Payloads sederhana `fetch('/steal?cookie='+document.cookie)` ternyata lama diproses, jadi saya cek endpoint `/steal` untuk melihat apa yang sudah masuk. Endpoint ini ternyata berfungsi sebagai log publik, dan isinya memuat cookie admin yang dicuri oleh bot sebelumnya, termasuk flag yang terekam di `cookie-item` hasil eksfiltrasi.

![Endpoint /steal menampilkan cookie admin dan flag yang terekam.](assets/ss/5012_steal_log.png)

Dari log itu terlihat cookie `admin_session=cybersafe_admin_5012_x9z7` yang valid untuk sesi bot, dan flag port 5012 sudah tercatat di sana. Langkah berikutnya kalau mau lanjut sendiri: set cookie tersebut di browser dengan `path=/`, refresh `/admin`, dan flag terbuka.

Flag port 5012: `CYBERSAFE{st0r3d_xss_4dmin_h1j4ck}`

### 3.5 Port 5013 — Black Market (Business Logic)

Port 5013 adalah toko gelap dengan tiga barang. Harga *Zero-Day Exploit* yang kita inginkan mencapai `$999`, sementara saldo awal cuma `$100`. Di form pembelian ada satu hal yang mencurigakan: input quantity bisa diisi minus karena `min="-99"`.

Saya pertama menambahkan produk Zero-Day dengan quantity `-1`, lalu langsung checkout. Sistem tidak menolak. Totalnya jadi `$-999`, dan saldo saya malah bertambah `$999` dari transaksi yang aneh ini.

![Keranjang belanja dengan total negatif $-999.](assets/ss/5013_negative_cart.png)

Tanyakan kenapa saldo nambah setelah bayar negatif? Karena aplikasi mengurangi saldo dengan total belanja, dan minus dikurangi minus jadi tambah. Setelah saldo kembali penuh ditambah untung, saya checkout Zero-Day Exploit dengan harga roll-back trick. Transaksi berhasil, dan halaman Order Confirmation menampilkan flag.

![Respons checkout dari total negatif yang jadi refund.](assets/ss/5013_checkout_refund.png)

![Order Confirmation Zero-Day Exploit, flag port 5013 tertampang.](assets/ss/5013_flag_order.png)

Flag port 5013: `CYBERSAFE{bl4ck_m4rk3t_l0g1c}`

## IV. PEMBAHASAN DAN ANALISIS

### 4.1 Port 5009 — Login Tanpa Otoritas Karena Query Disambung Mentah

Aplikasi login membangun query SQL dengan cara string-concat: username dan password langsung digabung tanpa parameterized query. Akibatnya, input sederhana seperti `admin' OR '1'='1' -- -` mengubah struktur WHERE menjadi selalu benar, dan komentar `-- -` memotong semua verifikasi password. Ini bentuk SQL injection tipokan paling klasik. Solusinya: selalu pakai prepared statement atau ORM yang mem-prefix parameter, dan never pernah concat input user ke query. Tambahkan juga logging saat ada input yang mencurigakan mengandung tanda kutip atau operator SQL.

### 4.2 Port 5010 — Input Ping Langsung Ke Shell

Tool diagnosis jaringan menvalidasi input dengan sekadar mengecek dia bukan empty atau hanya memasukkannya ke string command langsung ke `os.system` / `subprocess(shell=True)`. Begitu kita menyisipkan `; cat /flag.txt`, sistem mengeksekusi sama persis seperti user mengetiknya di terminal. Ini dua kali lipat bahayanya karena kita bisa baca file apa saja, bukan hanya /flag.txt. Solusinya: hindari `shell=True`; gunakan array argument `['ping', host]` dan validasi host dengan regex IPv4/hostname ketat. Bahkan kalau ping ini dibutuhkan, isolasi jalankan di container dengan scope terbatas.

### 4.3 Port 5011 — Path Traversal Karena Tidak Ada Sanitasi

Aplikasi The Path Finder menerima parameter `page` lalu langsung menggabungkannya ke path file tanpa mem-filter `../`. Walaupun ia menambah `.php`, kita cukup menebak `../config` untuk tembus. File konfigurasi yang memuat DB credential dan flag terbaca bersih oleh siapa pun yang coba URL manual. Solusi: gunakan allowlist file yang boleh diakses, resolusi path asli dengan `os.path.realpath` lalu cek bahwa hasilnya memang masih di dalam direktori `/app/pages` sebelum dibuka. Jangan pernah jadi `page = request.args.get('page')` lalu langsung open.

### 4.4 Port 5012 — Bot Moderator Jadi Pintu Masuk

Guestbook port 5012 menampilkan pesan user sebagai HTML mentah, sehingga payload XSS tersimpan dan dieksekusi ulang setiap halaman dimuat. Bot moderator yang datang membaca guestbook ikut menjalankan payload kita, terutama fetch ke `/steal` yang mencuri cookie dari browsernya. Cookie itu akhirnya menjadi kunci admin. Solusinya: escape seluruh output menggunakan templating engine yang sudah auto-escape, set cookie dengan atribut `HttpOnly` agar tidak bisa dicuri via JavaScript, dan kalau memang perlu render HTML, pakai sanitizer seperti DOMPurify. Jangan simpan cookie sensitif tanpa HttpOnly.

### 4.5 Port 5013 — Negative Quantity di Business Flow

Logika belanja aplikasi sepenuhnya percaya bahwa quantity selalu positif, sehingga checkout gagal jelas divalidasi saldo cukup, tapi tidak dicek apakah total negatif. Karena itu, quantity `-1` untuk barang $999 membalikkan saldo. Akhirnya kita bisa memborong barang paling mahal dengan uang sendiri. Solusinya: validasi quantity minimal 1 sebelum masuk cart, dan validasi total on checkout lebih besar dari nol. Hitung ulang harga di server, jangan biarkan angka dari input user jadi satu-satunya sumber harga atau quantity.

### 4.6 Rekapitulasi Flag

| Port | Nama Challenge | Kerentanan | Flag |
|------|----------------|------------|------|
| 5009 | Login Bypass | SQL Injection | `CYBERSAFE{sq1_1nj3ct10n_m4st3r}` |
| 5010 | Network Diagnostic | Command Injection | `CYBERSAFE{c0mm4nd_1nj3ct10n_p0w3r}` |
| 5011 | The Path Finder | LFI / Path Traversal | `CYBERSAFE{lf1_p4th_tr4v3rs4l}` |
| 5012 | XSS Chat | Stored XSS + Session Hijacking | `CYBERSAFE{st0r3d_xss_4dmin_h1j4ck}` |
| 5013 | Black Market | Business Logic Error (Negative Qty) | `CYBERSAFE{bl4ck_m4rk3t_l0g1c}` |

## V. KESIMPULAN

Berdasarkan praktikum pengujian keamanan pada rentang port 5009 sampai 5013, dapat disimpulkan bahwa:

1. Semua challenge pada rentang 5009 sampai 5013 berhasil diselesaikan dan menghasilkan flag, yaitu SQLi, command injection, LFI, stored XSS, dan business logic.
2. Pola kerentanannya lebih ke arah aplikasi yang terlalu percaya input dari client. Mulai dari username di login, host ping, nama file di parameter page, konten chat, sampai quantity belanja — semuanya diproses mentah-mentah tanpa validasi server.
3. Mitigasi yang paling masuk akal untuk semua kasus adalah: validasi input, parameterized query, jalankan sistem command tanpa shell, sanitasi dan allowlist file, escape output HTML, pakai cookie HttpOnly, serta cek harga dan quantity selalu di sisi server.
