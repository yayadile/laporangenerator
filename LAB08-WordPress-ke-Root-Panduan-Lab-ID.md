# LAB08 — Eskalasi dari WordPress ke Root Server

**Dari Situs WordPress hingga Kendali Penuh atas Server**

Panduan lab — rangkaian serangan dari pengunjung situs anonim hingga akun paling berkuasa di server.

> ⚠️ **Peringatan:** Semua yang ada di lab ini — brute force, web shell, privilege escalation — merupakan tindak pidana jika dilakukan tanpa izin tertulis. Jaringan lab adalah zona aman hukum Anda; di luarnya, perintah yang persis sama adalah kejahatan.

## Daftar Isi

1. Selamat Datang, Penyerang (untuk Sehari)
2. Konsep Kunci secara Mendalam
   - 2.1 Enumeration: Membaca Daftar Tamu
   - 2.2 Brute Force: Seni Menebak dengan Baik
   - 2.3 Web Shell: Remote Control Tersembunyi di Halaman Web
   - 2.4 Post-Exploitation: Menjarah Rumah yang Sudah Dibobol
   - 2.5 Privilege Escalation: Dari Kunci Cadangan ke Kunci Utama
   - 2.6 Opencode AI CLI sebagai Copilot Anda
3. Aturan Keamanan & Etika
4. Persiapan Sebelum Memulai
5. Rangkaian Serangan (Attack Chain)
   - Langkah 1: Enumeration — Temukan Nama Pengguna
   - Langkah 2: Brute Force — Tebak Kuncinya
   - Langkah 3: Initial Access — Tanam Web Shell
   - Langkah 4: Post-Exploitation — Temukan Kunci SSH
   - Langkah 5: Privilege Escalation — Menjadi Root
6. Tugas Anda
7. Glosarium

---

## 1. Selamat Datang, Penyerang

Target Anda adalah sebuah server pelatihan di `<target IP address>` yang menjalankan situs web WordPress (HTTP di port 80) dengan akses login jarak jauh yang aktif (SSH di port 22). Saat ini Anda belum tahu apa-apa tentangnya. Di akhir lab, Anda akan menguasainya sepenuhnya — Anda akan memegang akun root, kunci utama digital yang dapat membaca, mengubah, atau menghapus apa pun di mesin tersebut, serta mengambil flag yang disembunyikan di `/root` sebagai bukti.

Perjalanan ini mengikuti rangkaian serangan klasik — lima langkah yang sama dengan yang dilakukan penyusup sungguhan: (1) Enumeration: mengetuk pintu dan mencari tahu siapa yang tinggal di sini. (2) Brute Force: menebak kunci milik penghuninya. (3) Initial Access: masuk dan menanam alat kendali jarak jauh (web shell). (4) Post-Exploitation: menggeledah rumah mencari kunci cadangan (kredensial SSH). (5) Privilege Escalation: mengubah kunci cadangan menjadi kunci utama (root). Setiap langkah di bawah dijelaskan secara rinci sebelum Anda melakukannya.

Di akhir lab ini, Anda akan mampu:

- Melakukan enumerasi pengguna WordPress dengan wpscan dan menjelaskan mengapa nama pengguna yang bocor merupakan kelemahan keamanan.
- Menjelaskan brute force secara mendalam — wordlist, dictionary attack dibanding credential stuffing — dan menjalankannya dengan rockyou.txt.
- Mendapatkan akses awal melalui wp-admin, memasang plugin File Manager, dan mengunggah PHP web shell.
- Melakukan post-exploitation: berburu kredensial yang tersimpan dan berpindah (pivot) dari web shell ke sesi SSH sungguhan.
- Menjelaskan privilege escalation secara mendalam — aturan sudo, SUID, dan mengapa penyalahgunaan perintah find memberikan akses root — serta melakukannya dengan `sudo -l` dan `find -exec`.

## 2. Konsep Kunci secara Mendalam

Baca bagian ini sebelum menyentuh keyboard. Setiap perintah di lab adalah penerapan nyata dari salah satu konsep berikut.

### 2.1 Enumeration: Membaca Daftar Tamu

