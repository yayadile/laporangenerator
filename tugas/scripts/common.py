"""Shared helpers for JS-AI-02 (ML & DL Refresher) jobsheet runners.

- Captures stdout of every job and renders it as a terminal-style snapshot PNG
  (assets/ss/jobN_execution.png).
- Saves every figure as a high-resolution PNG (assets/ss/*.png).
- Accumulates all measured metrics into metrics.json for the final report.
"""

from __future__ import annotations

import contextlib
import io
import json
import textwrap
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\LAPORAN")
SS = ROOT / "assets" / "ss"
CKPT = ROOT / "tugas" / "scripts" / "ckpt"
METRICS_JSON = ROOT / "tugas" / "scripts" / "metrics.json"

SS.mkdir(parents=True, exist_ok=True)
CKPT.mkdir(parents=True, exist_ok=True)

FONT_REG = r"C:\Windows\Fonts\consola.ttf"
FONT_BOLD = r"C:\Windows\Fonts\consolab.ttf"
FONT_SIZE = 16
WRAP_COLS = 132
BG = (12, 12, 12)
TITLEBAR = (37, 37, 38)
TEXT = (204, 204, 204)
TITLE_TXT = (255, 255, 255)
ACCENT = (86, 156, 214)

_metrics: dict = {}
if METRICS_JSON.exists():
    _metrics = json.loads(METRICS_JSON.read_text(encoding="utf-8"))


def save_metrics(key: str, value) -> None:
    _metrics[key] = value
    METRICS_JSON.write_text(
        json.dumps(_metrics, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def render_terminal(text: str, path: Path, title: str, footer: str = "") -> Path:
    """Render captured console output as a terminal-window snapshot PNG."""
    font = ImageFont.truetype(FONT_REG, FONT_SIZE)
    bold = ImageFont.truetype(FONT_BOLD, FONT_SIZE)
    pad = 14
    bar_h = 34

    lines: list[str] = []
    for raw in text.splitlines() or [""]:
        if not raw:
            lines.append("")
        else:
            lines.extend(
                textwrap.wrap(
                    raw,
                    width=WRAP_COLS,
                    replace_whitespace=False,
                    drop_whitespace=False,
                )
                or [""]
            )

    tmp = Image.new("RGB", (10, 10))
    d = ImageDraw.Draw(tmp)
    col_w = max(
        [d.textlength(ch, font=font) for ch in "0Wmvil"] + [8]
    )
    body_w = int(col_w * WRAP_COLS) + 1
    line_h = int(FONT_SIZE * 1.45)
    width = body_w + pad * 2
    height = bar_h + pad + line_h * len(lines) + pad + (26 if footer else pad)

    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, width, bar_h], fill=TITLEBAR)
    draw.text((pad, (bar_h - FONT_SIZE) // 2 - 1), title, font=bold, fill=TITLE_TXT)

    y = bar_h + pad
    for ln in lines:
        if ln:
            if ln.lstrip().startswith("$") or ln.startswith(">>>"):
                draw.text((pad, y), ln, font=font, fill=ACCENT)
            else:
                draw.text((pad, y), ln, font=font, fill=TEXT)
        y += line_h

    if footer:
        draw.text((pad, height - 22), footer, font=font, fill=(120, 120, 120))

    img.save(path, dpi=(144, 144))
    return path


def run_job(job: str, title: str, fn) -> str:
    """Execute a job, tee its stdout, and store the snapshot PNG."""
    buf = io.StringIO()
    t0 = time.perf_counter()
    with contextlib.redirect_stdout(buf):
        fn()
    elapsed = time.perf_counter() - t0
    text = buf.getvalue()
    footer = (
        f"python 3.13.13 | torch 2.14.1+cpu | sklearn 1.8.0 | "
        f"elapsed {elapsed:.1f}s | 07-10-2026"
    )
    render_terminal(text, SS / f"{job}_execution.png", title, footer)
    print(text, end="")
    print(f"[saved] {SS / (job + '_execution.png')}")
    return text
