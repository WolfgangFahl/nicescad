import asyncio
import subprocess
from dataclasses import dataclass
from typing import List, Optional, Awaitable

@dataclass
class Subprocess:
    """A class representing a subprocess execution result."""

    stdout: str
    stderr: str
    cmd: List[str]
    returncode: int
    exception: Optional[BaseException] = None

    @staticmethod
    async def run_async(cmd: List[str])->Awaitable["Subprocess"]:
        """
        Asynchronously runs a command as a subprocess and returns the result as an instance of this class.
        
        Args:
            cmd (List[str]): The command to run.

        Returns:
            Subprocess: An instance of this class representing the result of the subprocess execution.
        """
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await proc.communicate()
    
            subprocess=Subprocess(
                stdout=stdout.decode(), 
                stderr=stderr.decode(), 
                cmd=cmd, 
                returncode=proc.returncode
            )
        except BaseException as ex:
            subprocess=Subprocess(stdout='', stderr=str(ex), cmd=cmd, returncode=-1, exception=ex)
        return subprocess    

    @staticmethod
    def run(cmd: List[str])->"Subprocess":
        """
        Runs a command as a subprocess and returns the result as an instance of this class.
        
        Args:
            cmd (List[str]): The command to run.

        Returns:
            Subprocess: An instance of this class representing the result of the subprocess execution.
        """
        subprocess=asyncio.run(Subprocess.run_async(cmd))
        return subprocess
