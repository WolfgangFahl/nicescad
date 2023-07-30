'''
Created on 2023-07-30

@author: wf
'''
import argparse
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from solid2 import *

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
    parser = argparse.ArgumentParser(description="Convert Python code to OpenSCAD code.")
    parser.add_argument("--python_code", help="Python code to convert to OpenSCAD code.")
    parser.add_argument("--file", help="File containing Python code to convert to OpenSCAD code.")
    parser.add_argument("--serve", action="store_true", help="Start the FastAPI server.")
    args = parser.parse_args()

    if args.serve:
        server = FastAPIServer()
        uvicorn.run(server.app, host="0.0.0.0", port=8000)
    else:
        if args.file:
            with open(args.file, 'r') as f:
                python_code = f.read()
        elif args.python_code:
            python_code = args.python_code
        else:
            raise ValueError("Either python_code or file must be provided.")
        
        converter = SolidConverter(python_code)
        print(converter.convert_to_openscad())

if __name__ == '__main__':
    main()
