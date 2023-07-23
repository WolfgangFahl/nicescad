echo(version=version());

function get_cylinder_h(p) = lookup(p, [
		[ -200, 5 ],
		[ -50, 20 ],
		[ -20, 18 ],
		[ +80, 25 ],
		[ +150, 2 ]
	]);

for (i = [-100:5:+100]) {
	// echo(i, get_cylinder_h(i));
	translate([ i, 0, -30 ]) cylinder(r1 = 6, r2 = 2, h = get_cylinder_h(i)*3);
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