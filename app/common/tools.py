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
    
    def get_command_docs(self):
        """Retrieve the docstrings for commands in the common module."""
        # Implementeer deze methode met de gewenste logica om de commando's op te halen.
        pass

    def get_subcommand_docs(self):
        """Retrieve the docstrings for subcommands in the common module."""
        # Implementeer deze methode met de gewenste logica om de subcommando's op te halen.
        pass

    def add_arguments(self, subparsers, name, doc):
        """Add arguments that this module supports."""
        # Voeg hier de logica toe om argumenten toe te voegen aan de subparsers voor de common-module.
        pass
