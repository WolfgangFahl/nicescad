/ Prompt:
// Create an OpenSCAD module named `polygonAt` that places a polygon-based beam at a 3D position `x,y,z`,
// applies 3D rotation `rx,ry,rz`, and extrudes the polygon with `linear_extrude(height=length)`.
// The polygon is defined via `points` and should be extruded symmetrically around its local origin.
// Define a second module `beamAt(x, y, z, rx, ry, rz, sx, sy, sz)` that creates a centered rectangular beam
// cross-section of width `sy`, height `sz` and extrudes it along its axis with length `sx`.
// Add example usage for a horizontal beam (extruded along X) and vertical beam (extruded along Z).
// Add a header comment with a link to https://wiki.bitplan.com/index.php/Creating_a_Model_Truss_Bridget_with_AI
// and // Copyright Wolfgang Fahl with current iso date

// https://wiki.bitplan.com/index.php/Creating_a_Model_Truss_Bridget_with_AI
// Copyright Wolfgang Fahl 2025-06-15

// place and extrude a 2D polygon at given 3D position and rotation
module polygonAt(x, y, z, rx, ry, rz, length, points) {
    translate([x, y, z])
        rotate([rx, ry, rz])
            translate([0, 0, -length/2])  // center extrusion symmetrically
                linear_extrude(height=length)
                    polygon(points);
}

// place a rectangular beam at 3D position with given rotation and dimensions
module beamAt(x, y, z, rx, ry, rz, sx, sy, sz) {
    polygonAt(x, y, z, rx, ry, rz, sx, [
        [-sy/2, -sz/2],
        [ sy/2, -sz/2],
        [ sy/2,  sz/2],
        [-sy/2,  sz/2]
    ]);
}

l=10; // length
h=1; // height
w=1; // width
// Example usage
// Horizontal beam along X → rotate Z→X
ry=90;
beamAt(
    0, 0, 0,
    0, ry, 0,
    l, w, h
);

// Vertical beam
beamAt(
    -l/2+w/2, 0, l/2,
    0, 0, 0,
    l, w, h
);