Enumeration berarti secara sistematis meminta sebuah sistem mengungkap rahasianya sebelum Anda menyerangnya. WordPress terkenal cerewet: halaman author-nya (`?author=1`), REST API, dan pesan kesalahan login semuanya bisa membocorkan nama pengguna yang valid. Tool wpscan mengotomatiskan pertanyaan-pertanyaan ini dengan opsi `-e u` ("enumerate users"). Mengapa ini penting? Form login membutuhkan dua rahasia — nama pengguna dan kata sandi. Jika situs web memberikan yang pertama secara gratis, pekerjaan penyerang berkurang separuh. Pertahanan: sembunyikan arsip author, blokir enumerasi pengguna, dan jangan biarkan halaman login mengakui apakah suatu nama pengguna ada ("invalid username" dan "wrong password" adalah dua pengakuan yang berbeda).

### 2.2 Brute Force: Seni Menebak dengan Baik

Brute force berarti mencoba kata sandi satu per satu sampai ada yang membuka pintu. Brute force murni mencoba setiap kombinasi (aaaa, aaab, ...) — secara matematis dijamin berhasil pada akhirnya, tetapi sangat lambat untuk kata sandi yang panjang. Serangan nyata lebih cerdas dan hadir dalam tiga varian. **Dictionary attack:** mencoba daftar terkurasi berisi kata sandi yang benar-benar dipakai manusia — inilah yang akan Anda lakukan dengan rockyou.txt, daftar legendaris berisi 14 juta kata sandi asli yang bocor pada 2009, yang di lab ini diambil 1.000 baris pertamanya (yang paling umum). **Credential stuffing:** mengambil pasangan nama pengguna+kata sandi yang bocor dari pembobolan lain dan mencobanya di sini, bertaruh bahwa orang memakai ulang kata sandi. **Password spraying:** mencoba satu kata sandi umum ("Spring2026!") terhadap banyak nama pengguna untuk menghindari penghitung penguncian akun. Lab Anda memakai varian dictionary: wpscan menembakkan wordlist ke halaman login WordPress sampai responsnya berbeda — respons yang berubah itu adalah bunyi pintu yang sedang terbuka. Pertahanan yang harus bisa Anda sebutkan setelah lab ini: passphrase panjang (panjang mengalahkan kerumitan), pembatasan laju dan penguncian akun, autentikasi multi-faktor, dan CAPTCHA — masing-masing membuat tebakan menjadi lebih lambat, lebih berisik, atau sia-sia.

### 2.3 Web Shell: Remote Control Tersembunyi di Halaman Web

Web shell adalah skrip kecil (di sini: PHP) yang diunggah ke server web dan mengubah permintaan HTTP menjadi perintah sistem. Kunjungi URL-nya dengan parameter seperti `?cmd=ls` dan server dengan patuh menjalankan `ls` lalu menampilkan hasilnya — Anda telah mengubah situs web menjadi terminal. Mengapa WordPress mengizinkan ini? Karena admin dapat memasang plugin, dan plugin hanyalah file PHP; plugin File Manager bahkan memungkinkan Anda mengunggah file sendiri. Itulah mengapa kata sandi admin yang dicuri sangat berbahaya: dashboard itu sendiri adalah pintu unggah file. Detail penting: perintah dari web shell berjalan sebagai akun server web (biasanya `www-data`), pengguna berhak istimewa rendah — cukup kuat untuk membaca file di sekitar situs web, tetapi jauh dari root. Keterbatasan inilah yang mendorong Anda ke tahap berikutnya.

### 2.4 Post-Exploitation: Menjarah Rumah yang Sudah Dibobol

Bisa masuk baru setengah cerita; post-exploitation adalah apa yang Anda lakukan di dalam: memetakan mesin, menemukan data berharga, dan menyiapkan lompatan berikutnya. Harta yang paling umum adalah kredensial tersimpan — orang menulis kata sandi di file teks, file konfigurasi, dan skrip (WordPress sendiri menyimpan kata sandi database di `wp-config.php`). Di lab ini, menjelajahi `/home` dengan web shell akan menemukan satu pengguna sistem dan file `password.txt`. File itu adalah pivot Anda: web shell itu rapuh dan terbatas, tetapi SSH memberi Anda terminal penuh yang stabil sebagai pengguna sistem sungguhan. Berpindah dari satu tingkat akses ke tingkat lain menggunakan hasil jarahan disebut pivoting, dan begitulah pembobolan kecil berubah menjadi penguasaan total.

