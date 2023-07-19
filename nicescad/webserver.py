"""
Created on 2023-06-19

@author: wf
"""
from typing import List, Optional
from nicescad.version import Version

from nicegui import ui
 
class WebServer:
    """
    webserver
    """

    def __init__(self):
        """
        constructor
        """
        pass
    
    @staticmethod
    def menu():
        ui.link('nicescad on GitHub', 'https://github.com/WolfgangFahl/nicescad')
       
    @ui.page('/')
    @staticmethod
    def home():
        WebServer.menu()
    
    @ui.page('/settings')
    @staticmethod
    def settings():
        WebServer.menu()
        

    @ui.page('/scholar')
    @staticmethod
    def scholar():
        WebServer.menu()
       
  
    def run(self, host, port):
        """
        run the ui
        """
        ui.run(title=Version.name, host=host, port=port, reload=False)
