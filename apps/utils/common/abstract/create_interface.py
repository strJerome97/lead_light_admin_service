from abc import ABC, abstractmethod

class CreateCommand(ABC):
    def __init__(self, request):
        self.request = request
    
    @abstractmethod
    def create(self):
        """Method to create a new record."""
        pass

    @abstractmethod
    def validate(self):
        """Method to validate the parameters before creation."""
        pass

    @abstractmethod
    def execute(self):
        """Method to execute the creation logic."""
        validation_result = self.validate()
        pass