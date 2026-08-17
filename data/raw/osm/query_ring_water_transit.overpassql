[out:json][timeout:90];
(
  nwr["amenity"~"drinking_water|fountain"](40.4000,-3.7000,40.4250,-3.6700);
  nwr["railway"~"station|halt"](40.4000,-3.7000,40.4250,-3.6700);
  nwr["public_transport"="station"](40.4000,-3.7000,40.4250,-3.6700);
  nwr["station"="subway"](40.4000,-3.7000,40.4250,-3.6700);
  node["highway"="bus_stop"](40.4000,-3.7000,40.4250,-3.6700);
);
out center tags;
