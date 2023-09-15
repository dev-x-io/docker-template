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

# ------------------ Constants ------------------

APP_VERSION = "v0.1.0"
STATIC_MODULES_PATH = "modules"
DYNAMIC_MODULES_PATH = "/dynamic"
EXCLUDE_MODULES = ['tools', 'observer']

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DYNAMIC_MODULES_PATH)

def debug_print(message, color="green"):
    """Prints the message only if --debug flag is provided."""
    if 'ARGS' in globals() and ARGS.debug:
        print_colored(message, color="yellow")

# ------------------ Utility Functions ------------------

def print_colored(text, color='green'):
    """Prints colored text. If debug is True, only prints when --debug flag is provided."""
    print(colored(text, color))

def discover_modules(path,debug=False):
    """Discover and return modules from a given path."""
    modules = [
        file[:-3] for file in os.listdir(path)
        if file.endswith('.py') and file != '__init__.py'
    ]
    debug_print(f"Discovered modules in {path}: {modules}", color="yellow")
    return modules

def add_modules_to_parser(subparsers, module_path, abstract_module, is_static=True, module_prefix="",debug=False):
    """Dynamically add modules to the command parser."""
    global module_instances

    for module_name in discover_modules(module_path):
        if module_name in EXCLUDE_MODULES:
            continue
        debug_print(f"Attempting to import module: {module_name}", color="yellow")
        try:
            if is_static:
                module = importlib.import_module(f"{STATIC_MODULES_PATH}.{module_name}")
            else:
                module = importlib.import_module(f"{module_name}")

            for name, cls in inspect.getmembers(module, inspect.isclass):
                if cls.__module__ == module.__name__ and issubclass(cls, abstract_module) and cls != abstract_module:
                    debug_print(f"Instantiating class {name} of module {module_name}...")
                    instance = cls()
                    module_instances[name.lower()] = instance
                    if hasattr(instance, 'add_arguments'):
                        subparser_prefix = f"{module_prefix}_" if module_prefix else ""
                        instance.add_arguments(subparsers, f"{subparser_prefix}{name.lower()}", cls.__doc__)
        except Exception as e:
            print_colored(f"Error importing module {module_name}: {e}", color="red")

# ------------------ Main Function ------------------

def main():
    global module_instances

    module_instances = {}
 
    # ------------------ Display App Banner ------------------
    banner = Banner(APP_VERSION)

    # ------------------ Setup Argument Parser ------------------
    parser = argparse.ArgumentParser(
        description=colored('devxio cli: Made user-friendly, dynamic and bonus; Ephemeral!', 'green')
    )

    # ------------------ Add Arguments ------------------
    parser.add_argument('--report', action='store_true', help='Report available commands and subcommands in JSON format.')
    parser.add_argument('--debug', action='store_true', help='Enable debug output.')

    # ------------------ Discover Modules ----------------------
    common_subparser = parser.add_subparsers(dest='common_module', help='Available common modules in app')

    # ------------------ Add Modules ---------------------------
    add_modules_to_parser(common_subparser, STATIC_MODULES_PATH, AbstractModule, is_static=True)

    global ARGS
    ARGS = parser.parse_args()

    # ------------------ Handle Report Argument ------------------
    if ARGS.report:
        report = {}
        for module_name, instance in module_instances.items():
            if hasattr(instance, 'module_commands'):
                report[module_name] = {
                    'commands': instance.module_commands,
                    'subcommands': instance.module_subcommands
                }
        print(json.dumps(report, indent=4))
        return

    # ------------------ Execute the Appropriate Module ------------------
    # if ARGS.common_module == None or (len(sys.argv) == 0 and not ARGS.debug):
    #     common_command = ARGS.common_module
    #     debug_print(f"Module instances before execution: {module_instances}")
    #     if common_command in module_instances:
    #         module_instances[common_command].execute(ARGS)
    #     else:
    #         print("No valid command provided.")
    # else:
    #     print_colored(f"Unknown common module: {ARGS.common_module}")
    #     parser.print_help()
    if ARGS.common_module in module_instances:
        # Print help for the specific module if no subcommand is provided
        if hasattr(ARGS, 'command') and not ARGS.command:
            parser.parse_args([ARGS.common_module, ARGS.subcommand, '-h'])
        else:
            parser.parse_args([ARGS.common_module, '-h'])
    else:
        print_colored(f"Unknown common module: {ARGS.common_module}")


if __name__ == "__main__":
    main()
