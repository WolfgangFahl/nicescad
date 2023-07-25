module knob(sides, height, radius, toothradius) {
  difference() {
    cylinder(r1=radius, r2=radius, h=height, center=true);
    for (i = [1:sides]) {
      rotate([0, 0, i * 360/sides]) {
        translate([radius + toothradius / 2, 0, 0]) {
          cylinder(r1=toothradius, r2=toothradius, h=height, center=true);
        }
      }
    }
  }
}

difference() {
  knob(16, 12, 30, 6);
  translate([0, 0, 4]) {
    knob(16, 12, 30, 6);
  }
}
