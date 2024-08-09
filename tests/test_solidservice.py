"""
Created on 2023-07-30

@author: wf
"""

import unittest

from fastapi.testclient import TestClient

import nicescad as nicescad
from nicescad.solidservice import FastAPIServer, SolidConverter
from tests.basetest import Basetest


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
        scad = converter.convert_to_openscad()
        debug = self.debug
        if debug:
            print(scad)
        scad = "".join(scad.split())
        if debug:
            print(scad)
        self.assertEqual(scad, expected_openscad_code)

    def check_server(self):
        """
        Check whether the FastAPI server is running and returns the expected version of the nicescad package.

        Returns:
        bool -- True if the server is running and the version is correct, False otherwise.
        """
        try:
            response = self.client.get("/version/")
            if response.status_code != 200:
                return False
            data = response.json()
            if "version" not in data or data["version"] != nicescad.__version__:
                return False
            return True
        except:
            return False

    def test_endpoint(self):
        """
        Test whether the FastAPI endpoint returns the expected OpenSCAD code for a
        given Python code input.
        """
        self.server = FastAPIServer()
        self.client = TestClient(self.server.app)
        if not self.check_server():
            print("Server not available")
            return

        python_code = "difference()(cube(10),sphere(15))"
        expected_openscad_code = """difference(){cube(size=10);sphere(r=15);}"""

        response = self.client.post("/convert/", json={"python_code": python_code})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("openscad_code", data)
        received_openscad_code = "".join(data["openscad_code"].split())

        self.assertEqual(received_openscad_code, expected_openscad_code)


if __name__ == "__main__":
    unittest.main()
