# Proposed observer.py module

from abc import ABC, abstractmethod


class ObserverInterface(ABC):
    """
    Observer Interface that all concrete observers must implement.
    """

    @abstractmethod
    def update(self, message: str):
        """
        Method to update the observer, used by the subject.
        """
        pass


class MainObserver(ObserverInterface):
    """
    Introducing the Dev-X-io Observers: The Silent Guardians!

    In the intricate dance of code and logic, where actions echo across the vast expanse of your application,
    there stand the Observers - ever vigilant, always watching.

    These silent sentinels don't interfere; they simply watch and, when the time is right, they react. 
    They're the unsung heroes, ensuring that when one part of your system speaks, the others listen.

    With the grace of a maestro conducting an orchestra, the Dev-X-io Observers ensure that every component
    plays its part in the grand symphony of your application.

    So, dear developer, rest easy knowing the Observers have your back. With them on your side,
    every event is a note, and every reaction, a melody. 🎵
    """


    def __init__(self):
        self.logs = []

    def update(self, message: str):
        """
        Overridden method from ObserverInterface. 
        Prints the received message and logs it.
        """
        print(f"Received notification: {message}")
        self.logs.append(message)

    def print_logs(self):
        """Prints all the logs."""
        print("Log History:")
        for log in self.logs:
            print(log)


# # Demonstrating the MainObserver
# observer_demo = MainObserver()
# observer_demo.update("Module 'boilerplate' has been initialized.")
# observer_demo.update("Ghost shell script has been generated.")
# observer_demo.print_logs()
