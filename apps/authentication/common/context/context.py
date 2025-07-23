
from apps.authentication.common.abstract.abstract import LoginService

class AuthenticationContext:
    def __init__(self, strategy: LoginService):
        self.strategy = strategy
        
    def set_strategy(self, strategy: LoginService):
        self.strategy = strategy
    
    def login(self, *args, **kwargs):
        """
        Execute the login process using the current strategy.
        Returns the result of the login operation.
        """
        return self.strategy.login(*args, **kwargs)