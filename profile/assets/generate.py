"""Draws the banner and the project tiles of the organization profile.

Every picture exists in two themes: `light` (cream background, ink mascot) and `dark`
(ink background, cream mascot). The README picks one with <picture>.

Run after changing a project's text or status:  python3 profile/assets/generate.py
"""

import math
from pathlib import Path

INK, CREAM, ORANGE = "#15120F", "#FFF3E4", "#FF6F47"
THEMES = {
    "light": {"bg": CREAM, "fg": INK, "muted": "#7A6C5D", "edge": "none"},
    "dark": {"bg": INK, "fg": CREAM, "muted": "#A89A8A", "edge": "#3A322C"},
}
FONT = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"

# Products Quant is an alternative to, as two lines of the banner.
ALTERNATIVE_TO = [
    ("OpenAI Dots", "Meta Muse", "Grok Bot", "Instinct"),
    ("Manus Cue", "Claude Cowork", "ChatGPT agent"),
]

# (file name, title, two description lines, ready)
PROJECTS = [
    ("core", "Quant-Core", ("The brain: agents on", "your server, 24/7"), False),
    ("voice-vector", "Quant-Voice-Vector", ("Voice profiles, so it", "knows who speaks"), True),
    ("ai-speaker", "Quant-Ai-Speaker", ("A smart speaker", "you build yourself"), False),
    ("tamagotchi", "Quant-Tamagotchi", ("A pocket companion", "you build yourself"), False),
]


def blob() -> str:
    """The mascot outline: a superellipse measured from the logo (radius 160, exponent 2.64)."""
    points = []
    for step in range(96):
        angle = 2 * math.pi * step / 96
        x, y = math.cos(angle), math.sin(angle)
        px = 250 + 160 * math.copysign(abs(x) ** (2 / 2.64), x)
        py = 250 + 160 * math.copysign(abs(y) ** (2 / 2.64), y)
        points.append(f"{px:.1f} {py:.1f}")
    return "M" + "L".join(points) + "Z"


def eyes(x1: float, x2: float, y: float, width: float, height: float) -> str:
    return "".join(
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{width / 2}" fill="{ORANGE}"/>'
        for x in (x1, x2)
    )


def mascot(kind: str, fg: str, bg: str) -> str:
    """The mascot in one of its roles, drawn on a 500x500 canvas."""
    if kind == "core":
        return f'<path d="{blob()}" fill="{fg}"/>' + eyes(190, 272, 202, 38, 89)
    if kind == "voice-vector":
        return (
            f'<rect x="170" y="62" width="160" height="262" rx="80" fill="{fg}"/>'
            + eyes(204, 264, 150, 32, 76)
            + f'<path d="M122 250A128 128 0 0 0 378 250M250 380V432M196 432H304" fill="none" '
            f'stroke="{fg}" stroke-width="26" stroke-linecap="round"/>'
        )
    if kind == "ai-speaker":
        return (
            f'<rect x="140" y="50" width="220" height="400" rx="70" fill="{fg}"/>'
            + eyes(214, 260, 100, 26, 62)
            + f'<circle cx="250" cy="320" r="72" fill="none" stroke="{bg}" stroke-width="18"/>'
            f'<circle cx="250" cy="320" r="22" fill="{bg}"/>'
        )
    if kind == "tamagotchi":
        buttons = "".join(
            f'<circle cx="{x}" cy="{y}" r="16" fill="{ORANGE}"/>'
            for x, y in ((190, 365), (250, 385), (310, 365))
        )
        return (
            '<path d="M250 50C360 50 410 170 410 280C410 390 340 450 250 450C160 450 90 390 90 '
            f'280C90 170 140 50 250 50Z" fill="{fg}"/>'
            f'<rect x="165" y="150" width="170" height="150" rx="30" fill="{bg}"/>'
            + eyes(218, 260, 190, 22, 56)
            + buttons
        )
    raise ValueError(kind)


def banner(theme: dict) -> str:
    bg, fg = theme["bg"], theme["fg"]
    names = "".join(
        f'<text x="444" y="{y}" font-size="25" fill="{fg}">{" · ".join(line)}</text>'
        for y, line in zip((246, 280), ALTERNATIVE_TO)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 360" font-family="{FONT}">
  <title>Quant: an open-source alternative to {", ".join(sum(ALTERNATIVE_TO, ()))}</title>
  <rect x="1" y="1" width="1198" height="358" rx="40" fill="{bg}" stroke="{theme["edge"]}" stroke-width="2"/>
  <g transform="translate(30 -20) scale(0.8)">{mascot("core", fg, bg)}</g>
  <text x="440" y="150" font-size="104" font-weight="700" fill="{fg}">Quant</text>
  <text x="444" y="204" font-size="30" font-weight="600" fill="{fg}">An open-source alternative to</text>
  {names}
  <text x="444" y="322" font-size="23" fill="{ORANGE}">Your server · your data · your devices</text>
</svg>
"""


def tile(kind: str, name: str, lines: tuple, ready: bool, theme: dict) -> str:
    bg, fg = theme["bg"], theme["fg"]
    status = "Ready" if ready else "In development"
    if ready:
        pill = (
            f'<rect x="100" y="296" width="100" height="34" rx="17" fill="{ORANGE}"/>'
            f'<text x="150" y="319" text-anchor="middle" font-size="15" font-weight="600" fill="{INK}">{status}</text>'
        )
    else:
        pill = (
            f'<rect x="72" y="296" width="156" height="34" rx="17" fill="none" stroke="{fg}" stroke-width="1.5"/>'
            f'<text x="150" y="319" text-anchor="middle" font-size="15" fill="{fg}">{status}</text>'
        )
    # The plain mascot is smaller than the others so that all four look the same size.
    place = "translate(50 0) scale(0.4)" if kind == "core" else "translate(60 12) scale(0.36)"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 360" font-family="{FONT}">
  <title>{name}: {" ".join(lines)}. {status}.</title>
  <rect x="1" y="1" width="298" height="358" rx="30" fill="{bg}" stroke="{theme["edge"]}" stroke-width="2"/>
  <g transform="{place}">{mascot(kind, fg, bg)}</g>
  <text x="150" y="224" text-anchor="middle" font-size="22" font-weight="700" fill="{fg}">{name}</text>
  <text x="150" y="252" text-anchor="middle" font-size="15.5" fill="{theme["muted"]}">{lines[0]}</text>
  <text x="150" y="273" text-anchor="middle" font-size="15.5" fill="{theme["muted"]}">{lines[1]}</text>
  {pill}
</svg>
"""


def main() -> None:
    out = Path(__file__).parent
    for name, theme in THEMES.items():
        (out / f"banner-{name}.svg").write_text(banner(theme), encoding="utf-8")
        for kind, title, lines, ready in PROJECTS:
            (out / f"tile-{kind}-{name}.svg").write_text(
                tile(kind, title, lines, ready, theme), encoding="utf-8"
            )


if __name__ == "__main__":
    main()
