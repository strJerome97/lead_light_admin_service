
from apps.utils.common.logger.logger import PortalLogger

logger = PortalLogger("USE_CASE")

class UseCase:
    """
    Abstract base class for use cases.
    This class is designed to encapsulate the execution of a command and ensure that the response
    adheres to a specific format.
    The response should be a dictionary with the following keys:
    - 'code': HTTP status code (int)
    - 'status': Status of the operation (str)
    - 'message': A message describing the result (str)
    - 'data': The data returned by the command (list or dict)
    If the response does not match this format, an error will be logged and a default error response will be returned.
    Usage:
        use_case = UseCase(SomeCommand(request))
        result = use_case.execute()
    """
    def __init__(self, command):
        self.command = command

    def execute(self):
        result = self.command.execute()
        if not isinstance(result, dict) or not all(key in result for key in ["code", "status", "message", "data"]):
            logger.debug(f"Invalid response format from command execution from command {self.command.__class__.__name__}")
            return {"code": 400, "status": "error", "message": "Invalid response format", "data": None}
        return result