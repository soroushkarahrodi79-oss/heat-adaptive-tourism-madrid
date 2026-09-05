"""View 1 — the spatial ground plane.

A point-marker map (no continuous raster/heatmap — Information Architecture
§2 non-precision guard). The MapContainer is created once and never rebuilt;
only the marker LayerGroup's children are swapped, so pan/zoom survives every
timestamp change and every selection.
"""
from __future__ import annotations

import dash_leaflet as dl
from dash import html

from .. import constants as C
from .. import data_loader as dl_data
from .. import theme as T
from .legend import map_hint, tile_fallback_notice
from .primitives import marker_aria_label, marker_html
from .replay import roles, ROLE_LABELS, ROLE_BADGES

# CartoDB Positron — muted, editorial basemap (light labels, low saturation).
# Not a satellite basemap: imagery would compete with the marker channels and
# imply a level of site detail the screening does not use.
_TILE_URL = "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
_TILE_ATTRIB = "© OpenStreetMap contributors © CARTO"

DEFAULT_ZOOM = 15


def map_center() -> list[float]:
    cat = dl_data.frame("catalog")
    return [float(cat["latitude"].mean()), float(cat["longitude"].mean())]


def build_markers(timestamp: str, selected: str | None = None, scenario: str | None = None) -> list:
    """One DivMarker per asset for the given timestamp.

    ``selected`` adds the neutral selection halo to exactly one marker and
    lifts it above its neighbours. Rebuilding this list is the *only* thing
    that changes on the map; the container, its centre and its zoom are
    untouched.
    """
    df = dl_data.assets_at_timestamp(timestamp)
    scenario_roles = roles(scenario, timestamp)
    markers = []
    for _, r in df.iterrows():
        rec = r.to_dict()
        is_selected = (selected is not None and rec["asset_id"] == selected)
        aria = marker_aria_label(rec)
        role = scenario_roles.get(rec["asset_id"])
        marker = marker_html(rec, selected=is_selected)
        if role:
            aria += f" Scenario {scenario}: {ROLE_LABELS[role]}."
            marker += (f'<span class="replay-map-badge" data-role="{role}" '
                       f'aria-hidden="true">{ROLE_BADGES[role]}</span>')
        gloss = C.CONFIDENCE_GLOSS.get(str(rec.get("decision_confidence", "")), "")
        tooltip = dl.Tooltip(
            html.Div(
                [
                    html.Div(str(rec["name"]), className="map-tip__name"),
                    html.Div(
                        C.DECISION_STATE_LABEL.get(
                            str(rec.get("decision_state", "")),
                            str(rec.get("decision_state", ""))),
                        className="map-tip__decision"),
                    html.Div(gloss, className="map-tip__gloss"),
                ],
                className="map-tip",
            ),
            direction="top",
            offset=[0, -18],
            className="map-tip-wrap",
        )
        size = T.MARKER_HIT
        markers.append(
            dl.DivMarker(
                position=[float(rec["latitude"]), float(rec["longitude"])],
                iconOptions={
                    "html": marker,
                    "className": "asset-marker-icon",
                    "iconSize": [size, size],
                    "iconAnchor": [size // 2, size // 2],
                },
                children=[tooltip],
                id={"type": "asset-marker", "index": rec["asset_id"]},
                n_clicks=0,
                # Leaflet's own keyboard support: the marker becomes
                # tab-focusable and Enter activates it, so asset selection is
                # not pointer-only.
                keyboard=True,
                title=aria,
                alt=aria,
                zIndexOffset=1000 if is_selected else 0,
                riseOnHover=True,
            )
        )
    return markers


def map_canvas(timestamp: str, selected: str | None = None):
    """The map surface plus the overlays that live on top of it."""
    return html.Div(
        [
            dl.MapContainer(
                [
                    dl.TileLayer(url=_TILE_URL, attribution=_TILE_ATTRIB,
                                 maxZoom=19, id="basemap-tiles"),
                    dl.LayerGroup(build_markers(timestamp, selected),
                                  id="asset-markers"),
                ],
                id="map-canvas",
                center=map_center(),
                zoom=DEFAULT_ZOOM,
                style={"height": "100%", "width": "100%"},
                scrollWheelZoom=True,
                zoomControl=True,
                attributionControl=True,
            ),
            tile_fallback_notice(),
            html.Div(id="map-overlay-legend", className="map-overlay-legend"),
            map_hint(),
        ],
        className="map-surface",
        id="map-surface",
        role="region",
        **{"aria-label": C.ARIA_MAP_REGION},
    )
