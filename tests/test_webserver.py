'''
Created on 2023-07-23

@author: wf
'''
from tests.basetest import Basetest
from nicescad.webserver import WebServer, FileSelector
import json

class TestWebServer(Basetest):
    """
    test nicescad WebServer
    """
    
    def test_get_dir_tree(self):
        """
        test getting the directory tree structure for
        the examples directory
        """
        file_selector=FileSelector(WebServer.examples_path(),".scad")
        debug=self.debug
        #debug=True
        if debug:
            print(json.dumps(file_selector.tree_structure, sort_keys=True, indent=2))
        self.assertTrue("id" in file_selector.tree_structure)