// nicescad truss bridge example
// see https://wiki.bitplan.com/index.php/Creating_a_Model_Truss_Bridget_with_AI
// WF 2025-06-14
// Prompt: "Create an OpenSCAD module named beamAt that places a cube beam at a specified 3D position, applies a 3D rotation, and uses given dimensions. Add an example usage rotating the beam 45 degrees around the Z-axis."
module beamAt(position, rotation, dimensions) {
  translate(position)
    rotate(rotation)
      cube(dimensions);
}

// example usage
beamAt([10, 5, 0], [0, 0, 45], [40, 3, 3]);  // beam at position, rotated 45° on Z-axis
