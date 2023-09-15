import argparse
import importlib
import inspect
import os
import sys
from termcolor import colored
from modules.banner import Banner
from modules.observer import MainObserver
from abc import ABC

# Constants
APP_VERSION = "v0.0.0"  # Default version if not set in environment variable
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


def main():
    banner = Banner(APP_VERSION)

    module_instances = {}
    parser = argparse.ArgumentParser(
        description=colored('docker shell: Made user-friendly, dynamic and bonus; Ephemeral!', 'green')
    )
    subparsers = parser.add_subparsers(dest='module', help='Available modules in app')

    for module_name in discover_modules():
        if module_name != "banner":
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

    # Check if no arguments were passed
    if len(sys.argv) <= 1:
        # Display the help message
        parser.print_help()
        return

    args = parser.parse_args()
    if args == None:
        banner.display()
        # return

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
