# Laporan Generator 📄

Generator laporan praktikum/jobsheet **Politeknik Negeri Semarang (Polines)**.
Tulis laporan dalam Markdown → keluar **PDF** dan **DOCX** yang sudah jadi,
lengkap dengan cover, format Times New Roman 12pt, margin 2.5cm, dan logo kampus.

```
raw-md/laporan-ctf-5007-idor.md  ──▶  output_matkul/ETHICAL HACKING/
                                          ├─ Adinda_Massa_Merah_3.34.24.2.01_LAB_03_IDOR.pdf
                                          └─ Adinda_Massa_Merah_3.34.24.2.01_LAB_03_IDOR.docx
```

---

## Daftar Isi

- [Fitur](#fitur)
- [Prasyarat](#prasyarat)
- [Instalasi](#instalasi)
- [Cara Pakai (CLI)](#cara-pakai-cli)
- [Cara Pakai (API HTTP)](#cara-pakai-api-http)
- [Struktur Proyek](#struktur-proyek)
- [Menulis Laporan (Format Markdown)](#menulis-laporan-format-markdown)
- [Konfigurasi](#konfigurasi)
- [Kustomisasi Template](#kustomisasi-template)
- [Deployment (Docker / Render)](#deployment-docker--render)
- [Troubleshooting](#troubleshooting)

---

## Fitur

- ✅ Dua format output sekaligus: **PDF** (via XeLaTeX) dan **DOCX** (via Pandoc).
- ✅ Cover otomatis: judul, matkul, dosen, nama, NIM, kelas, logo.
- ✅ Nama dosen otomatis dari `dosen_map.json` berdasarkan nama matkul.
- ✅ Mode interaktif (tinggal pilih-pilih) maupun non-interaktif (untuk script/CI).
- ✅ Bisa jalan sebagai **HTTP API** (`app.py`) untuk dipakai frontend/tools lain.
- ✅ Gambar, tabel, code block, dan daftar markdown didukung penuh.

---

## Prasyarat

| Kebutuhan | Keterangan |
|---|---|
| **Python 3.10+** | Cek: `python --version` |
| **Pandoc** | <https://pandoc.org/installing.html> — versi installer `.msi` (Windows) |
| **MiKTeX** | <https://miktex.org/download> — untuk compile PDF (XeLaTeX) |
| **Font** | *Times New Roman* dan *Consolas* (biasanya sudah ada di Windows) |

> **Windows:** kalau install Pandoc/MiKTeX pakai opsi *per-user* (tanpa admin),
> PATH sering tidak ke-update. `renderer.py` otomatis menambahkan lokasi umum
> ke PATH, tapi **restart terminal dulu** setelah install.

Cek kesiapan tool:

```bash
pandoc --version
xelatex --version
```

Kalau salah satu `tidak dikenali`, install ulang dengan opsi *Add to PATH*
atau restart terminal/laptop.

---

## Instalasi

```bash
git clone <url-repo-kamu>
cd laporangenerator

# (opsional) virtualenv
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

pip install -r requirements.txt
```

`requirements.txt` berisi dependency **runtime API**: `Flask` + `gunicorn`.

Tooling sekali-pakai ada di `requirements-dev.txt` (`Pillow` untuk
`tools/compress_assets.py`, `python-docx` untuk `make_reference.py`,
`websocket-client` untuk `tools/cdp_shoot.py`):

```bash
pip install -r requirements.txt        # wajib (API + CLI)
pip install -r requirements-dev.txt    # opsional, hanya untuk tooling
```

---

## Cara Pakai (CLI)

### 1. Mode interaktif (paling gampang)

```bash
python cli.py
```

Nanti ditanya berurutan:

1. **Pilih file markdown** dari folder `raw-md/` (ketik angka atau nama file).
2. **Pilih folder matkul** — pilih dari daftar, atau **ketik nama baru** untuk
   bikin folder output baru (contoh: `ETHICAL HACKING`).
   Nama dosen otomatis diambil dari `dosen_map.json`.
3. **Masukkan judul jobsheet** (contoh: `LAB 03 Analisis IDOR`).

Hasilnya muncul di `output_matkul/<MATKUL>/`.

### 2. Mode non-interaktif

```bash
python cli.py laporan-ctf-5007-idor.md --matkul "ETHICAL HACKING" --judul "LAB 03 IDOR"
```

Semua argumen bersifat opsional — kalau dilewati, CLI akan bertanya.

| Argumen | Fungsi | Default |
|---|---|---|
| `markdown` | File di `raw-md/` (nama saja, nama + `.md`, atau path lengkap) | pilih dari daftar |
| `--matkul` | Nama matkul = nama folder output (di-uppercase otomatis) | pilih dari daftar |
| `--judul` | Judul jobsheet, jadi nama file & judul cover | ditanya saat interaktif |
| `--dosen` | Override nama dosen | otomatis dari `dosen_map.json` |
| `--formats` | Format output: `pdf`, `docx`, atau `pdf,docx` | `pdf,docx` |

Contoh lengkap:

```bash
# Cuma PDF
python cli.py laporan-ctf-5007-idor.md \
  --matkul "ETHICAL HACKING" \
  --judul "LAB 03 IDOR" \
  --formats pdf

# Dosen diganti manual
python cli.py laporan-ctf-5007-idor.md \
  --matkul "SISTEM LAYANAN VIRTUAL" \
  --judul "LAB 01 Setup VM" \
  --dosen "Mardiyono, S.Kom., M.Sc."
```

---

## Cara Pakai (API HTTP)

Jalankan server:

```bash
python app.py
# default: http://localhost:8080  (ubah pakai env PORT)
```

### Endpoint

#### `POST /generate`

Body (JSON):

| Field | Tipe | Wajib | Keterangan |
|---|---|---|---|
| `markdown` | string | ✅ | Isi lengkap konten markdown laporan |
| `matkul_folder` | string | ✅ | Nama folder output, default `GENERAL` |
| `judul` | string | ✅ | Judul jobsheet (bisa juga lewat `metadata.judul_jobsheet`) |
| `metadata` | object | ❌ | Override metadata cover (`dosen`, `author`, `nim`, `kelas`, dll.) |
| `export_formats` | array | ❌ | `["pdf"]`, `["docx"]`, atau `["pdf","docx"]` (default) |

Contoh dengan `curl`:

```bash
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d @- <<'JSON'
{
  "markdown": "## I. TUJUAN PRAKTIKUM\n\nIsi laporan di sini...",
  "matkul_folder": "ETHICAL HACKING",
  "judul": "LAB 03 IDOR",
  "export_formats": ["pdf", "docx"],
  "metadata": { "dosen": "Rofiq Fauzi, S.Kom., MTCINE, CEH, CHFI" }
}
JSON
```

Contoh dengan Python:

```python
import json
from urllib import request

md = open("raw-md/laporan-ctf-5007-idor.md", encoding="utf-8").read()

payload = json.dumps({
    "markdown": md,
    "matkul_folder": "ETHICAL HACKING",
    "judul": "LAB 03 IDOR",
    "export_formats": ["pdf", "docx"],
}).encode("utf-8")

req = request.Request(
    "http://localhost:8080/generate",
    data=payload, headers={"Content-Type": "application/json"})
with request.urlopen(req) as resp:
    print(resp.status, json.dumps(json.load(resp), indent=2, ensure_ascii=False))
```

**Respons sukses (200):**

```json
{
  "status": "success",
  "message": "File berhasil digenerate!",
  "folder": "D:/.../output_matkul/ETHICAL HACKING",
  "files": ["D:/.../ETHICAL HACKING/Adinda_..._LAB_03_IDOR.pdf", "..."]
}
```

**Respons gagal:** `400` untuk error input (matkul/judul/konten kosong,
file tidak ditemukan), `500` untuk error render (pandoc/LaTeX gagal).

---

## Struktur Proyek

```
laporangenerator/
├── app.py                    # HTTP API (Flask) — POST /generate
├── cli.py                    # CLI interaktif & non-interaktif
├── renderer.py               # Core: markdown -> PDF/DOCX (dipakai cli & app)
├── make_reference.py         # (re)generate templates/reference.docx
├── tools/
│   └── compress_assets.py    # kompres screenshot assets/ (PSNR-gated)
│
├── raw-md/                   # ➡ Taruh sini laporan markdown kamu
│   └── laporan-ctf-5007-idor.md
├── templates/
│   ├── polines_jobsheet.latex  # Template cover + layout PDF
│   ├── reference.docx          # Style DOCX (jangan diedit manual!)
│   └── report_template.md      # Kerangka laporan (salin buat mulai nulis)
├── assets/
│   ├── logopolines.png         # Logo untuk cover
│   └── ss/                     # Screenshot laporan
├── output_matkul/               # ➡ Hasil render per matkul (di-ignore git)
│   └── ETHICAL HACKING/
├── sample_metadata.json         # Data cover default (nama, NIM, prodi, dll.)
├── dosen_map.json               # Pemetaan matkul -> dosen
│
├── requirements.txt             # runtime (Flask, gunicorn)
├── requirements-dev.txt         # tooling (Pillow, python-docx, ...)
├── .gitignore                   # output/data/cache/logs tidak masuk git
├── .dockerignore                # konteks build image hanya file runtime
├── Dockerfile
└── render.yaml                  # Konfigurasi deploy Render.com
```

> **Tidak di-version-control:** `output_matkul/` (hasil render), `data/`
> (dataset MNIST), `testing/`, `__pycache__/`, log & file cookie — semuanya
> regenerable, jadi clone tetap ringan dan tidak ada biner numpuk di git.

---

## Menulis Laporan (Format Markdown)

Salin `templates/report_template.md` ke `raw-md/` sebagai titik awal:

```bash
cp templates/report_template.md raw-md/laporan-baru.md
```

Kerangka baku laporan:

```markdown
## I. TUJUAN PRAKTIKUM

Setelah menyelesaikan praktikum ini, mahasiswa diharapkan mampu:
1. Menjelaskan konsep dasar [Topik].


## II. DASAR TEORI

### 2.1 Pengenalan Topik
Tuliskan penjelasan teori singkat.

### 2.2 Alat dan Bahan
- **Sistem Operasi:** Kali Linux / Windows 11
- **Aplikasi:** Wireshark, Burp Suite


## III. LANGKAH KERJA DAN HASIL PRAKTIKUM

1. Langkah pertama...

   ![Keterangan gambar](assets/ss/screenshot_01.png)


## IV. PEMBAHASAN DAN ANALISIS

Jelaskan analisis dari hasil di Bab III.


## V. KESIMPULAN

1. Kesimpulan pertama.
2. Kesimpulan kedua.
```

### Catatan penting heading

Nomor bab (`I.`, `2.1`, dst.) **ditulis manual di judul**, dan template LaTeX
sengaja *tidak* menomori ulang (`secnumdepth` dimatikan) — jadi jangan berharap
Pandoc/LaTeX menambahkan nomor sendiri.

Soal level heading: di **PDF semua heading dibuat seragam 12pt bold**, jadi `#`
atau `##` hasilnya sama. Beda cerita di **DOCX** (Heading 1 vs Heading 2).
Pokoknya konsisten saja — misalnya `#` untuk bab dan `##` untuk sub-bab
(mengikuti `templates/report_template.md`), atau `##` / `###` (mengikuti
contoh di `raw-md/`).

### Gambar

- Path gambar **relatif terhadap root proyek**, bukan terhadap file markdown.
  Contoh benar: `assets/ss/Screenshot 2026-10-01 151912.png`
- Path mengandung spasi wajib dibungkus `<...>`:

  ```markdown
  ![Autentikasi](<assets/ss/Screenshot 2026-10-01 152109.png>)
  ```

- Gambar terlalu lebar otomatis di-scale agar muat di halaman.
- Kalau gambar tidak muncul di PDF, biasanya ada warning `[WARNING] ... file ... not found`
  di terminal — periksa lagi path-nya.

### Lainnya

- **Bold:** `**teks**` · *italic:* `*teks*` · `inline code` pakai backtick.
- **Code block:** pakai ``` fence; di DOCX jadi kotak abu-abu monospace.
- **Tabel:** markdown table biasa didukung (longtable di PDF).

---

## Konfigurasi

### `sample_metadata.json` — data cover

```json
{
  "matkul": "ETHICAL HACKING",
  "judul_jobsheet": "LAB 02 Guide Digital Evidence Non Repudiation",
  "dosen": "Rofiq Fauzi, S.Kom., MTCINE, CEH, CHFI",
  "author": "Adinda Massa Merah Lawan Tirani",
  "nim": "3.34.24.2.01",
  "kelas": "IK-3C",
  "prodi": "D3 TEKNIK INFORMATIKA",
  "jurusan": "TEKNIK ELEKTRO",
  "tahun": "2026",
  "logo": "assets/logopolines.png"
}
```

Ganti `author`, `nim`, `kelas`, `prodi`, `jurusan`, `tahun` sekali di sini,
selanjutnya otomatis kepakai tiap render.
`matkul`, `judul_jobsheet`, dan `dosen` akan di-override oleh CLI/API.

> Semua field di atas juga bisa di-override per-render lewat `metadata` di API
> atau `--dosen` di CLI.

### `dosen_map.json` — matkul → dosen

```json
{
  "ETHICAL HACKING": "Rofiq Fauzi, S.Kom., MTCINE, CEH, CHFI",
  "SISTEM LAYANAN VIRTUAL": "Mardiyono, S.Kom., M.Sc."
}
```

- Key **case-insensitive** (otomatis di-uppercase).
- Matkul yang belum terdaftar → dosen jadi `"Dosen Pengampu"`.
- Matkul baru bisa langsung ditulis di sini, atau ketik nama baru saat CLI
  interaktif (folder output ikut dibuat).

---

## Kustomisasi Template

### PDF — `templates/polines_jobsheet.latex`

Mengatur class, margin, font, spacing, dan layout cover.
Variabel yang tersedia: `$matkul$`, `$judul_jobsheet$`, `$dosen$`, `$author$`,
`$nim$`, `$kelas$`, `$prodi$`, `$jurusan$`, `$tahun$`, `$logo$`, `$body$`.

### DOCX — `templates/reference.docx`

Aturan styling ada di **`make_reference.py`**, bukan di file `.docx`-nya.
Pandoc cuma membaca *styles*, jadi edit manual di Word **akan tertimpa**.

1. Ubah aturannya di `make_reference.py` (font, ukuran, margin, code block, dll).
2. Jalankan ulang:

   ```bash
   pip install python-docx
   python make_reference.py
   ```

   Perintah ini men-dump `reference.docx` default dari Pandoc lalu di-styling ulang.

Style bawaan saat ini: teks Times New Roman 12pt, heading 12pt bold hitam,
line spacing 1.5, margin 2.5cm, cover 14pt, code block Consolas 10.5pt
dengan border + latar `#F5F5F5`.

---

## Deployment (Docker / Render)

### Docker

```bash
docker build -t laporan-generator .
docker run -p 8080:8080 -e PORT=8080 laporan-generator
```

Image sudah termasuk Pandoc + `texlive-xetex`. Konteks build dibatasi
oleh `.dockerignore`, jadi `data/`, `output_matkul/`, `.git/` dan file
tooling tidak ikut → build cepat dan image tidak kegemukan.

> ℹ️ **Font di Linux:** image meng-alias *Times New Roman* → *Liberation Serif*
> dan *Consolas* → *Liberation Mono* lewat `/etc/fonts/local.conf` (metrik sama,
> hasil PDF tetap rapi). Kalau mau persis font Windows, salin `.ttf` ke
> `/usr/share/fonts/truetype/` lalu jalankan `fc-cache -f`.

`gunicorn` membaca env `PORT` (fallback 8080), jadi cocok untuk Render
yang meng-inject port sendiri.

### Render.com

`render.yaml` sudah tersedia (Docker-based, region Singapore, plan free).
**Port tidak di-hardcode** — Render meng-inject `PORT` dan dibaca oleh
`gunicorn`. Upload repo ke Render dan biarkan yang handle — atau pakai CLI:

```bash
render blueprint apply
```

---

## Troubleshooting

| Gejala | Solusi |
|---|---|
| `'pandoc' tidak ditemukan` | Install Pandoc, centang **Add to PATH**, restart terminal. |
| `'xelatex' tidak ditemukan` | Install MiKTeX, pastikan `xelatex --version` jalan. |
| MiKTeX minta install paket terus | Buka MiKTeX Console → *Install packages on-the-fly* = **Yes**. Atau install paket `geometry`, `fancyhdr`, `titlesec`, `fontspec`, `longtable`, `booktabs`. |
| Font Times New Roman tidak ada | Install font dari Windows (`C:\Windows\Fonts\times*.ttf`) atau pakai font lain di `polines_jobsheet.latex` (`\setmainfont{...}`). |
| Gambar hilang di PDF | Lihat warning `[WARNING]` di terminal → perbaiki path. Path relatif terhadap **root proyek**; path ber-spasi dibungkus `<...>`. |
| Render gagal exit non-zero | Baris error LaTeX ada di 15 baris terakhir output — biasanya ketik salah, link rusak, atau `\` di markdown yang belum di-escape. |
| Nomor bab dobel (`I. I. TUJUAN`) | Hapus nomor manual di judul — numbering LaTeX dimatikan, nomor harus kamu tulis sendiri di markdown. |
| NIM terpotong di nama file | Jangan khawatir — titik di NIM sengaja dipertahankan (renderer tidak pakai `with_suffix`). |
| Hasil DOCX styling-nya aneh | Regenerasi reference: `python make_reference.py` (jangan edit `reference.docx` manual). |
| Warning `Float too large for page` | Template sudah menyisakan 50pt ruang untuk caption — kalau muncul lagi, gambarnya hampir setinggi halaman; kecilkan tingginya di markdown. |
| Error `Too many unprocessed floats` | Sudah dicegah via `\extrafloats{100}` di `polines_jobsheet.latex`. Kalau masih muncul pada laporan super padat, naikkan angkanya. |
| Repo/assets terlalu besar | Kompres ulang screenshot: `python tools/compress_assets.py --apply` (ada `--out <dir>` untuk preview & `--min-psnr` untuk atur kualitas). |
| Mau mulai dari nol | `cp templates/report_template.md raw-md/laporan-baru.md` |

---

## License

Untuk keperluan internal tugas kuliah Polines. Sesuaikan bila mau dipublikasikan.
