# common/tools.py

from abc import ABC, abstractmethod

class AbstractModule(ABC):
    """Abstract Module to define the structure for all modules."""
    
    @abstractmethod
    def get_command_docs(self):
        """Retrieve the docstrings for commands."""
        pass

    @abstractmethod
    def get_subcommand_docs(self):
        """Retrieve the docstrings for subcommands."""
        pass

class Common(AbstractModule):
    """Common Module to define shared functionality."""
    def __init__(self):
        super().__init__()

    def get_command_docs(self):
        """Retrieve the docstrings for commands in the common module."""
        # Implementeer deze methode met de gewenste logica om de commando's op te halen.
        return {
            "common_command": "Description of common command."
        }

    def get_subcommand_docs(self):
        """Retrieve the docstrings for subcommands in the common module."""
        # Implementeer deze methode met de gewenste logica om de subcommando's op te halen.
        return {
            "common_subcommand": "Description of common subcommand."
        }

    def add_arguments(self, subparsers, name, doc, parent_parser):
        """Add arguments that this module supports."""
        module_parser = parent_parser.add_parser(name, help=doc.strip())

        # Voeg hier argumenten toe aan de parser voor dit specifieke module.
        module_parser.add_argument('--module-argument', help='An argument for this module')

        # Andere argumenten toevoegen...

        return module_parser