### 2.5 Privilege Escalation: Dari Kunci Cadangan ke Kunci Utama

Privilege escalation (disingkat "privesc") berarti mengubah akses terbatas menjadi akses tanpa batas. Ada dua arah: horizontal — menjadi pengguna biasa lain — dan vertikal — memanjat hingga root, yang merupakan tujuan lab ini. Linux menjaga pendakian ini dengan sudo: buku aturan yang menentukan perintah apa saja yang boleh dijalankan tiap pengguna dengan kekuasaan lebih tinggi. Perintah pengintaian pertama dari setiap privesc adalah `sudo -l` ("tampilkan hak sudo saya"). Sekarang bagian menariknya: sudo seharusnya aman karena hanya mengizinkan program tertentu — tetapi beberapa program yang diizinkan bisa diakali untuk menjalankan program lain. `find` adalah contoh klasik: opsi `-exec`-nya menjalankan perintah apa pun yang Anda berikan pada setiap file yang ditemukannya. Jadi `sudo find . -exec /bin/bash -p \; -quit` berarti: "jalankan find sebagai root; untuk hal pertama yang ditemukan, luncurkan shell root lalu berhenti." Flag `-p` memberi tahu bash untuk mempertahankan identitas root yang berkuasa alih-alih melepaskannya. Keluarga trik ini — menyalahgunakan program sah yang memiliki hak tinggi — dikatalogkan dalam daftar GTFOBins yang terkenal, dan pertahanannya adalah disiplin sederhana: jangan pernah memberi hak sudo kepada program yang bisa membuka shell atau mengedit file, dan utamakan whitelist baris perintah yang persis beserta argumennya.

### 2.6 Opencode AI CLI sebagai Copilot Anda

Lab ini juga melatih keterampilan modern: menggerakkan tool lewat asisten AI. Opencode AI CLI dapat menyusun perintah enumerasi wpscan untuk Anda, menjalankan brute force, dan kemudian membantu mendekode flag yang terenkripsi (misalnya Base64). Perlakukan ia sebagai penerjemah antara niat Anda dan baris perintah — tetapi Anda tetap harus memahami setiap perintah di bagian 2, karena AI yang mengetik untuk Anda tidak bisa menilai untuk Anda: dalam pekerjaan nyata, otorisasi, ruang lingkup, dan etika tetap menjadi tugas manusia.

## 3. Aturan Keamanan & Etika

- Serang hanya `<target IP address>` — server pelatihan milik lab. Jangan pernah mengarahkan wpscan, wordlist, atau shell ke mesin atau situs web lain mana pun.
- Melakukan brute force pada login yang bukan milik Anda adalah ilegal hampir di mana-mana, bahkan "hanya untuk menguji". Otorisasi adalah satu-satunya pembeda antara serangan dan lab.
- PHP shell yang Anda unggah adalah malware sungguhan. Gunakan hanya pada target, dan hapus saat pengajar meminta pembersihan.
- Dokumentasikan setiap perintah yang Anda jalankan di log bukti Anda — penetration test tanpa catatan hanyalah vandalisme.

## 4. Persiapan Sebelum Memulai

- Kali Linux berjalan dan terhubung ke jaringan lab; pastikan Anda bisa menjangkau target: `ping <target IP address>` dan buka `http://<target IP address>` di browser untuk melihat situs WordPress.
- Pastikan tool tersedia: wpscan (sudah terpasang di Kali) dan wordlist di `/usr/share/wordlists/rockyou.txt` (jika berupa file .gz, ekstrak dulu dengan `gunzip`).
- Opencode AI CLI tersedia untuk langkah-langkah berbantuan AI (pengajar akan mengonfirmasi pengaturannya).
- Satu tab browser siap untuk panel admin WordPress di `http://<target IP address>/wp-admin` — tetapi jangan login sampai Anda memiliki kredensial.
- Log bukti Anda terbuka — setiap flag, kata sandi, dan perintah harus dicatat.

