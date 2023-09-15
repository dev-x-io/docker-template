import platform
import socket
import multiprocessing
import os
import pyfiglet
import json
import argparse
from termcolor import colored
from abc import ABC, abstractmethod
from common import AbstractModule, Common

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
        super().__init__()
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
        self.module_commands = ["info"]
        self.module_subcommands = {}
        self._observers = []
        self.logs = []

    def info(self):
        """Displays the project banner."""
        print("Displaying the Banner...")
        self.display()

    def add_arguments(self, subparsers, subcommand, help_text, subparsers_variable):
        parser = subparsers.add_parser(subcommand, help=help_text)
        # Voeg hier argumenten toe aan de parser voor dit specifieke module.
        parser.add_argument('--module-argument', help='An argument for this module')

    def use_common_functionality(self, subparsers):
        common_instance = Common()
        # Gebruik methoden of attributen van common_instance zoals nodig
        common_command_docs = common_instance.get_command_docs()
        common_subcommand_docs = common_instance.get_subcommand_docs()
        # Voeg argumenten toe aan de parser voor dit specifieke module
        common_instance.add_arguments(subparsers, 'module_name', 'Module description', subparsers)  # Voeg subparsers_variable toe

    def discover_commands(self):
        commands = {}
        for command in self.module_commands:
            subcommands = getattr(self, f"{command}_subcommands", [])
            commands[command] = [f'"{subcmd}"' for subcmd in subcommands]
        return commands

    def get_command_docs(self):
        """Retrieve the docstrings for commands."""
        commands_dict = {}
        for command in self.module_commands:
            command_method = getattr(self, command, None)
            if command_method and command_method.__doc__:
                commands_dict[command] = command_method.__doc__.strip()
        return commands_dict

    def get_metadata(self, module_instances):
        """Generate a JSON report of metadata for all available modules."""
        report = {}
        for module_name, instance in module_instances.items():
            module_data = {
                'description': instance.module_description if hasattr(instance, 'module_description') else None,
                'version': instance.module_version if hasattr(instance, 'module_version') else None,
                'author': instance.module_author if hasattr(instance, 'module_author') else None,
                'license': instance.module_license if hasattr(instance, 'module_license') else None,
                'doc': instance.__doc__.strip() if instance.__doc__ else None
            }
            report[module_name] = module_data
        return json.dumps(report, indent=4)

    def get_subcommand_docs(self):
        """Retrieve the docstrings for subcommands."""
        subcommands_dict = {}
        for command, subcommands in self.module_subcommands.items():
            subcommands_dict[command] = {
                "description": getattr(self, command).__doc__.strip() if getattr(self, command) and getattr(
                    self, command).__doc__ else "",
                "subcommands": {}
            }
            for subcommand in subcommands:
                subcommand_method = getattr(self, subcommand, None)
                if subcommand_method and subcommand_method.__doc__:
                    subcommands_dict[command]["subcommands"][subcommand] = subcommand_method.__doc__.strip()
        return subcommands_dict

    def execute(self, args):
        """Execute the desired functionality based on user input."""
        # Log the executed command
        log_message = f"Executing command '{args.command}' in module '{self.module_name}'."
        self.logs.append(log_message)
        self.notify_observers(log_message)

        if args.command == 'info':
            self.display()
        elif args.command == 'logs':
            self.show_logs()
        else:
            self.print_help()

    def show_logs(self):
        """Display collected logs."""
        print(colored("Collected Logs:", 'yellow'))
        print('-' * 15)
        for log in self.logs:
            print(log)

    def print_help(self):
        """Display the help message."""
        # Header
        header = f"Available commands and subcommands for {self.module_name}:"
        print(colored(header, 'yellow'))
        print('-' * len(header))

        # Main commands
        main_commands_info = [{"command": command, "description": self.get_command_docs().get(command, "")} for
                               command in self.module_commands]

        # Display main commands
        max_command_length = max(len(command["command"]) for command in main_commands_info)

        for command in main_commands_info:
            print(colored(f"{command['command'].ljust(max_command_length)}", 'cyan') + f" : {command['description']}")

        # Display subcommands
        if self.module_subcommands:
            for command, subcommands in self.module_subcommands.items():
                for subcommand in subcommands:
                    subcommand_description = self.get_subcommand_docs().get(command, {}).get("subcommands", {}).get(
                        subcommand, "")
                    print(colored(f"{command} {subcommand}", 'green') + f" : {subcommand_description}")

    def display(self, module_instances=None):
        """Render the majestic banner for all to behold."""
        print(colored(self.banner, self.info_color))

        self.display_system_info()

        print(colored(Banner.__doc__, "green"))

        if not os.path.isfile("/helpers/.devxio"):
            print(
                colored("Uhoh.. Dev-X-io file absent.\nBrace yourself for the powdered milk experience!\n", 'white'))
        else:
            print(
                colored(
                    "Yes; Dev-X-io file detected!\nHold onto your pants, probably lose your socks.\nThis app is so universal..\nthings are about to get unreal!\n",
                    'green'))

        # Display module information if provided
        if module_instances:
            self.display_module_info(module_instances)

