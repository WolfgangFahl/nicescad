"""
Created on 2023-06-19

@author: wf
"""
from typing import List, Optional
from nicescad.version import Version
from nicescad.openscad import OpenScad
from nicescad.local_filepicker import LocalFilePicker
from nicegui import ui, app
from pathlib import Path
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
        self.oscad = OpenScad(scad_prepend="""//https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#$fa,_$fs_and_$fn
// default number o facets for arc generation
$fn=30;""")
        self.code="""// nicescad example
module example() {
  translate([0,0,15]) {
     cube(30,center=true);
     sphere(20);
  }
}
example();"""        
        self.input="example.scad"
        self.is_local=False
        app.add_static_files('/stl', self.oscad.tmp_dir)
        self.log_view=None
        self.do_trace=True
        self.html_view=None

        @ui.page('/')
        def home():
            self.home()
            
        @ui.page('/settings')
        def settings():
            self.settings()
            
            
    def handle_exception(self, e: BaseException, trace: Optional[bool] = False):
        """Handles an exception by creating an error message.

        Args:
            e (BaseException): The exception to handle.
            trace (bool, optional): Whether to include the traceback in the error message. Default is False.
        """
        if trace:
            self.error_msg = str(e) + "\n" + traceback.format_exc()
        else:
            self.error_msg = str(e)
        if self.log_view:
            self.log_view.push(self.error_msg)
        print(self.error_msg,file=sys.stderr)

        
    async def render(self, _click_args):
        """Renders the OpenScad string and updates the 3D scene with the result.

        Args:
            click_args (object): The click event arguments.
        """
        try:
            self.progress_view.visible = True
            ui.notify("rendering ...")
            with self.scene:
                self.scene.clear()
            openscad_str = self.code_area.value
            render_result= await self.oscad.openscad_str_to_file_async(openscad_str)
            # show render result in log
            self.log_view.push(render_result.stderr)
            if render_result.returncode==0:
                ui.notify("stl created ... loading into scene")
                with self.scene:
                    self.scene.stl("/stl/tmp.stl").move(x=0.0).scale(0.1)    
        except BaseException as ex:
            self.handle_exception(ex,self.do_trace)  
        self.progress_view.visible=False  
            
    def do_read_input(self, input_str: str):
        """Reads the given input.

        Args:
            input_str (str): The input string representing a URL or local path.
        """
        if input_str.startswith('http://') or input_str.startswith('https://'):
            response = requests.get(input_str)
            if response.status_code == 200:
                return response.text
            else:
                raise Exception(f'Unable to retrieve data from URL: {input_str}')
        else:
            if os.path.exists(input_str):
                with open(input_str, 'r') as file:
                    return file.read()
            else:
                raise Exception(f'File does not exist: {input_str}')
    
    def read_input(self, input: str):
        """Reads the given input and handles any exceptions.

        Args:
            input (str): The input string representing a URL or local file.
        """
        try:
            self.code = self.do_read_input(input)
            self.input_input.set_value(input)
            self.code_area.set_value(self.code)
            self.log_view.clear()
            self.error_msg = None
        except BaseException as e:
            self.code = None
            self.handle_exception(e, self.do_trace)
            
    def save_file(self):
        """Saves the current code to the last input file, if it was a local path."""
        if self.is_local and self.input:
            with open(self.input, 'w') as file:
                file.write(self.code)
            ui.notify(f"{self.input} saved")
        else:
            raise Exception('No local file to save to')
    
    async def open_file(self) -> None:
        """Opens a Local filer picker dialog and reads the selected input file."""
        if self.is_local:
            pick_list = await LocalFilePicker('~', multiple=False)
            if len(pick_list)>0:
                input_file=pick_list[0]
                ui.notify(f'Opening {input_file}')
                self.read_input(input_file)
    pass

    async def reload_file(self):
        """
        reload the input file
        """
        ui.notify(f"reloading {self.input} ...")
        self.read_input(self.input)
    
    def link_button(self, name: str, target: str, icon_name: str):
        """
        Creates a button with a specified icon that opens a target URL upon being clicked.
    
        Args:
            name (str): The name to be displayed on the button.
            target (str): The target URL that should be opened when the button is clicked.
            icon_name (str): The name of the icon to be displayed on the button.
    
        Returns:
            The button object.
        """
        with ui.button(name,icon=icon_name) as button:
            button.on("click",lambda: (ui.open(target)))
        return button
    
    def tool_button(self,name:str,icon:str,handler:callable):
        """
        Creates an icon button that triggers a specified function upon being clicked.
    
        Args:
            name (str): The name of the button (not displayed, but could be used for identification).
            icon (str): The name of the icon to be displayed on the button.
            handler (function): The function to be called when the button is clicked.
    
        Returns:
            The icon button object.
            
        valid icons may be found at:    
            https://fonts.google.com/icons
        """
        icon=ui.icon(icon, color='primary').classes('text-4xl').tooltip(name).on("click",handler=handler)  
        return icon   
    
    def setup_pygments(self):
        """
        prepare pygments syntax highlighting by loading style
        """
        pygments_css_file=(Path(__file__).parent / 'web'/'static' / 'css'/ 'pygments.css')
        pygments_css= pygments_css_file.read_text()
        ui.add_head_html(f"<style>{pygments_css}</style>")
 
        
    def setup_menu(self):
        """Adds a link to the project's GitHub page in the web server's menu."""
        with ui.header() as self.header:
            self.link_button("home","/","home")
            self.link_button("settings","/settings","settings")
            self.link_button("github",Version.cm_url,"bug_report")
            self.link_button("chat",Version.chat_url,"chat")
            self.link_button("help",Version.doc_url,"help")
    
    def setup_footer(self):
        """
        setup the footer
        """
        with ui.footer() as self.footer:
            ui.label("(c)2023 Wolfgang Fahl")
            ui.link("Powered by nicegui","https://nicegui.io/").style("color: #fff") 
  
    def input_changed(self,cargs):
        """
        react on changed input
        """
        self.input=cargs.value
        pass
    
    def code_changed(self,cargs):
        """
        react on changed code
        """
        self.code=cargs.value
        pass
    
    def highlight_code(self,_cargs):
        """
        highlight the code and show the html 
        """
        try:
            if self.code_area.visible:
                self.code_area.visible=False
                code_html=self.oscad.highlight_code(self.code)
                self.html_view.content=code_html
                self.html_view.visible=True
            else:
                self.html_view.visible=False
                self.code_area.visible=True
        except BaseException as ex:
            self.handle_exception(ex, self.do_trace)
        
    def home(self):
        """Generates the home page with a 3D viewer and a code editor."""
        self.setup_pygments()
        self.setup_menu()
        with ui.column():
            with ui.splitter() as splitter:
                with splitter.before:
                    with ui.scene(width=1024, height=768).classes("w-full") as scene:
                        self.scene = scene
                        scene.spot_light(distance=100, intensity=0.2).move(-10, 0, 10)
                    with splitter.after:
                        with ui.element("div").classes("w-full"):
                            self.input_input=ui.input(
                                value=self.input,
                                on_change=self.input_changed).props("size=100")
                            self.tool_button(name="highlight", icon="colorize", handler=self.highlight_code)    
                            if self.is_local:
                                self.tool_button(name="save",icon="save",handler=self.save_file)
                            self.tool_button(name="reload",icon="refresh",handler=self.reload_file)
                            if self.is_local:
                                self.tool_button(name="open",icon="file_open",handler=self.open_file)
                            self.tool_button(name="render",icon="play_circle",handler=self.render)
                            self.progress_view = ui.spinner('dots', size='lg', color='blue')
                            self.progress_view.visible = False
                            self.code_area = ui.textarea(value=self.code,on_change=self.code_changed).props('clearable').props("rows=25")
                            self.html_view = ui.html()
                            self.html_view.visible=False
                            self.log_view = ui.log(max_lines=20).classes('w-full h-40')        
        self.setup_footer()        
        if self.args.input:
            self.read_input(self.args.input)
        
    def settings(self):
        """Generates the settings page with a link to the project's GitHub page."""
        self.setup_menu()
        v = ui.checkbox('debug with trace', value=True)
        sp_input=ui.textarea("scad prepend",value=self.oscad.scad_prepend).props("cols=80")
        sp_input.bind_value(self.oscad,"scad_prepend")
        self.setup_footer()
       
    def run(self, args):
        """Runs the UI of the web server.

        Args:
            args (list): The command line arguments.
        """
        self.args=args
        self.is_local=args.local
        ui.run(title=Version.name, host=args.host, port=args.port, show=args.client,reload=False)
