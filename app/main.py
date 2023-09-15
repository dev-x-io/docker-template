import argparse
import importlib
import inspect
import os
import sys
import json
from termcolor import colored
from modules.banner import Banner, AbstractModule
from modules.observer import MainObserver
from common.tools import Common as common
from abc import ABC

# Constants
APP_VERSION = "v0.1.0"  # Default version if not set in environment variable
STATIC_MODULES_PATH = "modules"  # Directory where all static modules reside
DYNAMIC_MODULES_PATH = "/dynamic"  # Directory where all dynamic modules reside
EXCLUDE_MODULES = ['tools', 'observer']  # Modules to be excluded

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DYNAMIC_MODULES_PATH)  # Add dynamic modules path to the Python path

def print_colored(text, color='green'):
    """Helper function to print colored text."""
    print(colored(text, color))

def discover_modules(path):
    """Discover all available modules in the specified path."""
    modules = [
        file[:-3] for file in os.listdir(path)
        if file.endswith('.py') and file != '__init__.py'
    ]
    print_colored(f"Discovered modules in {path}: {modules}", color="yellow")  # Debugging line
    return modules

def add_modules_to_parser(subparsers, module_path, abstract_module, is_static=True, module_prefix=""):
    """Function to add modules to the argument parser."""

    for module_name in discover_modules(module_path):
        if module_name in EXCLUDE_MODULES:
            continue

        print_colored(f"Attempting to import module: {module_name}", color="yellow")  # Debugging line
        try:
            if is_static:
                module = importlib.import_module(f"{STATIC_MODULES_PATH}.{module_name}")
            else:
                module = importlib.import_module(f"{module_name}")
                print(f"Detected classes in {module_name}: {[name for name, _ in inspect.getmembers(module, inspect.isclass)]}")  # Debugging line

            for name, cls in inspect.getmembers(module, inspect.isclass):
                if cls.__module__ == module.__name__ and issubclass(cls, abstract_module) and cls != abstract_module:
                    print(f"Instantiating class {name} of module {module_name}...")  # Debug line
                    instance = cls()
                    if hasattr(instance, 'add_arguments'):
                        print(f"Calling add_arguments for class {name} of module {module_name}...")  # Debug line
                        
                        # Voeg een voorvoegsel toe aan de subparsers om conflicten te voorkomen
                        subparser_prefix = f"{module_prefix}_" if module_prefix else ""
                        instance.add_arguments(subparsers, f"{subparser_prefix}{name.lower()}", cls.__doc__)
        except Exception as e:
            print_colored(f"Error importing module {module_name}: {e}", color="red")  # Debugging line

def main():
    module_instances = {}  # Maak de dictionary voor module-instanties

    banner = Banner(APP_VERSION)

    parser = argparse.ArgumentParser(
        description=colored('docker shell: Made user-friendly, dynamic and bonus; Ephemeral!', 'green')
    )

    # Voeg hier de subparser-logica toe voor de "common"-module.
    common_subparser = parser.add_subparsers(dest='common_module', help='Available common modules in app')
    add_modules_to_parser(common_subparser, STATIC_MODULES_PATH, AbstractModule, is_static=True)

    # Add the --report argument
    parser.add_argument('--report', action='store_true', help='Report available commands and subcommands in JSON format.')

    # Check if no arguments were passed
    args = parser.parse_args()

    if args.report:
        # Generate the report in the format van het oude script
        report = {}
        for module_name, instance in module_instances.items():
            if hasattr(instance, 'module_commands'):
                report[module_name] = {
                    'commands': instance.module_commands,
                    'subcommands': instance.module_subcommands
                }
        print(json.dumps(report, indent=4))
        return

    if len(sys.argv) <= 1:
        # Display the help message
        parser.print_help()
        return

    # If a common module is selected, execute the corresponding function with its arguments
    if args.common_module:
        # Hier halen we de naam van het subcommando uit de args
        common_command = args.common_module
        module_instances[common_command].execute(args)
    else:
        print(f"Unknown common module: {args.common_module}")
        parser.print_help()
    # if args.common_module in module_instances:
    #     # Hier halen we de naam van het subcommando uit de args
    #     common_command = getattr(args, 'common_command', None)
    #     if common_command:
    #         module_instances[args.common_module].execute(common_command, args)
    #     else:
    #         print(f"No subcommand structure defined for common module: {args.common_module}")
    #         parser.print_help()
    # else:
    #     print(f"Unknown common module: {args.common_module}")
    #     parser.print_help()

if __name__ == "__main__":
    main()