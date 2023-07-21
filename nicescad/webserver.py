"""
Created on 2023-06-19

@author: wf
"""
from typing import List, Optional
from nicescad.version import Version
from nicescad.openscad import OpenScad
from nicescad.local_filepicker import LocalFilePicker
from nicegui import ui, app
import os
import sys
import requests
import traceback

class WebServer:
    """WebServer class that manages the server and handles OpenScad operations.

    Attributes:
        oscad (OpenScad): An OpenScad object that aids in performing OpenScad operations.
    """

    def __init__(self):
        """Constructs all the necessary attributes for the WebServer object."""
        self.oscad = OpenScad()
        self.code="""c=cube(3;center=true);
s=sphere(2,center=true);"""        
        self.input="example.stl"
        self.is_local=True
        app.add_static_files('/stl', self.oscad.tmp_dir)
        self.error_area=None
        self.do_trace=True

        @ui.page('/')
        def home():
            self.home()
            
        @ui.page('/settings')
        def settings():
            self.settings()
            
            
    def handle_exception(self, e: Exception, trace: Optional[bool] = False):
        """Handles an exception by creating an error message.

        Args:
            e (Exception): The exception to handle.
            trace (bool, optional): Whether to include the traceback in the error message. Default is False.
        """
        if trace:
            self.error_msg = str(e) + "\n" + traceback.format_exc()
        else:
            self.error_msg = str(e)
        if self.error_area:
            self.error_area.text=self.error_msg
        print(self.error_msg,file=sys.stderr)

 
    def render(self, click_args):
        """Renders the OpenScad string and updates the 3D scene with the result.

        Args:
            click_args (object): The click event arguments.
        """
        openscad_str = self.code_area.value
        stl = self.oscad.openscad_str_to_file(openscad_str)
        with self.scene:
            self.scene.clear()
            self.scene.stl("/stl/tmp.stl").move(x=-0.5).scale(0.06)
            
    def do_read_input(self, input: str):
        """Reads the given input.

        Args:
            input (str): The input string representing a URL or local path.
        """
        if input.startswith('http://') or input.startswith('https://'):
            response = requests.get(input)
            if response.status_code == 200:
                return response.text
            else:
                raise Exception(f'Unable to retrieve data from URL: {input}')
        else:
            if os.path.exists(input):
                with open(input, 'r') as file:
                    return file.read()
            else:
                raise Exception(f'File does not exist: {input}')
    
    def read_input(self, input: str):
        """Reads the given input and handles any exceptions.

        Args:
            input (str): The input string representing a URL or local file.
        """
        self.input=input
        try:
            self.code = self.do_read_input(input)
            self.error_msg = None
        except Exception as e:
            self.code = None
            self.handle_exception(e, self.do_trace)
            
    def save_file(self):
        """Saves the current code to the last input file, if it was a local path."""
        if self.is_local and self.input:
            with open(self.input, 'w') as file:
                file.write(self.code)
        else:
            raise Exception('No local file to save to')
    
    async def open_file(self) -> None:
        """Opens a dialog."""
        result = await LocalFilePicker('~', multiple=True)
        ui.notify(f'You chose {result}')
    pass
    
    def menu(self):
        """Adds a link to the project's GitHub page in the web server's menu."""
        ui.link('nicescad on GitHub', 'https://github.com/WolfgangFahl/nicescad')
        with ui.row().classes('w-full items-center'):
            result = ui.label().classes('mr-auto')
            with ui.button(icon='menu'):
                with ui.menu() as menu:
                    ui.menu_item('Open', self.open_file)
                    ui.menu_item('Save', self.save_file)
                    ui.separator()
                    ui.menu_item('Close', on_click=menu.close)
       
    def home(self):
        """Generates the home page with a 3D viewer and a code editor."""
        self.menu()
        with ui.splitter() as splitter:
            with splitter.before:
                with ui.scene(width=1024, height=768) as scene:
                    self.scene = scene
                    scene.spot_light(distance=100, intensity=0.1).move(-10, 0, 10)
            with splitter.after:
                self.input_input=ui.input(value=self.input)
                self.code_area = ui.textarea(value=self.code).props('clearable;rows=20')
                self.error_area = ui.textarea()
                ui.button('Render', on_click=self.render)
        if self.args.input:
            self.read_input(self.args.input)
  
        
    def settings(self):
        """Generates the settings page with a link to the project's GitHub page."""
        self.menu()
       
    def run(self, args):
        """Runs the UI of the web server.

        Args:
            args (list): The command line arguments.
        """
        self.args=args
        ui.run(title=Version.name, host=args.host, port=args.port, reload=False)
