"""
Created on 2023-06-19

@author: wf
"""

import os
import uuid
from pathlib import Path

from ngwidgets.file_selector import FileSelector
from ngwidgets.input_webserver import InputWebserver, InputWebSolution
from ngwidgets.local_filepicker import LocalFilePicker
from ngwidgets.scene_frame import SceneFrame
from ngwidgets.short_url import ShortUrl
from ngwidgets.webserver import WebserverConfig
from nicegui import Client, app, ui

from nicescad.openscad import OpenScad
from nicescad.version import Version


class NiceScadWebServer(InputWebserver):
    """WebServer class that manages the server and handles OpenScad operations.

    Attributes:
        oscad (OpenScad): An OpenScad object that aids in performing OpenScad operations.
    """

    @classmethod
    def get_config(cls) -> WebserverConfig:
        copy_right = "(c)2023-2025 Wolfgang Fahl"
        config = WebserverConfig(
            copy_right=copy_right,
            version=Version(),
            default_port=9858,
            short_name="nicescad",
        )
        server_config = WebserverConfig.get(config)
        server_config.solution_class = NiceScadSolution
        return server_config

    def __init__(self):
        """Constructs all the necessary attributes for the WebServer object."""
        InputWebserver.__init__(self, config=NiceScadWebServer.get_config())
        self.oscad = OpenScad(
            scad_prepend="""//https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#$fa,_$fs_and_$fn
// default number of facets for arc generation
$fn=30;
"""
        )
        self.design_dir = Path.home() / ".nicescad" / "designs"
        self.design_dir.mkdir(parents=True, exist_ok=True)
        app.add_static_files("/stl", self.oscad.tmp_dir)
        app.add_static_files("/designs", self.design_dir)
        self.short_url = ShortUrl(
            base_path=self.design_dir,
            suffix=".scad",
            required_keywords=["module", "// Copyright Wolfgang Fahl"],
            lenient=True,
        )

        @ui.page("/design/{short_id}")
        async def show_design(short_id: str, client: Client):
            return await self.page(client, NiceScadSolution.show_design, short_id)

    def configure_run(self):
        root_path = (
            self.args.root_path
            if self.args.root_path
            else NiceScadWebServer.examples_path()
        )
        self.root_path = os.path.abspath(root_path)
        self.allowed_urls = [
            "https://raw.githubusercontent.com/WolfgangFahl/nicescad/main/examples/",
            "https://raw.githubusercontent.com/openscad/openscad/master/examples/",
            self.examples_path(),
            self.root_path,
        ]

    @classmethod
    def examples_path(cls) -> str:
        # the root directory (default: examples)
        path = os.path.join(os.path.dirname(__file__), "../nicescad_examples")
        path = os.path.abspath(path)
        return path


