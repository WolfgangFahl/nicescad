class AxesHelper:
    """
    A Python class for creating a 3D helper for visualizing the axes in a scene.
    This class is designed to be used with the `nicegui` library (https://pypi.org/project/nicegui/)
    for creating 3D scenes. It creates line objects for the x, y, and z axes,
    each with a distinct color, and provides a method for changing these colors.

    Original JavaScript code refactored into Python and authored by: OpenAI's ChatGPT
    Original JavaScript code can be found at: https://raw.githubusercontent.com/mrdoob/three.js/master/src/helpers/AxesHelper.js

    For the refactoring, following prompts were given:
    1. Refactor a JavaScript class for handling ThreeJS scenes into a Python class using the `nicegui` library.
    2. The class should allow to hide/show axes.
    3. Usage of `nicegui` library's API for the colors.
    4. Include Google docstrings and type hints to the code.
    5. The scene should be a constructor parameter to be remembered.

    Attributes:
        size (float): The size of the axes to be drawn.
        scene (ui.scene): The scene where the axes will be drawn.

    Usage:
        scene = ui.scene().classes('w-full h-64')
        axes_helper = AxesHelper(scene, size=10.0)
        axes_helper.set_colors('#FF0000', '#00FF00', '#0000FF') # set colors for x, y, and z axes

    """
    def __init__(self, scene: "ui.scene", size: float = 10):
        """
        The constructor for AxesHelper class.

        Args:
            scene (ui.scene): The scene where the axes will be drawn.
            size (float): The size of the axes to be drawn.
        """
        self.scene = scene
        self.vertices = [
            (0, 0, 0),    (size, 0, 0),
            (0, 0, 0),    (0, size, 0),
            (0, 0, 0),    (0, 0, size)
        ]

        # red / green / blue
        self.colors = ['#FF0000', '#00FF00', '#0000FF']
        self.lines = []

        # Draw lines in the scene to represent axes
        with self.scene as scene:
            for i in range(0, len(self.vertices), 2):
                color_index=i//2
                self.lines.append(scene.line(self.vertices[i], self.vertices[i+1]).material(self.colors[color_index]))
            scene.update()    

    def set_colors(self, x_axis_color: str, y_axis_color: str, z_axis_color: str):
        """
        A method to set colors of the axes.

        Args:
            x_axis_color (str): Color of the x-axis.
            y_axis_color (str): Color of the y-axis.
            z_axis_color (str): Color of the z-axis.
        """
        self.lines[0].material(x_axis_color)
        self.lines[1].material(y_axis_color)
        self.lines[2].material(z_axis_color)
