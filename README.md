# nicescad
nicescad brings OpenScad to the browser (again)

[![Join the discussion at https://github.com/WolfgangFahl/nicescad/discussions](https://img.shields.io/github/discussions/WolfgangFahl/nicescad)](https://github.com/WolfgangFahl/nicescad/discussions)
[![pypi](https://img.shields.io/pypi/pyversions/nicescad)](https://pypi.org/project/nicescad/)
[![Github Actions Build](https://github.com/WolfgangFahl/nicescad/actions/workflows/build.yml/badge.svg)](https://github.com/WolfgangFahl/nicescad/actions/workflows/build.yml)
[![PyPI Status](https://img.shields.io/pypi/v/nicescad.svg)](https://pypi.python.org/pypi/nicescad/)
[![GitHub issues](https://img.shields.io/github/issues/WolfgangFahl/nicescad.svg)](https://github.com/WolfgangFahl/nicescad/issues)
[![GitHub closed issues](https://img.shields.io/github/issues-closed/WolfgangFahl/nicescad.svg)](https://github.com/WolfgangFahl/nicescad/issues/?q=is%3Aissue+is%3Aclosed)
[![API Docs](https://img.shields.io/badge/API-Documentation-blue)](https://WolfgangFahl.github.io/nicescad/)
[![License](https://img.shields.io/github/license/WolfgangFahl/nicescad.svg)](https://www.apache.org/licenses/LICENSE-2.0)

## Demo
[Demo](https://nicescad.bitplan.com/)

## Features
* OpenSCAD editor with 3D view of the rendered STL
* share links `/design/<id>` e.g. [webcam arm](https://nicescad.bitplan.com/design/gdzux4w4), [curve](https://nicescad.bitplan.com/design/quutn5nn)
* import of [BlocksCAD](https://www.blockscad3d.com/) files, see [nicescad_examples/blockscad](https://github.com/WolfgangFahl/nicescad/tree/main/nicescad_examples/blockscad)

## Prerequisites
* [OpenSCAD](https://openscad.org/) command line, detected automatically or set via the environment variables `OPENSCAD_EXEC` and `OPENSCAD_TMP_DIR`
* OpenSCAD 2021.01 renders with the CGAL backend only; the faster Manifold backend waits for the next OpenSCAD release, see [#30](https://github.com/WolfgangFahl/nicescad/issues/30)

## Docs and Tutorials
[Wiki](https://wiki.bitplan.com/index.php/nicescad)

## Examples
* [Basics/logo](https://raw.githubusercontent.com/openscad/openscad/master/examples/Basics/logo.scad)
* [Intersection](https://github.com/WolfgangFahl/nicescad/blob/main/nicescad_examples/scad/openscad_examples/Basics/intersection.scad)

## Links
* https://openscad.org/
* https://nicegui.io
### Alternative online editors
* https://ochafik.com/openscad2/
* http://www.implicitcad.org/editor
* https://www.blockscad3d.com/editor/
* https://openjscad.xyz/
* https://cad-n-done.de (closed source)
### Jupyter notebook integration
* https://github.com/nickc92/ViewSCAD
### Python integration
* https://github.com/jeff-dh/SolidPython