class NiceScadSolution(InputWebSolution):
    """
    the NiceScad solution
    """

    def __init__(self, webserver: NiceScadWebServer, client: Client):
        """
        Initialize the solution

        Calls the constructor of the base solution
        Args:
            webserver (NiceScadWebServer): The webserver instance associated with this context.
            client (Client): The client instance this context is associated with.
        """
        super().__init__(webserver, client)  # Call to the superclass constructor
        self.input = "example.scad"
        self.stl_name = f"nicescad_{uuid.uuid4().hex}.stl"
        self.do_trace = True
        self.html_view = None
        self.oscad = webserver.oscad
        self.code = """// nicescad example
module example() {
  translate([0,0,15]) {
     cube(30,center=true);
     sphere(20);
  }
}
example();"""

    async def render(self, _click_args=None):
        """Renders the OpenScad string and updates the 3D scene with the result.

        Args:
            click_args (object): The click event arguments.
        """
        try:
            self.progress_view.visible = True
            ui.notify("rendering ...")
            with self.scene:
                self.stl_link.visible = False
                self.scene_frame.color_picker_button.disable()
            openscad_str = self.code
            stl_path = stl_path = os.path.join(self.oscad.tmp_dir, self.stl_name)
            if os.path.exists(stl_path):
                os.remove(stl_path)
            render_result = await self.oscad.openscad_str_to_file(
                openscad_str, stl_path
            )
            if render_result.returncode == 0:
                ui.notify("stl created ... loading into scene")
                self.stl_link.visible = True
                self.scene_frame.clear()
                # avoid caching
                stl_url=f"/stl/{self.stl_name}?v={uuid.uuid4().hex}"
                self.scene_frame.load_stl(
                    stl_name=self.stl_name, url=stl_url, scale=0.1
                )
                self.scene_frame.update()
            else:
                ui.notify(
                    f"failed to create stl return code {render_result.returncode}"
                )
            # show render result in log
            self.log_view.push(render_result.stderr)
        except BaseException as ex:
            self.handle_exception(ex, self.do_trace)
        self.progress_view.visible = False

    def read_input(self, input_str: str):
        """Reads the given input and handles any exceptions.

        Args:
            input_str (str): The input string representing a URL or local file.
        """
        try:
            ui.notify(f"reading {input_str}")
            self.code = self.do_read_input(input_str)
            self.input_input.set_value(input_str)
            self.log_view.clear()
            self.error_msg = None
            self.stl_link.visible = False
        except BaseException as e:
            self.code = None
            self.handle_exception(e)

    def save_file(self):
        """Saves the current code to the last input file, if it was a local path."""
        if self.is_local and self.input:
            with open(self.input, "w") as file:
                file.write(self.code)
            ui.notify(f"{self.input} saved")
        else:
            raise Exception("No local file to save to")

    def create_short_url(self):
        """
        Create a short URL ID for the current code and store it via ShortUrl.

        Shows debug output and UI notifications with the generated ID and storage path.
        """
        try:
            msg = self.webserver.short_url.validate_code(self.code)
            if msg:
                ui.notify(msg)
            else:
                short_id = self.webserver.short_url.save(self.code)
                ui.notify(f"✅ short id: {short_id} created")
                url = f"/design/{short_id}"
                ui.navigate.to(url)

        except Exception as ex:
            self.handle_exception(ex, self.do_trace)

    async def open_file(self) -> None:
        """Opens a Local filer picker dialog and reads the selected input file."""
        if self.is_local:
            pick_list = await LocalFilePicker("~", multiple=False)
            if len(pick_list) > 0:
                input_file = pick_list[0]
                await self.read_and_optionally_render(input_file)

    pass

    async def clear(self):
        self.scene_frame.clear()
        self.scene_frame.update()

    def setup_pygments(self):
        """
        prepare pygments syntax highlighting by loading style
        """
        pygments_css_file = (
            Path(__file__).parent / "web" / "static" / "css" / "pygments.css"
        )
        pygments_css = pygments_css_file.read_text()
        ui.add_head_html(f"<style>{pygments_css}</style>")

    async def code_changed(self, _cargs):
        """
        react on changed code
        """
        ui.notify("code changed")

    async def highlight_code(self, _cargs):
        """
        highlight the code and show the html
        """
        try:
            if self.code_area.visible:
                self.code_area.visible = False
                code_html = self.oscad.highlight_code(self.code)
                self.html_view.content = code_html
                self.html_view.visible = True
            else:
                self.html_view.visible = False
                self.code_area.visible = True
            self.toggle_icon(self.highlight_button)
        except BaseException as ex:
            self.handle_exception(ex, self.do_trace)

    def prepare_ui(self):
        """
        handle the command line arguments
        """
        InputWebSolution.prepare_ui(self)
        self.setup_pygments()

    def setup_ui(self):
        """
        setup the ui
        """
        with ui.column():
            with ui.splitter() as splitter:
                with splitter.before:
                    self.scene_frame = SceneFrame(self)
                    self.scene_frame.setup_button_row()
                    with ui.scene(width=1024, height=768).classes("w-full") as scene:
                        self.scene = scene
                        self.scene_frame.scene = scene
                        scene.spot_light(distance=100, intensity=0.2).move(-10, 0, 10)
                    with splitter.after:
                        with ui.element("div").classes("w-full"):
                            extensions = {"scad": ".scad", "xml": ".xml"}
                            self.example_selector = FileSelector(
                                path=self.root_path,
                                handler=self.read_and_optionally_render,
                                extensions=extensions,
                            )
                            self.input_input = ui.input(
                                value=self.input, on_change=self.input_changed
                            ).props("size=100")
                            self.highlight_button = self.tool_button(
                                tooltip="highlight",
                                icon="html",
                                toggle_icon="code",
                                handler=self.highlight_code,
                            )
                            if self.is_local:
                                self.tool_button(
                                    tooltip="save", icon="save", handler=self.save_file
                                )
                            else:
                                self.tool_button(
                                    tooltip="create short_url",
                                    icon="save",
                                    handler=self.create_short_url,
                                )
                            self.tool_button(
                                tooltip="reload",
                                icon="refresh",
                                handler=self.reload_file,
                            )
                            self.tool_button(
                                tooltip="clear",
                                icon="clear",
                                handler=self.clear,
                            )
                            if self.is_local:
                                self.tool_button(
                                    tooltip="open",
                                    icon="file_open",
                                    handler=self.open_file,
                                )
                            self.tool_button(
                                tooltip="render",
                                icon="play_circle",
                                handler=self.render,
                            )
                            self.stl_link = ui.link(
                                "stl result", f"/stl/{self.stl_name}", new_tab=True
                            )
                            self.stl_link.visible = False
                            self.progress_view = ui.spinner(
                                "dots", size="lg", color="blue"
                            )
                            self.progress_view.visible = False
                            self.code_area = (
                                ui.textarea(on_change=self.code_changed)
                                .bind_value(self, "code")
                                .props("clearable")
                                .props("rows=25")
                            )
                            self.html_view = ui.html()
                            self.html_view.visible = False
                            self.log_view = ui.log(max_lines=20).classes("w-full h-40")

    async def show_design(self, short_id: str):
        def show():
            try:
                self.setup_ui()
                self.code = self.webserver.short_url.load(short_id)
            except Exception as _ex:
                ui.notify(f"invalid design {short_id}")

        await self.setup_content_div(show)

    async def home(self):
        """Generates the home page with a 3D viewer and a code editor."""

        def show():
            self.setup_ui()

        await self.setup_content_div(show)

    def configure_settings(self):
        """Generates the settings page with a link to the project's GitHub page."""
        sp_input = ui.textarea("scad prepend", value=self.oscad.scad_prepend).props(
            "cols=80"
        )
        sp_input.bind_value(self.oscad, "scad_prepend")
