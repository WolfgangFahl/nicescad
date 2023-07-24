'''
Created on 2023-07-19

@author: wf
'''
import asyncio
import os
from tests.basetest import Basetest
from nicescad.openscad import OpenScad

class TestOpenScad(Basetest):
    """
    test openscad wrapper
    """
    
    def test_detect_openscad_exec(self):
        """
        test finding the openscad executable
        """
        oscad=OpenScad()
        self.assertTrue(oscad.openscad_exec is not None)
        
    def testRender(self):
        """
        test rendering a scad file
        """
        # openscad_exec="/Users/wf/bin/openscad"
        oscad=OpenScad()
        openscad_str="cube(5);"
        stl_path = os.path.join(oscad.tmp_dir, 'cube5.stl') 
        subprocess=asyncio.run(oscad.openscad_str_to_file(openscad_str,stl_path))
        debug=self.debug
        #debug=True
        if debug:
            print(subprocess)
        self.assertEqual(0,subprocess.returncode)
        self.assertEqual(stl_path,subprocess.stl_path)
        self.assertTrue(os.path.isfile(stl_path))
        pass
    
    def test_highlight_code(self):
        """
        Tests the 'highlight_code' function by checking if the output starts with 
        the standard beginning of an HTML string outputted by Pygments.
        
        This test case assumes the presence of a '<div' tag at the start of the 
        HTML string, which is standard for Pygments' HtmlFormatter. Adjust the 
        test case as necessary if you're using a different formatter or 
        configuration.
        
        Reference: https://github.com/WolfgangFahl/nicescad/issues/12
        
        """
        oscad=OpenScad()
        test_code = 'module test() { echo("Hello, world!"); }'
        highlighted_code = oscad. highlight_code(test_code)
        debug=self.debug
        if debug:
            print(highlighted_code)
        self.assertTrue(highlighted_code.startswith('<div'))