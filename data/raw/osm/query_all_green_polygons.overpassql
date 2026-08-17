[out:json][timeout:90];
(
  way["leisure"~"park|garden"](40.4040,-3.6960,40.4210,-3.6775);
  relation["leisure"~"park|garden"](40.4040,-3.6960,40.4210,-3.6775);
  way["natural"="wood"](40.4040,-3.6960,40.4210,-3.6775);
  way["landuse"="forest"](40.4040,-3.6960,40.4210,-3.6775);
);
out geom;
