import os
import jinja2
from termcolor import colored

MODULES_PATH = "modules"  # Path to the modules directory
TEMPLATES_PATH = "templates"  # Path to the templates directory
HELPERS_PATH = "/helpers"  # Path to the directory for helper scripts outside /app

class Boilerplate:
    """
    Behold, The Legendary Dev-X-io Boilerplate!

    In the boundless realm of coding, legends whisper of a template so mighty, so versatile, 
    it can mold any idea into a masterpiece. That legend... is no myth. It's the Dev-X-io Boilerplate!

    This isn't just a starting point; it's a launchpad. A canvas primed and ready for the strokes 
    of genius. Whether you're crafting a potion or conjuring a spell, this Boilerplate is the 
    alchemy you need.

    So, intrepid developer, the stage is set, the spotlight's on. Are you ready to craft your legacy?
    With the Dev-X-io Boilerplate, every line of code is a step towards legend. 🌟
    """

    
    def __init__(self):
        self.module_name = "boilerplate"
        self.module_description = "A foundation for all future modules."
        self.module_version = "0.1.0"
        self.module_author = "Dev-X-io"
        self.module_license = "MIT"
        self.module_path = os.path.dirname(os.path.realpath(__file__))
        self.module_commands = ["init"]
        self.module_subcommands = {
            "init": ["module", "ghost"]
        }
        self._observers = []
        self.logs = []

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

    def add_arguments(self, subparsers, name, doc):
        """Add arguments that this module supports."""
        module_parser = subparsers.add_parser(name, help=doc.strip())
        command_subparsers = module_parser.add_subparsers(dest='command', help=f'{name} commands')

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
                "args": [{"name": "--docker-image", "help": "Name of the Docker image for the ghost shell.", "required": True}]
            }
        ]

        for subcommand in subcommands:
            parser = init_subparsers.add_parser(subcommand["name"], help=subcommand["help"])
            for arg in subcommand["args"]:
                parser.add_argument(arg["name"], help=arg["help"], required=arg["required"])

            # Log the added subcommands
            log_message = f"Added subcommand '{subcommand['name']}' with arguments {[arg['name'] for arg in subcommand['args']]} in module '{self.module_name}'."
            self.logs.append(log_message)
            self.notify_observers(log_message)

        # Add logs command directly to the module command level
        logs_parser = command_subparsers.add_parser("logs", help="Display logs.")
        logs_parser.set_defaults(func=self.show_logs)

    def execute(self, args):
        """Execute the desired functionality based on user input."""
        # Log the executed command
        log_message = f"Executing command '{args.command}' with init_type '{getattr(args, 'init_type', 'N/A')}' in module '{self.module_name}'."
        self.logs.append(log_message)
        self.notify_observers(log_message)

        if args.command == 'init':
            if args.init_type == 'module':
                self.init_new_module(args.name)
            elif args.init_type == 'ghost':
                self.init_ghost_shell(args.docker_image)
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
        header = "Available commands and subcommands for boilerplate:"
        print(colored(header, 'yellow'))
        print('-' * len(header))
        
        # Main commands
        main_commands_info = [
            {
                "command": "init",
                "arguments": "",
                "description": "Initialize components."
            },
            {
                "command": "logs",
                "arguments": "",
                "description": "Display logs."
            }
        ]
        
        # Display main commands
        max_command_length = max(len(command["command"]) for command in main_commands_info)
        max_arguments_length = max(len(command["arguments"]) for command in main_commands_info)
        
        for command in main_commands_info:
            print(colored(f"{command['command'].ljust(max_command_length)}", 'cyan') +
                  f" {command['arguments'].ljust(max_arguments_length)} : {command['description']}")

        print("\nSubcommands for 'init':")
        
        # Subcommands for 'init'
        subcommands_info = [
            {
                "command": "module",
                "arguments": "--name [module_name]",
                "description": "Initialize a new module."
            },
            {
                "command": "ghost",
                "arguments": "--docker-image [image_name]",
                "description": "Generate a ghost shell script."
            }
        ]

        # Display subcommands
        max_command_length = max(len(subcommand["command"]) for subcommand in subcommands_info)
        max_arguments_length = max(len(subcommand["arguments"]) for subcommand in subcommands_info)
        
        for subcommand in subcommands_info:
            print(colored(f"{subcommand['command'].ljust(max_command_length)}", 'green') +
                  f" {subcommand['arguments'].ljust(max_arguments_length)} : {subcommand['description']}")

    def init_new_module(self, module_name):
        """Initialize a new module using the Boilerplate as a template."""
        module_path = os.path.join(MODULES_PATH, f"{module_name}.py")
        
        if os.path.exists(module_path):
            print(f"Module '{module_name}' already exists!")
            return

        with open(os.path.join(TEMPLATES_PATH, "shell_module_template.j2")) as template_file:
            template = jinja2.Template(template_file.read())
            module_content = template.render(module_name=module_name)

        with open(module_path, 'w') as module_file:
            module_file.write(module_content)

        print(f"Module '{module_name}' has been initialized!")

    def init_ghost_shell(self, docker_image):
        """Generate a ghost shell script using the provided Docker image name."""
        shell_script_path = os.path.join(HELPERS_PATH, "ghost.app")
        
        with open(os.path.join(TEMPLATES_PATH, "ghost_template.j2")) as template_file:
            template = jinja2.Template(template_file.read())
            shell_script_content = template.render(docker_image=docker_image, commands=self.discover_commands())

        with open(shell_script_path, 'w') as shell_script_file:
            shell_script_file.write(shell_script_content)

        print(f"Ghost shell script has been generated in the '{HELPERS_PATH}' directory!")

    def discover_commands(self):
        """Discover all available command modules in the MODULES_PATH."""
        commands = []
        for file in os.listdir(MODULES_PATH):
            if file.endswith('.py') and file != '__init__.py':
                commands.append(file[:-3])
        return commands

# Note: This is a representation of the code with the desired changes.
# Actual file changes should be made in the project directory.
