FROM python:3.11-slim

# Pandoc + XeTeX untuk export PDF.
# fontconfig + fonts-liberation dipakai sebagai pengganti Times New Roman
# dan Consolas yang tidak ship di Linux (lihat alias di bawah).
RUN apt-get update && apt-get install -y --no-install-recommends \
        pandoc \
        texlive-xetex \
        texlive-fonts-recommended \
        texlive-plain-generic \
        fontconfig \
        fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Template LaTeX memanggil \setmainfont{Times New Roman} dan Consolas.
# Aliaskan ke font Liberation (metrik sama) supaya xelatex tidak gagal
# dengan "The font Times New Roman cannot be found".
RUN printf '%s\n' \
      '<?xml version="1.0"?>' \
      '<!DOCTYPE fontconfig SYSTEM "fonts.dtd">' \
      '<fontconfig>' \
      '  <match target="pattern">' \
      '    <test qual="any" name="family"><string>Times New Roman</string></test>' \
      '    <edit name="family" mode="assign" binding="same"><string>Liberation Serif</string></edit>' \
      '  </match>' \
      '  <match target="pattern">' \
      '    <test qual="any" name="family"><string>Consolas</string></test>' \
      '    <edit name="family" mode="assign" binding="same"><string>Liberation Mono</string></edit>' \
      '  </match>' \
      '</fontconfig>' > /etc/fonts/local.conf \
    && fc-cache -f \
    && fc-list | grep -qi "Liberation Serif"

WORKDIR /app

# Layer dependency duluan: ubah kode saja -> pip tidak diulang
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Hanya file runtime (lihat .dockerignore - data/output/.git tidak ikut)
COPY app.py renderer.py dosen_map.json sample_metadata.json ./
COPY templates/ templates/
COPY assets/ assets/

EXPOSE 8080

# PORT di-inject Render/Docker; fallback 8080 untuk pemakaian lokal
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:${PORT:-8080} --workers 2 --threads 4 --timeout 120 app:app"]
