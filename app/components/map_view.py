"""View 1 — Territorial / Time View.

A point-marker map (no continuous raster/heatmap — Information Architecture
§2 non-precision guard). The MapContainer is created once and never rebuilt;
only the marker LayerGroup's children are swapped when the timestamp changes,
so pan/zoom stays stable.
"""
from __future__ import annotations

import dash_leaflet as dl

from .. import constants as C
from .. import data_loader as dl_data
from .primitives import marker_html

# CartoDB Positron — muted, editorial basemap (labels light, non-saturated).
_TILE_URL = "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
_TILE_ATTRIB = ('© OpenStreetMap contributors © CARTO')


def _map_center() -> list[float]:
    cat = dl_data.frame("catalog")
    return [float(cat["latitude"].mean()), float(cat["longitude"].mean())]


def build_markers(timestamp: str) -> list:
    """One DivMarker per asset for the given timestamp."""
    df = dl_data.assets_at_timestamp(timestamp)
    markers = []
    for _, r in df.iterrows():
        rec = r.to_dict()
        gloss = C.CONFIDENCE_GLOSS.get(str(rec.get("decision_confidence", "")), "")
        decision_lbl = C.DECISION_STATE_LABEL.get(
            str(rec.get("decision_state", "")), str(rec.get("decision_state", "")))
        tooltip = dl.Tooltip(
            [
                f"{rec['name']}",
                f" — {decision_lbl}",
                f" · {C.CONFIDENCE_SHORT.get(str(rec.get('decision_confidence','')), '')}",
                f". {gloss}",
            ],
            direction="top",
        )
        markers.append(
            dl.DivMarker(
                position=[float(rec["latitude"]), float(rec["longitude"])],
                iconOptions={
                    "html": marker_html(rec),
                    "className": "asset-marker-icon",
                    "iconSize": [34, 34],
                    "iconAnchor": [17, 17],
                },
                children=[tooltip],
                id={"type": "asset-marker", "index": rec["asset_id"]},
                n_clicks=0,
            )
        )
    return markers


def map_canvas(timestamp: str):
    center = _map_center()
    return dl.MapContainer(
        [
            dl.TileLayer(url=_TILE_URL, attribution=_TILE_ATTRIB, maxZoom=19),
            dl.LayerGroup(build_markers(timestamp), id="asset-markers"),
        ],
        id="map-canvas",
        center=center,
        zoom=15,
        style={"height": "100%", "width": "100%"},
        scrollWheelZoom=True,
        zoomControl=True,
    )
