'''
Created on 2023-07-19

@author: wf
'''
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
        oscad=OpenScad(openscad_exec="/Users/wf/bin/openscad")
        openscad_str="cube(5);"
        stl=oscad.openscad_str_to_file(openscad_str)
        print(stl)
        pass
        