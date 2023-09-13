import os
import jinja2

MODULES_PATH = "modules"  # Path to the modules directory
TEMPLATES_PATH = "templates"  # Path to the templates directory
HELPERS_PATH = "/helpers"  # Path to the directory for helper scripts outside /app

class Boilerplate:
    """
    The Boilerplate: A foundation for all future modules.
    
    This module serves as a template for creating new modules.
    Modify this class to fit the specific needs of your new module.
    """
    
    def __init__(self):
        self.module_name = "boilerplate"

    def add_arguments(self, subparsers, name, doc):
        """Add arguments that this module supports."""
        module_parser = subparsers.add_parser(name, help=doc.strip())
        module_subparsers = module_parser.add_subparsers(dest='command', help=f'{name} commands')

        # Add a subcommand for initializing
        init_parser = module_subparsers.add_parser("init", help="Initialize a new item.")
        
        # Subparsers for types of initialization
        init_subparsers = init_parser.add_subparsers(dest='init_type', help='Type of initialization')

        # Add a subcommand for initializing new modules
        module_init_parser = init_subparsers.add_parser("module", help="Initialize a new module.")
        module_init_parser.add_argument("--name", help="Name for the new module.", required=True)

        # Add a subcommand for generating the universal shell script
        helperx_init_parser = init_subparsers.add_parser("helper-x", help="Generate a universal shell script.")
        helperx_init_parser.add_argument("--docker-image", help="Name of the Docker image for the universal shell.", required=True)

    def execute(self, args):
        """Execute the desired functionality based on user input."""
        if hasattr(args, 'command') and args.command == 'init':
            if args.init_type == 'module':
                self.init_new_module(args.name)
            elif args.init_type == 'helper-x':
                self.init_universal_shell(args.docker_image)
        else:
            print("Available subcommands for boilerplate:")
            print("  init module --name [module_name] : Initialize a new module.")
            print("  init helper-x --docker-image [image_name] : Generate a universal shell script.")

    def init_new_module(self, module_name):
        """Initialize a new module using the Boilerplate as a template."""
        module_path = os.path.join(MODULES_PATH, f"{module_name}.py")
        
        if os.path.exists(module_path):
            print(f"Module '{module_name}' already exists!")
            return

        with open(os.path.join(TEMPLATES_PATH, "module_template.j2")) as template_file:
            template = jinja2.Template(template_file.read())
            module_content = template.render(module_name=module_name)

        with open(module_path, 'w') as module_file:
            module_file.write(module_content)

        print(f"Module '{module_name}' has been initialized!")

    def init_universal_shell(self, docker_image):
        """Generate a universal shell script using the provided Docker image name."""
        shell_script_path = os.path.join(HELPERS_PATH, "helper-x.app")
        
        with open(os.path.join(TEMPLATES_PATH, "helper-x.j2")) as template_file:
            template = jinja2.Template(template_file.read())
            shell_script_content = template.render(docker_image=docker_image, commands=self.discover_commands())

        with open(shell_script_path, 'w') as shell_script_file:
            shell_script_file.write(shell_script_content)

        print(f"Universal shell script has been generated in the '{HELPERS_PATH}' directory!")

    def discover_commands(self):
        """Discover all available command modules in the MODULES_PATH."""
        commands = []
        for file in os.listdir(MODULES_PATH):
            if file.endswith('.py') and file != '__init__.py':
                commands.append(file[:-3])
        return commands
