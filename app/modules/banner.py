import platform
import socket
import multiprocessing
import pyfiglet
import os
from termcolor import colored

class Banner:
    """
    Welcome aboard the Dev-X-io Express!

    Fasten your seat belts and get ready for an exhilarating ride through the cosmos of code.
    This isn't just a shell; it's a spectacle, a symphony of bytes and bits, harmoniously orchestrated to give you
    the performance of a lifetime. From the neon streets of cyberpunk cities to the vast expanse of the digital universe, 
    this is your ticket to a journey like no other.

    So, dear coder, are you ready to embark on an epic quest for code nirvana?
    All aboard the Dev-X-io Express! 🚀
    """

    
    def __init__(self, app_version="v0.0.0"):
        """Initialize the environment details for the banner."""
        self.version = os.environ.get("APP_VERSION", app_version)
        self.basename = os.path.basename(os.getcwd())
        self.banner = pyfiglet.figlet_format(f'Dev-X Input/Output {self.version}', font='digital')
        self.info_color = "green" if os.path.isfile("/helpers/dev-x.io") else "red"

        # Metadata
        self.module_name = "banner"
        self.module_description = "Displays a warm welcome banner."
        self.module_version = "0.1.0"
        self.module_author = "Dev-X-io"
        self.module_license = "MIT"
        self.module_commands = ["show", "list"]
        self.module_subcommands = {}

    def add_arguments(self, subparsers, name, doc):
        """Add arguments for the Banner module."""
        module_parser = subparsers.add_parser(name, help=doc.strip())
        module_subparsers = module_parser.add_subparsers(dest='command', help=f'{name} commands')
        module_subparsers.add_parser("show", help="Display the banner.")
        module_subparsers.add_parser("list", help="List available subcommands.")

    def execute(self, args):
        """Execute the banner display or list subcommands."""
        if args.command == "show":
            self.display()
        elif args.command == "list":
            self.list_subcommands()
        else:
            self.print_help()

    def list_subcommands(self):
        """List available subcommands."""
        print("Available subcommands for banner:")
        for command in self.module_commands:
            print(f"  {command}")

    def print_help(self):
        """Display the help message."""
        print(f"Available commands for {self.module_name}:")
        for command in self.module_commands:
            print(f"  {command}")
        if self.module_subcommands:
            print("\nAvailable subcommands:")
            for command, subcommands in self.module_subcommands.items():
                for subcommand in subcommands:
                    print(f"  {command} {subcommand}")

    def display_system_info(self):
        """Display detailed system information."""
        print(colored("Operating System:", self.info_color), platform.system())
        print(colored("Hostname:", self.info_color), socket.gethostname())
        print(colored("Platform:", self.info_color), platform.platform())
        print(colored("Architecture:", self.info_color), platform.architecture()[0])
        print(colored("Python Version:", self.info_color), platform.python_version())
        print(colored("Number of CPUs:", self.info_color), multiprocessing.cpu_count())
        print(colored("Modules path:", self.info_color), os.path.dirname(os.path.abspath(__file__)))
        
    def display(self):
        """Render the majestic banner for all to behold."""
        print(colored(self.banner, self.info_color))
        
        self.display_system_info()

        print(colored(Banner.__doc__, "green"))

        if not os.path.isfile("/helpers/.devxio"):
            print(colored("Uhoh.. Dev-X-io file absent.\nBrace yourself for the powdered milk experience!\n", 'white'))
        else:
            print(colored("Yes; Dev-X-io file detected!\nHold onto your pants, probably lose you're socks.\nThis app is so universal..\nthings are about to get unreal!\n", 'green'))
