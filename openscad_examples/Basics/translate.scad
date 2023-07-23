// translate.scad - Example for translate() usage in OpenSCAD

echo(version=version());

module example_translate()
{
	translate([0, 0, -120]) {
		difference() {
			cylinder(h = 50, r = 100);
			translate([0, 0, 10]) cylinder(h = 50, r = 80);
			translate([100, 0, 35]) cube(50, center = true);
		}
		for (i = [0:5]) {
			echo(360*i/6, sin(360*i/6)*80, cos(360*i/6)*80);
			translate([sin(360*i/6)*80, cos(360*i/6)*80, 0 ])
				cylinder(h = 200, r=10);
		}
		translate([0, 0, 200])
			cylinder(h = 80, r1 = 120, r2 = 0);
	}
}

example_translate();



// Written by Clifford Wolf &ltclifford@clifford.at> and Marius
// Kintel &ltmarius@kintel.net>
//
// To the extent possible under law, the author(s) have dedicated all
// copyright and related and neighboring rights to this software to the
// public domain worldwide. This software is distributed without any
// warranty.
//
// You should have received a copy of the CC0 Public Domain
// Dedication along with this software.
// If not, see &lthttp://creativecommons.org/publicdomain/zero/1.0/&gt.