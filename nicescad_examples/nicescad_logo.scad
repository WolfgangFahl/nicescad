/*
If you're new to OpenSCAD, please visit the following link to learn the basics:
https://openscad.org/documentation.html

This is the logo model for NiceSCAD. For more information, please visit: http://nicescad.bitplan.com/

The logo is a 3D model of a cube with multiple diagonally oriented tubes running through it. 
The tubes are longer than the cube's diagonal, and the extra length is a customizable parameter. 
The thickness of the tubes is also customizable. 
The tubes are evenly spaced and oriented orthogonally, creating a 'see through' effect. 
The number of tubes can be adjusted as required.

This model was developed following these prompts:
- Create an OpenSCAD model with a 40x40x40 cube.
- The cube has an inner tube with a diameter of 10 oriented towards the viewer, creating a "see-through" effect.
- The tube is longer than the cube's diagonal.
- The tube is slightly rotated for an added visual appeal.
- The final model is encapsulated into a module named 'nice_scad_logo'.
- The 'tube' is created as a separate module.
- The whole model is translated upwards for better visibility.
- The thickness of the tube is 3.
- All initial parameters are defined as variables.
- Multiple tubes are included, all orthogonal and evenly spaced.
- The number of tubes is a parameter that can be adjusted.
- The tubes are rotated on two axes for a 3D effect. The initial rotation and subsequent angle increments are calculated for visual appeal.

Model designed and created by OpenAI's language model (ChatGPT).
*/

// Initial parameters
cube_size = 30; // Size of the cube
outer_diameter = 20; // Outer diameter of the tube
tube_thickness = 3; // Thickness of the tube
inner_diameter = outer_diameter - 2 * tube_thickness; // Inner diameter of the tube
tube_extra_length = 5; // Extra length of the tube beyond the cube's space diagonal
tube_height = sqrt(3)*cube_size + tube_extra_length; // Tube length is cube's space diagonal plus extra length
num_tubes = 4; // Number of tubes
render_margin = 0.01; // Small value to ensure holes are visible after rendering

// Define rotation sequences for four orthogonal tubes
rotations = [[0, 45, 0], [90, 45, 0], [0, 45, 90], [90, 45, 90]];

// The 'tube' module creates a cylindrical tube with a specified outer diameter, rotation and position.
module tube(h, outer_d, inner_d, rot) {
    rotate(rot) {
        difference() {
            cylinder(h=h, d=outer_d, center=true);
            cylinder(h=h + render_margin, d=inner_d, center=true);
        }
    }
}

// The 'cubes_with_tubes' module creates a cube with a number of tubes going through it.
module cubes_with_tubes(s, h, outer_d, inner_d, num_tubes) {
    union() {
        cube(s, center=true);
        for (i = [0 : num_tubes - 1]) {
            tube(h, outer_d, inner_d, rotations[i]);
        }
    }
}

// The 'drilled_cubes_with_tubes' module takes the 'cubes_with_tubes' and subtracts inner cylinders for the 'see through' effect.
module drilled_cubes_with_tubes(s, h, inner_d, num_tubes) {
    difference() {
        cubes_with_tubes(s, h, outer_diameter, inner_d, num_tubes);
        for (i = [0 : num_tubes - 1]) {
            rotate(rotations[i]) cylinder(h=h + render_margin, d=inner_d, center=true);
        }
    }
}

// The 'nice_scad_logo' module calls 'drilled_cubes_with_tubes' as the main active module
module nice_scad_logo() {
    drilled_cubes_with_tubes(cube_size, tube_height, inner_diameter, num_tubes);
}

// Module for testing the 'tube' module
module test_tube() {
    translate([50,0,0]) tube(tube_height, outer_diameter, inner_diameter, rotations[0]);
}

// Module for testing the 'cubes_with_tubes' module
module test_cubes_with_tubes() {
    translate([-50,0,0]) cubes_with_tubes(cube_size, tube_height, outer_diameter, inner_diameter, num_tubes);
}

// Module for testing the 'drilled_cubes_with_tubes' module
module test_drilled_cubes_with_tubes() {
    translate([0,-50,0]) drilled_cubes_with_tubes(cube_size, tube_height, inner_diameter, num_tubes);
}

// Calling the main module
nice_scad_logo();

// Uncomment the following lines to test the individual modules
//test_tube();
//test_cubes_with_tubes();
//test_drilled_cubes_with_tubes();