## 5. Rangkaian Serangan (Attack Chain)

### Langkah 1: Enumeration — Temukan Nama Pengguna

Minta WordPress mengungkap para penggunanya. Jalankan wpscan terhadap target dengan mode enumerasi pengguna aktif:

```bash
wpscan --url http://<target IP address> -e u
```

Alternatif dengan Opencode AI CLI: *"enumerate using wpscan the wordpress website http://<target IP address> to find the username"*.

**Mengapa ini penting:** Enumeration mengubah serangan buta menjadi serangan yang tertarget: alih-alih menebak nama pengguna DAN kata sandi, kini Anda hanya menebak kata sandi. Catat setiap nama pengguna yang ditampilkan wpscan — mereka adalah kandidat Anda untuk Langkah 2.

### Langkah 2: Brute Force — Tebak Kuncinya

Pilih satu nama pengguna dari Langkah 1. Siapkan kamus berisi 1.000 kata sandi dari baris-baris pertama (paling umum) rockyou.txt, lalu tembakkan ke halaman login:

```bash
head -n 1000 /usr/share/wordlists/rockyou.txt > /home/kali/rockyou.txt
wpscan --url http://<target IP address> -U <username> -P /home/kali/rockyou.txt
```

Alternatif dengan Opencode AI CLI: *"brute force user \<username> using 1000 of first lines of wordlist rockyou"* — Opencode AI juga dapat menganalisis output dan menyorot kredensial yang berhasil untuk Anda.

**Mengapa ini penting:** Anda sedang menyaksikan dictionary attack dari bagian 2.2 terjadi secara langsung: wpscan mencoba tiap kata sandi dan membaca responsnya. Sebagian besar gagal dengan cara yang sama; yang berhasil mengubah respons — itulah kredensial Anda. Perhatikan betapa cepat kata sandi lemah tumbang, dan ingat pertahanan yang seharusnya bisa menghentikan Anda: penguncian akun, MFA, pembatasan laju.

### Langkah 3: Initial Access — Tanam Web Shell

Login ke dashboard WordPress di `http://<target IP address>/wp-admin` dengan kredensial yang berhasil Anda pecahkan. Pasang plugin "File Manager", gunakan untuk mengunggah PHP web shell (cari di GitHub yang sederhana, misalnya shell satu baris yang menjalankan parameter `cmd`), lalu kunjungi URL shell tersebut dan jalankan `ls /home` untuk menemukan pengguna sistem di server.

**Mengapa ini penting:** Anda kini sudah di dalam, tetapi hanya sebagai akun web berhak rendah (`www-data`). Output `ls /home` lebih penting daripada kelihatannya: setiap nama direktori di sana adalah pengguna sistem sungguhan — identitas potensial berikutnya dalam pendakian Anda.

### Langkah 4: Post-Exploitation — Temukan Kunci SSH

Masih melalui web shell, jelajahi direktori home pengguna yang ditemukan dan baca file kata sandinya. Lalu tingkatkan akses Anda: tinggalkan web shell yang rapuh dan buka sesi SSH sungguhan sebagai pengguna tersebut.

```bash
cat /home/<found_user>/password.txt
ssh <user>@<target IP address>
```

**Mengapa ini penting:** Inilah pivoting: setiap kredensial yang Anda jarah berubah menjadi posisi yang lebih kuat. Menyimpan kata sandi di file teks biasa adalah salah satu kesalahan paling umum di dunia nyata — langkah ini adalah alasan mengapa pihak bertahan pantang melakukannya.

### Langkah 5: Privilege Escalation — Menjadi Root

Di dalam sesi SSH Anda, tampilkan hak sudo. Anda akan melihat bahwa `find` boleh dijalankan sebagai root. Manfaatkan opsi `-exec` untuk memunculkan shell root, lalu masuk ke `/root` dan baca flag-nya. Jika flag tampak terenkripsi (misalnya Base64), minta Opencode AI untuk mendekodenya.

