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
    A class used to manage a web server. 

    ...

    Attributes
    ----------
    oscad : OpenScad
        a helper object for handling OpenScad operations
    home : method
        a method for generating the home page of the web server
    settings : method
        a method for generating the settings page of the web server

    Methods
    -------
    render(click_args):
        Renders the OpenScad string.
    menu():
        Creates a menu with a link to the project's GitHub page.
    home():
        Creates the home page with a 3D viewer and code editor.
    settings():
        Creates the settings page with a menu link.
    run(host, port):
        Runs the UI of the web server.
    """

    def __init__(self):
        """
        Constructs the necessary attributes for the WebServer object.

        Parameters
        ----------
        None
        """
        self.oscad = OpenScad()
        app.add_static_files('/stl', self.oscad.tmp_dir)

        @ui.page('/')
        def home():
            self.home()
            
        @ui.page('/settings')
        def settings():
            self.settings()
 
    
    def render(self, click_args):
        """
        Renders the OpenScad string and updates the 3D scene with the result.

        Parameters
        ----------
        click_args : object
            The click event arguments.
        """
        openscad_str = self.code_area.value
        stl = self.oscad.openscad_str_to_file(openscad_str)
        with self.scene:
            self.scene.stl("/stl/tmp.stl").move(x=-0.5).scale(0.06)
    
    def menu(self):
        """
        Adds a link to the project's GitHub page in the web server's menu.

        Parameters
        ----------
        None
        """
        ui.link('nicescad on GitHub', 'https://github.com/WolfgangFahl/nicescad')
       
    def home(self):
        """
        Generates the home page with a 3D viewer and a code editor.

        Parameters
        ----------
        None
        """
        self.menu()
        with ui.splitter() as splitter:
            with splitter.before:
                with ui.scene(width=1024, height=768) as scene:
                    self.scene = scene
                    scene.spot_light(distance=100, intensity=0.1).move(-10, 0, 10)
            with splitter.after:
                self.code_area = ui.textarea(value='cube(10);').props('clearable')
                ui.button('Render', on_click=self.render)
        
    def settings(self):
        """
        Generates the settings page with a link to the project's GitHub page.

        Parameters
        ----------
        None
        """
        self.menu()
       
  
    def run(self, host: str, port: int):
        """
        Runs the UI of the web server.

        Parameters
        ----------
        host : str
            The host address of the web server.
        port : int
            The port number of the web server.
        """
        ui.run(title=Version.name, host=host, port=port, reload=False)
