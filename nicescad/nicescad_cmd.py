'''
Created on 2023-07-19

@author: wf
'''
from nicescad.version import Version
import sys
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import traceback
import webbrowser
from nicescad.webserver import WebServer

def getArgParser(description:str,version_msg)->ArgumentParser:
    """
    Setup command line argument parser
    
    Args:
        description(str): the description
        version_msg(str): the version message
        
    Returns:
        ArgumentParser: the argument parser
    """
    parser = ArgumentParser(description=description, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-a","--about",help="show about info [default: %(default)s]",action="store_true")
    parser.add_argument("-c","--client", action="store_true", help="start client [default: %(default)s]")
    parser.add_argument("-d", "--debug", dest="debug", action="store_true", help="show debug info [default: %(default)s]")
    parser.add_argument("-l", "--local", dest="local", action="store_true", help="run with local file system access [default: %(default)s]")
    parser.add_argument("-i", "--input", help="input file")
    parser.add_argument("-rp", "--root_path",default=WebServer.examples_path(),help="path to scad files [default: %(default)s]")

    parser.add_argument("--host", default="localhost",
                            help="the host to serve / listen from [default: %(default)s]")
    parser.add_argument("--port",type=int,default=9858,help="the port to serve from [default: %(default)s]")
    parser.add_argument("-s","--serve", action="store_true", help="start webserver [default: %(default)s]")
    parser.add_argument("-V", "--version", action='version', version=version_msg)
    return parser


def main(argv=None): 
    '''main program.'''

    if argv is None:
        argv=sys.argv[1:]
        
    program_name = Version.name
    program_version =f"v{Version.version}" 
    program_build_date = str(Version.date)
    program_version_message = f'{program_name} ({program_version},{program_build_date})'

    try:
        parser=getArgParser(description=Version.license,version_msg=program_version_message)
        args = parser.parse_args(argv)
        if len(argv) < 1:
            parser.print_usage()
            sys.exit(1)
        if args.about:
            print(program_version_message)
            print(f"see {Version.doc_url}")
            webbrowser.open(Version.doc_url)
        if args.client:
            url=f"http://{args.host}:{args.port}"
            webbrowser.open(url)
        if args.serve:
            ws=WebServer()
            ws.run(args)
        
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 1
    except Exception as e:
        if DEBUG:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        if args.debug:
            print(traceback.format_exc())
        return 2       
        
DEBUG = 1
if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-d")
    sys.exit(main())