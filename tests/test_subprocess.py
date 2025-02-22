"""
Created on 2023-07-24

@author: wf
"""

from nicescad.process import Subprocess
from tests.basetest import Basetest


class TestSubprocess(Basetest):
    """
    test subprocess wrapper
    """

    def testPython(self):
        """
        test running a python command
        """
        # path="/opt/local/bin"
        cmd = [f"python", "--version"]
        subprocess = Subprocess.run(cmd)
        debug = True
        if debug:
            print(subprocess)
        self.assertEqual(0, subprocess.returncode)
