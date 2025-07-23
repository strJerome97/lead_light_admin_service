from abc import ABC, abstractmethod

class LoginService(ABC):
    @abstractmethod
    def login(self, *args, **kwargs):
        pass
