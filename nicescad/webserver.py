"""
Created on 2023-06-19

@author: wf
"""
from typing import List, Optional
from nicescad.version import Version
from nicescad.openscad import OpenScad

from nicegui import ui, app
 
class WebServer:
    """
    webserver
    """

    def __init__(self):
        """
        constructor
        """
        self.oscad=OpenScad()
        app.add_static_files('/stl', self.oscad.tmp_dir)
        pass
    
        @ui.page('/')
        def home():
            self.home()
            
        @ui.page('/settings')
        def settings():
            self.settings()
 
    
    def render(self,click_args):
        """
        render the openscad str
        """
        openscad_str=self.code_area.value
        stl=self.oscad.openscad_str_to_file(openscad_str)
        self.scene.stl("/stl/tmp.stl").move(x=-0.5).scale(0.06)
        pass
    
    def menu(self):
        ui.link('nicescad on GitHub', 'https://github.com/WolfgangFahl/nicescad')
       
    def home(self):
        self.menu()
        with ui.splitter() as splitter:
            with splitter.before:
                self.code_area = ui.textarea(value='cube(5);').props('clearable')
                ui.button('Render', on_click=self.render)
            with splitter.after:
                with ui.scene(width=1024, height=768) as scene:
                    self.scene=scene
                    scene.spot_light(distance=100, intensity=0.1).move(-10, 0, 10)
                    teapot = 'https://upload.wikimedia.org/wikipedia/commons/9/93/Utah_teapot_(solid).stl'
                    scene.stl(teapot).scale(0.2).move(-3, 4)
        
    def settings(self):
        self.menu()
       
  
    def run(self, host, port):
        """
        run the ui
        """
        ui.run(title=Version.name, host=host, port=port, reload=False)
