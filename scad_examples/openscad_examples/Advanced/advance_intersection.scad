echo(version=version());

intersection()
{
	linear_extrude(height = 100, center = true, convexity= 3)
		import(file = "advance_intersection.dxf");
	rotate([0, 90, 0])
	linear_extrude(height = 100, center = true, convexity= 3)
		import(file = "advance_intersection.dxf");
	rotate([90, 0, 0])
	linear_extrude(height = 100, center = true, convexity= 3)
		import(file = "advance_intersection.dxf");
}

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