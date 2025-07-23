from abc import ABC, abstractmethod

class LoginService(ABC):
    def __init__(self, parent):
        self.parent = parent
        
    @abstractmethod
    def login(self, **kwargs):
        pass
