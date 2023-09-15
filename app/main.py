import importlib
import inspect
import os
import sys
import json
import argparse
from argparse import ArgumentParser
from termcolor import colored
from common import Common as common, AbstractModule
from modules.banner.banner import Banner

# Paden naar de modules directories
STATIC_MODULES_PATH = "modules"
DYNAMIC_MODULES_PATH = "/dynamic"  # Pad voor nieuw gegenereerde modules

# Modules die je wilt uitsluiten van import
EXCLUDE_MODULES = ['tools', 'observer']

APP_VERSION = os.environ.get("APP_VERSION", "v0.1.0")

# Voeg het huidige scriptdirectorypad toe aan de Python-path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(STATIC_MODULES_PATH)  # Voeg het pad van statische modules toe aan de Python-path
sys.path.append(DYNAMIC_MODULES_PATH)  # Voeg het pad van dynamische modules toe aan de Python-path

# Debug helperfunctie
def print_colored(message, color="white"):
    print(colored(message, color))

# Ontdek beschikbare modules in de opgegeven directory
def discover_modules(module_path):
    try:
        return [f[:-3] for f in os.listdir(module_path) if f.endswith('.py') and f not in EXCLUDE_MODULES]
    except Exception as e:
        print_colored(f"Error discovering modules in {module_path}: {e}", color="red")
        return []

def discover_and_instantiate_modules(module_path, base_class, is_static=True, module_prefix=""):
    module_instances = {}
    parser = argparse.ArgumentParser(description=colored('docker shell: Made user-friendly, dynamic and bonus; Ephemeral!', 'green'))

    for module_name in discover_modules(module_path):
        if module_name in EXCLUDE_MODULES:
            continue

        print_colored(f"Attempting to import module: {module_name}", color="yellow")
        try:
            if is_static:
                module = importlib.import_module(f"{STATIC_MODULES_PATH}.{module_name}")
            else:
                module = importlib.import_module(f"{module_name}")
                print(f"Detected classes in {module_name}: {[name for name, _ in inspect.getmembers(module, inspect.isclass)]}")

            for name, cls in inspect.getmembers(module, inspect.isclass):
                if cls.__module__ == module.__name__ and issubclass(cls, base_class) and cls != base_class:
                    print(f"Instantiating class {name} of module {module_name}...")
                    instance = cls()
                    if hasattr(instance, 'add_arguments'):
                        print(f"Calling add_arguments for class {name} of module {module_name}...")
                        
                        # Voeg een voorvoegsel toe aan de subparsers om conflicten te voorkomen
                        subparser_prefix = f"{module_prefix}_" if module_prefix else ""
                        instance.add_arguments(parser, f"{subparser_prefix}{name.lower()}", cls.__doc__, parser)
                    module_instances[module_name] = instance
        except Exception as e:
            print_colored(f"Error importing module {module_name}: {e}", color="red")
    
    return module_instances

# Voeg modules toe aan de command-line parser
def add_arguments(subparsers: ArgumentParser, subcommand: str, help_text: str, subparsers_variable: ArgumentParser, module_prefix=""):
    for module_name in discover_modules(STATIC_MODULES_PATH):
        if module_name in EXCLUDE_MODULES:
            continue

        print_colored(f"Attempting to import module: {module_name}", color="yellow")
        try:
            module = importlib.import_module(f"{STATIC_MODULES_PATH}.{module_name}")
            print(f"Detected classes in {module_name}: {[name for name, _ in inspect.getmembers(module, inspect.isclass)]}")

            for name, cls in inspect.getmembers(module, inspect.isclass):
                if cls.__module__ == module.__name__ and issubclass(cls, AbstractModule) and cls != AbstractModule:
                    print(f"Instantiating class {name} of module {module_name}...")
                    instance = cls()
                    if hasattr(instance, 'add_arguments'):
                        print(f"Calling add_arguments for class {name} of module {module_name}...")
                        
                        # Voeg een voorvoegsel toe aan de subparsers om conflicten te voorkomen
                        subparser_prefix = f"{module_prefix}_" if module_prefix else ""
                        instance.add_arguments(subparsers, f"{subparser_prefix}{name.lower()}", cls.__doc__, subparsers)  # Geef subparsers als argument door
        except Exception as e:
            print_colored(f"Error importing module {module_name}: {e}", color="red")

def main():
    module_instances = {}
    banner = Banner(APP_VERSION)
    parser = argparse.ArgumentParser(description=colored('docker shell: Made user-friendly, dynamic and bonus; Ephemeral!', 'green'))
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')

    common_subparser = parser.add_subparsers(dest='common_module', help='Available common modules in app')  # pylint: disable=redundant-keyword-arg

    # Ontdek en instantieer statische modules
    module_instances.update(discover_and_instantiate_modules(STATIC_MODULES_PATH, AbstractModule, is_static=True, module_prefix="static"))

    # Ontdek en instantieer dynamische modules
    module_instances.update(discover_and_instantiate_modules(DYNAMIC_MODULES_PATH, AbstractModule, is_static=False, module_prefix="dynamic"))

    # Voeg gemeenschappelijke modules toe aan de subparsers
    add_arguments(common_subparser, 'common', 'Common modules', common_subparser)

    args = parser.parse_args()

    if args.debug:
        print_colored("Debug mode enabled.", color="yellow")
        print(args)

    if args.common_module:
        if args.common_module in module_instances:
            module_instances[args.common_module].run(args)
        else:
            print_colored(f"Common module '{args.common_module}' not found.", color="red")

    if not len(sys.argv) > 1:
        banner.print_banner()
        parser.print_help()
        sys.exit(0)

if __name__ == '__main__':
    main()
