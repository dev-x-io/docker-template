import platform
import socket
import multiprocessing
import os
import pyfiglet
import json
from termcolor import colored
from abc import ABC, abstractmethod  # Toegevoegd voor abstracte klasse


class AbstractModule(ABC):
    """
    Abstract Module to define the structure for all modules.
    """

    @abstractmethod
    def get_command_docs(self):
        """Retrieve the docstrings for commands."""
        pass

    @abstractmethod
    def get_subcommand_docs(self):
        """Retrieve the docstrings for subcommands."""
        pass


class Banner(AbstractModule):
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
        self.module_commands = ["show", "list", "banner"]
        self.module_subcommands = {}

    def get_command_docs(self):
        """Retrieve the docstrings for commands."""
        commands_dict = {}
        for command in self.module_commands:
            command_method = getattr(self, command, None)
            if command_method and command_method.__doc__:
                commands_dict[command] = command_method.__doc__.strip()
        return commands_dict

    def get_subcommand_docs(self):
        """Retrieve the docstrings for subcommands."""
        # Since Banner class does not have subcommands, we return an empty dictionary
        return {}

    @staticmethod
    def generate_report(module_instances):
        """Generate a JSON report of all available modules, commands, subcommands, metadata, and docstrings."""
        report = {}
        for module_name, instance in module_instances.items():
            module_data = {
                'metadata': {
                    'description': instance.module_description if hasattr(instance, 'module_description') else None,
                    'version': instance.module_version if hasattr(instance, 'module_version') else None,
                    'author': instance.module_author if hasattr(instance, 'module_author') else None,
                    'license': instance.module_license if hasattr(instance, 'module_license') else None,
                    'doc': instance.__doc__.strip() if instance.__doc__ else None,
                },
                'commands': instance.get_command_docs() if hasattr(instance, 'get_command_docs') else {},
                'subcommands': instance.get_subcommand_docs() if hasattr(instance, 'get_subcommand_docs') else {}
            }
            report[module_name] = module_data
        return json.dumps(report, indent=4)

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

    def display_module_info(self, module_instances):
        """Display detailed module commands and their docstrings."""
        print(colored("\nAvailable Modules and Commands:\n", 'yellow'))
        for module_name, instance in module_instances.items():
            print(colored(f"{module_name}:", "cyan"))
            if hasattr(instance, 'get_commands_with_docs'):
                commands_with_docs = instance.get_commands_with_docs()
                for command, doc in commands_with_docs.items():
                    print(f"  {command} - {doc}")

            if hasattr(instance, 'get_subcommands_with_docs'):
                subcommands_with_docs = instance.get_subcommands_with_docs()
                for command, subcommands in subcommands_with_docs.items():
                    for subcommand, subdoc in subcommands.items():
                        print(f"  {command} {subcommand} - {subdoc}")
            print()

    def display(self, module_instances=None):
        """Render the majestic banner for all to behold."""
        print(colored(self.banner, self.info_color))

        self.display_system_info()

        print(colored(Banner.__doc__, "green"))

        if not os.path.isfile("/helpers/.devxio"):
            print(colored("Uhoh.. Dev-X-io file absent.\nBrace yourself for the powdered milk experience!\n", 'white'))
        else:
            print(colored("Yes; Dev-X-io file detected!\nHold onto your pants, probably lose your socks.\nThis app is so universal..\nthings are about to get unreal!\n", 'green'))

        # Display module information if provided
        if module_instances:
            self.display_module_info(module_instances)


# Voeg eventuele extra functionaliteit of methoden hieronder toe
