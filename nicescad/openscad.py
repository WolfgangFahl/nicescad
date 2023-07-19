'''
Created on 2023-07-19

@author: wf
'''
import platform
import os

class OpenScad(object):
    '''
    wrapper for OpenScad
    https://openscad.org/
    '''

    def __init__(self):
        '''
        Constructor
        '''
     
    def _try_executable(self, executable_path):
        if os.path.isfile(executable_path):
            self.openscad_exec = executable_path
               
    def try_detect_openscad_exec(self):
        """
        try finding the openscad executable
        
        see https://github.com/nickc92/ViewSCAD/blob/d4597ff6870316dfaafa4f9ecc8ef62773081c61/viewscad/renderer.py#L206C5-L222C1
        """
        self.openscad_exec = None
        platfm = platform.system()
        if platfm == 'Linux':
            self._try_executable('/usr/bin/openscad')
            if self.openscad_exec is None:
                self._try_executable('/usr/local/bin/openscad')
        elif platfm == 'Darwin':
            self._try_executable('/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD')
        elif platfm == 'Windows':
            self._try_executable(os.path.join(
                    os.environ.get('Programfiles(x86)','C:'),
                    'OpenSCAD\\openscad.exe'))
            self._try_executable(os.path.join(
                    os.environ.get('Programfiles','C:'),
                    'OpenSCAD\\openscad.exe'))

        