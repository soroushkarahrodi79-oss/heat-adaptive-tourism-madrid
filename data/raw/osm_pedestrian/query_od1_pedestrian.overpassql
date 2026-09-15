/*
GATE 2 (pedestrian-heat) — bounded OD1 pedestrian-network acquisition.
OD1: Atocha (A09, 40.404557,-3.688683) -> Puerta de Alcala (A14, 40.419987,-3.688724).
Corridor bbox (S,W,N,E) = (40.4035,-3.6950,40.4210,-3.6820): covers Alt A
(Paseo del Prado/Recoletos axis, west) and Alt B (Real Jardin Botanico / Retiro
western edge + Calle Alfonso XII, east). BOUNDED corridor clip — NOT city-wide.
Purpose: walkable ways + crossings + barriers + access for a MANUAL route/access
audit. No thermal information is used in construction. Licence: ODbL (OSM contributors).
*/
[out:json][timeout:120][bbox:40.4035,-3.6950,40.4210,-3.6820];
(
  /* every highway way in the corridor: gives footways, pedestrian streets,
     steps, living_street, service, and the carriageways whose sidewalks and
     legal crossings the audit must trace */
  way[highway];
  /* explicit standalone pedestrian/park infrastructure */
  way[footway];
  way[barrier];
);
out body geom;
/* pedestrian-relevant nodes: crossings, signals, barriers, park gates/entrances */
(
  node[highway=crossing];
  node[crossing];
  node[highway=traffic_signals];
  node[barrier];
  node[entrance];
  node[access];
);
out body;
