// OpenSCAD
// http://nicescad.bitplan.com/issue/23

module knob(sides, height, radius, toothradius) {
  difference() {
    cylinder(r = radius, h = height, center = true);
    for (i = [1 : sides]) {
      rotate([0, 0, i*360/sides])
        translate([radius+1+toothradius, 0, 0])
        difference() {
          cylinder(r = toothradius, h = height, center = true);
          translate([0, 0, 4])
            knob(12, 8, 18.06, 4.4);
        }
    }
  }
}

difference() {
  knob(16, 12, 30, 6);
  translate([0, 0, 4])
    knob(12, 8, 18.06, 4.4);
}