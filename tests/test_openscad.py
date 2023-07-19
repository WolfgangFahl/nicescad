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
        oscad.try_detect_openscad_exec()
        self.assertTrue(oscad.openscad_exec is not None)
        