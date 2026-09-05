"""Local inline-SVG functional icons.

``dash-iconify`` was evaluated and rejected: it resolves every icon over the
network from ``api.iconify.design`` at render time, so the interface loses
its iconography in exactly the offline / network-restricted environments a
reproducibility-focused research artefact has to survive (see
docs/PHASE4_2_DESIGN_SPEC.md §11). These twelve icons are shipped in-repo,
weigh ~2 KB in total, and require no network. ``dash-svg`` (already a transitive dependency of
``dash-leaflet``) is promoted to a direct dependency to render them.

Every icon in this application is paired with a text label. No icon is ever
the sole carrier of meaning, so an icon that failed to render would degrade
the interface, never the science. Icons are ``aria-hidden`` for that reason:
the adjacent text is the accessible name.
"""
from __future__ import annotations

from dash_svg import Path, Svg

# 24x24 stroke paths, 1.6px stroke, round caps — one consistent geometry.
_PATHS: dict[str, list[str]] = {
    "chevron-right": ["M9 6l6 6-6 6"],
    "chevron-down": ["M6 9l6 6 6-6"],
    "close": ["M6 6l12 12", "M18 6L6 18"],
    "arrow-left": ["M19 12H5", "M11 18l-6-6 6-6"],
    "info": ["M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18z", "M12 11v5",
             "M12 7.6v.2"],
    "help": ["M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18z",
             "M9.6 9.4a2.5 2.5 0 1 1 3.3 2.4c-.6.2-.9.8-.9 1.4v.6",
             "M12 16.7v.2"],
    "layers": ["M12 4l8 4-8 4-8-4 8-4z", "M4 13l8 4 8-4"],
    "map-pin": ["M12 21s6.5-5.6 6.5-10a6.5 6.5 0 1 0-13 0C5.5 15.4 12 21 12 21z",
                "M12 11.6a1.9 1.9 0 1 0 0-3.8 1.9 1.9 0 0 0 0 3.8z"],
    "clock": ["M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18z", "M12 7.5V12l3 2"],
    "search": ["M10.8 17.6a6.8 6.8 0 1 0 0-13.6 6.8 6.8 0 0 0 0 13.6z",
               "M20 20l-4.4-4.4"],
    "scale": ["M12 4v16", "M6 8h12", "M6 8l-3 6h6l-3-6z",
              "M18 8l-3 6h6l-3-6z"],
    "document": ["M14 3H7a1.6 1.6 0 0 0-1.6 1.6v14.8A1.6 1.6 0 0 0 7 21h10a1.6 1.6 0 0 0 1.6-1.6V7.6L14 3z",
                 "M14 3v4.6h4.6"],
    "no-result": ["M4.5 4.5l15 15", "M12 21a9 9 0 0 1-6.4-15.4",
                  "M7.6 3.9A9 9 0 0 1 20.1 16.4"],
}


def icon(name: str, size: int = 16, *, className: str = "",
         stroke_width: float = 1.6):
    """One functional icon. ``aria-hidden`` by design — always label the text
    beside it, never the icon."""
    paths = _PATHS.get(name)
    if paths is None:
        raise KeyError(f"unknown icon {name!r}; add it to app/components/icons.py")
    children = [
        Path(d=d, fill="none", stroke="currentColor",
             strokeWidth=str(stroke_width), strokeLinecap="round",
             strokeLinejoin="round")
        for d in paths
    ]
    return Svg(
        children,
        viewBox="0 0 24 24",
        width=str(size), height=str(size),
        className=f"hati-icon {className}".strip(),
        **{"aria-hidden": "true"},
    )


def available() -> tuple[str, ...]:
    return tuple(sorted(_PATHS))
