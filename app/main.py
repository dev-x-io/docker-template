import argparse
import importlib
import inspect
import os
import sys
import json
from termcolor import colored
from modules.banner import Banner
from modules.observer import MainObserver
from abc import ABC

# Constants
APP_VERSION = "v0.1.0"  # Default version if not set in environment variable
MODULES_PATH = "modules"  # Directory where all modules reside

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def print_colored(text, color='green'):
    """Helper function to print colored text."""
    print(colored(text, color))


def discover_modules():
    """Discover all available modules in the MODULES_PATH."""
    return [
        file[:-3] for file in os.listdir(MODULES_PATH)
        if file.endswith('.py') and file != '__init__.py'
    ]


def generate_report(module_instances):
    """Generate a JSON report of all available commands and subcommands."""
    report = {}
    for module_name, instance in module_instances.items():
        if hasattr(instance, 'module_commands'):
            report[module_name] = {
                'commands': instance.module_commands,
                'subcommands': instance.module_subcommands
            }
    return json.dumps(report, indent=4)


def main():
    banner = Banner(APP_VERSION)

    module_instances = {}
    parser = argparse.ArgumentParser(
        description=colored('docker shell: Made user-friendly, dynamic and bonus; Ephemeral!', 'green')
    )
    subparsers = parser.add_subparsers(dest='module', help='Available modules in app')

    for module_name in discover_modules():
        module = importlib.import_module(f"{MODULES_PATH}.{module_name}")
        for name, cls in inspect.getmembers(module, inspect.isclass):
            if cls.__module__ == module.__name__ and not issubclass(cls, ABC):
                instance = cls()
                module_instances[name.lower()] = instance
                if hasattr(instance, 'add_arguments'):
                    instance.add_arguments(subparsers, name.lower(), cls.__doc__)


    # Register main.py as an observer
    boilerplate_instance = module_instances.get("boilerplate", None)
    if boilerplate_instance:
        main_observer = MainObserver()
        boilerplate_instance.register_observer(main_observer)

    # Add the --report argument
    parser.add_argument('--report', action='store_true', help='Report available commands and subcommands in JSON format.')

    # Check if no arguments were passed
    args = parser.parse_args()

    if args.report:
            print(Banner.generate_report(module_instances))
            return

    if len(sys.argv) <= 1:
        # Display the help message
        parser.print_help()
        return

    # If a module is selected, execute the corresponding function with its arguments
    if args.module in module_instances:
        if hasattr(args, 'command'):
            module_instances[args.module].execute(args)
        else:
            print(f"No subcommand structure defined for module: {args.module}")
            parser.print_help()
    else:
        print(f"Unknown module: {args.module}")
        parser.print_help()

if __name__ == "__main__":
    main()
