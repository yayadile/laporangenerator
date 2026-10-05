FROM python:3.11-slim

# Install Pandoc & LaTeX/XeTeX untuk PDF export
RUN apt-get update && apt-get install -y \
    pandoc \
    texlive-xetex \
    texlive-fonts-recommended \
    texlive-plain-generic \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Download & Setup Template Eisvogel
RUN mkdir -p /root/.local/share/pandoc/templates \
    && curl -L -o /tmp/eisvogel.zip https://github.com/Wandmalfarbe/pandoc-latex-template/releases/latest/download/Eisvogel.zip \
    && unzip /tmp/eisvogel.zip -d /tmp/eisvogel \
    && mv /tmp/eisvogel/eisvogel.tex /root/.local/share/pandoc/templates/eisvogel.latex \
    && rm -rf /tmp/eisvogel*

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir flask

EXPOSE 8080
CMD ["python", "app.py"]