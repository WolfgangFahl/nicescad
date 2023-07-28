/*
If you're new to OpenSCAD, please visit the following link to learn the basics: https://openscad.org/documentation.html
This is the logo model for NiceSCAD.
For more information, please visit: http://nicescad.bitplan.com/

Prompt commands:
- Create a parameterized OpenScad module
- Create a logo for the nicescad library
- Code is modular, well-commented
- Each module has a separate test module
- Logo consists of a cube with size=35, bottom aligned with base plane
- Add hollow tubes=8, diameter=15, thickness=2
- Tubes are evenly and orthogonally placed in 3D
- Add a slight slant of 5 to the tubes
- One tube oriented properly towards the user's perspective
- Tubes are slightly longer than the diagonal by an extra length of 5
- Drill holes at the end to achieve a "see thru" effect
- Add render_margin=0.01 to avoid rounding errors but do not use render()
  Instead, subtract a cylinder longer by render_margin

Author: ChatGPT-4 from OpenAI
Date: 2023-07-28
*/

// Parameters
size = 35;                      // Cube size
tube_d = 15;                    // Tube diameter
tube_t = 2;                     // Tube thickness
tube_extra_length = 5;          // Extra length of the tubes
tube_slant = 5;                 // Slant of the tubes
num_tubes = 8;                  // Number of tubes
render_margin = 0.1;           // Render margin to avoid rounding errors
initial_rotation = [0, 0, 45];  // Initial rotation to orient first tube towards user
local_fn = 20;                  // Local resolution of the cylinders

// Main cube module
module main_cube(size) {
    cube(size, center=true);
}

// Hollow tube module
module hollow_tube(d, h, t, render_margin, local_fn) {
    difference() {
        cylinder(d = d, h = h, center = true, $fn = local_fn);
        cylinder(d = d - 2 * t, h = h + 2 * render_margin, center = true, $fn = local_fn);
    }
}

// Tube placements
module place_tubes(num_tubes, size, tube_d, tube_t, tube_extra_length, tube_slant, render_margin, initial_rotation, local_fn) {
    for(i = [0:num_tubes-1]) {
        angle = i * 360/num_tubes;
        rotate(initial_rotation + [angle, angle + tube_slant, 0]) {
            hollow_tube(tube_d, sqrt(3) * size + tube_extra_length, tube_t, render_margin, local_fn);
        }
    }
}

// Logo module
module nice_scad_logo(size, tube_d, tube_t, tube_extra_length, tube_slant, num_tubes, render_margin, initial_rotation, local_fn) {
    difference() {
        union() {
            main_cube(size);
            place_tubes(num_tubes, size, tube_d, tube_t, tube_extra_length, tube_slant, render_margin, initial_rotation, local_fn);
        }
        for(i = [0:num_tubes-1]) {
            angle = i * 360/num_tubes;
            rotate(initial_rotation + [angle, angle + tube_slant, 0]) {
                cylinder(d = tube_d - 2 * tube_t, h = sqrt(3) * size + tube_extra_length + 2 * render_margin, center = true, $fn = local_fn);
            }
        }
    }
}

// Test modules
module test_main_cube() {
    translate([-1.5 * size, 0, 0]) {
        main_cube(size);
    }
}

module test_hollow_tube() {
    translate([0, -1.5 * size, 0]) {
        hollow_tube(tube_d, sqrt(3) * size + tube_extra_length, tube_t, render_margin, local_fn);
    }
}

module test_place_tubes() {
    translate([1.5 * size, 0, 0]) {
        place_tubes(num_tubes, size, tube_d, tube_t, tube_extra_length, tube_slant, render_margin, initial_rotation, local_fn);
    }
}

// Uncomment below to run test modules
// test_main_cube();
// test_hollow_tube();
// test_place_tubes();

// Generate the logo
 translate([0, 0, size/2])nice_scad_logo(size, tube_d, tube_t, tube_extra_length, tube_slant, num_tubes, render_margin, initial_rotation, local_fn);