# Voeg eventuele extra functionaliteit of methoden hieronder toe
    def register_observer(self, observer):
        """Add an observer to the list."""
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        """Remove an observer from the list."""
        self._observers.remove(observer)

    def notify_observers(self, message):
        """Notify all observers of a change."""
        for observer in self._observers:
            observer.update(message)

    # def discover_commands(self):
    #     commands = {}
    #     for command in self.module_commands:
    #         subcommands = getattr(self, f"{command}_subcommands", [])
    #         commands[command] = [f'"{subcmd}"' for subcmd in subcommands]
    #     return commands
        
    # def get_command_docs(self):
    #     """Retrieve the docstrings for commands."""
    #     commands_dict = {}
    #     for command in self.module_commands:
    #         command_method = getattr(self, command, None)
    #         if command_method and command_method.__doc__:
    #             commands_dict[command] = command_method.__doc__.strip()
    #     return commands_dict

    # def get_metadata(self, module_instances):
    #     """Generate a JSON report of metadata for all available modules."""
    #     report = {}
    #     for module_name, instance in module_instances.items():
    #         module_data = {
    #             'description': instance.module_description if hasattr(instance, 'module_description') else None,
    #             'version': instance.module_version if hasattr(instance, 'module_version') else None,
    #             'author': instance.module_author if hasattr(instance, 'module_author') else None,
    #             'license': instance.module_license if hasattr(instance, 'module_license') else None,
    #             'doc': instance.__doc__.strip() if instance.__doc__ else None
    #         }
    #         report[module_name] = module_data
    #     return json.dumps(report, indent=4)


    # def get_subcommand_docs(self):
    #     """Retrieve the docstrings for subcommands."""
    #     subcommands_dict = {}
    #     for command, subcommands in self.module_subcommands.items():
    #         subcommands_dict[command] = {
    #             "description": getattr(self, command).__doc__.strip() if getattr(self, command) and getattr(self, command).__doc__ else "",
    #             "subcommands": {}
    #         }
    #         for subcommand in subcommands:
    #             subcommand_method = getattr(self, subcommand, None)
    #             if subcommand_method and subcommand_method.__doc__:
    #                 subcommands_dict[command]["subcommands"][subcommand] = subcommand_method.__doc__.strip()
    #     return subcommands_dict

    # def execute(self, args):
    #     """Execute the desired functionality based on user input."""
    #     # Log the executed command
    #     log_message = f"Executing command '{args.command}' in module '{self.module_name}'."
    #     self.logs.append(log_message)
    #     self.notify_observers(log_message)

    #     if args.command == 'info':
    #         self.display()
    #     elif args.command == 'logs':
    #         self.show_logs()
    #     else:
    #         self.print_help()


    def get_logs(self):
        """Retrieve all logs."""
        return self.logs

    # def show_logs(self):
    #     """Display collected logs."""
    #     print(colored("Collected Logs:", 'yellow'))
    #     print('-' * 15)
    #     for log in self.logs:
    #         print(log)     


    # def print_help(self):
    #     """Display the help message."""    
    #     # Header
    #     header = f"Available commands and subcommands for {self.module_name}:"
    #     print(colored(header, 'yellow'))
    #     print('-' * len(header))
        
    #     # Main commands
    #     main_commands_info = [{"command": command, "description": self.get_command_docs().get(command, "")} for command in self.module_commands]
        
    #     # Display main commands
    #     max_command_length = max(len(command["command"]) for command in main_commands_info)
        
    #     for command in main_commands_info:
    #         print(colored(f"{command['command'].ljust(max_command_length)}", 'cyan') + f" : {command['description']}")
        
    #     # Display subcommands
    #     if self.module_subcommands:
    #         for command, subcommands in self.module_subcommands.items():
    #             for subcommand in subcommands:
    #                 subcommand_description = self.get_subcommand_docs().get(command, {}).get("subcommands", {}).get(subcommand, "")
    #                 print(colored(f"{command} {subcommand}", 'green') + f" : {subcommand_description}")


    def display_module_info(self, module_instances):
        """Display detailed module commands and their docstrings."""
        print(colored("\nAvailable Modules and Commands:\n", 'yellow'))
        for module_name, instance in module_instances.items():
            print(colored(f"{module_name}:", "cyan"))
            if hasattr(instance, 'print_help'):
                instance.print_help()
            print()

    def display_system_info(self):
        """Display detailed system information."""
        print(colored("Operating System:", self.info_color), platform.system())
        print(colored("Hostname:", self.info_color), socket.gethostname())
        print(colored("Platform:", self.info_color), platform.platform())
        print(colored("Architecture:", self.info_color), platform.architecture()[0])
        print(colored("Python Version:", self.info_color), platform.python_version())
        print(colored("Number of CPUs:", self.info_color), multiprocessing.cpu_count())
        print(colored("Modules path:", self.info_color), os.path.dirname(os.path.abspath(__file__)))

    # def display(self, module_instances=None):
    #     """Render the majestic banner for all to behold."""
    #     print(colored(self.banner, self.info_color))

    #     self.display_system_info()

    #     print(colored(Banner.__doc__, "green"))

    #     if not os.path.isfile("/helpers/.devxio"):
    #         print(colored("Uhoh.. Dev-X-io file absent.\nBrace yourself for the powdered milk experience!\n", 'white'))
    #     else:
    #         print(colored("Yes; Dev-X-io file detected!\nHold onto your pants, probably lose your socks.\nThis app is so universal..\nthings are about to get unreal!\n", 'green'))

    #     # Display module information if provided
    #     if module_instances:
    #         self.display_module_info(module_instances)


# Voeg eventuele extra functionaliteit of methoden hieronder toe
