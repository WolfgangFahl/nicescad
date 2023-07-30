'''
Created on 2023-07-23

@author: wf
'''
from tests.basetest import Basetest
from nicescad.file_selector import FileSelector
from nicescad.webserver import WebServer
import json

class TestFileSelector(Basetest):
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
            print(json.dumps(file_selector.tree_structure, indent=2))
        self.assertTrue("id" in file_selector.tree_structure)
        sample_id="1.1.1.1"
        node=file_selector.find_node_by_id(file_selector.tree_structure,sample_id)
        if debug:
            print(json.dumps(node,indent=2))
        self.assertIsNotNone(node)
        for key in ["id","label","value"]:
            self.assertTrue(key in node)