
import json
from apps.utils.common.logger.logger import PortalLogger
from apps.company.common.payload import scaffold
from apps.utils.common.validation.general_validations import GeneralValidationService as validation_service

logger = PortalLogger(__name__)
COMPANY_SCAFFOLD = scaffold.COMPANY_SCAFFOLD

class ValidateCompanyPayload:
    def __init__(self, payload):
        self.payload = payload

    def validate(self):
        """
        Validate the company payload against the scaffold.
        This method checks if all required fields are present in the payload.
        Returns a dictionary with validation results.
        """
        for key in COMPANY_SCAFFOLD:
            # Check if the key exists in the payload
            if key not in self.payload:
                return {"code": 400, "success": False, "message": f"Missing required payload group: {key}", "data": None}
        return {"code": 200, "success": True, "message": "Validation successful", "data": self.payload}

class ValidateCompanyDetails:
    def __init__(self, company_details):
        self.company_details = company_details

    def validate(self):
        """Validate the company details."""
        result = validation_service(COMPANY_SCAFFOLD["details"]).validate(self.company_details)
        if not result:
            logger.error("Validation failed for company details.")
            return {"code": 400, "success": False, "message": "Validation failed for company details.", "data": None}
        
        return {"code": 200, "success": True, "message": "Validation successful", "data": self.company_details}

class ValidateCompanyAddress:
    def __init__(self, address):
        self.address = address

    def validate(self):
        """Validate the company address."""
        result = validation_service(COMPANY_SCAFFOLD["address"]).validate(self.address)
        if not result:
            logger.error("Validation failed for company address.")
            return {"code": 400, "success": False, "message": "Validation failed for company address.", "data": None}
        return {"code": 200, "success": True, "message": "Validation successful", "data": self.address}


class ValidateCompanyBankAccount:
    def __init__(self, bank_account):
        self.bank_account = bank_account

    def validate(self):
        """Validate the company bank account."""
        result = validation_service(COMPANY_SCAFFOLD["bankAccount"]).validate(self.bank_account)
        if not result:
            logger.error("Validation failed for company bank account.")
            return {"code": 400, "success": False, "message": "Validation failed for company bank account.", "data": None}
        return {"code": 200, "success": True, "message": "Validation successful", "data": self.bank_account}