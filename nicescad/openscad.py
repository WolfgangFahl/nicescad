"""
Created on 2023-07-19

@author: wf

This module contains the class OpenScad, a wrapper for OpenScad.
"""

from typing import Dict
import tempfile
import os
import platform
from nicescad.process import Subprocess


class OpenScad:
    """
    A wrapper for OpenScad (https://openscad.org/).
    """

    def __init__(self,scad_prepend:str= '',**kw) -> None:
        """
        Initializes the OpenScad object.
        """
        self.scad_prepend=scad_prepend
        self.openscad_exec = None
        self.openscad_tmp_dir = None
        if 'OPENSCAD_EXEC' in os.environ: self.openscad_exec = os.environ['OPENSCAD_EXEC']
        if 'OPENSCAD_TMP_DIR' in os.environ: self.openscad_tmp_dir = os.environ['OPENSCAD_TMP_DIR']
        if self.openscad_tmp_dir is not None:
            self.tmp_dir = self.openscad_tmp_dir
        else:
            self.tmp_dir = tempfile.mkdtemp()
        if 'openscad_exec' in kw: self.openscad_exec = kw['openscad_exec']
        if self.openscad_exec is None:
            self._try_detect_openscad_exec()
        if self.openscad_exec is None:
            raise Exception('openscad exec not found!')
     
    def _try_executable(self, executable_path: str) -> None:
        """
        Checks if the specified path is a file. If it is, sets it as the OpenScad executable.

        Args:
            executable_path (str): The path to the executable file.
        """
        if os.path.isfile(executable_path):
            self.openscad_exec = executable_path
               
    def _try_detect_openscad_exec(self) -> None:
        """
        Tries to find the OpenScad executable on the system.

        References:
            https://github.com/nickc92/ViewSCAD/blob/d4597ff6870316dfaafa4f9ecc8ef62773081c61/viewscad/renderer.py#L206C5-L222C1
        """
        platfm = platform.system()
        if platfm == 'Linux':
            self._try_executable('/usr/bin/openscad')
            if self.openscad_exec is None:
                self._try_executable('/usr/local/bin/openscad')
        elif platfm == 'Darwin':
            self._try_executable('/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD')
        elif platfm == 'Windows':
            self._try_executable(os.path.join(os.environ.get('Programfiles(x86)', 'C:'), 'OpenSCAD\\openscad.exe'))
            self._try_executable(os.path.join(os.environ.get('Programfiles', 'C:'), 'OpenSCAD\\openscad.exe'))

    def render_to_file(self, openscad_str: str, fl_name: str, **kwargs) -> Subprocess:
        """
        Renders an OpenSCAD string to a file.

        Args:
            openscad_str (str): The OpenSCAD code.
            fl_name (str): The name of the output file.
            kwargs: Additional arguments, could be 'dollar_sign_vars' for dollar-sign variables or 'rough' for rough rendering.
        
        Raises:
            Subprocess: the openscad execution result
        """     
        scad_tmp_file = os.path.join(self.tmp_dir, 'tmp.scad')
        with open(scad_tmp_file, 'w') as of:
            of.write(self.scad_prepend)
            of.write(openscad_str)

        # now run openscad to generate stl:
        cmd = [self.openscad_exec, '-o', fl_name, scad_tmp_file]
        result = Subprocess.run(cmd)
        # on success we'll remove the temporary file
        if result.returncode==0:
            if os.path.isfile(scad_tmp_file):
                os.remove(scad_tmp_file)
        else:
            result.scad_tmp_file=scad_tmp_file
        return result
                
    def openscad_str_to_file(self, openscad_str: str, **kwargs) -> Subprocess:
        """
        Renders the OpenSCAD code to a file.
    
        Args:
            openscad_str (str): The OpenSCAD code.
            **kwargs: Additional arguments, could include 'outfile' to specify the output file name.
    
        Returns:
            Subprocess: The result of the subprocess run, encapsulated in a Subprocess object.
        """
        self.saved_umask = os.umask(0o077)
        try:
            if 'outfile' in kwargs:
                openscad_out_file = kwargs['outfile']
            else:
                openscad_out_file = os.path.join(self.tmp_dir, 'tmp.stl')                    
            
            result = self.render_to_file(openscad_str, openscad_out_file, **kwargs)
            
            return result
        finally:
            os.umask(self.saved_umask)

