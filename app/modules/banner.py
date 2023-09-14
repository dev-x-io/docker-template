#!/usr/bin/env python3
import platform
import socket
import multiprocessing
import pyfiglet
import os
from termcolor import colored

class Banner:
    """
    The Banner: A warm welcome to your 'g(ood-)host' shell!
    
    Unfurls a splendid banner upon the screen, declaring the presence of the glorious shell
    and any pertinent details of the environment. It's not just about the information, but the presentation!
    """
    
    def __init__(self,app_version="v0.0.0"):
        """Initialize the environment details for the banner."""
        # Fetch the version from an environment variable or use a default value
        self.version = os.environ.get("APP_VERSION", app_version)
        # Fetch the name of the current directory
        self.basename = os.path.basename(os.getcwd())
        # Craft the main banner
        self.banner = pyfiglet.figlet_format(f'Dev-X-io docker shell {self.version}', font='digital')
        # Set the info color based on the presence of the Helper-X.app file
        self.info_color = "green" if os.path.isfile("/helpers/dev-x.io") else "red"


    def add_arguments(self, subparsers, name, doc):
        """Add arguments for the Banner module."""
        
        # Create a parser for this module (e.g., "banner")
        module_parser = subparsers.add_parser(name, help=doc.strip())
        
        # Add subparsers for this module's commands
        module_subparsers = module_parser.add_subparsers(dest='command', help=f'{name} commands')
        
        # Add a subcommand called "show" to the "banner" command
        module_subparsers.add_parser("show", help="Display the banner.")
        
        # Add a default subcommand called "list" to the "banner" command
        module_subparsers.add_parser("list", help="List available subcommands.")

    def execute(self, args):
        """Execute the banner display or list subcommands."""
        if args.command == "show":
            self.display()
        elif args.command == "list":
            self.list_subcommands()
        else:
            print("Unknown subcommand:", args.command)

    def list_subcommands(self):
        """List available subcommands."""
        print("Available subcommands for banner:")
        print("- show: Display the banner.")
        # Add more as you add more subcommands

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
        # Display the banner
        print(colored(self.banner, self.info_color))
        
        # Information about the current status of SSH keys
        if not os.path.isfile("/helpers/helper-x.app"):
            print(colored("Uhoh.. the helper-x.app file absent.\nBrace yourself for the powdered milk experience!\n", 'white'))
        else:
            print(colored("Yes! The helper-x.app file detected.\nHold onto your pants, as this app is universal, so..\nthings are about to get real!\n", 'green'))
        
        # System Info
        self.display_system_info()

if __name__ == "__main__":
    banner = Banner()
    banner.display()
