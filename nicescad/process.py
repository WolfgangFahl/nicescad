import asyncio
import subprocess
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Subprocess:
    """A class representing a subprocess execution result."""

    stdout: str
    stderr: str
    cmd: List[str]
    returncode: int
    exception: Optional[BaseException] = None

    @staticmethod
    async def run_async(cmd: List[str]):
        """
        Asynchronously runs a command as a subprocess and returns the result as an instance of this class.
        
        Args:
            cmd (List[str]): The command to run.

        Returns:
            Subprocess: An instance of this class representing the result of the subprocess execution.
        """
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await proc.communicate()

        return Subprocess(
            stdout=stdout.decode(), 
            stderr=stderr.decode(), 
            cmd=cmd, 
            returncode=proc.returncode
        )

    @staticmethod
    def run(cmd: List[str]):
        """
        Runs a command as a subprocess and returns the result as an instance of this class.
        
        Args:
            cmd (List[str]): The command to run.

        Returns:
            Subprocess: An instance of this class representing the result of the subprocess execution.
        """
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True)
            return Subprocess(stdout=proc.stdout, stderr=proc.stderr, cmd=cmd, returncode=proc.returncode)
        except subprocess.CalledProcessError as cpe:
            return Subprocess(stdout=cpe.stdout, stderr=cpe.stderr, cmd=cmd, returncode=cpe.returncode, exception=cpe)
        except Exception as e:
            return Subprocess(stdout='', stderr=str(e), cmd=cmd, returncode=-1, exception=e)