```bash
sudo -l
sudo find . -exec /bin/bash -p \; -quit
cd /root && ls && cat <flag_file>
```

**Mengapa ini penting:** Ingat kembali bagian 2.5: sudo memberi kekuasaan kepada sebuah program, dan program itu bisa menjalankan program lain — maka kekuasaannya bocor kepada Anda. Flag `-p` mencegah bash melepaskan identitas root. Selamat: Anda telah menyelesaikan seluruh rangkaian dari pengunjung anonim hingga penguasa mesin. Sekarang berpikirlah seperti pihak bertahan: aturan tunggal mana di server ini yang seharusnya bisa memutus rangkaian Anda?

## 6. Tugas Anda

Jawab di log bukti Anda; bersiaplah mempertahankan setiap jawaban di kelas.

- **Hasil enumeration:** nama pengguna apa saja yang ditemukan wpscan, dan melalui fitur WordPress apa mereka bocor? Pengaturan apa yang seharusnya bisa menyembunyikannya?
- **Analisis brute force:** pasangan nama pengguna+kata sandi mana yang berhasil, dan kira-kira di baris ke berapa dari daftar 1.000 kata? Jelaskan dengan kata-kata Anda sendiri mengapa dictionary attack mengalahkan brute force murni, dan sebutkan dua pertahanan yang seharusnya bisa menggagalkan serangan Anda.
- **Web shell:** akun sistem apa yang menjalankan perintah Anda (petunjuk: `whoami`), dan mengapa jawaban itu memaksa Anda terus memanjat?
- **Privilege escalation:** kutip baris `sudo -l` yang membuka celah untuk Anda, dan jelaskan langkah demi langkah apa yang dilakukan setiap bagian dari `sudo find . -exec /bin/bash -p \; -quit` — termasuk peran `-p`.
- **Flag:** kumpulkan flag dari `/root`. Jika terenkripsi, sebutkan jenis encoding-nya (misalnya Base64) dan tunjukkan bentuk terenkripsi maupun hasil dekodenya.
- **Sudut pandang pembela:** pilih tiga dari lima langkah dan usulkan satu perbaikan konkret per langkah yang seharusnya bisa memutus rangkaian serangan Anda.

## 7. Glosarium

| Istilah | Arti |
|---|---|
| Enumeration | Meminta sistem secara sistematis untuk mengungkap pengguna, layanan, dan struktur sebelum menyerang. |
| Brute force | Mencoba kata sandi satu per satu sampai ada yang berhasil. |
| Dictionary attack | Brute force dengan daftar terkurasi berisi kata sandi asli yang umum, alih-alih setiap kombinasi. |
| Wordlist | File daftar kata sandi yang dipakai dalam dictionary attack, misalnya rockyou.txt. |
| Credential stuffing | Mencoba ulang pasangan nama pengguna+kata sandi yang bocor dari situs lain, bertaruh pada penggunaan ulang kata sandi. |
| Web shell | Skrip yang diunggah ke server dan mengubah permintaan web menjadi perintah sistem. |
| Post-exploitation | Semua yang dilakukan setelah berhasil masuk: memetakan, menjarah, dan menyiapkan lompatan berikutnya. |
| Pivoting | Menggunakan akses hasil jarahan untuk mencapai posisi yang lebih kuat atau mesin lain. |
| Privilege escalation | Mengubah akses terbatas menjadi akses lebih tinggi; vertikal = mencapai root. |
| sudo | Buku aturan Linux untuk menjalankan perintah tertentu dengan kekuasaan lebih tinggi; `sudo -l` menampilkan hak Anda. |
| SUID | Izin file yang membuat program berjalan dengan hak pemiliknya — permukaan privesc klasik. |
| GTFOBins | Katalog program Linux sah yang bisa disalahgunakan untuk membuka shell dan eskalasi hak istimewa. |
| root | Superuser: bisa membaca, mengubah, atau menghapus apa pun di sistem Linux. |
| Flag | Token rahasia yang ditanam di target sebagai bukti keberhasilan pembobolan (gaya CTF). |
| Base64 | Encoding teks umum (bukan enkripsi!) yang sering dipakai untuk menyamarkan flag. |
