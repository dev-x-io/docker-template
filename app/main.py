import argparse
import importlib
import inspect
import os
import sys
from termcolor import colored
from modules.banner import Banner

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Let's imagine we have a folder called 'modules' with individual Python files for each module.
# Each module will contain functions that we want to support in app.

MODULES_PATH = "modules"  # Assuming this is the directory where all modules will reside.

def print_colored(text, color='green'):
    """Helper function to print colored text."""
    print(colored(text, color))

def discover_modules():
    """Discover all available modules in the MODULES_PATH."""
    modules = []
    for file in os.listdir(MODULES_PATH):
        if file.endswith('.py') and file != '__init__.py':
            modules.append(file[:-3])  # Remove the '.py' extension
    return modules


def main():
    # Toon altijd de banner bij het starten van het script
    banner = Banner()
    banner.display()

    module_instances = {}

    parser = argparse.ArgumentParser(description=colored('g(ood-)host-shell: Your friendly & dynamic shell!', 'green'))
    
    subparsers = parser.add_subparsers(dest='module', help='Available modules in app')

    # Dynamically load available module classes and their arguments, excluding the banner module
    for module_name in discover_modules():
        if module_name != "banner":
            module = importlib.import_module(f"{MODULES_PATH}.{module_name}")
            for name, cls in inspect.getmembers(module, inspect.isclass):
                # Ensure that we only get classes from the current module (not imported ones)
                if cls.__module__ == module.__name__:
                    instance = cls()  # Create an instance of the class
                    module_instances[name.lower()] = instance  # Use class name instead of module name
                    if hasattr(instance, 'add_arguments'):
                        # Pass the class name and its docstring for better help text
                        instance.add_arguments(subparsers, name.lower(), cls.__doc__)

    # Check if no arguments were passed
    if len(sys.argv) <= 1:
        # Display the help message
        parser.print_help()
        return

    args = parser.parse_args()

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
