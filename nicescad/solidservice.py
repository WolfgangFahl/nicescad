"""
Created on 2023-07-30

@author: wf
"""
import argparse

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from solid2 import *
from starlette.responses import HTMLResponse

import nicescad as nicescad


class SolidConverter:
    """
    Class for conversion of Python code to OpenSCAD code.
    """

    def __init__(self, python_code):
        self.python_code = python_code

    def convert_to_openscad(self):
        """
        Function to convert the input Python code into OpenSCAD code using SolidPython

        Returns:
        str -- OpenSCAD code
        """
        d = eval(self.python_code)
        openscad_code = scad_render(d)
        return openscad_code


class Item(BaseModel):
    python_code: str


class FastAPIServer:
    """
    Class for FastAPI server.
    """

    def __init__(self):
        self.app = FastAPI()
        self.app.post("/convert/")(self.convert)
        self.app.get("/version/")(self.version)
        self.app.get("/", response_class=HTMLResponse)(self.home)

    async def home(self):
        """
        Endpoint to return the homepage with links.

        Returns:
        str -- HTML content
        """
        return """
        <html>
            <head>
                <title>Nicescad solidpython converter service</title>
            </head>
            <body>
                <h1>Welcome to the nicescad solidpython to scad converter</h1>
                <ul>
                    <li><a href="/version/">Check the version of nicescad</a></li>
                    <li><a href="https://github.com/WolfgangFahl/nicescad/issues/28">nicescad GitHub issue</a></li>
                </ul>
            </body>
        </html>
        """

    async def version(self):
        """
        Endpoint to return the version of the nicescad package.

        Returns:
        dict -- the version
        """
        return {"version": nicescad.__version__}

    async def convert(self, item: Item):
        """
        Endpoint to convert Python code to OpenSCAD code.

        Arguments:
        item: Item -- input Python code

        Returns:
        dict -- the OpenSCAD code
        """
        converter = SolidConverter(item.python_code)
        openscad_code = converter.convert_to_openscad()
        return {"openscad_code": openscad_code}


def main():
    parser = argparse.ArgumentParser(
        description="Convert Python code to OpenSCAD code."
    )
    parser.add_argument(
        "--python_code", help="Python code to convert to OpenSCAD code."
    )
    parser.add_argument(
        "--file", help="File containing Python code to convert to OpenSCAD code."
    )
    parser.add_argument(
        "--serve", action="store_true", help="Start the FastAPI server."
    )
    parser.add_argument(
        "--host", default="0.0.0.0", help="Host address to bind the server to."
    )
    parser.add_argument(
        "--port", default=8000, type=int, help="Port number to bind the server to."
    )

    args = parser.parse_args()

    if args.serve:
        server = FastAPIServer()
        uvicorn.run(server.app, host="0.0.0.0", port=8000)
    else:
        if args.file:
            with open(args.file, "r") as f:
                python_code = f.read()
        elif args.python_code:
            python_code = args.python_code
        else:
            raise ValueError("Either python_code or file must be provided.")

        converter = SolidConverter(python_code)
        print(converter.convert_to_openscad())


if __name__ == "__main__":
    main()
