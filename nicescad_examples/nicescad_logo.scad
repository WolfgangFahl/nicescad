/*
If you're new to OpenSCAD, please visit the following link to learn the basics: https://openscad.org/documentation.html
This is the logo model for NiceSCAD.
For more information, please visit: http://nicescad.bitplan.com/

Prompt commands:
- Create a parameterized OpenScad module
- Create a logo for the nicescad library
- Code is modular, well-commented
- Each module has a separate test module
- Logo consists of a cube with size=35
- Add hollow tubes=8, diameter=15, thickness=2
- Tubes are evenly and orthogonally placed in 3D
- Add a slight slant of 5 to the tubes
- One tube oriented properly towards the user's perspective
- Tubes are slightly longer than the diagonal by an extra length of 5
- Drill holes at the end to achieve a "see thru" effect
- Add render_margin=0.01 to avoid rounding errors

Author: ChatGPT-4 from OpenAI
Date: 2023-07-27
*/

// Parameters
size = 35;                      // Cube size
tube_d = 15;                    // Tube diameter
tube_t = 2;                     // Tube thickness
tube_extra_length = 5;          // Extra length of the tubes
tube_slant = 5;                 // Slant of the tubes
num_tubes = 8;                  // Number of tubes
render_margin = 0.01;           // Render margin to avoid rounding errors
initial_rotation = [65,35,0];   // Initial rotation to orient first tube towards user

// Main cube module
module main_cube(size) {
    // Creates a cube with a specified size
    cube(size, center=true);
}

// Hollow tube module
module hollow_tube(d, h, t, render_margin) {
    // Creates a hollow tube by subtracting a smaller cylinder from a larger one
    render(convexity = 2, $fn = d * 10, $fa = render_margin) {
        difference() {
            cylinder(d = d, h = h, center = true);
            cylinder(d = d - 2 * t, h = h, center = true);
        }
    }
}

// Tube placements
module place_tubes(num_tubes, size, tube_d, tube_t, tube_extra_length, tube_slant, render_margin, initial_rotation) {
    // Iterate over the number of tubes and rotate each tube by a multiple of 360/num_tubes around the X, Y, and Z axes
    // The tube length is calculated to be slightly longer than the diagonal of the cube
    for(i = [0:num_tubes-1]) {
        angle = i * 360/num_tubes;
        rotate(initial_rotation + [angle, angle + tube_slant, 0]) {
            hollow_tube(tube_d, sqrt(3) * size + tube_extra_length, tube_t, render_margin);
        }
    }
}

// Logo module
module nice_scad_logo(size, tube_d, tube_t, tube_extra_length, tube_slant, num_tubes, render_margin, initial_rotation) {
    // The logo is constructed by union of the cube and the placed tubes
    // Then the inner cylinders are subtracted to create the "see-thru" effect
    difference() {
        union() {
            main_cube(size);
            place_tubes(num_tubes, size, tube_d, tube_t, tube_extra_length, tube_slant, render_margin, initial_rotation);
        }
        for(i = [0:num_tubes-1]) {
            angle = i * 360/num_tubes;
            rotate(initial_rotation + [angle, angle + tube_slant, 0]) {
                cylinder(d = tube_d - 2 * tube_t, h = sqrt(3) * size + tube_extra_length, center = true);
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
        hollow_tube(tube_d, sqrt(3) * size + tube_extra_length, tube_t, render_margin);
    }
}

module test_place_tubes() {
    translate([1.5 * size, 0, 0]) {
        place_tubes(num_tubes, size, tube_d, tube_t, tube_extra_length, tube_slant, render_margin, initial_rotation);
    }
}

// Uncomment below to run test modules
// test_main_cube();
// test_hollow_tube();
// test_place_tubes();

// Generate the logo
nice_scad_logo(size, tube_d, tube_t, tube_extra_length, tube_slant, num_tubes, render_margin, initial_rotation);
