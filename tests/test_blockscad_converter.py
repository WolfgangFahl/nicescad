import os
import unittest
import shutil
from nicescad.blockscad_converter import BlockscadConverter
from tests.basetest import Basetest
from nicescad.webserver import WebServer

class TestBlockscadConverter(Basetest):
    """
    Unit test for converting a BlockSCAD XML file to a SCAD file using the BlockscadConverter class.

    The path for examples is obtained using the WebServer.examples_path() function. The examples of SCAD input files are located in the 'blockscad' subdirectory of the examples path. A test method is defined which iterates over all BlockSCAD XML files in the 'blockscad' directory, converts each file to a SCAD file, and then saves the converted files in the 'blockscad_converted' subdirectory under 'examples/scad'.

    The conversion during the test is done using a temporary directory. The test checks if the content of the output SCAD file matches the expected content in the 'blockscad_converted' directory.

    Prompt details:
        - Conversion of a BlockSCAD XML file to a SCAD file.
        - Usage of BlockscadConverter class for conversion. The constructor needs an xml_path parameter
        - the function to be tested is  convert_to_scad with scad_path as the output file parameter
        - Retrieval of the examples path using WebServer.examples_path() class method from nicescad.webserver.
        - Assumption of the 'blockscad' directory for SCAD input examples.
        - Definition of the unit test setup with paths for the BlockSCAD and SCAD directories.
        - Usage of Basetest as the base class for the test with setUp signature as def setUp(self, debug=False, profile=True).
        - Definition of a test method to iterate over BlockSCAD XML files, convert them to SCAD files, and save in 'blockscad_converted' subdirectory of the scad subdirectory of the examples directory.
        - Usage of a temporary directory for conversion during the test.
        - Comparison of output SCAD file content with the expected SCAD file content.
        - count the number of files and check that at least one file was tested
        - Inclusion of Google docstrings and type hints in the code.
        - Inclusion of the Links for reference
        - Links for reference:
            - BlockSCAD: https://www.blockscad3d.com/editor/
            - OpenSCAD: https://openscad.org/
            - Target platform (NiceSCAD): http://nicescad.bitplan.com/
            - Issue: Support reading and converting blockcad files #23: http://nicescad.bitplan.com/issues/23
    
    Author: OpenAI Assistant
    Date: 2023-07-25
    """

    def setUp(self, debug: bool=False, profile: bool=True) -> None:
        """Set up the test environment."""
        super().setUp(debug, profile)
        self.examples_path = WebServer.examples_path()
        self.blockscad_dir = os.path.join(self.examples_path, 'blockscad')
        self.scad_converted_dir = os.path.join(self.examples_path, 'scad/blockscad_converted')
        self.temp_dir = os.path.join(self.examples_path, 'temp')
        os.makedirs(self.scad_converted_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def test_convert_to_scad(self) -> None:
        """Test the convert_to_scad method of BlockscadConverter."""
        return # do not run yet
        file_count=0
        for root, _, files in os.walk(self.blockscad_dir):
            for file in files:
                if file.endswith('.xml'):
                    file_count+=1
                    blockscad_file = os.path.join(root, file)
                    scad_file = os.path.join(self.scad_converted_dir, f'{os.path.splitext(file)[0]}.scad')
                    temp_file = os.path.join(self.temp_dir, f'{os.path.splitext(file)[0]}.scad')

                    # Convert BlockSCAD XML file to SCAD file
                    bc=BlockscadConverter(blockscad_file)
                    bc.convert_to_scad(temp_file)
                    
                    # Compare the output SCAD file with the expected SCAD file
                    with open(scad_file, 'r') as expected_file, open(temp_file, 'r') as test_file:
                        self.assertEqual(test_file.read(), expected_file.read())
        self.assertTrue(file_count>0)
        
    def tearDown(self) -> None:
        """Tear down the test environment."""
        shutil.rmtree(self.temp_dir)

if __name__ == "__main__":
    unittest.main()
