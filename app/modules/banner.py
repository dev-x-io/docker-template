import platform
import socket
import multiprocessing
import os
import pyfiglet
import json
from termcolor import colored
from common.tools import AbstractModule, Common


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

    # ------------------ Initialization Methods ------------------

    def __init__(self, app_version="v0.0.0"):
        """Initialize the environment details for the banner."""
        self.basename = os.path.basename(os.getcwd())

        # Metadata
        self.module_name = "banner"
        self.module_description = "Displays a warm welcome banner."
        self.module_version = os.environ.get("APP_VERSION", app_version)
        self.module_author = "Dev-X-io"
        self.module_license = "MIT"
        self.module_commands = ["show", "logs"]
        self.module_subcommands = {}

        self.info = pyfiglet.figlet_format(f'Dev-X Input/Output {self.module_version}', font='digital')
        self.info_color = "green" if os.path.isfile("/helpers/dev-x.io") else "red"

        self._observers = []
        self.logs = []

    # ------------------ Command Execution Methods ------------------

    def execute(self, args):
        """Execute the desired functionality based on user input."""
        log_message = f"Executing command '{args.command}' in module '{self.module_name}'."
        self.logs.append(log_message)
        self.notify_observers(log_message)

        if args.command == 'show':
            self.show()
        elif args.command == 'logs':
            self.show_logs()
        else:
            self.print_help()

    # ------------------ Command and Subcommand Handling Methods ------------------

    def add_arguments(self, subparsers, name, doc):
        """Add arguments that this module supports."""
        module_parser = subparsers.add_parser(name, help=doc.strip())
        command_subparsers = module_parser.add_subparsers(dest='command', help=f'{name} commands')

        common_instance = Common()  
        common_instance.add_arguments(module_parser, name, doc)  

        show_parser = command_subparsers.add_parser("show", help="Displays a warm welcome banner.")
        log_message = f"Added command 'show' in module '{name}'."
        self.logs.append(log_message)
        self.notify_observers(log_message)

        logs_parser = command_subparsers.add_parser("logs", help="Display logs.")
        logs_parser.set_defaults(func=self.show_logs)

    def discover_commands(self):
        commands = {}
        for command in self.module_commands:
            subcommands = getattr(self, f"{command}_subcommands", [])
            commands[command] = [f'"{subcmd}"' for subcmd in subcommands]
        return commands

    def get_command_docs(self):
        commands_dict = {}
        for command in self.module_commands:
            command_method = getattr(self, command, None)
            if command_method and command_method.__doc__:
                commands_dict[command] = command_method.__doc__.strip()
        return commands_dict

    def get_subcommand_docs(self):
        subcommands_dict = {}
        for command, subcommands in self.module_subcommands.items():
            subcommands_dict[command] = {
                "description": getattr(self, command).__doc__.strip() if getattr(self, command) and getattr(self, command).__doc__ else "",
                "subcommands": {}
            }
            for subcommand in subcommands:
                subcommand_method = getattr(self, subcommand, None)
                if subcommand_method and subcommand_method.__doc__:
                    subcommands_dict[command]["subcommands"][subcommand] = subcommand_method.__doc__.strip()
        return subcommands_dict

    # ------------------ Observer Pattern Methods ------------------

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

    # ------------------ Display Methods ------------------

    def show(self):
        """Displays detailed info about the banner."""
        self.display()

    def print_help(self):
        """Display the help message."""  
        header = f"Available commands and subcommands for {self.module_name}:"
        print(colored(header, 'yellow'))
        print('-' * len(header))
        
        main_commands_info = [{"command": command, "description": self.get_command_docs().get(command, "")} for command in self.module_commands]
        
        max_command_length = max(len(command["command"]) for command in main_commands_info)
        for command in main_commands_info:
            print(colored(f"{command['command'].ljust(max_command_length)}", 'cyan') + f" : {command['description']}")
        
        if self.module_subcommands:
            for command, subcommands in self.module_subcommands.items():
                for subcommand in subcommands:
                    subcommand_description = self.get_subcommand_docs().get(command, {}).get("subcommands", {}).get(subcommand, "")
                    print(colored(f"{command} {subcommand}", 'green') + f" : {subcommand_description}")

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

    def display(self, module_instances=None):
        """Render the majestic banner for all to behold."""
        print(colored(self.info, self.info_color))
        self.display_system_info()
        print(colored(Banner.__doc__, "green"))
        if module_instances:
            self.display_module_info(module_instances)

    # ------------------ Miscellaneous Methods ------------------

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

    def get_logs(self):
        """Retrieve all logs."""
        return self.logs

    def show_logs(self):
        """Display collected logs."""
        print(colored("Collected Logs:", 'yellow'))
        print('-' * 15)
        for log in self.logs:
            print(log)

    # ------------------ Additional Methods ------------------
