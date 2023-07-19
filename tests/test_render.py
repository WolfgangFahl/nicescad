'''
Created on 2023-07-19

@author: wf
'''
from tests.basetest import Basetest


class Test(Basetest):
    """
    test rendering
    """


    def testRender(self):
        """
        """
        scad_cmds="c=cylinder(r=5,h=2)"
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()