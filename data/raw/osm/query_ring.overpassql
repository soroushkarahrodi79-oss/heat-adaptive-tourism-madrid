[out:json][timeout:90];
(
  nwr["tourism"~"attraction|museum|viewpoint|gallery|artwork"](40.4000,-3.7000,40.4250,-3.6700);
  nwr["historic"](40.4000,-3.7000,40.4250,-3.6700);
  nwr["leisure"~"park|garden"](40.4000,-3.7000,40.4250,-3.6700);
);
out center tags;
