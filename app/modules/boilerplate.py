import os
import jinja2
from termcolor import colored
from abc import ABC, abstractmethod  # Toegevoegd voor abstracte klasse
from common.tools import AbstractModule, Common

# Constants
MODULES_PATH = "modules"  # Path to the modules directory
TEMPLATES_PATH = "/templates"  # Path to the templates directory
DYNAMIC_MODULE_PATH = "/dynamic"
RUNTIME_PATH = "/devxio"  # Path for newly generated modules


class Boilerplate(AbstractModule):
    """Behold, The Legendary Dev-X-io Boilerplate! ... [shortened for brevity]"""

    def __init__(self, app_version="v0.1.0"):
        self.module_name = "boilerplate"
        self.module_description = "A foundation for all future modules."
        self.module_version = os.environ.get("APP_VERSION", app_version)
        self.module_author = "Dev-X-io"
        self.module_license = "MIT"
        self.module_path = os.path.dirname(os.path.realpath(__file__))
        self.module_commands = ["init"]
        self.module_subcommands = {
            "init": ["module", "ghost"]
        }
        self._observers = []
        self.logs = []

    def init(self):
        """Ignites the Boilerplate's core."""
        pass

    def module(self):
        """Crafts a new module from the template."""
        pass

    def ghost(self):
        """Conjures a ghost shell script."""
        pass
    

    def add_arguments(self, subparsers, name, doc):
        """Add arguments that this module supports."""
        module_parser = subparsers.add_parser(name, help=doc.strip())
        command_subparsers = module_parser.add_subparsers(dest='command', help=f'{name} commands')

        # Voeg de Common klasse toe aan boilerplate
        common_instance = Common()  # Maak een instantie van de Common klasse
        common_instance.add_arguments(module_parser, name, doc)  # Roep de add_arguments methode van Common aan

        # Voeg andere argumenten voor boilerplate toe
        # ...

        init_parser = command_subparsers.add_parser("init", help="Initialize components.")
        init_subparsers = init_parser.add_subparsers(dest='init_type', help='init subcommands')

        subcommands = [
            {
                "name": "module",
                "help": "Initialize a new module.",
                "args": [{"name": "--name", "help": "Name for the new module.", "required": True}]
            },
            {
                "name": "ghost",
                "help": "Generate a ghost shell script.",
                "args": []
            }
        ]

        for subcommand in subcommands:
            parser = init_subparsers.add_parser(subcommand["name"], help=subcommand["help"])
            for arg in subcommand["args"]:
                parser.add_argument(arg["name"], help=arg["help"], required=arg["required"])

            # Log the added subcommands
            log_message = f"Added subcommand '{subcommand['name']}' with arguments {[arg['name'] for arg in subcommand['args']]} in module '{name}'."
            self.logs.append(log_message)
            self.notify_observers(log_message)

        # Add logs command directly to the module command level
        logs_parser = command_subparsers.add_parser("logs", help="Display logs.")
        logs_parser.set_defaults(func=self.show_logs)
        
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
    
    def discover_commands(self):
        commands = {}
        for command in self.module_commands:
            subcommands = getattr(self, f"{command}_subcommands", [])
            commands[command] = [f'"{subcmd}"' for subcmd in subcommands]
        return commands

    def get_metadata(self):
        """Retrieve the metadata for the module."""
        return {
            'description': self.module_description,
            'version': self.module_version,
            'author': self.module_author,
            'license': self.module_license,
            'doc': self.__doc__.strip() if self.__doc__ else None
        }

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

    def execute(self, args):
        """Execute the desired functionality based on user input."""
        # Log the executed command
        log_message = f"Executing command '{args.command}' with init_type '{getattr(args, 'init_type', 'N/A')}' in module '{self.module_name}'."
        self.logs.append(log_message)
        self.notify_observers(log_message)

        if args.command == 'init':
            if args.init_type == 'module':
                self.module()
            elif args.init_type == 'ghost':
                self.ghost()
        elif args.command == 'logs':
            self.show_logs()
        else:
            self.print_help()

    def get_logs(self):
        """Retrieve all logs."""
        return self.logs

    def show_logs(self):
        """Display collected logs."""
        print(colored("Collected Logs:", 'yellow'))
        print('-' * 15)
        for log in self.logs:
            print(log)

    def print_help(self):
        """Improved custom help function."""    
        # Header
        header = f"Available commands and subcommands for {self.module_name}:"
        print(colored(header, 'yellow'))
        print('-' * len(header))
        
        # Main commands
        max_command_length = max(len(command) for command in self.module_commands)
        for command in self.module_commands:
            description = getattr(self, command).__doc__.strip() if getattr(self, command) and getattr(self, command).__doc__ else ""
            print(colored(f"{command.ljust(max_command_length)}", 'cyan') + f" : {description}")

        # Subcommands
        for command, subcommands in self.module_subcommands.items():
            print(f"\nSubcommands for '{command}':")
            
            max_subcommand_length = max(len(subcommand) for subcommand in subcommands)
            for subcommand in subcommands:
                description = getattr(self, subcommand).__doc__.strip() if getattr(self, subcommand) and getattr(self, subcommand).__doc__ else ""
                print(colored(f"{subcommand.ljust(max_subcommand_length)}", 'green') + f" : {description}")

    def init_new_module(self, module_name):
        """Initialize a new module using the Boilerplate as a template."""
        module_path = os.path.join(DYNAMIC_MODULE_PATH ,f"{module_name}.py")
        
        if os.path.exists(module_path):
            print(f"Module '{module_name}' already exists!")
            return

        with open(os.path.join(TEMPLATES_PATH, "shell_module_template.j2")) as template_file:
            template = jinja2.Template(template_file.read())
            module_content = template.render(module_name=module_name)

        with open(module_path, 'w') as module_file:
            module_file.write(module_content)

        print(f"Module '{module_name}' has been initialized!")

    def init_ghost_shell(self):
        """Initialize ghost shell scripts for both bash and PowerShell."""
        commands = self.discover_commands()

        # Iterate over both shell types and generate scripts
        for shell_type in ["bash", "powershell"]:
            template_path = os.path.join(TEMPLATES_PATH, f"{shell_type}_template.j2")
            with open(template_path) as template_file:
                template = jinja2.Template(template_file.read())
                shell_script_content = template.render(commands=commands)

            shell_script_path = os.path.join(RUNTIME_PATH, f"{shell_type if shell_type == 'powershell' else 'sh'}")
            with open(shell_script_path, "w") as shell_script_file:
                shell_script_file.write(shell_script_content)

            print(f"Generated script for {shell_type} at {shell_script_path}")
