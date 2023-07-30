'''
Created on 2023-07-30

@author: wf
'''
import unittest
from tests.basetest import Basetest
from nicescad.solidservice import SolidConverter

class TestSolidConverter(Basetest):
    """
    Unit tests for the OpenSCAD code converter (SolidConverter class in the nicescad.solidservice module).

    The test_conversion function checks whether the SolidConverter returns the
    expected OpenSCAD code for a given Python code input.

    These tests are for https://github.com/WolfgangFahl/nicescad/issues/28.

    Attributes:
    Author: OpenAI GPT-4
    Date: July 30, 2023
    """

    def setUp(self):
        super().setUp(debug=False, profile=True)

    def test_conversion(self):
        """
        Test whether the SolidConverter returns the expected OpenSCAD code for a 
        given Python code input.
        """
        # The Python code to be converted
        python_code = "difference()(cube(10),sphere(15))"

        # The expected OpenSCAD code
        expected_openscad_code = """difference(){cube(size=10);sphere(r=15);}"""
        # Initialize a SolidConverter object with the Python code
        converter = SolidConverter(python_code)

        # Assert that the conversion result matches the expected OpenSCAD code
        scad=converter.convert_to_openscad()
        debug=self.debug
        if debug:
            print(scad)
        scad = "".join(scad.split())
        if debug:
            print(scad)
        self.assertEqual(scad, expected_openscad_code)

if __name__ == '__main__':
    unittest.main()
