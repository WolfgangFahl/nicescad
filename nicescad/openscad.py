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

from pygments.lexer import RegexLexer, bygroups
from pygments.token import *
from pygments import highlight
from pygments.formatters.html import HtmlFormatter

class OpenSCADLexer(RegexLexer):
    """
    Lexer for OpenSCAD, a language for creating solid 3D CAD models.
    
    Attributes:
        name (str): The name of the lexer.
        aliases (list of str): A list of strings that can be used as aliases for the lexer.
        filenames (list of str): A list of strings that define filename patterns that match this lexer.
    """

    name = 'OpenSCAD'
    aliases = ['openscad']
    filenames = ['*.scad']

    tokens = {
        'root': [
            (r'\s+', Text.Whitespace),
            (r'//.*?$', Comment.Single),
            (r'/\*.*?\*/', Comment.Multiline),
            (r'[a-z_][\w]*', Name.Variable),
            (r'\d+', Number.Integer),
            (r'\+\+|--', Operator),
            (r'[=+\-*/%&|^<>!]=?', Operator),
            (r'[\[\]{}();,.]', Punctuation),
            (r'"(\\\\|\\"|[^"])*"', String),
            (r'\b(module|if|else|for|let|echo)\b', Keyword),
            (r'\b(true|false|undef)\b', Keyword.Constant),
            (r'\b(cube|sphere|cylinder|polyhedron|square|circle|polygon|import|scale|resize|color|offset|minkowski|hull|render|surface|rotate|translate|mirror|multmatrix|projection|rotate_extrude|linear_extrude)\b', Name.Builtin),
        ],
    }

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
        
    def highlight_code(self, code: str) -> str:
        """
        Highlights the provided OpenSCAD code and returns the highlighted code in HTML format.
    
        Args:
            code (str): The OpenSCAD code to highlight.
    
        Returns:
            str: The input OpenSCAD code, highlighted and formatted as an HTML string.
        """
        html = highlight(code, OpenSCADLexer(), HtmlFormatter())
        return html

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


    def write_to_tmp_file(self, openscad_str: str):
        """
        Writes an OpenSCAD string to a temporary file.

        Args:
            openscad_str (str): The OpenSCAD code.
        
        Returns:
            scad_tmp_file: The temporary file path.
        """
        scad_tmp_file = os.path.join(self.tmp_dir, 'tmp.scad')
        with open(scad_tmp_file, 'w') as of:
            of.write(self.scad_prepend)
            of.write(openscad_str)
        return scad_tmp_file

    async def render_to_file_async(self, openscad_str: str, fl_name: str) -> Subprocess:
        """
        Asynchronously renders an OpenSCAD string to a file.

        Args:
            openscad_str (str): The OpenSCAD code.
            fl_name (str): The name of the output file.
        
        Raises:
            Subprocess: the openscad execution result
        """
        scad_tmp_file = self.write_to_tmp_file(openscad_str)

        # now run openscad to generate stl:
        cmd = [self.openscad_exec, '-o', fl_name, scad_tmp_file]
        result = await Subprocess.run_async(cmd)

        self.cleanup_tmp_file(result, scad_tmp_file)
        return result

    def render_to_file(self, openscad_str: str, fl_name: str) -> Subprocess:
        """
        Renders an OpenSCAD string to a file.

        Args:
            openscad_str (str): The OpenSCAD code.
            fl_name (str): The name of the output file.
        
        Raises:
            Subprocess: the openscad execution result
        """
        scad_tmp_file = self.write_to_tmp_file(openscad_str)

        # now run openscad to generate stl:
        cmd = [self.openscad_exec, '-o', fl_name, scad_tmp_file]
        result = Subprocess.run(cmd)

        self.cleanup_tmp_file(result, scad_tmp_file)
        return result

    def cleanup_tmp_file(self, result, scad_tmp_file):
        """
        Cleanup temporary files after subprocess execution.

        Args:
            result (Subprocess): The result of the subprocess execution.
            scad_tmp_file (str): The path to the temporary file.
        """
        if result.returncode == 0:
            if os.path.isfile(scad_tmp_file):
                os.remove(scad_tmp_file)
        else:
            result.scad_tmp_file = scad_tmp_file

    async def openscad_str_to_file_async(self, openscad_str: str, **kwargs) -> Subprocess:
        """
        Asynchronously renders the OpenSCAD code to a file.
    
        Args:
            openscad_str (str): The OpenSCAD code.
            **kwargs: Additional arguments, could include 'outfile' to specify the output file name.
    
        Returns:
            Subprocess: The result of the subprocess run, encapsulated in a Subprocess object.
        """
        return await self.render_cleanup_wrapper(self.render_to_file_async, openscad_str, **kwargs)

    def openscad_str_to_file(self, openscad_str: str, **kwargs) -> Subprocess:
        """
        Renders the OpenSCAD code to a file.
    
        Args:
            openscad_str (str): The OpenSCAD code.
            **kwargs: Additional arguments, could include 'outfile' to specify the output file name.
    
        Returns:
            Subprocess: The result of the subprocess run, encapsulated in a Subprocess object.
        """
        return self.render_cleanup_wrapper(self.render_to_file, openscad_str, **kwargs)

    def render_cleanup_wrapper(self, render_func, openscad_str: str, **kwargs):
        """
        Wrapper function to perform rendering and cleanup tasks.

        Args:
            render_func (function): The rendering function to use (either synchronous or asynchronous).
            openscad_str (str): The OpenSCAD code.
            **kwargs: Additional arguments, could include 'outfile' to specify the output file name.

        Returns:
            result: The result of the rendering function.
        """
        self.saved_umask = os.umask(0o077)
        try:
            if 'outfile' in kwargs:
                openscad_out_file = kwargs['outfile']
            else:
                openscad_out_file = os.path.join(self.tmp_dir, 'tmp.stl')                    

            result = render_func(openscad_str, openscad_out_file, **kwargs)

            return result
        finally:
            os.umask(self.saved_umask)

