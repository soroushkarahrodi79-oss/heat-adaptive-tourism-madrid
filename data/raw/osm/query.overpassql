[out:json][timeout:60];
(
  nwr["tourism"~"attraction|museum|viewpoint|gallery|artwork"](40.4040,-3.6960,40.4210,-3.6775);
  nwr["historic"](40.4040,-3.6960,40.4210,-3.6775);
  nwr["leisure"~"park|garden"](40.4040,-3.6960,40.4210,-3.6775);
  nwr["amenity"~"drinking_water|fountain"](40.4040,-3.6960,40.4210,-3.6775);
  nwr["railway"~"station|halt"](40.4040,-3.6960,40.4210,-3.6775);
  nwr["public_transport"="station"](40.4040,-3.6960,40.4210,-3.6775);
  nwr["station"="subway"](40.4040,-3.6960,40.4210,-3.6775);
);
out center tags;
