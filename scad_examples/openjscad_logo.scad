// title  : OpenJSCAD.org Logo
// author : Rene K. Mueller
// license: MIT licene
// tags   : Logo, Intersection, Sphere, Cube
// file   : openjscad_logo.scad
module openjscad_logo()
{
    scale(10)
    translate([0, 0, 1.5])
	union() {
		difference() {
            color([231/255,93/255,231/255,1.0])
     		cube(3, center = true);
			sphere(2,$fn=60);
		}
		intersection() {
	        color([231/255,93/255,231/255,1.0])
			sphere(1.3,$fn=30);
     		cube(2.1, center = true);
		}
	}
}

openjscad_logo();
