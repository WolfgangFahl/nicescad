"""
Unit test for BlockscadConverter class to convert BlockSCAD XML files to SCAD files.

This test is based on the following prompts:
- "Conversion of a BlockSCAD XML file to a SCAD file."
- "Usage of nicescad.blockscad_converter.BlockscadConverter class for conversion."
- "The constructor needs an xml_path parameter."
- "The function to be tested is convert_to_scad with scad_path as the output file parameter."
- "Retrieval of the examples path using WebServer.examples_path() class method from nicescad.webserver."
- "Assumption of the 'blockscad' directory for SCAD input examples."
- "Definition of the unit test setup with paths for the BlockSCAD and SCAD directories."
- "Usage of test.basetest.Basetest as the base class for the test. Using def setUp(self, debug=False, profile=True):"
- "Definition of a test method to iterate over BlockSCAD XML files, convert them to SCAD files, and save in 'blockscad_converted' subdirectory."
- "Usage of a temporary directory for conversion during the test."
- "Comparison of output SCAD file content with the expected SCAD file content."
- "Inclusion of Google docstrings and type hints in the code."
- "Include links to the BlockSCAD editor (https://www.blockscad3d.com/editor/), OpenSCAD (https://openscad.org/), and the target platform (NiceSCAD, http://nicescad.bitplan.com/)."
- "Include the link to the relevant issue: 'support reading and converting blockscad files #23' on http://nicescad.bitplan.com/issue/23"
- "If self.debug is True, print the content of the compared files before doing the check."
- "Count the number of files and check that at least one file was tested."

Links for reference:
- BlockSCAD: https://www.blockscad3d.com/editor/
- OpenSCAD: https://openscad.org/
- Target platform (NiceSCAD): http://nicescad.bitplan.com/
- Issue: Support reading and converting blockcad files #23: http://nicescad.bitplan.com/issues/23

Author: OpenAI ChatGPT
Date: July 25, 2023
"""

import unittest
import tempfile
from tests.basetest import Basetest
from pathlib import Path
from nicescad.webserver import WebServer
from nicescad.blockscad_converter import BlockscadConverter

class TestBlockscadConverter(Basetest):
    def setUp(self, debug=True, profile=True):
        """
        Set up the test environment. Initializes paths for BlockSCAD XML files and expected SCAD files.

        Args:
            debug (bool): If True, prints the compared files before doing the check. Defaults to False.
            profile (bool): If True, the test is profiled. Defaults to True.
        """
        Basetest.setUp(self, debug, profile)
        self.examples_path = WebServer.examples_path()
        self.blockscad_dir = Path(self.examples_path) / 'blockscad'
        self.blockscad_converted_dir = Path(self.examples_path) / 'scad' / 'blockscad_converted'
    
    def compare_strings_ignore_whitespace(self,str1, str2):
        """
        Compares two strings for equality, ignoring any whitespace.
    
        Args:
            str1 (str): The first string to compare.
            str2 (str): The second string to compare.
    
        Returns:
            bool: True if the strings are equal when ignoring whitespace, False otherwise.
        """
        return ''.join(str1.split()) == ''.join(str2.split())
    
    def test_convert_to_scad(self):
        """
        Test the conversion of BlockSCAD XML files to SCAD files. Compares the content of the output SCAD files
        with the expected content.
        """
        if self.inPublicCI():
            return
        # only comment out when really testing since openai API usage
        # has a cost
        return
        blockscad_files = list(self.blockscad_dir.glob('*.xml'))
        self.assertGreater(len(blockscad_files), 0, "No BlockSCAD XML files found for testing.")
        failures=[]
        for xml_file in blockscad_files:
            converter = BlockscadConverter(str(xml_file))
            with tempfile.TemporaryDirectory() as temp_dir:
                scad_file = Path(temp_dir) / (xml_file.stem + '.scad')
                ok=False
                expected_scad_file = self.blockscad_converted_dir / (xml_file.stem + '.scad')
                try:
                    converter.convert_to_scad(str(scad_file))
                    with open(scad_file, 'r') as output_file, open(expected_scad_file, 'r') as expected_file:
                        output_content = output_file.read()
                        expected_content = expected_file.read()
                        ok = self.compare_strings_ignore_whitespace(output_content, expected_content)
                        if not ok:
                            print(f"Output content: \n{output_content}")
                            print(f"Expected content: \n{expected_content}")
                except Exception as ex:
                    print(str(ex))
                    pass            
                if not ok:
                    failures.append(expected_scad_file)
                            
        self.assertEqual(0,len(failures))                

if __name__ == '__main__':
    unittest.main()
