"""
Created on 2023-07-19

@author: wf

This module contains the class OpenScad, a wrapper for OpenScad.
"""
from typing import Awaitable
import tempfile
import os
import platform
from nicescad.process import Subprocess

from pygments.lexer import RegexLexer
from pygments.token import Comment,Keyword,Name,Number,Operator, Punctuation,String,Text
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

    def write_to_tmp_file(self, openscad_str: str, do_prepend: bool=True):
        """
        Writes an OpenSCAD string to a temporary file. 
    
        The `scad_prepend` string is prepended to the OpenSCAD code before writing, 
        unless the OpenSCAD code contains the string '//!OpenSCAD', or `do_prepend` 
        is set to `False`. In these cases, only the OpenSCAD code is written to the file.
    
        Args:
            openscad_str (str): The OpenSCAD code.
            do_prepend (bool, optional): If `True`, the `scad_prepend` string is 
                                          prepended to the OpenSCAD code. Defaults to `True`.
        
        Returns:
            str: The path to the temporary file where the OpenSCAD code (and 
                 possibly the `scad_prepend` string) was written.
        """
        scad_tmp_file = os.path.join(self.tmp_dir, 'tmp.scad')
        with open(scad_tmp_file, 'w') as of:
            if do_prepend and '//!OpenSCAD' not in openscad_str:
                of.write(self.scad_prepend)
            of.write(openscad_str)
        return scad_tmp_file


    async def render_to_file_async(self, openscad_str: str, stl_path: str) -> Awaitable[Subprocess]:
        """
        Asynchronously renders an OpenSCAD string to a file.

        Args:
            openscad_str (str): The OpenSCAD code.
            stl_path(str): The path to the output file.
        
        Returns:
            Subprocess: the openscad execution result
        """
        scad_tmp_file = self.write_to_tmp_file(openscad_str)

        # now run openscad to generate stl:
        cmd = [self.openscad_exec, '-o', stl_path, scad_tmp_file]
        self.saved_umask = os.umask(0o077)
        result = await Subprocess.run_async(cmd)
        os.umask(self.saved_umask)

        self.cleanup_tmp_file(result, scad_tmp_file)
        result.stl_path=stl_path
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

    async def openscad_str_to_file(self, openscad_str: str, stl_path:str) -> Subprocess:
        """
        Renders the OpenSCAD code to a file.
    
        Args:
            openscad_str (str): The OpenSCAD code.
            stl_path(str): the path to the stl file
    
        Returns:
            Subprocess: The result of the subprocess run, encapsulated in a Subprocess object.
        """
        result=await self.render_to_file_async(openscad_str, stl_path)
        return result
