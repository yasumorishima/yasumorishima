# -*- coding: utf-8 -*-
"""Render the At-a-glance dashboard as two self-hosted SVG cards (light / dark).

The SVGs live in this repository, so no third-party badge service can break
them and nothing is hot-linked.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

WIDTH = 880
PAD = 16
GAP = 12
HEADER = 44
TILE_H = 76
COLS = 4

THEMES = {
    "light": {
        "bg": "#ffffff",
        "tile": "#f6f8fa",
        "border": "#d0d7de",
        "text": "#1f2328",
        "muted": "#59636e",
        "accent": "#0969da",
    },
    "dark": {
        "bg": "#0d1117",
        "tile": "#161b22",
        "border": "#30363d",
        "text": "#e6edf3",
        "muted": "#8b949e",
        "accent": "#58a6ff",
    },
}

FONT = (
    "ui-sans-serif, -apple-system, BlinkMacSystemFont, Segoe UI, "
    "Helvetica, Arial, sans-serif"
)


def esc(value: object) -> str:
    """Escape the three characters that matter inside SVG text nodes."""
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def columns_for(count: int) -> int:
    """Choose 4 or 3 columns, whichever leaves the last row least ragged."""
    def waste(cols):
        rows = (count + cols - 1) // cols
        return (rows * cols - count, rows)

    return min((4, 3), key=waste)


def render(tiles: list[tuple[str, str, str]], updated: str, theme: str) -> str:
    """Render one themed card. tiles is a list of (value, label, sub)."""
    c = THEMES[theme]
    COLS = columns_for(len(tiles))
    rows = (len(tiles) + COLS - 1) // COLS
    tile_w = (WIDTH - 2 * PAD - (COLS - 1) * GAP) / COLS
    height = int(HEADER + rows * TILE_H + (rows - 1) * GAP + PAD)

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}"'
        f' viewBox="0 0 {WIDTH} {height}" role="img"'
        f' aria-label="At a glance metrics">',
        f"<style>text{{font-family:{FONT}}}</style>",
        f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="10"'
        f' fill="{c["bg"]}" stroke="{c["border"]}"/>',
        f'<text x="{PAD + 4}" y="30" font-size="15" font-weight="600"'
        f' fill="{c["text"]}">At a glance</text>',
        f'<text x="{WIDTH - PAD - 4}" y="30" font-size="11" text-anchor="end"'
        f' fill="{c["muted"]}">updated {esc(updated)}</text>',
    ]

    last_row = len(tiles) % COLS or COLS

    for i, (value, label, sub) in enumerate(tiles):
        col, row = i % COLS, i // COLS
        # A short final row is centred, so a 7-tile card does not read as a gap.
        indent = 0.0
        if row == rows - 1 and last_row < COLS:
            indent = (COLS - last_row) * (tile_w + GAP) / 2
        tx = round(PAD + indent + col * (tile_w + GAP), 1)
        ty = HEADER + row * (TILE_H + GAP)
        out.append(
            f'<rect x="{tx}" y="{ty}" width="{round(tile_w, 1)}" height="{TILE_H}"'
            f' rx="8" fill="{c["tile"]}" stroke="{c["border"]}"/>'
        )
        out.append(
            f'<text x="{tx + 14}" y="{ty + 36}" font-size="27" font-weight="700"'
            f' fill="{c["accent"]}">{esc(value)}</text>'
        )
        out.append(
            f'<text x="{tx + 14}" y="{ty + 54}" font-size="12"'
            f' fill="{c["text"]}">{esc(label)}</text>'
        )
        if sub:
            out.append(
                f'<text x="{tx + 14}" y="{ty + 69}" font-size="11"'
                f' fill="{c["muted"]}">{esc(sub)}</text>'
            )

    out.append("</svg>")
    return "\n".join(out) + "\n"


def _without_date(svg: str) -> str:
    """The card minus its date line, so an unchanged card is not rewritten."""
    return "\n".join(x for x in svg.split("\n") if ">updated " not in x)


def write(tiles: list[tuple[str, str, str]], updated: str) -> list[Path]:
    """Write both themed cards into assets/ and return the paths written.

    A card whose numbers did not move is left alone: otherwise every run would
    produce a commit that only bumps the date.
    """
    ASSETS.mkdir(exist_ok=True)
    written = []
    for theme in THEMES:
        path = ASSETS / f"dashboard-{theme}.svg"
        svg = render(tiles, updated, theme)
        if path.exists() and _without_date(path.read_text(encoding="utf-8")) == _without_date(svg):
            continue
        path.write_text(svg, encoding="utf-8")
        written.append(path)
    return written
