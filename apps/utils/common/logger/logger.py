import logging

class PortalLogger:
    def __init__(self, log_code=None):
        self.logger = logging.getLogger("payroll_admin_service")
        self.log_code = log_code
        
    def _format(self, message):
        tag = self.log_code if self.log_code else "UNSPECIFIED"
        return f"{tag} - {message}"

    def info(self, message):
        self.logger.info(self._format(message))

    def debug(self, message):
        self.logger.debug(self._format(message))

    def warning(self, message):
        self.logger.warning(self._format(message))

    def error(self, message):
        self.logger.error(self._format(message))

    def critical(self, message):
        self.logger.critical(self._format(message))